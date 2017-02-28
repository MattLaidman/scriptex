"""
TeX Assembly Python library.

Provides a means of assembling the given TeX markup according to the index file.
"""


# def assemble_document(log,input,output):
#     log = open(log)
#     input = open(input)
#     output = open(output, 'w+')
#     string=input.read()
#     lstring=log.read()
#     i=0
#     j=1
#     out=string.split('\n')
#     output.write('\\documentclass{article}\n')
#     output.write('\\setlength{\\parindent}{0pt}\n')
#     output.write('\\begin{document}\n')
#     while j<=int(out[0]):
#         if lstring[i]==' ':
#             output.write(' ')
#         elif lstring[i]=='\n':
#             output.write('\\newline ')
#         else:
#             wordlen=int(lstring[i])
#             word=out[j:j+wordlen]
#             word=''.join(word)
#             output.write(word)
#             j=j+wordlen
#         i=i+1
#     output.write('\n\\end{document}')
#     output.close()
#     input.close()
#     log.close()


def assemble_document(charmap, symbols, outfile):

    num_symbols = 0
    num_lines = 0
    symbol_list = []
    charmap_list = {}

    # Read symbols
    with open(symbols, 'r') as file:
        # Read number of symbols
        num_symbols = int(file.readline())
        # Read symbols
        for _ in range(num_symbols):
            symbol_list.append(file.readline().split())

    # Read Character Map
    with open(charmap, 'r') as file:
        # Read each line
        lines = file.readlines()
        num_lines = len(lines)
        # split each line
        for i in range(num_lines):
            charmap_list[i] = lines[i].split()

    # Assemble document
    with open(outfile, 'w+') as file:
        file.write('\\documentclass{article}\n\\setlength{\\parindent}{0pt}\n\\begin{document}\n')
        index = 0
        for i in range(num_lines):
            for j in range(len(charmap_list[i])):
                for _ in range(int(charmap_list[i][j])):
                    file.write(symbol_list[index][0])
                    index = index + 1
                file.write(' ')
            file.write('\\newline\n')
        file.write('\\end{document}')
