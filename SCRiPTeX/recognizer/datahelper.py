"""
Helper utility used in the training of the Convolutional Neural Network

Reads data sets and creates training/testing lists
Expects that files exists, that there are equal number of characters (files) in both
training/testing directories, and that file names match.
"""


import os
import random


class DataHelper:

    """
    A helper class for the model trainer script to manage the training and testing datasets.
    """

    def __init__(self):

        self._numcharacters = 126

        self._trainingsymbols = []
        self._trainingsymbolslabels = []

        self._testingsymbols = []
        self._testingsymbolslabels = []

        self._trainingscripts = []
        self._trainingscriptslabels = []

        self._testingscripts = []
        self._testingscriptslabels = []

        self._read_data()
        self._shuffle_data()

    def _read_data(self):

        """
        Reads the entire training and testing datasets into a list.
        """

        os.chdir('recognizer/symbols/training')
        trainingfiles = os.listdir()

        for f in trainingfiles:
            with open(f, 'r') as file:
                numsamples = file.readline()
                for _ in range(int(numsamples)):
                    self._trainingsymbols.append(file.readline().split())
                    temp = [0]*self._numcharacters
                    temp[int(file.name[:-4])] = 1
                    self._trainingsymbolslabels.append(temp)

        os.chdir('../testing')
        testingfiles = os.listdir()

        for f in testingfiles:
            with open(f, 'r') as file:
                numsamples = file.readline()
                for _ in range(int(numsamples)):
                    self._testingsymbols.append(file.readline().split())
                    temp = [0]*self._numcharacters
                    temp[int(file.name[:-4])] = 1
                    self._testingsymbolslabels.append(temp)

        os.chdir('../../scripts/training')
        trainingfiles = os.listdir()

        for f in trainingfiles:
            with open(f, 'r') as file:
                numsamples = file.readline()
                for _ in range(int(numsamples)):
                    self._trainingscripts.append(file.readline().split())
                    temp = [0]*self._numcharacters
                    temp[int(file.name[:-4])] = 1
                    self._trainingscriptslabels.append(temp)

        os.chdir('../testing')
        testingfiles = os.listdir()

        for f in testingfiles:
            with open(f, 'r') as file:
                numsamples = file.readline()
                for _ in range(int(numsamples)):
                    self._testingscripts.append(file.readline().split())
                    temp = [0]*self._numcharacters
                    temp[int(file.name[:-4])] = 1
                    self._testingscriptslabels.append(temp)

        os.chdir('../../../')


    def _shuffle_data(self):

        """
        Shuffles the training and testing data lists.
        """

        temp = list(zip(self._trainingsymbols, self._trainingsymbolslabels))
        random.shuffle(temp)
        self._trainingsymbols, self._trainingsymbolslabels = zip(*temp)

        temp = list(zip(self._testingsymbols, self._testingsymbolslabels))
        random.shuffle(temp)
        self._testingsymbols, self._testingsymbolslabels = zip(*temp)

        temp = list(zip(self._trainingscripts, self._trainingscriptslabels))
        random.shuffle(temp)
        self._trainingscripts, self._trainingscriptslabels = zip(*temp)

        temp = list(zip(self._testingscripts, self._testingscriptslabels))
        random.shuffle(temp)
        self._testingscripts, self._testingscriptslabels = zip(*temp)


    def get_symbol_training_batch(self, size):

        """
        Returns a batch of training data of given size.
        """

        batch = []
        symbols = []
        labels = []

        for _ in range(size):
            index = random.randint(0, len(self._trainingsymbols)-1)
            symbols.append(self._trainingsymbols[index])
            labels.append(self._trainingsymbolslabels[index])

        batch.append(symbols)
        batch.append(labels)

        return batch

    def get_symbol_testing_batch(self, size):

        """
        Returns a batch of testing data of given size.
        """

        batch = []
        symbols = []
        labels = []

        for _ in range(size):
            index = random.randint(0, len(self._testingsymbols)-1)
            symbols.append(self._testingsymbols[index])
            labels.append(self._testingsymbolslabels[index])

        batch.append(symbols)
        batch.append(labels)

        return batch

    def get_script_training_batch(self, size):

        """
        Returns a batch of training data of given size.
        """

        batch = []
        scripts = []
        labels = []

        for _ in range(size):
            index = random.randint(0, len(self._trainingscripts)-1)
            scripts.append(self._trainingscripts[index])
            labels.append(self._trainingscriptslabels[index])

        batch.append(scripts)
        batch.append(labels)

        return batch

    def get_script_testing_batch(self, size):

        """
        Returns a batch of testing data of given size.
        """

        batch = []
        scripts = []
        labels = []

        for _ in range(size):
            index = random.randint(0, len(self._testingscripts)-1)
            scripts.append(self._testingscripts[index])
            labels.append(self._testingscriptslabels[index])

        batch.append(scripts)
        batch.append(labels)

        return batch
