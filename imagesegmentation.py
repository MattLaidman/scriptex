"""
Image Segmentation module driver of the SCRiPTeX Application.
"""


import os
import filecmp

from modules.imagesegmentation import pyimagesegmentation


TEMPSEGMENTED = 'imagesegmentation_tempsegmented'
TEMPINDEX = 'imagesegmentation_tempindex'

def run_imagesegmentation(infile, segmented, index):

    """
    Runs the image segmentation module on the passed input file, writing segmented
    characters to the passed output file.

    Assumes that the input file exists and is valid.
    """

    pyimagesegmentation.segment_image(infile, segmented, index)


def test_imagesegmentation(infile, expectedsegmented, expectedindex):

    """
    Runs the image segmentation module on the passed input file and returns if the output
    matches the passed expected output file.

    Assumes that input file exists and is valid.
    """

    # Run image resizer
    run_imagesegmentation(infile, TEMPSEGMENTED + '.txt', TEMPINDEX + '.txt')

    # Compare files
    match = filecmp.cmp(expectedsegmented, TEMPSEGMENTED + '.txt')

    if match:
        match = filecmp.cmp(expectedindex, TEMPINDEX + '.txt')

    # Delete temporary file
    os.remove(TEMPSEGMENTED + '.txt')
    os.remove(TEMPINDEX + '.txt')

    return match
