import os
import random
import numpy as np
from numpy.core.fromnumeric import shape
import orhelper
from orhelper import FlightDataType


def generate_chromosome():
    '''
    First two entries are the tip chords of both stages (first stage then second stage),
    then sweep lengths of both stages and then the fin heights for both stages.
    Output a chromosome with valid dimensions.
    '''
    random.seed()
    chromosome=[random.randrange(0,200),random.randrange(0,200),
    random.randrange(0,200),random.randrange(0,200), 
    random.randrange(100,200),random.randrange(100,200)]
    # This loop makes sure that the tip chord of a fin combination does
    # not extend over the back of the root chord for aesthetic reasons 
    while (chromosome[0]+chromosome[2])>300 and (chromosome[1]+chromosome[3])>300:
        chromosome=[random.randrange(0,200),random.randrange(0,200),
        random.randrange(0,200),random.randrange(0,200), 
        random.randrange(100,200),random.randrange(100,200)]
    return chromosome


def create_generation(size):
    '''
    Create initial generation of size
    Output is an array of dimensions size by 6
    Not all outputs will pass the validity test based on simulated stability
    '''
    i=0
    array=np.empty([size,6], dtype=int)
    while i<size:
        array[i,:]=np.array(generate_chromosome())
        i+=1
    return array


def calculate_cost(pred_h, target_height):
    '''
    Cost function. Inputs are the simulated value for 
    height as well as the target height.
    '''
    costs=np.empty(len(pred_h))
    costs=(target_height-pred_h)**2
    return costs


def choose_parents(all_parents, all_costs):
    '''
    One input is an array of size by 6, which is a current batch of all parents.
    The second input is the corresponding size by 1 dimension array of associated
    costs for each parent. Returns array of chosen parents based on likelihood
    of parent. Output array size is same as input "all_parents (size by 6)."
    A single parent may be selected multiple times, and therefore be paired up
    to form multiple children, especially if the parent has a favorable cost value.  
    '''
    random.seed()
    worst=max(all_costs)
    indexofmin=np.argmin(all_costs)
    all_costs[indexofmin]+=1
    likelihood= worst/all_costs
    length=len(all_parents)
    chosen_ones=all_parents[random.choices(range(length),weights=likelihood,k=length),:]
    return chosen_ones


def crossover(combos, index_to_consider, all_costs):
    '''
    Cross over the chosen parents to create children until children
    is the same shape as the full original size by 6 array.
    '''
    random.seed()
    parents=choose_parents(combos[index_to_consider:,:],all_costs[index_to_consider:])
    length=len(combos)
    children=np.empty(np.shape(combos), dtype=np.int32)

    count=0
    while count<index_to_consider:
        children[count,:]=combos[count,:]
        count+=1

    while count<length:
        beta=random.random()
        crossover_point=random.randint(0,5)
        child1=parents[count-index_to_consider]
        child2=parents[count+1-index_to_consider]

        child1[crossover_point]=(1-beta)*child1[crossover_point]+beta*child2[crossover_point]
        child2[crossover_point]=(1-beta)*child2[crossover_point]+beta*child1[crossover_point]

        children[count]=child1
        children[count+1]=child2
        
        count+=2
        
    return children

def mutate(children,prob_mutation,max_mutation):
    '''
    Mutation function takes in a fin combinations array of dimensions
    size by 6, and two 1 by 6 arrays representing the probability of mutation
    for each parameter of the fins as well as the maximum amount of mutation
    for each parameter. Mutate outputs a size by 6 array of fin combinations,
    some of which have been mutated in one or more combination parameters. 
    '''
    temp = np.array(children)
    for i in temp:
        will_mutate = (prob_mutation > np.random.uniform(0, 1))
        c = 0
        while c < len(i):
            if (will_mutate[c] == True):
                i[c] = i[c] + max_mutation[c]*np.random.uniform(-1, 1)
            c+=1
    return temp.astype(int)






