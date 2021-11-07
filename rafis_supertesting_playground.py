# Recieve: 1000 (valid or invalid) fin combinations that are children of good combos and elitists
# Array is 1000 by 6
import numpy as np

def mutate(children, rate_mutation):
    prob_mutation = np.array([.25, .5, .3, .4, .1, 0])
    #rate_mutation = np.array([.01, .01, .01, .01, .01, .01])
    will_mutate = np.array([False, False, False, False, False])
    i = 0
    while (i < len(children)):
        will_mutate = 
        if (prob_mutation[0] > np.random.rand()):
            children[i, 0]


rate_mutation = np.array([.01, .01, .01, .01, .01, .01])
#mutate(children, rate_mutation)