"""
TeX Lookup module driver of the SCRiPTeX Application.
"""


import os
import filecmp

from modules.texlookup import texlookup


TEMPFILE = 'texlookup_temp'


def run_texlookup(infile, outfile):

    """
    Runs the tex lookup module on the passed input file, writing the tex markup to the
    passed output file

    Assumes that the input file exists and is valid.
    """

    # List for indices
    indices = []

    # Read input file
    with open(infile, 'r') as file:
        # Get number of symbols
        numsymbols = int(file.readline())
        # Append each index to list
        for _ in range(numsymbols):
            indices.append(file.readline())


    # Open output file
    with open(outfile, 'w+') as file:
        # Write numsymbols to output file
        file.write(repr(numsymbols) + '\n')
        # For each index
        for i in range(numsymbols):
            # Write the corresponding tex markup
            file.write(texlookup.get_tex(int(indices[i])) + '\n')


def test_texlookup(infile, expectedoutfile):

    """
    Runs the TeX lookup module on the passed input file and returns if the output
    matches the passed expected output file.

    Assumes that input file exists and is valid.
    """

    # Run TeX Lookup
    run_texlookup(infile, TEMPFILE + '.txt')

    # Compare files
    match = filecmp.cmp(expectedoutfile, TEMPFILE + '.txt')

    # Delete temporary file
    os.remove(TEMPFILE + '.txt')

    return match
