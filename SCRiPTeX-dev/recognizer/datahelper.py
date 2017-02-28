"""
Helper utility used in the training of the Character Recognition module's Neural Network

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

        self._numcharacters = 0

        self._trainingsymbols = []
        self._traininglabels = []

        self._testingsymbols = []
        self._testinglabels = []

        self._read_data()
        self._shuffle_data()

    def _read_data(self):

        """
        Reads the entire training and testing datasets into a list.
        """

        os.chdir('recognizer/symbols/training')
        trainingfiles = os.listdir()
        self._numcharacters = len(trainingfiles)

        for i in range(self._numcharacters):
            with open(trainingfiles[i], 'r') as file:
                numsamples = file.readline()
                for _ in range(int(numsamples)):
                    self._trainingsymbols.append(file.readline().split())
                    temp = [0]*107
                    temp[int(file.name[:-4])] = 1
                    self._traininglabels.append(temp)

        os.chdir('../testing')
        testingfiles = os.listdir()

        for i in range(self._numcharacters):
            with open(testingfiles[i], 'r') as file:
                numsamples = file.readline()
                for _ in range(int(numsamples)):
                    self._testingsymbols.append(file.readline().split())
                    temp = [0]*107
                    temp[int(file.name[:-4])] = 1
                    self._testinglabels.append(temp)

        os.chdir('../../../')


    def _shuffle_data(self):

        """
        Shuffles the training and testing data lists.
        """

        temp = list(zip(self._trainingsymbols, self._traininglabels))
        random.shuffle(temp)
        self._trainingsymbols, self._traininglabels = zip(*temp)

        temp = list(zip(self._testingsymbols, self._testinglabels))
        random.shuffle(temp)
        self._testingsymbols, self._testinglabels = zip(*temp)


    def get_training_batch(self, size):

        """
        Returns a batch of training data of given size.
        """

        batch = []
        symbols = []
        labels = []

        for _ in range(size):
            index = random.randint(0, len(self._trainingsymbols)-1)
            symbols.append(self._trainingsymbols[index])
            labels.append(self._traininglabels[index])

        batch.append(symbols)
        batch.append(labels)

        return batch

    def get_testing_batch(self, size):

        """
        Returns a batch of testing data of given size.
        """

        batch = []
        symbols = []
        labels = []

        for _ in range(size):
            index = random.randint(0, len(self._testingsymbols)-1)
            symbols.append(self._testingsymbols[index])
            labels.append(self._testinglabels[index])

        batch.append(symbols)
        batch.append(labels)

        return batch
