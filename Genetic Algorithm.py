#final genetic algorithm

import os
from numpy.core.fromnumeric import sort
from numpy.lib import index_tricks
import orhelper
import numpy as np
import functions as fs
from orhelper import FlightDataType 
import time

start=time.time()
#this depenedency will be flipped when the final GA file is made

generation_size=6

#stopping condition (for now will be a simple max number of generations)
num_generations=5

#required stabilities at different flight events
launchrod=1.5
seperation=2

generation=fs.create_generation(generation_size)
print(type(generation[0,0]))
apogees=np.empty(generation_size)






def sort_combined_arrays(array1,array2):
        count=0
        newarray=[]
        while count<len(array1):
                newarray.append((array1[count],array2[count]))
                count+=1
        newarray.sort(key= lambda array: array[1])

        return newarray


with orhelper.OpenRocketInstance() as instance:
        orh = orhelper.Helper(instance)
        doc = orh.load_doc(os.path.join('examples', 'Tantalus.ork'))
        sim = doc.getSimulation(0)
        opts = sim.getOptions()
        rocket = opts.getRocket()
        count=0
        rejectcount=0
        generationcount=0
        firststagefins=orh.get_component_named(rocket, "First Stage Fins")
        secondstagefins=orh.get_component_named(rocket, "Second Stage Fins")
        print("Initial generation...")
        
        for x in generation:


                fins=x
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

                outputs=[max(altitude),stabilityoffrod<launchrod,stabilityatseperation<seperation,max(data[FlightDataType.TYPE_VELOCITY_TOTAL])]
                apogees[count]=outputs[0]
                #ensures a valid combo is chosen 
                while outputs[1] or outputs[2]:
                        x=fs.generate_chromosome()
                        fins=x
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

                        outputs=[max(altitude),stabilityoffrod<launchrod,stabilityatseperation<seperation,max(data[FlightDataType.TYPE_VELOCITY_TOTAL])]
                        apogees[count]=outputs[0]
                
               
        costs=fs.calculate_cost(apogees)       
        

        children=fs.crossover(generation,2,costs)
        children=fs.mutate(children)

        #need to add statement that appends children so that it becomes an array of length generation_size

       
        while generationcount<num_generations:
                print("Current generation number: {}" .format(generationcount+1))
                count=0
                for x in children:


                        fins=x
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

                        outputs=[max(altitude),stabilityoffrod<launchrod,stabilityatseperation<seperation,max(data[FlightDataType.TYPE_VELOCITY_TOTAL])]
                        apogees[count]=outputs[0]
                        #ensures a valid combo is chosen 
                        while outputs[1] or outputs[2]:
                                x=fs.generate_chromosome()
                                fins=x
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

                                outputs=[max(altitude),stabilityoffrod<launchrod,stabilityatseperation<seperation,max(data[FlightDataType.TYPE_VELOCITY_TOTAL])]
                                apogees[count]=outputs[0]
                        
                        costs=fs.calculate_cost(apogees)       
                        children=fs.crossover(children,2,costs)
                        children=fs.mutate(children)
                        count+=1
                generationcount+=1

                    
                                       
                
                
              

        
        print(np.amax(apogees))
        print(children)   

     


