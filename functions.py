import random
import numpy

def generate_chromosome():
    random.seed(version=2)
    #first two entries are the tip chords of both stages, then sweep lengths 
    # of both stages and then the fin heights for both stages
    chromosome=[random.randrange(0,200),random.randrange(0,200),
    random.randrange(0,200),random.randrange(0,200), 
    random.randrange(100,200),random.randrange(100,200)]
    #this loop makes sure that the tip chord of a fin combination does
    # does not extend over the back of the root chord for aesthetic reasons 
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







