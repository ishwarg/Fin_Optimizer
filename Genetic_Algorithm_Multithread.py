# Final Genetic Algorithm

'''
Ishwarjot Grewal and Rafi Hakim
'''

# Imports
import os
import orhelper
import numpy as np
from pandas import concat
import functions as fs
from orhelper import FlightDataType 
from orhelper import FlightEvent
import threading
import time
import locale

start=time.time()

# Comments
'''
# Stopping condition (for now will be a simple max number of generations)
# Required stabilities at different flight events are inputted
# Probability of mutation per run and maximum integer +- mutation value
# can be set individually for each parameter out of 6
'''

## The following are inputs:

# Target Variables
target_height = 9296.4
launchrod=1.45 # minimum stability off rod
seperation=2.0 # minimum stability at seperation
offrod_target = 2 # ideal stability off rod
sep_target = 2 # ideal stability at seperation

# Learning Variables:
generation_size=36# Input as even integer
num_generations=16# Input as integer
prob_mutation = np.array([.5, .5, .5, .5, .8, .8])  # Input as 1 by 6 array
max_mutation = np.array([6, 6, 6, 6, 10, 10])  # Input as 1 by 6 array
offrod_mul = 1 # recommended to be set to around 
sep_mul = 1 # recommended to be set to around 
numruns=10

# Other Variables
or_file_name = 'Tantalus.ork'  # Input as string
# 3billion G and 2.25 scalarMultiplier finishes within 15 minutes
G = 1.483*10**8 # may differ in directions, use minimum value with safety factor
t = "fin thickness"
apogees=np.empty(generation_size)
maxvelocities=np.empty(generation_size)
altitudesAtMaxVelocities=np.empty(generation_size)
locale.setlocale(locale.LC_ALL, '')
totalstabilities=np.empty((generation_size,2))
willflutter=False
willdiverge=False
soundspeed=0
pressure=0



# Natural and Convenient Variables
P0 = 101325

