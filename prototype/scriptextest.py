#!/usr/bin/env python3


"""
SCRiPTeX Prototype Testing Suite

A component of the SCRiPTeX prototype software.
"""


import os


# Import SCRiPTeX Modules

import imagedecoder
import imagesegmentation
import imageresizer
import characterrecognition
import texlookup
import texassembly


# Test Temp Files

INFILE = ''                         # Custom input file
INFILE2 = ''                        # Custom input file
MOD12 = 'tests/custom/mod12.txt'    # Module 1 output file, module 2 input file
MOD23 = 'tests/custom/mod23.txt'    # Module 2 output file, module 3 input file
MOD26 = 'tests/custom/mod26.txt'    # Module 2 output file, module 6 input file
MOD34 = 'tests/custom/mod34.txt'    # Module 3 output file, module 4 input file
MOD45 = 'tests/custom/mod45.txt'    # Module 4 output file, module 5 input file
MOD56 = 'tests/custom/mod56.txt'    # Module 5 output file, module 6 input file
OUTFILE = ''                        # Custom output file
OUTFILE2 = ''                       # Custom output file


# Automated Test Files

U1_1 = 'tests/module1/1.jpg'
U1_2 = 'tests/module1/1.tiff'
U1_3 = 'tests/module1/1.png'
U1_EXPECTED = 'tests/module1/1_expected.txt'

U2 = 'tests/module2/1.txt'
U2_EXPECTED1 = 'tests/module2/1_expected1.txt'
U2_EXPECTED2 = 'tests/module2/1_expected2.txt'

U3 = 'tests/module3/1.txt'
U3_EXPECTED = 'tests/module3/1_expected.txt'

U4 = 'tests/module4/1.txt'
U4_EXPECTED = 'tests/module4/1_expected.txt'

U5 = 'tests/module5/1.txt'
U5_EXPECTED = 'tests/module5/1_expected.txt'

U6_1 = 'tests/module6/1_1.txt'
U6_2 = 'tests/module6/1_2.txt'
U6_EXPECTED = 'tests/module6/1_expected.tex'


# Helper Functions

def get_test_type():
    while True:
        print('Test type to perform:')
        print('1. Unit Test')
        print('2. Integration Test')
        print('3. Systems Test')
        print('0. Quit')
        test_type = int(input('Test type [0..3]: '))
        if test_type >= 0 and test_type <= 3:
            return test_type

def is_automated_test():
    while True:
        print('Automated tests or a custom test:')
        print('1. Automated Tests')
        print('2. Custom Test')
        test_type = int(input('Test type [1..2]: '))
        if test_type == 1:
            return True
        elif test_type == 2:
            return False

def get_custom_files(modnum):
    if modnum != 2 and modnum != 6:
        INFILE = input('Custom input file: ')
        OUTFILE = input('Custom expected output file: ')
    else:
        if modnum == 2:
            INFILE = input('Custom input file: ')
            OUTFILE = input('Custom expected segmented output file: ')
            OUTFILE2 = input('Custom expected index output file: ')
        else:
            INFILE = input('Custom TeX markup input file: ')
            INFILE2 = input('Custom index input file: ')
            OUTFILE = input('Custom expected output file: ')

def get_unit_type():
    while True:
        print('Test which module:')
        print('1. Image Decoder')
        print('2. Image Segmentation')
        print('3. Image Resizer')
        print('4. Character Recognition')
        print('5. TeX Lookup')
        print('6. TeX Assembly')
        print('0. Cancel')
        test_type = int(input('Test type [0..6]: '))
        if test_type >= 0 and test_type <= 6:
            return test_type

def get_integration_type():
    while True:
        print('Test which modules:')
        print('1. Image Decoder and Image Segmentation')
        print('2. Image Segmentation and Image Resizer')
        print('3. Image Resizer and Character Recognition')
        print('4. Character Recognition and TeX Lookup')
        print('5. TeX Lookup, Image Segmentation, and TeX Assembly')
        print('0. Cancel')
        test_type = int(input('Test type [0..5]: '))
        if test_type >= 0 and test_type <= 5:
            return test_type


# Program

