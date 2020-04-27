# -*- coding: utf-8 -*-
"""
Created on Thu Feb 21 14:41:19 2019

@author: iant

FIT LNO NADIR LENGTHS TO THERMAL RULE

"""

from nomad_obs.config.constants import INITIALISATION_TIME, PRECOOLING_TIME, THERMAL_RULE_ON_TIME



__project__   = "NOMAD Observation Planning"
__author__    = "Ian Thomas"
__contact__   = "ian . thomas AT aeronomie . be"










def fitNadirToThermalRule(orbit_list):
    """check for clashing start/end times and reduce LNO on time to fit within thermal rule"""
    #TODO: check for clashes between nadirs and occultations and adjust nadir start/end times accordingly
    ORBIT_PLAN_NAME = "completeOrbitPlan"

    
    for orbit in orbit_list:
        irMeasuredObsTypes = [occultationType for occultationType in orbit["allowedObservationTypes"][:] if occultationType in ["ingress", "egress", "merged", "grazing"]]
    
        if orbit[ORBIT_PLAN_NAME]["irDayside"] != "": #if LNO observing
            
            dayside = orbit["dayside"]
            
            totalObsTime = 0
            for occultationType in irMeasuredObsTypes:
                occultation = orbit[occultationType]
                totalObsTime += occultation["obsDuration"]
                
            oldNadirDuration = dayside["duration"]
            remainingObsTime = THERMAL_RULE_ON_TIME - totalObsTime - PRECOOLING_TIME - INITIALISATION_TIME
    
            if remainingObsTime < oldNadirDuration: #if allowed on time is less than long nadir duration, then nadir obs must be shortened
                dayside["oldEtStart"] = dayside["etStart"]
                dayside["oldEtEnd"] = dayside["etEnd"]
                
                dayside["etStart"] = dayside["etMidpoint"] - (remainingObsTime / 2.0)
                dayside["etEnd"] = dayside["etMidpoint"] + (remainingObsTime / 2.0)
    
            dayside["obsStart"] = dayside["etStart"] - PRECOOLING_TIME - INITIALISATION_TIME
            dayside["obsEnd"] = dayside["etEnd"]
            dayside["obsDuration"] = dayside["obsEnd"] - dayside["obsStart"]
    return orbit_list
        
