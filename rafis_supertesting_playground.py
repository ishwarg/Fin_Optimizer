# Recieve: 1000 (valid or invalid) fin combinations that are children of good combos and elitists
# Array is 1000 by 6
import numpy as np


children = np.array([[0, 1, 2, 3, 4, 5.],[1, 2, 3, 4, 5, 6.]])

def mutate(children):
    prob_mutation = np.array([.25, 1, .3, .6, .9, 0])
    max_mutation = np.array([10, 5, 7, 10, 15, 3])
    for i in children:
        will_mutate = (prob_mutation > np.random.uniform(0, 1))
        c = 0
        while c < len(i):
            if (will_mutate[c] == True):
                i[c] = i[c] + max_mutation[c]*np.random.uniform(-1, 1)
            c+=1
    return children.astype(int)

mutated = mutate(children)
print(mutated)