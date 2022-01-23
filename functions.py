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


def calculate_cost(pred_h, totalstabilities, target_height, offrod_target, sep_target, offrod_mul, sep_mul):
    '''
    Cost function. Inputs are the simulated value for 
    height, stability off rod, and stability at seperation.
    Additionally the target height and target stability off rod and at seperation.
    Finally, the multipliers for importance of offrod stability and seperation stability.
    '''
    costs=np.empty(len(pred_h))
    costs=((target_height-pred_h)**2 + offrod_mul*(offrod_target-totalstabilities[0])**2 + 
    sep_mul*(sep_target-totalstabilities[1])**2)
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


def get_flutter(root_chord, tip_chord, G, S, t, b, a, P, P0):
  '''
  These equations (get_flutter and get_divergence) are based on sources:

  https://www.abbottaerospace.com/downloads/naca-tn-4197-summary-of-flutter-experiences
  -as-a-guide-to-the-preliminary-design-of-lifting-surfaces-on-missiles/

  http://www.aerorocket.com/finsim.html

  https://apogeerockets.com/education/downloads/Newsletter291.pdf
  
  We found mistakes in the 2nd source (aerorocket) with regards to the lambda definition.
  These mistakes are corrected in our implementation of the equation.

  We recognize certain simplifications in these equations:
  Applies most accurately to trapezoidal fins, where root_chord and fin_chord
  are parallel.

  root_chord, tip_chord, and b are all parameters of the fin, used throughout genetic algorithm
  S, surface area, can be calculated from other parameters
  G and t, shear modulus and fin thickness, are inputs to the program defined at the top
  a and P, the speed of sound and atmospheric presures at maximum velocity location are extracted
  ... from OpenRocket during simulation step
  P0, the atmospheric presure at sea level at standard temperature,
  ... is a natural constant defined at the top of algorithm

  get_flutter returns the velocity at which fin flutter begins to occur
  get_divergence returns the velocity at which divergence begins to occur
  Flutter velocity is almost always lower than divergence velocity
  Divergence velocity should absolutely NEVER be exceeded
  Divergence velocity refers to the speed where the fins will
  ... increasingly flutter in a feedback loop.
  
  Make sure to leave a margin of error. The inputed shear modulus, G,
  ... should be the minimum value possible. Shear modulus in composites
  ... can vary significantly depending on direction etc. This number may be taken
  ... from manufacture specifications or elsewhere

  All inputs to the function are in meters, meters/second, and pascals. 
  Conversions neccesary since equation sources use units of freedom/eagle.
  '''
  # conversion equations
  m_to_inch = 39.370
  mpers_to_mph = 2.237
  pasc_to_psi = (1/6895.000)
  mph_to_mpers = (1/2.237)
  # conversions
  root_chord = root_chord*m_to_inch
  tip_chord = tip_chord*m_to_inch
  t = t*m_to_inch
  b = b*m_to_inch
  a = a*mpers_to_mph
  S = 0.5*(root_chord+tip_chord)*b
  G = G*pasc_to_psi
  P = P*pasc_to_psi
  P0 = P0*pasc_to_psi
  # formula
  lam = tip_chord/root_chord
  AR = (b**2)/S
  denom = ((39.3*(AR**3)) / (((t/root_chord)**3) * (AR + 2))) * ((lam+1)/2) * (P/P0)
  return (a * np.sqrt(G / denom))*mph_to_mpers


def get_divergence(root_chord, tip_chord, G, S, t, b, a, P, P0):
  '''
  Refer to comments in get_flutter
  All inputs are in meters, meters/second, and pascals. Conversions neccesary 
  since equation sources use units of freedom/eagle.
  '''
  # conversion equations
  m_to_inch = 39.370
  mpers_to_mph = 2.237
  pasc_to_psi = (1/6895.000)
  mph_to_mpers = (1/2.237)
  # conversions
  root_chord = root_chord*m_to_inch
  tip_chord = tip_chord*m_to_inch
  t = t*m_to_inch
  b = b*m_to_inch
  a = a*mpers_to_mph
  S = 0.5*(root_chord+tip_chord)*b
  G = G*pasc_to_psi
  P = P*pasc_to_psi
  P0 = P0*pasc_to_psi
  # formula  
  AR = (b**2)/S
  calc = (3.3*P)/(1+(2/AR)) * ((root_chord+tip_chord)/(t**3)) * b**2
  return a * np.sqrt(G / calc)*mph_to_mpers


