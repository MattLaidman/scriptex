"""
Character Recognition module driver of the SCRiPTeX Application.
"""


import modules.characterrecognition.networkmodel as nm


NUM_CLASSES = 107


# Create and load network model
MODEL = nm.Model('modules/characterrecognition/model/model')


def run_characterrecognition(infile, outfile):

    """
    Runs the character recognition module on the passed input file and outputs recognized
    character indices to passed output file.

    Assumes that input file exists and is valid. Output file will be overwritten if it exists.
    """

    symbols = []

    # Read input file
    with open(infile, 'r') as file:
        # Get number of symbols
        numsymbols = int(file.readline())
        # Append each image to list as list of pixel values
        for _ in range(numsymbols):
            symbols.append(file.readline().split())

    # Recognize symbols
    if numsymbols != 0:
        recognizedsymbols = MODEL.run_model(symbols)

    # Write to output file
    with open(outfile, 'w') as file:
        # Write number of symbols to file
        file.write(repr(numsymbols) + '\n')
        # Write each symbol index to file
        for i in range(numsymbols):
            file.write(repr(recognizedsymbols[i]) + '\n')


def test_characterrecognition(infile, expectedoutfile):

    """
    Runs the character recognition module on the passed input file and returns the accuracy
    of the batch.

    Assumes that input file exists and is valid.
    """

    symbols = []

    # Read input file
    with open(infile, 'r') as file:
        # Get number of symbols
        numinputsymbols = int(file.readline())
        # Append each image to list as list of pixel values
        for _ in range(numinputsymbols):
            symbols.append(file.readline().split())

    indices = []

    # Read expected output file
    with open(expectedoutfile, 'r') as file:
        # Get number of symbols
        numindices = int(file.readline())
        # Append each index to list
        for _ in range(numindices):
            indices.append(file.readline())

    # Convert each index to a one-hot vector
    for i in range(numindices):
        # Create a list of zeros
        temp = [0] * NUM_CLASSES
        # Make corresponding index 1
        temp[int(indices[i])] = 1
        # Replace the index with the one-hot vector
        indices[i] = temp

    # Create a network test batch from symbols and indices
    batch = []
    batch.append(symbols)
    batch.append(indices)

    # Return the accuracy of the batch
    return MODEL.test_model(batch)
