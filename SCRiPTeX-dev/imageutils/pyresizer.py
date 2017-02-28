"""
Python wrapper module for the resizer C++ library
"""


import ctypes


RESIZER = ctypes.cdll.LoadLibrary('imageutils/resizer.so')
RESIZER.resizeImage.argtypes = [ctypes.c_char_p]


def resize_image(image):

    """
    Resize the passed image file to 32x32
    """

    RESIZER.resizeImage(ctypes.c_char_p(image.encode('utf-8')))
