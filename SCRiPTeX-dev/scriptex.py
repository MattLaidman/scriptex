#!/usr/bin/env python3

"""
SCRiPTeX protoype program driver.
"""


import sys
import os
import shutil


# Import SCRiPTeX Modules

import imageutils.pysegmenter as ps
import imageutils.pyresizer as pr
import recognizer.networkmodel as nm


# Parameters

INFILE = sys.argv[1]            # Module 1 input file
TEMPFOLDER = 'segmentPGM'
OUTFILE = INFILE[:-4]+ '.tex'   # Module 6 output file

segmenter = ps.PySegmenter(INFILE)
index = segmenter.get_index().split(', ')
del segmenter

rawimages = []

os.chdir(TEMPFOLDER);
images = os.listdir()
numimages = len(images)

# For each image
for i in range(numimages):
    # Resize image
    pr.resize_image(images[i])

    # Read resized image
    raw = ''
    with open(images[i], 'r') as file:
        file.readline()
        file.readline()
        file.readline()
        for line in file:
            for value in line.split():
                raw = raw + value + ' '
    rawimages.append(raw.split())

os.chdir('../')


# Run Character Recognition
# Recognize symbols
MODEL = nm.Model('recognizer/model/model')
markup = []
if numimages != 0:
    markup = MODEL.run_model(rawimages)
del MODEL

# Assemble document
index = index[:-1]

k = 0;
with open(OUTFILE, 'w+') as file:
    file.write('\\documentclass{article}\n\\setlength{\\parindent}{0pt}\n\\begin{document}\n')
    for i in range(len(index)):
        if int(index[i]) == -1:
            file.write('\\newline\n')
        elif k < len(markup):
            for j in range(int(index[i])):
                file.write(markup[k])
                k = k + 1;
            file.write(' ')
    file.write('\\end{document}')

# Delete shit!

shutil.rmtree(TEMPFOLDER)