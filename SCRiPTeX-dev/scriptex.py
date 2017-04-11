#!/usr/bin/env python3

"""
SCRiPTeX program driver.
"""


import sys
import os
import shutil


def run_scriptex(infile, outfile):

    # Import SCRiPTeX Modules

    import imageutils.pysegmenter as ps
    import imageutils.pynormalizer as pn
    import recognizer.networkmodel as nm


    segmenter = ps.PySegmenter(infile)
    nsindex = segmenter.get_nsindex().split()
    sindex = segmenter.get_sindex().split()
    srindex = segmenter.get_srindex().split()
    rindex = segmenter.get_rindex().split()
    del segmenter

    rawimages = []

    os.chdir(TEMPFOLDER)
    images = os.listdir()
    numimages = len(images)
    # For each image
    for i in range(numimages):
        # Normalize image
        pn.normalize_image(repr(i) + '.pgm')

        # Read Normalized image
        raw = ''
        with open(repr(i) + '.pbm', 'r') as file:
            file.readline()
            file.readline()
            for line in file:
                for value in line.split():
                    raw = raw + value + ' '
        rawimages.append(raw.split())
        for raws in rawimages:
            raws = list(map(int, raws))

    os.chdir('../')


    # Recognize symbols
    model = nm.Model('recognizer/model/model')
    if numimages != 0:
        markup = model.run_model(rawimages)
    del model

    genDocument(markup, nsindex, sindex, rindex, srindex)