# initialize
vis_costs1 = []
vis_costs2 = []
vis_apogees = []
vis_children0 = []
vis_children1 = []
vis_children2 = []
vis_children3 = []
vis_children4 = []
vis_children5 = []
vis_generationcount = []

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
    data=orh.get_timeseries(sim, [FlightDataType.TYPE_TIME,FlightDataType.TYPE_ALTITUDE, FlightDataType.TYPE_STABILITY,FlightDataType.TYPE_VELOCITY_TOTAL, FlightDataType.TYPE_AIR_PRESSURE,FlightDataType.TYPE_SPEED_OF_SOUND])
    events = orh.get_events(sim)
            
    ind=np.where(data[FlightDataType.TYPE_TIME]==events[FlightEvent.LAUNCHROD])
    flag1= np.size(data[FlightDataType.TYPE_STABILITY][ind])!=1
        
    
   
    
    stabilityoffrod=data[FlightDataType.TYPE_STABILITY][ind]
    ind=np.where(data[FlightDataType.TYPE_TIME]==events[FlightEvent.STAGE_SEPARATION])
    flag2= np.size(data[FlightDataType.TYPE_STABILITY][ind])!=1
    stabilityatseperation=data[FlightDataType.TYPE_STABILITY][ind]
    
    ind=np.where(data[FlightDataType.TYPE_TIME]==events[FlightEvent.APOGEE])
    flag3=np.size(data[FlightDataType.TYPE_ALTITUDE][ind])!=1
    
    apogee=data[FlightDataType.TYPE_ALTITUDE][ind]
    if (not flag1):
            totalstabilities[index,0]=stabilityoffrod
    if (not flag2):
        totalstabilities[index,1]=stabilityatseperation
    ind=np.argmax(data[FlightDataType.TYPE_VELOCITY_TOTAL])
    maxvelocities[index]=data[FlightDataType.TYPE_VELOCITY_TOTAL][ind]
    altitudesAtMaxVelocities[index]=data[FlightDataType.TYPE_ALTITUDE][ind]
    soundspeed=data[FlightDataType.TYPE_SPEED_OF_SOUND][ind]
    pressure=data[FlightDataType.TYPE_AIR_PRESSURE][ind]
    #include that checks for flutter here if possible and add a true false into outputlist
        
    willflutter=fs.get_flutter(0.3,chromosome[0]/1000,G,.003,chromosome[4]/1000,soundspeed, pressure, P0)<max(data[FlightDataType.TYPE_VELOCITY_TOTAL]) or fs.get_flutter(0.3,chromosome[1]/1000,G,0.003,chromosome[5]/1000,soundspeed, pressure, P0)<max(data[FlightDataType.TYPE_VELOCITY_TOTAL])
    willdiverge=fs.get_divergence(0.3,chromosome[0]/1000,G,.003,chromosome[4]/1000,soundspeed, pressure, P0)<max(data[FlightDataType.TYPE_VELOCITY_TOTAL]) or fs.get_divergence(0.3,chromosome[1]/1000,G,0.003,chromosome[5]/1000,soundspeed, pressure, P0)<max(data[FlightDataType.TYPE_VELOCITY_TOTAL])
    
    badshape=(chromosome[0]+chromosome[2])>300 and (chromosome[1]+chromosome[3])>300 and (chromosome[0]<8 or chromosome[1]<8)
    outputs=[apogee,stabilityoffrod<launchrod,stabilityatseperation<seperation,max(data[FlightDataType.TYPE_VELOCITY_TOTAL]),willflutter,willdiverge, badshape, flag1, flag2, flag3]
    
    if (not flag3):
        apogees[index]=apogee
    
    while outputs[1] or outputs[2] or outputs[6] or outputs[7] or outputs[8] or outputs[9]: #removed the check for flutter temporarily

        chromosome=fs.generate_chromosome()
        firststagefins.setTipChord(float(chromosome[0])/1000)
        firststagefins.setSweep(float(chromosome[2])/1000)
        firststagefins.setHeight(float(chromosome[4])/1000)
        secondstagefins.setTipChord(float(chromosome[1])/1000)
        secondstagefins.setSweep(float(chromosome[3])/1000)
        secondstagefins.setHeight(float(chromosome[5])/1000)
        
        
        orh.run_simulation(sim)
        data=orh.get_timeseries(sim, [FlightDataType.TYPE_TIME,FlightDataType.TYPE_ALTITUDE, FlightDataType.TYPE_STABILITY,FlightDataType.TYPE_VELOCITY_TOTAL,FlightDataType.TYPE_AIR_PRESSURE,FlightDataType.TYPE_SPEED_OF_SOUND])
        events = orh.get_events(sim)

        ind=np.where(data[FlightDataType.TYPE_TIME]==events[FlightEvent.LAUNCHROD])

        flag1 = (np.size(data[FlightDataType.TYPE_STABILITY][ind])!=1)
        stabilityoffrod=data[FlightDataType.TYPE_STABILITY][ind]
        ind=np.where(data[FlightDataType.TYPE_TIME]==events[FlightEvent.STAGE_SEPARATION])
        flag2=(np.size(data[FlightDataType.TYPE_STABILITY][ind])!=1)
        stabilityatseperation=data[FlightDataType.TYPE_STABILITY][ind]
        ind=np.where(data[FlightDataType.TYPE_TIME]==events[FlightEvent.APOGEE])
        flag3=np.size(data[FlightDataType.TYPE_ALTITUDE][ind])!=1
        apogee=data[FlightDataType.TYPE_ALTITUDE][ind]
        
        if (not flag1):
            totalstabilities[index,0]=stabilityoffrod
        if (not flag2):
            totalstabilities[index,1]=stabilityatseperation
        ind=np.argmax(data[FlightDataType.TYPE_VELOCITY_TOTAL])
        maxvelocities[index]=data[FlightDataType.TYPE_VELOCITY_TOTAL][ind]
        altitudesAtMaxVelocities[index]=data[FlightDataType.TYPE_ALTITUDE][ind]
        soundspeed=data[FlightDataType.TYPE_SPEED_OF_SOUND][ind]
        
        pressure=data[FlightDataType.TYPE_AIR_PRESSURE][ind]
        
        #include that checks for flutter here if possible and add a true false into outputlist
            
        willflutter=fs.get_flutter(0.3,chromosome[0]/1000,G,.003,chromosome[4]/1000,soundspeed, pressure, P0)<max(data[FlightDataType.TYPE_VELOCITY_TOTAL]) or fs.get_flutter(0.3,chromosome[1]/1000,G,0.003,chromosome[5]/1000,soundspeed, pressure, P0)<max(data[FlightDataType.TYPE_VELOCITY_TOTAL])
        willdiverge=fs.get_divergence(0.3,chromosome[0]/1000,G,.003,chromosome[4]/1000,soundspeed, pressure, P0)<max(data[FlightDataType.TYPE_VELOCITY_TOTAL]) or fs.get_divergence(0.3,chromosome[1]/1000,G,0.003,chromosome[5]/1000,soundspeed, pressure, P0)<max(data[FlightDataType.TYPE_VELOCITY_TOTAL])
        badshape=(chromosome[0]+chromosome[2])>300 and (chromosome[1]+chromosome[3])>300
        outputs=[apogee,stabilityoffrod<launchrod,stabilityatseperation<seperation,max(data[FlightDataType.TYPE_VELOCITY_TOTAL]),willflutter,willdiverge, badshape, flag1, flag2, flag3]
    
        if (not flag3):
            apogees[index]=apogee
        children[index,:]=chromosome

        
        

            




