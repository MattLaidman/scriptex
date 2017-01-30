"""
TeX Lookup module driver of the SCRiPTeX Application.
"""


"""
TeX Assembly module driver of the SCRiPTeX Application.
"""

import os
import filecmp

from modules.texassembly import texassembly


TEMPFILE = 'texassembly_temp'


def run_texassembly(charmap, symbols, outfile):

    """
    Runs the TeX Assembly module on the passed input file, writing the tex markup to the
    passed output file

    Assumes that the input file exists and is valid.
    """

    texassembly.assemble_document(charmap, symbols, outfile)


def test_texassembly(charmap, symbols, expectedoutfile):

    """
    Runs the TeX Assembly module on the passed input file and returns if the output
    matches the passed expected output file.

    Assumes that input file exists and is valid.
    """

    # Run TeX Assembly
    run_texassembly(charmap, symbols, TEMPFILE + '.txt')

    # Compare files
    match = filecmp.cmp(expectedoutfile, TEMPFILE + '.txt')

    # Delete temporary file
    os.remove(TEMPFILE + '.txt')

    return match
