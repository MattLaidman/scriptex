"""
Python wrapper module for the segmentation C++ library
"""


import ctypes


SEGMENTER = ctypes.cdll.LoadLibrary('imageutils/segmenter.so')
SEGMENTER.getSegmenterInstance.argtypes = [ctypes.c_char_p]
SEGMENTER.getIndex.restype = ctypes.c_char_p

class PySegmenter:

    """
    PySegmenter Python Wrapper for Segmenter class of segmenter C++ library
    """

    def __init__(self, image):
        self._segmenterinst = \
            SEGMENTER.getSegmenterInstance(ctypes.c_char_p(image.encode('UTF-8')))


    def __del__(self):
        SEGMENTER.destroySegmenterInstance(self._segmenterinst)


    def get_index(self):

        """
        Return the index
        """
        return str(SEGMENTER.getIndex(self._segmenterinst).decode('UTF-8'))
