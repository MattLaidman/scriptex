#!/usr/bin/env python3

import os
import shutil

os.chdir('training_images')

charfolders = os.listdir()
numcharfolders = len(charfolders)

for i in range(numcharfolders):
    print(charfolders[i])
    if os.path.exists(charfolders[i]) and os.path.isdir(charfolders[i]):
        os.chdir(charfolders[i])
        for j in range(5):
            if os.path.isdir(repr(j)):
                # os.chdir(subfolders[j])

                # files = os.listdir()
                # numfiles = len(files)

                # for k in range(numfiles):
                #     shutil.move(files[k], '../segmented/' + files[k])

                # os.chdir('../')

                os.rmdir(repr(j))

        os.chdir('../')

os.chdir('../')
