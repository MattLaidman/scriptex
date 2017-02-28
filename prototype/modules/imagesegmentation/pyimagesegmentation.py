"""
Python wrapper module for the imagesegmentation C++ library
"""


import ctypes


IMAGESEGMENTATION = ctypes.cdll.LoadLibrary('modules/imagesegmentation/imagesegmentation.so')
IMAGESEGMENTATION.segmentImage.argtypes = [ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p]


def segment_image(infile, segmented, index):

    """
    Segment the passed image file into individual characters
    """

    IMAGESEGMENTATION.segmentImage(ctypes.c_char_p(infile.encode('utf-8')),
                                   ctypes.c_char_p(segmented.encode('utf-8')),
                                   ctypes.c_char_p(index.encode('utf-8')))
