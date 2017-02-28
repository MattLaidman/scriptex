"""
Image Decoder module driver of the SCRiPTeX Application.
"""


import os
import filecmp

from modules.imagedecoder import pyimagedecoder


TEMPFILE = 'imagedecoder_temp'


def run_imagedecoder(infile, outfile):

    """
    Runs the image decoder module on the passed input file, writing decoded images
    to the passed output file.

    Assumes that the input file exists and is valid.
    """

    pyimagedecoder.decode_image(infile, outfile)


def test_imagedecoder(infile, expectedoutfile):

    """
    Runs the image decoder module on the passed input file and returns if the output
    matches the passed expected output file.

    Assumes that input file exists and is valid.
    """

    # Run image decoder
    run_imagedecoder(infile, TEMPFILE + '.txt')

    # Compare files
    match = filecmp.cmp(expectedoutfile, TEMPFILE + '.txt')

    # Delete temporary file
    os.remove(TEMPFILE + '.txt')

    return match
