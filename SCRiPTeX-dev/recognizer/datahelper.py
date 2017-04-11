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

        self._trainingsymbols = [None]*self._numcharacters
        self._trainingsymbolslabels = [None]*self._numcharacters

        self._testingsymbols = [None]*self._numcharacters
        self._testingsymbolslabels = [None]*self._numcharacters


        self._read_data()

    def _read_data(self):

        """
        Reads the entire training and testing datasets into a list.
        """

        os.chdir('recognizer/symbols/training')
        trainingfiles = os.listdir()

        for f in trainingfiles:
            with open(f, 'r') as file:
                numsamples = file.readline()
                self._trainingsymbols[int(file.name[:-4])] = []
                for _ in range(int(numsamples)):
                    self._trainingsymbols[int(file.name[:-4])].append(list(map(int, file.readline().split())))
                    temp = [0]*self._numcharacters
                    temp[int(file.name[:-4])] = 1
                    self._trainingsymbolslabels[int(file.name[:-4])] = temp

        os.chdir('../testing')
        testingfiles = os.listdir()

        for f in testingfiles:
            with open(f, 'r') as file:
                numsamples = file.readline()
                self._testingsymbols[int(file.name[:-4])] = []
                for _ in range(int(numsamples)):
                    self._testingsymbols[int(file.name[:-4])].append(list(map(int, file.readline().split())))
                    temp = [0]*self._numcharacters
                    temp[int(file.name[:-4])] = 1
                    self._testingsymbolslabels[int(file.name[:-4])] = temp

        os.chdir('../../../')


    def get_training_batch(self, size):

        """
        Returns a batch of training data of given size.
        """

        batch = []
        symbols = []
        labels = []

        i = 0
        for _ in range(size):
            index = random.randint(0, len(self._trainingsymbols)-1)
            while self._trainingsymbols[index] == None:
                index = random.randint(0, len(self._trainingsymbols)-1)
            symbols.append(self._trainingsymbols[index][random.randint(0, len(self._trainingsymbols[index])-1)])
            labels.append(self._trainingsymbolslabels[index])

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
            while self._testingsymbols[index] == None:
                index = random.randint(0, len(self._testingsymbols)-1)
            symbols.append(self._testingsymbols[index][random.randint(0, len(self._testingsymbols[index])-1)])
            labels.append(self._testingsymbolslabels[index])

        batch.append(symbols)
        batch.append(labels)

        return batch
