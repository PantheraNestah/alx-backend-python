#!/usr/bin/python3
import sys
processing = __import__('1-batch_processing')

##### print processed users in a batch of 50
try:
    for user in processing.batch_processing(50):
        pass
except BrokenPipeError:
    sys.stderr.close()