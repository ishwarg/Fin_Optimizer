import os
import numpy as np
from numpy.core.fromnumeric import sort
from numpy.lib import index_tricks
import orhelper
import functions as fs
from orhelper import FlightDataType 

# total_gen is defined in functions.py

valid_combos_full = fs.valid_total_gen()
# We now have all valid combos in a total_gen by 6 array

# This next step of evaluating cost functions will not be done until we have 1000 valid combinations
# Will have to get the predicted height from simulation -> predict all heights for all combinations at the same time
# So, pred_h is a 1 by 1000 array of predicted heights

#########


def calculate_height(valid_combos_full):
    pred_h = np.zeros((1000)) # temporary
    return pred_h

def calculate_cost(pred_h):
    costs=[(x*-1 + 30500) for x in pred_h]
    return np.square(costs)
