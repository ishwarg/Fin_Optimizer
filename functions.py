import random
import numpy
import orhelper

def generate_chromosome():
    random.seed(version=2)
    #first two entries are the tip chords of both stages, then sweep lengths 
    # of both stages and then the fin heights for both stages
    chromosome=[random.randrange(0,200),random.randrange(0,200),
    random.randrange(0,200),random.randrange(0,200), 
    random.randrange(100,200),random.randrange(100,200)]
    #this loop makes sure that the tip chord of a fin combination does
    #not extend over the back of the root chord for aesthetic reasons 
    while (chromosome[0]+chromosome[2])>300 and (chromosome[1]+chromosome[3])>300:
        chromosome=[random.randrange(0,200),random.randrange(0,200),
        random.randrange(0,200),random.randrange(0,200), 
        random.randrange(100,200),random.randrange(100,200)]
    return chromosome

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


#creates a population of potential solutions with a "size" 
# with each solution stored as a string
def create_generation(size):
    count=0
    array=[None]*size
    while(count<size):
        array[count]=convert_to_continuous_string(generate_chromosome())
        count+=1
    print("done")
    return array

################


import numpy as np


# Combos is an 1 by 1000 array of the 1000 fin cominations


# Will get the predicted stabilities from OR -> predict all stabilities for all combinations at the same time, 
# ... for both the full rocket and 2nd stage
# So, pred_sb is a 2 by 1000 array of predicted stabilities

def calculate_stability(combos):
    pred_sb = np.zeros((2,1000)) # temporary
    return pred_sb

def toss_and_more(pred_sb, valid_combos, combos):
    sb_min_full = 1.6 # Minimum stability full rocket
    sb_min_stage2 = 1.4 # Minimum stability 2nd stage
    valid_combos = valid_combos.append(combos[(pred_sb[0] > sb_min_full) and (pred_sb[1] > sb_min_stage2)])
    generate_more = 1000 - np.size(valid_combos)
    return valid_combos, generate_more 
    # Returns an array 1 by (less or equal to 1000), 
    # and returns the number of new combos that need to be generated due to being tossed out
    # generate_more will be fed into the generating function to create more combos ... 
    # those combos will then be analyzed for this entire section again to approve validity and calculate cost

# helper function
def generate(generate_more):
    combos = generation_function_whateverItIs(generate_more)
    pred_sb = calculate_stability(combos)
    valid_combos, generate_more = toss_and_more(pred_sb)
    return valid_combos, generate_more

# combination final function 
def valid_1000():
    generate_more = 1000
    valid_combos = np.zeros(()) # Empty array
    valid_combos, generate_more = generate(generate_more)
    while (generate_more > 0):
        valid_combos, generate_more = generate(generate_more)
    return valid_combos

valid_combos_full = valid_1000()


# This next step of evaluating cost functions will not be done until we have 1000 valid combinations


# Will have to get the predicted height from simulation -> predict all heights for all combinations at the same time
# So, pred_h is a 1 by 1000 array of predicted heights
def calculate_height(valid_combos_full):
    pred_h = np.zeros((1000)) # temporary
    return pred_h

def calculate_cost(pred_h):
    return (30,500 - pred_h)**2


def crossover(sorted_combos, index_to_consider, percent_to_consider):
    amount=(int(percent_to_consider*len(sorted_combos))-index_to_consider)
    if amount-index_to_consider % 2 !=0:
        amount-=1
    parents=sorted_combos[index_to_consider:amount]
    children=[None]*len(parents)

    count=0
    while count<len(parents):
        beta=random.random()
        crossover_point=random.range(0,6)

        child1=convert_string_to_array(parents[count])
        child2=convert_string_to_array(parents[count+1])

        child1[crossover_point]=(1-beta)*child1[crossover_point]+beta*child2[crossover_point]
        child2[crossover_point]=(1-beta)*child2[crossover_point]+beta*child1[crossover_point]

        children[count]=convert_to_continuous_string(child1)
        children[count+1]=convert_to_continuous_string(child2)
        
        count+=2
        
    return children



    


# run
pred_h = calculate_height()
costs = calculate_cost(pred_h)




