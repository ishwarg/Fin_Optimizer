# Final Genetic Algorithm

'''
Ishwarjot Grewal and Rafi Hakim
'''

# Imports
import os
from numpy.core.fromnumeric import sort
from numpy.lib import index_tricks
import orhelper
import numpy as np
import functions as fs
from orhelper import FlightDataType 
from orhelper import FlightEvent


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
generation_size=10  # Input as integer
num_generations=1  # Input as integer
prob_mutation = np.array([.7, .7, .3, .3, .5, .5])  # Input as 1 by 6 array
max_mutation = np.array([16, 16, 14, 14, 12, 12])  # Input as 1 by 6 array
offrod_mul = 10 # recommended to be set to around 
sep_mul = 10 # recommended to be set to around 

# Other Variables
or_file_name = 'Tantalus.ork'  # Input as string
G = "shear modulus" # may differ in directions, use minimum value with safety factor 
t = "fin thickness"

# Natural and Convenient Variables
P0 = "atmospheric presure @ sea level temp height"


# Start of Program

generation=fs.create_generation(generation_size)

apogees=np.empty(generation_size)
totalstabilities=np.empty((generation_size,2))

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
        
        while count<generation_size:


                firststagefins.setTipChord(float(generation[count,0])/1000)
                firststagefins.setSweep(float(generation[count,2])/1000)
                firststagefins.setHeight(float(generation[count,4])/1000)
                secondstagefins.setTipChord(float(generation[count,1])/1000)
                secondstagefins.setSweep(float(generation[count,3])/1000)
                secondstagefins.setHeight(float(generation[count,5])/1000)
                
                
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
                apogees[count]=outputs[0]
                
                totalstabilities[count,0]=stabilityoffrod
                totalstabilities[count,1]=stabilityatseperation

                # ensures a valid combo is chosen 
                while outputs[1] or outputs[2]:
                        generation[count,:]=fs.generate_chromosome()
                        
                        firststagefins.setTipChord(float(generation[count,0])/1000)
                        firststagefins.setSweep(float(generation[count,2])/1000)
                        firststagefins.setHeight(float(generation[count,4])/1000)
                        secondstagefins.setTipChord(float(generation[count,1])/1000)
                        secondstagefins.setSweep(float(generation[count,3])/1000)
                        secondstagefins.setHeight(float(generation[count,5])/1000)
                        
                        
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
                        apogees[count]=outputs[0]
                        totalstabilities[count,0]=stabilityoffrod
                        totalstabilities[count,1]=stabilityatseperation
                count+=1
        children=generation       
               
        # need to add statement that appends children so that it becomes an array of length generation_size

        while generationcount<num_generations:
                print("Current generation number: {}" .format(generationcount+1))
                count=0
                costs=fs.calculate_cost(apogees, totalstabilities, target_height, offrod_target,
                sep_target, offrod_mul, sep_mul)
                children=fs.crossover(generation,2,costs)
                children=fs.mutate(children,prob_mutation,max_mutation)
                while count<generation_size:

                        firststagefins.setTipChord(float(children[count,0])/1000)
                        firststagefins.setSweep(float(children[count,2])/1000)
                        firststagefins.setHeight(float(children[count,4])/1000)
                        secondstagefins.setTipChord(float(children[count,1])/1000)
                        secondstagefins.setSweep(float(children[count,3])/1000)
                        secondstagefins.setHeight(float(children[count,5])/1000)
                        
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
                       
                        
                        apogees[count]=outputs[0]
                        totalstabilities[count,0]=stabilityoffrod
                        totalstabilities[count,1]=stabilityatseperation

                        # ensures a valid combo is chosen 
                        while outputs[1] or outputs[2]:
                                children[count,:]=fs.generate_chromosome()
                                firststagefins.setTipChord(float(children[count,0])/1000)
                                firststagefins.setSweep(float(children[count,2])/1000)
                                firststagefins.setHeight(float(children[count,4])/1000)
                                secondstagefins.setTipChord(float(children[count,1])/1000)
                                secondstagefins.setSweep(float(children[count,3])/1000)
                                secondstagefins.setHeight(float(children[count,5])/1000)
                                
                                
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
                                apogees[count]=outputs[0]
                                totalstabilities[count,0]=stabilityoffrod
                                totalstabilities[count,1]=stabilityatseperation
                                
                        
                        count+=1
                

                
                       
                generationcount+=1

   
      
               
              

        
        ind=np.where(apogees==np.amax(apogees))
        index=ind[0]
        
        print(np.amax(apogees))
        print(children[index,:])
       
        


