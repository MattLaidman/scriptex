"""
Python wrapper module for the imageresizer C++ library
"""


import ctypes


IMAGERESIZER = ctypes.cdll.LoadLibrary('modules/imageresizer/imageresizer.so')
IMAGERESIZER.resizeImage.argtypes = [ctypes.c_char_p]


def resize_image(image):

    """
    Resize the passed image file to 32x32
    """

    IMAGERESIZER.resizeImage(ctypes.c_char_p(image.encode('utf-8')))
