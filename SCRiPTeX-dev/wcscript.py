#!/usr/bin/env python3

"""
A utility for use in developement of the SCRiPTeX application.
"""


import os


os.chdir('training')

files = os.listdir()
numfiles = len(files)

for i in range(numfiles):
    os.system('wc -l < ' + files[i] + ' > temp')
    os.system('cat ' + files[i] + ' >> temp && mv temp ' + files[i])

os.chdir('../testing')

files = os.listdir()
numfiles = len(files)

for i in range(numfiles):
    os.system('wc -l < ' + files[i] + ' > temp')
    os.system('cat ' + files[i] + ' >> temp && mv temp ' + files[i])