"""
Python wrapper module for the resizer C++ library
"""


import ctypes


RESIZER = ctypes.cdll.LoadLibrary('imageutils/normalizer.so')
RESIZER.normalizeImage.argtypes = [ctypes.c_char_p]


def normalize_image(image):

    """
    Resize the passed image file to 32x32
    """

    RESIZER.normalizeImage(ctypes.c_char_p(image.encode('utf-8')))
