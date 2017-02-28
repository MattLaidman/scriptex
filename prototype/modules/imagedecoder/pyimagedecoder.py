"""
Python wrapper module for the imagedecoder C++ library
"""


import ctypes


IMAGEDECODER = ctypes.cdll.LoadLibrary('modules/imagedecoder/imagedecoder.so')
IMAGEDECODER.decodeImage.argtypes = [ctypes.c_char_p, ctypes.c_char_p]


def decode_image(infile, outfile):

    """
    Segment the passed image file into individual characters
    """

    IMAGEDECODER.decodeImage(ctypes.c_char_p(infile.encode('utf-8')),
                                   ctypes.c_char_p(outfile.encode('utf-8')))
