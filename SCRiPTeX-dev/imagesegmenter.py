#!/usr/bin/env python3

"""
A utility for use in developement of the SCRiPTeX application.

Converts input images to training data.
"""

import gc
import os
import shutil
import time
import random


# Import SCRiPTeX modules

import imageutils.pysegmenter as ps


os.chdir('script_sheets')

imagefolders = os.listdir()
numfolders = len(imagefolders)

for i in range(numfolders):

    print('Processing: ' + imagefolders[i])

    os.chdir(imagefolders[i])

    imagefiles = os.listdir()
    ps.PySegmenter(' '.join(imagefiles))

    os.chdir('../')

    gc.collect()