def genDocument (charIndex, spaceLineIndex, scriptIndex, resegIndex, sqrtIndex):
    with open('texOut\\out.tex', 'w+') as outFile:

        #variables for the tex writing
        openScriptBraces = 0
        openResegBraces = 0
        openSqrtBraces = 0
        charLoc = 0
        currScriptLoc = 0
        currResegLoc = 0
        currSqrtLoc = 0

        #flags
        inMathMode = False
        inFraction = False
        inSummation = False
        inIntegral = False
        inLimit = False
        inProduct = False
        inSqrt = False

        #file initalizations
        outFile.write('\\documentclass[12pt]{article}\n\\setlength{\\parindent}{0pt}\n')
        outFile.write('\\usepackage{amsmath}\n')
        outFile.write('\\begin{document}\n')

        #file building based on indices
        for spaceLoc in range(len(spaceLineIndex)):
            spaceTemp = int(spaceLineIndex[spaceLoc])
            #newline
            if spaceTemp == -1:
                for braces in range(openScriptBraces + openResegBraces + openSqrtBraces):
                    outFile.write('}')
                    openScriptBraces = 0
                    openResegBraces = 0
                    openSqrtBraces = 0
                outFile.write('\n\\newline\n')
            #character
            elif spaceTemp == 1:
                #scripting check
                scriptTemp = int(scriptIndex[charLoc])
                if scriptTemp > 0:          #superscripting
                    if scriptTemp > currScriptLoc:
                        currScriptLoc += 1
                        openScriptBraces += 1
                        outFile.write('\\textsuperscript{')
                    elif scriptTemp < currScriptLoc:
                        currScriptLoc -= 1
                        openScriptBraces -= 1
                        outFile.write('}')
                elif scriptTemp < 0:        #subscripting
                    if scriptTemp < currScriptLoc:
                        currScriptLoc -= 1
                        openScriptBraces += 1
                        outFile.write('\\textsubscript{')
                    elif scriptTemp > currScriptLoc:
                        currScript += 1
                        openScriptBraces -= 1
                        outFile.write('}')
                else:                       #close any open scripting braces
                    for i in range(openScriptBraces):
                        outFile.write('}')
                    openScriptBraces = 0
                    currScriptLoc = 0

                #resegment check
                resegTemp = int(resegIndex[charLoc])
                if resegTemp == 2:
                    if (inFraction or inSummation or inIntegral or inLimit or inProduct):
                        for braces in range(openResegBraces):
                            outFile.write('}')
                        openResegBraces = 0
                        inFraction = False
                        inSummation = False
                        inIntegral = False
                        inLimit = False
                        inProduct = False
                    #Find out what the resegment is and open it
                    tempLoc = charLoc
                    #priority check for limit
                    if (charLoc+2 < len(charIndex)) and ((characterSet[int(charIndex[charLoc])] + characterSet[int(charIndex[charLoc+1])] + characterSet[int(charIndex[charLoc+2])]) == 'lim'):
                        inLimit = True
                        limCount = 3
                        toWrite = '\\lim\limits_{'
                    else:
                        #check for anyother resegs if limit failed 
                        for location in range(tempLoc+1, len(resegIndex)):
                            temp = int(charIndex[location])
                            if int(resegIndex[location]) == 0 or int(resegIndex[location]) == 2 :
                                break
                            elif temp == 120: #Fraction
                                inFraction = True
                                toWrite = "\\frac{"
                            elif temp == 86: #Summation
                                inSummation = True
                                toWrite = "\\sum\\limits^{"
                            elif temp == 121: #integral
                                inIntegral = True
                                toWrite = "\\int\\limits^{"
                            elif temp == 125: #Product
                                inProduct = True
                                toWrite = "\\prod\\limits^{"
                    if (not inMathMode) and (inFraction or inSummation or inIntegral or inLimit or inProduct):
                        outFile.write('$')
                        inMathMode = True
                    if inFraction or inSummation or inIntegral or inLimit or inProduct:
                        outFile.write(toWrite)
                        openResegBraces += 1
                elif resegTemp == 0:
                    #close any potentially open Resegments
                    for braces in range(openResegBraces):
                        outFile.write('}')
                    openResegBraces = 0
                    inFraction = False
                    inSummation = False
                    inIntegral = False
                    inLimit = False
                    inProduct = False
                    if inMathMode and not(inFraction or inSummation or inIntegral or inLimit or inProduct or inSqrt):
                        outFile.write('$')
                        inMathMode = False
                #squareroot check
                tempSqrt = int(sqrtIndex[charLoc])
                if tempSqrt == 2 and int(charIndex[charLoc]) == 124:
                    #begin a sqrt, first check if mathmode must be started
                    if not inMathMode:
                        outFile.write('$')
                        inMathMode = True
                    outFile.write('\\sqrt{')
                    openSqrtBraces += 1
                    inSqrt = True
                elif tempSqrt == 0:
                    #close any potentially open Sqrt
                    for braces in range(openSqrtBraces):
                        outFile.write('}')
                    openSqrtBraces = 0
                    inSqrt = False
                    if inMathMode and not(inFraction or inSummation or inIntegral or inLimit or inSqrt or inProduct):
                        outFile.write('$')
                        inMathMode = False
                        
                #Character placement and special cases for placement
                tempIndex = int(charIndex[charLoc])
                if inFraction and tempIndex == 120:             #ignore fraction sybmol if in a fraction
                    outFile.write('}{')
                elif inSummation and tempIndex == 86:           #ignore Sigma if in a Summation
                    outFile.write('}_{')
                elif inIntegral and tempIndex == 121:           #ignore Integral symbol if in an Integral
                    outFile.write('}_{')
                elif inLimit and limCount > 0:                  #ignore 'lim' if we are in a Limit
                    limCount -= 1
                elif inProduct and tempIndex == 125:            #ignore UC pi if in a product
                    outFile.write('}_{')
                elif ((62 <= tempIndex <= 89) or (113 <= tempIndex <= 119) or (tempIndex in (95, 96, 97, 101, 102, 120, 121, 122, 123, 125))) and not inMathMode:   #special mathMode cases
                    outFile.write('$')
                    outFile.write(characterSet[tempIndex])
                    outFile.write('$')
                elif tempIndex != 124:                          #ignore sqrt symbol in all cases
                    outFile.write(characterSet[tempIndex])
                charLoc += 1
            #put a space in TeX file
            else:
                outFile.write(' ')


        #file closing 
        for braces in range(openScriptBraces + openResegBraces + openSqrtBraces):
            outFile.write('}')
        if openResegBraces != 0 or inMathMode:
            outFile.write('$')
        outFile.write('\n\\end{document}')

