"""
Python wrapper module for the segmentation C++ library
"""


import ctypes


SEGMENTER = ctypes.cdll.LoadLibrary('imageutils/segmenter.so')
SEGMENTER.getSegmenterInstance.argtypes = [ctypes.c_char_p]
SEGMENTER.getNSIndex.restype = ctypes.c_char_p
SEGMENTER.getSIndex.restype = ctypes.c_char_p
SEGMENTER.getRIndex.restype = ctypes.c_char_p
SEGMENTER.getSRIndex.restype = ctypes.c_char_p


class PySegmenter:

    """
    PySegmenter Python Wrapper for Segmenter class of segmenter C++ library
    """

    def __init__(self, image):
        self._segmenterinst = \
            SEGMENTER.getSegmenterInstance(ctypes.c_char_p(image.encode('UTF-8')))


    def __del__(self):
        SEGMENTER.destroySegmenterInstance(self._segmenterinst)


    def get_nsindex(self):

        """
        Return the nsindex
        """
        return str(SEGMENTER.getNSIndex(self._segmenterinst).decode('UTF-8'))

    def get_sindex(self):

        """
        Return the sindex
        """
        return str(SEGMENTER.getSIndex(self._segmenterinst).decode('UTF-8'))

    def get_rindex(self):

        """
        Return the rindex
        """
        return str(SEGMENTER.getRIndex(self._segmenterinst).decode('UTF-8'))

    def get_srindex(self):

        """
        Return the srindex
        """
        return str(SEGMENTER.getSRIndex(self._segmenterinst).decode('UTF-8'))
