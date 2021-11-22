import os
import random
import numpy as np
import orhelper
from orhelper import FlightDataType
generation_size=10


def generate_chromosome():
    
    #first two entries are the tip chords of both stages (first stage then second stage),
    #then sweep lengths of both stages and then the fin heights for both stages
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
    array=[]
    while(count<size):
        array.append(generate_chromosome())
        count+=1
    return array
################

total_gen = 10

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

# This next step of evaluating cost functions will not be done until we have 1000 valid combinations


# Will have to get the predicted height from simulation -> predict all heights for all combinations at the same time
# So, pred_h is a 1 by 1000 array of predicted heights

#########


def calculate_height(valid_combos_full):
    pred_h = np.zeros((1000)) # temporary
    return pred_h

def calculate_cost(pred_h):
    costs=(30500-pred_h)**2
    return costs


def choose_parents(all_parents, all_costs):

   if len(all_costs):
    worst=max(all_costs)
    indexofmin=np.argmin(all_costs)
    all_costs[indexofmin]+=1
    likelihood=[worst/x for x in all_costs]
    chosen_ones=random.choices(all_parents,weights=likelihood,k=len(all_parents))

    return chosen_ones
   

    

def crossover(sorted_combos, index_to_consider, percent_to_consider, all_costs):


    amount=(int(percent_to_consider*len(sorted_combos))-index_to_consider)
    prelim_parents=sorted_combos[index_to_consider:amount]
    if len(prelim_parents) % 2 == 1:
        prelim_parents=sorted_combos[index_to_consider:amount]
    prelim_parents=sorted_combos[index_to_consider:]


    parents=choose_parents(prelim_parents,all_costs[index_to_consider:])
    

    children=[]

    count=0
    length=len(parents)
    if length == 1:
        return parents
    else:
        while count<length:
            beta=random.random()
            crossover_point=random.randint(0,5)
    while count<length:
        beta=random.random()
        crossover_point=random.randint(0,5)
        child1=parents[count]
        child2=parents[count+1]

        child1[crossover_point]=(1-beta)*child1[crossover_point]+beta*child2[crossover_point]
        child2[crossover_point]=(1-beta)*child2[crossover_point]+beta*child1[crossover_point]

        children.append(child1)
        children.append(child2)
        
        count+=2
        
            
    while count<generation_size:
        children.append(generate_chromosome())
        count+=1
    return children

def mutate(children):
    temp = children.copy()
    prob_mutation = np.array([.25, 1, .3, .6, .9, 0])
    max_mutation = np.array([10, 5, 7, 10, 15, 3])
    for i in temp:
        will_mutate = (prob_mutation > np.random.uniform(0, 1))
        c = 0
        while c < len(i):
            if (will_mutate[c] == True):
                i[c] = i[c] + max_mutation[c]*np.random.uniform(-1, 1)
            c+=1
    temp.astype(int)
   
    return temp

def simulatefincombo(fincombo,stability1,stability2):

    with orhelper.OpenRocketInstance() as instance:
        orh = orhelper.Helper(instance)
        doc = orh.load_doc(os.path.join('examples', 'Tantalus.ork'))
        sim = doc.getSimulation(0)
        opts = sim.getOptions()
        rocket = opts.getRocket()

        fins=convert_string_to_array(fincombo)
        firststagefins=orh.get_component_named(rocket, "First Stage Fins")
        secondstagefins=orh.get_component_named(rocket, "Second Stage Fins")
        firststagefins.setTipChord(float(fins[0])/1000)
        firststagefins.setSweep(float(fins[2])/1000)
        firststagefins.setHeight(float(fins[4])/1000)
        secondstagefins.setTipChord(float(fins[1])/1000)
        secondstagefins.setSweep(float(fins[3])/1000)
        secondstagefins.setHeight(float(fins[5])/1000)
        
        
        orh.run_simulation(sim)
        data=orh.get_timeseries(sim, [FlightDataType.TYPE_TIME,FlightDataType.TYPE_ALTITUDE, FlightDataType.TYPE_STABILITY,FlightDataType.TYPE_VELOCITY_TOTAL])
        events = orh.get_events(sim)
        eventsvaluesdic=list(events.values())
        times=list(data[FlightDataType.TYPE_TIME])
        altitude=list(data[FlightDataType.TYPE_ALTITUDE])

        stabilityoffrod=data[FlightDataType.TYPE_STABILITY][times.index(eventsvaluesdic[3])]
        stabilityatseperation=data[FlightDataType.TYPE_STABILITY][times.index(eventsvaluesdic[6])]

        #include that checks for flutter here if possible and add a true false into outputlist

        outputlist=[max(altitude),stabilityoffrod<stability1,stabilityatseperation<stability2,max(data[FlightDataType.TYPE_VELOCITY_TOTAL])]

        return outputlist




    


# run





