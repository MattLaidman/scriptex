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

SYMBOL_NUM_EPOCHS = 25000
SYMBOL_BATCH_SIZE = 100
SYMBOL_DISPLAY_STEP = 50

SCRIPT_NUM_EPOCHS = 10000
SCRIPT_BATCH_SIZE = 100
SCRIPT_DISPLAY_STEP = 50


SYMBOL_ACC = open('symbol_accuracy.dat', 'w+')
SYMBOL_XENT = open('symbol_xentropy.dat', 'w+')
SCRIPT_ACC = open('script_accuracy.dat', 'w+')
SCRIPT_XENT = open('script_xentropy.dat', 'w+')


DH = dh.DataHelper()
MODEL = nm.Model()

shutil.rmtree('recognizer/model') # Clear old network if exist
os.mkdir('recognizer/model') # Remake drectory

print('Training Symbol Network')
for i in range(SYMBOL_NUM_EPOCHS):
    # Get batch
    batch = DH.get_symbol_training_batch(SYMBOL_BATCH_SIZE)
    # Train network on batch
    MODEL.train_symbol_model(batch)
    # Compute accuracy for batch
    stats = MODEL.test_symbol_model(DH.get_symbol_testing_batch(SYMBOL_BATCH_SIZE))
    SYMBOL_XENT.write(repr(i+1) + ' ' + repr(stats[0]) + '\n')
    SYMBOL_ACC.write(repr(i+1) + ' ' + '{0:.2f}'.format(stats[1]) + '\n')
    if i != 0 and i % SYMBOL_DISPLAY_STEP == 0:
        print(repr(i) + ' ' + repr(stats[0]) + ' ' + '{0:.2f}'.format(stats[1]))
    gc.collect()
SYMBOL_ACC.close()
SYMBOL_XENT.close()


print('\nTraining Script Network')
for i in range(SCRIPT_NUM_EPOCHS):
    # Get batch
    batch = DH.get_script_training_batch(SCRIPT_BATCH_SIZE)
    # Train network on batch
    MODEL.train_symbol_model(batch)
    # Compute accuracy for batch
    stats = MODEL.test_symbol_model(DH.get_script_testing_batch(SCRIPT_BATCH_SIZE))
    SCRIPT_XENT.write(repr(i+1) + ' ' + repr(stats[0]) + '\n')
    SCRIPT_ACC.write(repr(i+1) + ' ' + '{0:.2f}'.format(stats[1]) + '\n')
    if i != 0 and i % SCRIPT_DISPLAY_STEP == 0:
        print(repr(i) + ' ' + repr(stats[0]) + ' ' + '{0:.2f}'.format(stats[1]))
    gc.collect()
SCRIPT_ACC.close()
SYMBOL_XENT.close()



print('Saving Network')
MODEL.save_model(MODEL_NAME)
