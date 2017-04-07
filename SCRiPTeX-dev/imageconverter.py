#!/usr/bin/env python3

"""
A utility for use in developement of the SCRiPTeX application.

Converts input images to training data.
"""


import os
import random


# Import SCRiPTeX modules

import imageutils.pynormalizer as pn

 
os.mkdir('training')
os.mkdir('testing')
os.chdir('script_sheets')
imagefolders = os.listdir()
numfolders = len(imagefolders)

for i in range(numfolders):

    print('Processing: ' + imagefolders[i])

    trainfile = open('../training/' + imagefolders[i] + '.txt', 'a+')
    testfile = open('../testing/' + imagefolders[i] + '.txt', 'a+')

    os.chdir(imagefolders[i] + '/segmentPGM')
    symbolfiles = os.listdir()
    numsymbols = len(symbolfiles)
    for j in range(numsymbols):
        pn.normalize_image(symbolfiles[j])
        with open(symbolfiles[j][:-4] + '.pbm', 'r') as image:
            image.readline()
            image.readline()
            # image.readline()
            img = ''
            for k in range(32):
                img = img + image.readline()[:-1]
            if random.random() > 0.15:
                trainfile.write(img + '\n')
            else:
                testfile.write(img + '\n')
    trainfile.close()
    testfile.close()
    os.chdir('../')
    os.chdir('../')
os.chdir('../')