while True:

    test_type = get_test_type()

    if test_type == 0:
        break;
    else:

        # Unit Tests

        if test_type == 1:
            unit_type = get_unit_type()
            is_automated = is_automated_test()
            if unit_type == 1:
                if is_automated:
                    if imagedecoder.test_imagedecoder(U1_1, U1_EXPECTED) and \
                       imagedecoder.test_imagedecoder(U1_2, U1_EXPECTED) and \
                       imagedecoder.test_imagedecoder(U1_3, U1_EXPECTED):
                        print('Module 1 test was successful.')
                    else:
                        print('Module 1 test was unsuccessful.')
                else:
                    get_custom_files(1)
                    if imagedecoder.test_imagedecoder(INFILE, OUTFILE):
                        print('Module 1 test was successful.')
                    else:
                        print('Module 1 test was unsuccessful.')
            if unit_type == 2:
                if is_automated:
                    if imagesegmentation.test_imagesegmentation(U2, U2_EXPECTED1, U2_EXPECTED2):
                        print('Module 2 test was successful.')
                    else:
                        print('Module 2 test was unsuccessful.')
                else:
                    get_custom_files(2)
                    if imagesegmentation.test_imagesegmentation(INFILE, OUTFILE2, OUTFILE):
                        print('Module 2 test was successful.')
                    else:
                        print('Module 2 test was unsuccessful.')
            if unit_type == 3:
                if is_automated:
                    if imageresizer.test_imageresizer(U3, U3_EXPECTED):
                        print('Module 3 test was successful.')
                    else:
                        print('Module 3 test was unsuccessful.')
                else:
                    get_custom_files(3)
                    if imageresizer.test_imageresizer(INFILE, OUTFILE):
                        print('Module 3 test was successful.')
                    else:
                        print('Module 3 test was unsuccessful.')
            if unit_type == 4:
                if is_automated:
                    print('Module 4 test was ' + repr(characterrecognition.test_characterrecognition(U4, U4_EXPECTED)) \
                          + '% accurate.')
                else:
                    get_custom_files(4)
                    print('Module 4 test was ' + repr(characterrecognition.test_characterrecognition(INFILE, OUTFILE)) \
                          + '% accurate.')
            if unit_type == 5:
                if is_automated:
                    if texlookup.test_texlookup(U5, U5_EXPECTED):
                        print('Module 5 test was successful.')
                    else:
                        print('Module 5 test was unsuccessful.')
                else:
                    get_custom_files(5)
                    if texlookup.test_texlookup(INFILE, OUTFILE):
                        print('Module 5 test was successful.')
                    else:
                        print('Module 5 test was unsuccessful.')
            if unit_type == 6:
                if is_automated:
                    if texassembly.test_texassembly(U6_2, U6_1, U6_EXPECTED):
                        print('Module 6 test was successful.')
                    else:
                        print('Module 6 test was unsuccessful.')
                else:
                    get_custom_files(6)
                    if texassembly.test_texassembly(INFILE2, INFILE, OUTFILE):
                        print('Module 6 test was successful.')
                    else:
                        print('Module 6 test was unsuccessful.')

        # Integration Tests

        if test_type == 2:
            integration_type = get_integration_type()
            if integration_type == 1:
                imagedecoder.run_imagedecoder(U1_1, MOD12)
                if imagesegmentation.test_imagesegmentation(MOD12, U2_EXPECTED1, U2_EXPECTED2):
                    print('Integration test 1 was successful.')
                else:
                    print('Integration test 1 was unsuccessful.')
            if integration_type == 2:
                imagesegmentation.run_imagesegmentation(U2, MOD23, MOD26)
                if imageresizer.test_imageresizer(MOD23, U3_EXPECTED):
                    print('Integration test 2 was successful.')
                else:
                    print('Integration test 2 was unsuccessful.')
            if integration_type == 3:
                imageresizer.run_imageresizer(U3, MOD34)
                print('Integration test 3 was ' + repr(characterrecognition.test_characterrecognition(MOD34, U4_EXPECTED)) \
                          + '% accurate.')
            if integration_type == 4:
                if texlookup.test_texlookup(U5, U5_EXPECTED):
                    print('Integration test 4 was successful.')
                else:
                    print('Integration test 4 was unsuccessful.')
            if integration_type == 5:
                imagesegmentation.run_imagesegmentation(U2, MOD23, MOD26)
                if texassembly.test_texassembly(MOD26, MOD56, U6_EXPECTED):
                    print('Integration test 5 was successful.')
                else:
                    print('Integration test 5 was unsuccessful.')

        # Systems Test

        if test_type == 3:
            
            is_automated = is_automated_test()

            if is_automated:
                imagedecoder.run_imagedecoder(U1_1, MOD12)
                imagesegmentation.run_imagesegmentation(MOD12, MOD23, MOD26)
                imageresizer.run_imageresizer(MOD23, MOD34)
                characterrecognition.run_characterrecognition(MOD34, MOD45)
                texlookup.run_texlookup(MOD45, MOD56)
                if texassembly.test_texassembly(MOD26, MOD56, U6_EXPECTED):
                    print('Systems test was successful.')
                else:
                    print('Systems test was unsuccessful')
            else:
                get_custom_files(1)
                imagedecoder.run_imagedecoder(INFILE, MOD12)
                imagesegmentation.run_imagesegmentation(MOD12, MOD23, MOD26)
                imageresizer.run_imageresizer(MOD23, MOD34)
                characterrecognition.run_characterrecognition(MOD34, MOD45)
                texlookup.run_texlookup(MOD45, MOD56)
                texassembly.run_texassembly(MOD26, MOD56, OUTFILE)