# Final Genetic Algorithm

'''
Ishwarjot Grewal and Rafi Hakim
'''

# Imports
import os
from numpy.core.fromnumeric import sort
from numpy.lib import index_tricks
from numpy.lib.function_base import average
import orhelper
import numpy as np
import functions as fs
from orhelper import FlightDataType 
from orhelper import FlightEvent

import threading
import time
import sys
import locale



# Comments
'''
# Stopping condition (for now will be a simple max number of generations)
# Required stabilities at different flight events are inputted
# Probability of mutation per run and maximum integer +- mutation value
# can be set individually for each parameter out of 6
'''

# Target Variables
target_height = 30500
launchrod=1.55 # minimum stability off rod
seperation=2.0 # minimum stability at seperation
offrod_target = 2 # ideal stability off rod
sep_target = 2 # ideal stability at seperation

# Learning Variables:
generation_size=50# Input as even integer
num_generations=50 # Input as integer
prob_mutation = np.array([.7, .7, .3, .3, .5, .5])  # Input as 1 by 6 array
max_mutation = np.array([16, 16, 14, 14, 12, 12])  # Input as 1 by 6 array
offrod_mul = 10 # recommended to be set to around 
sep_mul = 10 # recommended to be set to around 

# Other Variables
or_file_name = 'Tantalus.ork'  # Input as string
G = "shear modulus" # may differ in directions, use minimum value with safety factor 
t = "fin thickness"
apogees=np.empty(generation_size)
children=fs.create_generation(generation_size)
locale.setlocale(locale.LC_ALL, '')


# Natural and Convenient Variables
P0 = "atmospheric presure @ sea level temp height"

#simulating a single combination for multi threading purposes
def simulate_fin_combo(index):
	
	
	chromosome=children[index,:]
		
	

	firststagefins.setTipChord(float(chromosome[0])/1000)
	firststagefins.setSweep(float(chromosome[2])/1000)
	firststagefins.setHeight(float(chromosome[4])/1000)
	secondstagefins.setTipChord(float(chromosome[1])/1000)
	secondstagefins.setSweep(float(chromosome[3])/1000)
	secondstagefins.setHeight(float(chromosome[5])/1000)
	orh.run_simulation(sim)
	data=orh.get_timeseries(sim, [FlightDataType.TYPE_TIME,FlightDataType.TYPE_ALTITUDE, FlightDataType.TYPE_STABILITY,FlightDataType.TYPE_VELOCITY_TOTAL])
	events = orh.get_events(sim)
			
	ind=np.where(data[FlightDataType.TYPE_TIME]==events[FlightEvent.LAUNCHROD])
	
	
	
	stabilityoffrod=data[FlightDataType.TYPE_STABILITY][ind[0]]
	
	ind=np.where(data[FlightDataType.TYPE_TIME]==events[FlightEvent.STAGE_SEPARATION])
	stabilityatseperation=data[FlightDataType.TYPE_STABILITY][ind[0]]
	
	ind=np.where(data[FlightDataType.TYPE_TIME]==events[FlightEvent.APOGEE])
	apogee=data[FlightDataType.TYPE_ALTITUDE][ind[0]]
	#include that checks for flutter here if possible and add a true false into outputlist

	outputs=[apogee,stabilityoffrod<launchrod,stabilityatseperation<seperation,max(data[FlightDataType.TYPE_VELOCITY_TOTAL])]
	
	
	apogees[index]=apogee
	
		
	while outputs[1] or outputs[2]:
		chromosome=fs.generate_chromosome()
		
		firststagefins.setTipChord(float(chromosome[0])/1000)
		firststagefins.setSweep(float(chromosome[2])/1000)
		firststagefins.setHeight(float(chromosome[4])/1000)
		secondstagefins.setTipChord(float(chromosome[1])/1000)
		secondstagefins.setSweep(float(chromosome[3])/1000)
		secondstagefins.setHeight(float(chromosome[5])/1000)
		
		
		orh.run_simulation(sim)
		data=orh.get_timeseries(sim, [FlightDataType.TYPE_TIME,FlightDataType.TYPE_ALTITUDE, FlightDataType.TYPE_STABILITY,FlightDataType.TYPE_VELOCITY_TOTAL])
		events = orh.get_events(sim)

		ind=np.where(data[FlightDataType.TYPE_TIME]==events[FlightEvent.LAUNCHROD])
		stabilityoffrod=data[FlightDataType.TYPE_STABILITY][ind[0]]
		ind=np.where(data[FlightDataType.TYPE_TIME]==events[FlightEvent.STAGE_SEPARATION])
		stabilityatseperation=data[FlightDataType.TYPE_STABILITY][ind[0]]
		ind=np.where(data[FlightDataType.TYPE_TIME]==events[FlightEvent.APOGEE])
		apogee=data[FlightDataType.TYPE_ALTITUDE][ind[0]]
		# include that checks for flutter here if possible and add a true false into outputlist

		outputs=[apogee,stabilityoffrod<launchrod,stabilityatseperation<seperation,max(data[FlightDataType.TYPE_VELOCITY_TOTAL])]
		
		
		apogees[index]=apogee
		children[index,:]=chromosome
		
		

			




# Start of Program


threads=[None]*generation_size


totalstabilities=np.empty((generation_size,2))

start=time.time()
with orhelper.OpenRocketInstance() as instance:
	orh = orhelper.Helper(instance)
	doc = orh.load_doc(os.path.join('examples', or_file_name))
	sim = doc.getSimulation(0)
	opts = sim.getOptions()
	rocket = opts.getRocket()
	count=0
	generationcount=0
	firststagefins=orh.get_component_named(rocket, "First Stage Fins")
	secondstagefins=orh.get_component_named(rocket, "Second Stage Fins")
	print("Initial generation...")
	
	for i in range(len(threads)):
		threads[i]=threading.Thread(target=simulate_fin_combo, args=(i,))
		
		
	
	for x in threads:
		x.start()

	for x in threads:
		x.join()
	
	while generationcount<num_generations:
			
		print("Current generation number: {}" .format(generationcount+1))
		
		
		costs=fs.calculate_cost(apogees, totalstabilities, target_height, offrod_target,
		sep_target, offrod_mul, sep_mul)
		averagecost=np.average(costs)
		print(locale.format("%d", averagecost, grouping=True))
		children=fs.crossover(children,2,costs)
		children=fs.mutate(children,prob_mutation,max_mutation)
		for i in range(len(threads)):
			threads[i]=threading.Thread(target=simulate_fin_combo, args=(i,))
		for x in threads:
			x.start()

		for x in threads:
			x.join()
		print(children)
		generationcount+=1
		

costs=fs.calculate_cost(apogees, totalstabilities, target_height, offrod_target, sep_target, offrod_mul, sep_mul)



ind=np.where(costs==np.amin(costs))
index=ind[0]

print(apogees[index])
print(children[index,:])

	


