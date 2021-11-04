import random
import numpy

def generate_chromosome():
    random.seed(version=2)
    #first two entries are the tip chords of both stages, then sweep lengths 
    # of both stages and then the fin heights for both stages
    chr=[random.randrange(0,200),random.randrange(0,200),
    random.randrange(0,200),random.randrange(0,200), 
    random.randrange(100,200),random.randrange(100,200)]
    #this loop makes sure that the tip chord of a fin combination does
    # does not extend over the back of the root chord for aesthetic reasons 
    while (chr(0)+chr(2))>300&(chr(1)+chr(3))>300:
        chr=[random.randrange(0,200),random.randrange(0,200),
        random.randrange(0,200),random.randrange(0,200), 
        random.randrange(100,200),random.randrange(100,200)]

    