#Build the CharacterSet Lookup list
characterSet = {}
characterSet[0] = '0'
characterSet[1] = '1'
characterSet[2] = '2'
characterSet[3] = '3'
characterSet[4] = '4'
characterSet[5] = '5'
characterSet[6] = '6'
characterSet[7] = '7'
characterSet[8] = '8'
characterSet[9] = '9'
characterSet[10] = 'a'
characterSet[11] = 'b'
characterSet[12] = 'c'
characterSet[13] = 'd'
characterSet[14] = 'e'
characterSet[15] = 'f'
characterSet[16] = 'g'
characterSet[17] = 'h'
characterSet[18] = 'i'
characterSet[19] = 'j'
characterSet[20] = 'k'
characterSet[21] = 'l'
characterSet[22] = 'm'
characterSet[23] = 'n'
characterSet[24] = 'o'
characterSet[25] = 'p'
characterSet[26] = 'q'
characterSet[27] = 'r'
characterSet[28] = 's'
characterSet[29] = 't'
characterSet[30] = 'u'
characterSet[31] = 'v'
characterSet[32] = 'w'
characterSet[33] = 'x'
characterSet[34] = 'y'
characterSet[35] = 'z'
characterSet[36] = 'A'
characterSet[37] = 'B'
characterSet[38] = 'C'
characterSet[39] = 'D'
characterSet[40] = 'E'
characterSet[41] = 'F'
characterSet[42] = 'G'
characterSet[43] = 'H'
characterSet[44] = 'I'
characterSet[45] = 'J'
characterSet[46] = 'K'
characterSet[47] = 'L'
characterSet[48] = 'M'
characterSet[49] = 'N'
characterSet[50] = 'O'
characterSet[51] = 'P'
characterSet[52] = 'Q'
characterSet[53] = 'R'
characterSet[54] = 'S'
characterSet[55] = 'T'
characterSet[56] = 'U'
characterSet[57] = 'V'
characterSet[58] = 'W'
characterSet[59] = 'X'
characterSet[60] = 'Y'
characterSet[61] = 'Z'
characterSet[62] = '\\alpha '
characterSet[63] = '\\beta '
characterSet[64] = '\\gamma '
characterSet[65] = '\\delta '
characterSet[66] = '\\epsilon '
characterSet[67] = '\\zeta '
characterSet[68] = '\\eta '
characterSet[69] = '\\theta '
characterSet[70] = '\\lambda '
characterSet[71] = '\\mu '
characterSet[72] = '\\xi '
characterSet[73] = '\\pi '
characterSet[74] = '\\rho '
characterSet[75] = '\\sigma '
characterSet[76] = '\\tau '
characterSet[77] = '\\phi '
characterSet[78] = '\\chi '
characterSet[79] = '\\psi '
characterSet[80] = '\\omega '
characterSet[81] = '\\Gamma '
characterSet[82] = '\\Delta '
characterSet[83] = '\\Theta '
characterSet[84] = '\\Lambda '
characterSet[85] = '\\Xi '
characterSet[86] = '\\Sigma '
characterSet[87] = '\\Phi '
characterSet[88] = '\\Psi '
characterSet[89] = '\\Omega '
characterSet[90] = '+'
characterSet[91] = '-'
characterSet[92] = '*'
characterSet[93] = '\\'
characterSet[94] = '='
characterSet[95] = '\\neq '
characterSet[96] = '\\simeq '
characterSet[97] = '\\vert '
characterSet[98] = '%'
characterSet[99] = '<'
characterSet[100] = '>'
characterSet[101] = '\\leq '
characterSet[102] = '\\geq '
characterSet[103] = '('
characterSet[104] = ')'
characterSet[105] = '['
characterSet[106] = ']'
characterSet[107] = '{'
characterSet[108] = '}'
characterSet[109] = '.'
characterSet[110] = ','
characterSet[111] = ':'
characterSet[112] = ';'
characterSet[113] = '\\forall '
characterSet[114] = '\\exists '
characterSet[115] = '\\in '
characterSet[116] = '\\notin '
characterSet[117] = '\\rightarrow '
characterSet[118] = '\\leftarrow '
characterSet[119] = '\\emptyset '
characterSet[120] = '\\frac{}{}'
characterSet[121] = '\\int'
characterSet[122] = '\\infty '
characterSet[123] = '\\pm '
characterSet[124] = '\\sqrt '
characterSet[125] = '\\Pi '

# Parameters
TEMPFOLDER = 'segmentPGM'
if __name__ == '__main__':
    INFILE = sys.argv[1]
    OUTFILE = INFILE.split('.')[0]+ '.tex'
    run_scriptex(INFILE, OUTFILE)
# shutil.rmtree(TEMPFOLDER)
