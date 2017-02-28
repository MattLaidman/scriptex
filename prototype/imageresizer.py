"""
Image Resizer module driver of the SCRiPTeX Application.
"""


import os
import filecmp

from modules.imageresizer import pyimageresizer


TEMPFILE = 'imageresizer_temp'


def run_imageresizer(infile, outfile):

    """
    Runs the image resizer module on the passed input file, writing resized images
    to the passed output file.

    Assumes that the input file exists and is valid.
    """

    # List for images: length, width, list of pixel values
    images = []

    # Output file
    ofile = open(outfile, 'w+')

    # Read input file
    with open(infile, 'r') as file:
        # Get number of images
        numimages = int(file.readline())
        # Append each image to list as list of pixel values
        for _ in range(numimages):
            images.append(file.readline().split())

    # Write numimages to output file
    ofile.write(repr(numimages) + '\n')

    # For each image
    for i in range(numimages):
        # Construct PGM
        with open(TEMPFILE + '.pbm', 'w+') as file:
            file.write('P1\n')
            file.write(images[i][0] + ' ' + images[i][1] + '\n')
            for j in range(len(images[i]) - 2):
                file.write(images[i][j+2])
                if (j + 1) % int(images[i][0]) == 0:
                    file.write('\n')
                else:
                    file.write(' ')

        # Resize image
        pyimageresizer.resize_image(TEMPFILE + '.pbm')

        # Read resized image
        raw = ''
        with open(TEMPFILE + '.pbm', 'r') as file:
            file.readline()
            file.readline()
            for line in file:
                for value in line.split():
                    raw = raw + value + ' '

        # Write resized image to output file
        ofile.write(raw[0:-1] + '\n')

    ofile.close()
    # os.remove(TEMPFILE + '.pbm')


def test_imageresizer(infile, expectedoutfile):

    """
    Runs the image resizer module on the passed input file and returns if the output
    matches the passed expected output file.

    Assumes that input file exists and is valid.
    """

    # Run image resizer
    run_imageresizer(infile, TEMPFILE + '.txt')

    # Compare files
    match = filecmp.cmp(expectedoutfile, TEMPFILE + '.txt')

    # Delete temporary file
    # os.remove(TEMPFILE + '.txt')

    return match
