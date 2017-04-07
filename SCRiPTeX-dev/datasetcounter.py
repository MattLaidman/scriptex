#!/usr/bin/env python3

"""
A utility for use in developement of the SCRiPTeX application.
"""


import os


numfiles = 0

os.chdir('recognizer/symbols/training')

files = os.listdir()
numfiles = numfiles + len(files)

for file in files:
    os.system('wc -l < ' + file + '>> ../../../temp')

os.chdir('../testing')

files = os.listdir()
numfiles = numfiles + len(files)

for file in files:
    os.system('wc -l < ' + file + '>> ../../../temp')

os.chdir('../../scripts/training')

files = os.listdir()
numfiles = numfiles + len(files)

for file in files:
    os.system('wc -l < ' + file + '>> ../../../temp')

os.chdir('../testing')

files = os.listdir()
numfiles = numfiles + len(files)

for file in files:
    os.system('wc -l < ' + file + '>> ../../../temp')

os.chdir('../../../')


count = 0;

with open('temp') as file:
    for i in range(numfiles):
        count = count + int(file.readline())

count = count - numfiles

print(count)

