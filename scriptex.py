#!/usr/bin/env python3

"""
SCRiPTeX protoype program driver.
"""


import sys
import os


# Import SCRiPTeX Modules

import imagedecoder
import imagesegmentation
import imageresizer
import characterrecognition
import texlookup
import texassembly


# Parameters

INFILE = sys.argv[1]            # Module 1 input file
MOD12 = 'mod12.txt'             # Module 1 output file, module 2 input file
MOD23 = 'mod23.txt'             # Module 2 output file, module 3 input file
MOD26 = 'mod26.txt'             # Module 2 output file, module 6 input file
MOD34 = 'mod34.txt'             # Module 3 output file, module 4 input file
MOD45 = 'mod45.txt'             # Module 4 output file, module 5 input file
MOD56 = 'mod56.txt'             # Module 5 output file, module 6 input file
OUTFILE = INFILE[:-4]+ '.tex'   # Module 6 output file


# Run Modules

imagedecoder.run_imagedecoder(INFILE, MOD12)
imagesegmentation.run_imagesegmentation(MOD12, MOD23, MOD26)
imageresizer.run_imageresizer(MOD23, MOD34)
characterrecognition.run_characterrecognition(MOD34, MOD45)
texlookup.run_texlookup(MOD45, MOD56)
texassembly.run_texassembly(MOD26, MOD56, OUTFILE)

# Clean Up

os.remove(MOD12)
os.remove(MOD23)
os.remove(MOD26)
os.remove(MOD34)
os.remove(MOD45)
os.remove(MOD56)
os.remove('imageresizer_temp.pbm') # Move Me