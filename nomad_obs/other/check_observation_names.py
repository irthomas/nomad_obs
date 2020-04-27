# -*- coding: utf-8 -*-
"""
Created on Mon Apr 27 12:27:18 2020

@author: iant
"""




def checkKeys(occultationObservationDict, nadirObservationDict, observationCycles):
    """check if all keys in the observation cycles can be found in the observation dictionaries"""
    occultationObservationNames = []
    for key, value in observationCycles.items():
        if value[0] == "Occultation":
            occultationObservationNames.extend(value[1])
    uniqueOccultationObservationNames = list(set(occultationObservationNames))        
    
    nadirObservationNames = []
    for key, value in observationCycles.items():
        if value[0] == "Nadir":
            nadirObservationNames.extend(value[1])
    uniqueNadirObservationNames = list(set(nadirObservationNames))        

    for observation_name in uniqueOccultationObservationNames:
        if observation_name not in list(occultationObservationDict.keys()):
            print("Error: %s not found in occultation dictionary!" %observation_name)
    
    for observation_name in uniqueNadirObservationNames:
        if observation_name not in list(nadirObservationDict.keys()):
            print("Error: %s not found in nadir dictionary!" %observation_name)


