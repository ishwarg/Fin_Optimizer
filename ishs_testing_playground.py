#final genetic algorithm

import os
from numpy.core.fromnumeric import sort
from numpy.lib import index_tricks
import orhelper
#import numpy as np
import functions as fs
from orhelper import FlightDataType 
import time
start=time.time()
#this depenedency will be flipped when the final GA file is made

generation_size=fs.generation_size

#stopping condition (for now will be a simple max number of generations)
num_generations=10

#required stabilities at different flight events
launchrod=1.5
seperation=2

generation=fs.create_generation(generation_size)
altitudes=[]

#stores indexes of rejected combos 
rejectedcombos=[]



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

        while count<len(generation):


                fins=fs.convert_string_to_array(generation[count])
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

                if outputs[1] or outputs[2]:
                        rejectedcombos.append(count)
                        rejectcount+=1
                altitudes.append(outputs[0])
                count+=1
                        
        amountrejected=rejectcount
        index_of_first_rejection=len(generation)-amountrejected

        for x in rejectedcombos:
               altitudes.append(altitudes[x])
               altitudes.pop(x)
               generation.append(generation[x])
               generation.pop(x)
        
        altitudesofaccepted=altitudes[:index_of_first_rejection]
        costs=fs.calculate_cost(altitudesofaccepted)
        costsandcombos= sort_combined_arrays(generation[:index_of_first_rejection], costs)

        costs=[]
        combos=[]
        for x in costsandcombos:
                combos.append(x[0])
        for x in costsandcombos:
                costs.append(x[1])
        children=fs.crossover(combos,0, 0.7,costs)

        
        


        while generationcount<num_generations:
                count=0
                haslength=True
                while haslength:
                        while count<len(children):
                                print(children,count)
                                fins=fs.convert_string_to_array(children[count])
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

                                if outputs[1] or outputs[2]:
                                        rejectedcombos.append(count)
                                        rejectcount+=1
                                altitudes.append(outputs[0])
                                count+=1
                                hasLengh=False
                               # if rejectcount != len(altitudes):
                                        #haslength=False
                
                amountrejected=len(rejectedcombos)
                index_of_first_rejection=len(children)-amountrejected

                for x in rejectedcombos:
                        altitudes.append(altitudes[x])
                        altitudes.pop(x)
                        children.append(children[x])
                        children.pop(x)
                
                costs=fs.calculate_cost(altitudes[:index_of_first_rejection])
                costsandcombos= sort_combined_arrays(children[:index_of_first_rejection],costs)

                count=0
                costs=[]
                combos=[]
                for x in costsandcombos:
                        combos.append(x[0])
                for x in costsandcombos:
                        costs.append(x[1])
                children=fs.crossover(combos,0, 0.7,costs)
                #need to add statement that appends children so that it becomes an array of length generation_size
                generationcount+=1

print(children[:10])   

     


