import os
import random
import numpy as np
from numpy.core.fromnumeric import shape
import orhelper
from orhelper import FlightDataType

def convert_to_continuous_string(array):
    count=0
    string=""
    while(count<len(array)):
        x=array[count]
        if x<10:
            string+="00"
            string+=str(x)
        elif x<100:
            string+="0"
            string+=str(x)
        else:
            string+=str(x)
        count+=1
    return string

def convert_string_to_array(string):
    count=0
    array=[None]*6
    secondcount=0
    while(secondcount<6):
        array[secondcount]=int(string[count:count+3])
        count+=3
        secondcount+=1
    return array

def generation_function_whateverItIs(generate_more):
    i = 0
    arr = np.empty((0, 6), float)
    while (i < generate_more):
        a = np.random.uniform(0, 5)
        b = np.random.uniform(0, 5)
        c = np.random.uniform(0, 5)
        d = np.random.uniform(0, 5)
        e = np.random.uniform(0, 5)
        f = np.random.uniform(0, 5)
        temp = np.array([[a, b, c, d, e, f]])
        arr = np.append(arr, temp, axis = 0)
        i +=1
    return arr

def calculate_stability(combos):
    i = 0
    pred_sb1 = np.array([])
    pred_sb2 = np.array([])
    while (i < len(combos)):
        pred_sb1 = np.append(pred_sb1, (combos[i][0]+combos[i][1]+combos[i][2]))
        pred_sb2 = np.append(pred_sb2, combos[i][0]+combos[i][1]+0)
        i+=1
    pred_sb = np.array([pred_sb1, pred_sb2])
    return pred_sb

# Package of disused functions:

total_gen = 10

def toss_and_more(pred_sb, valid_combos, combos):
    # avg stab is 7.5 and 5 for the two stages
    sb_min_full = 9 # Minimum stability full rocket
    sb_min_stage2 = 4 # Minimum stability 2nd stage
    i = 0
    filter_arr = (pred_sb[0] > sb_min_full)*(pred_sb[1] > sb_min_stage2)
    filters = combos[filter_arr]
    valid_combos = np.append(valid_combos, filters, axis = 0)
    generate_more = total_gen - np.size(valid_combos[:, 0])
    return valid_combos, generate_more 

def generate(valid_combos, generate_more):
    combos = generation_function_whateverItIs(generate_more)
    pred_sb = calculate_stability(combos)
    valid_combos, generate_more = toss_and_more(pred_sb, valid_combos, combos)
    return valid_combos, generate_more

def valid_total_gen():
    generate_more = total_gen
    valid_combos = np.empty((0,6), float) # Empty array
    valid_combos, generate_more = generate(valid_combos, generate_more)
    while (generate_more > 0):
        valid_combos, generate_more = generate(valid_combos, generate_more)
        #print(np.size(valid_combos[:, 0]), generate_more)
    return valid_combos