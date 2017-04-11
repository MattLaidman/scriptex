#!/usr/bin/env python3

"""
A utility for use in developement of the SCRiPTeX application.

Trains and saves a networks according to the parameters
"""


import gc
import os
import shutil

import recognizer.networkmodel as nm
import recognizer.datahelper as dh


# Parameters

MODEL_NAME = 'recognizer/model/model'

NUM_EPOCHS = 5000
BATCH_SIZE = 100
DISPLAY_STEP = 50


ACC = open('symbol_accuracy.dat', 'w+')
XENT = open('symbol_xentropy.dat', 'w+')


DH = dh.DataHelper()
MODEL = nm.Model()

try:
    shutil.rmtree('recognizer/model') # Clear old network if exist
except:
    pass
os.mkdir('recognizer/model') # Remake drectory

print('Training Symbol Network')
for i in range(NUM_EPOCHS):
    # Get batch
    batch = DH.get_training_batch(BATCH_SIZE)
    # Train network on batch
    MODEL.train_model(batch)
    # Compute accuracy for batch
    stats = MODEL.test_model(DH.get_testing_batch(BATCH_SIZE))
    XENT.write(repr(i+1) + ' ' + repr(stats[0]) + '\n')
    ACC.write(repr(i+1) + ' ' + '{0:.2f}'.format(stats[1]) + '\n')
    if i != 0 and i % DISPLAY_STEP == 0:
        print(repr(i) + ' ' + repr(stats[0]) + ' ' + '{0:.2f}'.format(stats[1]))
    gc.collect()
ACC.close()
XENT.close()


print('Saving Network')
MODEL.save_model(MODEL_NAME)
