# Final Genetic Algorithm

# Imports
import os
from numpy.core.fromnumeric import sort
from numpy.lib import index_tricks
import orhelper
import numpy as np
import functions as fs
from orhelper import FlightDataType 
from orhelper import FlightEvent

# Depenedency will be flipped when the final GA file is made
generation_size=10

# Stopping condition (for now will be a simple max number of generations)
num_generations=1

# required stabilities at different flight events
launchrod=1.55
seperation=2.0

# Probability of mutation per run and maximum integer +- mutation value
# can be set individually for each parameter out of 6
prob_mutation = np.array([.25, 1, .3, .6, .9, 0])
max_mutation = np.array([10, 5, 7, 10, 15, 3])




# Start of Program

generation=fs.create_generation(generation_size)

apogees=np.empty(generation_size)
totalstabilities=np.empty((generation_size,2))

with orhelper.OpenRocketInstance() as instance:
        orh = orhelper.Helper(instance)
        doc = orh.load_doc(os.path.join('examples', 'Tantalus.ork'))
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
                costs=fs.calculate_cost(apogees)       
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
       
        