# Start of Program
threads=[None]*generation_size



start=time.time()
with orhelper.OpenRocketInstance() as instance:
    orh = orhelper.Helper(instance)
    doc = orh.load_doc(os.path.join('ork files', or_file_name))
    sim = doc.getSimulation(0)
    opts = sim.getOptions()
    rocket = opts.getRocket()
    #opts.setWindSpeedDeviation(0.42)
    
    count=0
    generationcount=0
    firststagefins=orh.get_component_named(rocket, "First Stage Fins")
    secondstagefins=orh.get_component_named(rocket, "Second Stage Fins")
    while count<numruns:
        children=fs.create_generation(generation_size)
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
            print("costs: ", costs)
            averagecost=np.average(costs)
            print(locale.format("%d", averagecost, grouping=True))
            children=fs.crossover(children,0,costs)
            children=fs.mutate(children,prob_mutation,max_mutation)
            for i in range(len(threads)):
                threads[i]=threading.Thread(target=simulate_fin_combo, args=(i,))
            for x in threads:
                x.start()

            for x in threads:
                x.join()
            print("children", children)
            
            # visualizations
            '''vis_costs1 = vis_costs1.append(np.min(costs))
            vis_costs2 = vis_costs2.append(np.max(costs))
            vis_apogees = vis_apogees.append(np.mean(apogees))
            vis_children0 = vis_children0.append(np.mean(children[:, 0]))
            vis_children1 = vis_children1.append(np.mean(children[:, 1]))
            vis_children2 = vis_children2.append(np.mean(children[:, 2]))
            vis_children3 = vis_children3.append(np.mean(children[:, 3]))
            vis_children4 = vis_children4.append(np.mean(children[:, 4]))
            vis_children5 = vis_children5.append(np.mean(children[:, 5]))
            vis_generationcount = vis_generationcount.append(generationcount)'''

            generationcount+=1
            

        costs=fs.calculate_cost(apogees, totalstabilities, target_height, offrod_target, sep_target, offrod_mul, sep_mul)
        ind=np.where(costs==np.amin(costs))
        index=ind[0]
        maxvelocity = maxvelocities[index]
        altitudeatmax = altitudesAtMaxVelocities[index]
        

        print("max apogee: ",apogees[index]*3.281)
        print("combination: ",children[index,:])
        #print("maximum velocity: ", maxvelocity)
        #print("altitude at max velocity: ", altitudeatmax)
        print("execution time: ",time.time()-start)
        print()
        with open("final combos 30500 goal.txt", "a") as myfile:
            inputstring="Combination: " + str(children[index,:]) + " Apogee: "+ str(apogees[index]*3.281) + " Max Velocity: " + str(maxvelocity) + " Altitude at Max Velocity: " + str(altitudeatmax)
            myfile.write(inputstring)
            myfile.write('\n')
            myfile.close()
        count+=1
    print("done")

    
#fs.visualization(vis_costs1, vis_costs2, vis_apogees, vis_children0, vis_children1, vis_children2, vis_children3, vis_children4, vis_children5, vis_generationcount)

