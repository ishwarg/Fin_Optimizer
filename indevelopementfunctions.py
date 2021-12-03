import os
import random
import numpy as np
from numpy.core.fromnumeric import shape
import orhelper
from orhelper import FlightDataType
import disusedfunctions as disfun


def simulatefincombo(fincombo,stability1,stability2):
    with orhelper.OpenRocketInstance() as instance:
        orh = orhelper.Helper(instance)
        doc = orh.load_doc(os.path.join('examples', 'Tantalus.ork'))
        sim = doc.getSimulation(0)
        opts = sim.getOptions()
        rocket = opts.getRocket()

        fins=disfun.convert_string_to_array(fincombo)
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
