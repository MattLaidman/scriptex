#!/usr/bin/env python3

"""
A utility for use in developement of the SCRiPTeX application.

Trains and saves a networks according to the parameters
"""


import recognizer.networkmodel as nm
import recognizer.datahelper as dh


# Parameters

NUM_TESTS = 1000
BATCH_SIZE = 250
MODEL_NAME = 'recognizer/model/model'


DH = dh.DataHelper()
MODEL = nm.Model(MODEL_NAME)

accuracy = [0.0]*NUM_TESTS


for i in range(NUM_TESTS):
    batch = DH.get_testing_batch(BATCH_SIZE)

    accuracy[i] = MODEL.test_model(batch)
    print(repr(i) + ' ' + repr(accuracy[i]))

accuracy_sum = 0.0

for i in range(NUM_TESTS):
    accuracy_sum = accuracy_sum + accuracy[i]


print('Average Accuracy: ' + repr(accuracy_sum/NUM_TESTS))