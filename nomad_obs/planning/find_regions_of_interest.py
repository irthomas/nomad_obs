# -*- coding: utf-8 -*-
"""
Created on Mon Apr 27 12:20:19 2020

@author: iant
"""

import numpy as np
import random



from nomad_obs.planning.spice_functions import et2utc, getLonLatIncidenceLst, getLonLatLst, getTangentAltitude
from nomad_obs.config.constants import NADIR_SEARCH_STEP_SIZE, MAXIMUM_SEARCH_INCIDENCE_ANGLE, OCCULTATION_SEARCH_STEP_SIZE, MAXIMUM_GRAZING_ALTITUDE




def regionsOfInterestNadir(orbit_list, regions_of_interest, observationCycles, silent=True):
    """check for nadir observations near regions of interest. Add region dictionary to orbit list where matches are found"""
    #loop through each observation, making lat/lon steps and check against regions of interest
    for orbit in orbit_list:
        if "dayside" in orbit.keys():
            dayside = orbit["dayside"]
            
            etStart = dayside["etStart"]
            etEnd = dayside["etEnd"]
            ets = np.arange(etStart, etEnd, NADIR_SEARCH_STEP_SIZE)
            daysideData = np.asfarray([getLonLatIncidenceLst(et) for et in ets])
            
            lons = daysideData[:, 0]
            lats = daysideData[:, 1]
            incidence_angles = daysideData[:, 2]
            lst = daysideData[:, 3]
            
            #write all found regions of interest to orbit
            for regionOfInterest in regions_of_interest:
                matches = np.logical_and(
                        np.logical_and((regionOfInterest[4] < lats), (regionOfInterest[5] > lats)),
                        np.logical_and((regionOfInterest[6] < lons), (regionOfInterest[7] > lons))
                        )
                if np.any(matches):
                    i = int(np.mean(np.where(matches)[0])) #find centre index
                    if incidence_angles[i] < MAXIMUM_SEARCH_INCIDENCE_ANGLE: #check if solar angle too low

                        #get random observation name from cycleName:
                        cycleName = regionOfInterest[3]
                        observationName = random.choice(observationCycles[cycleName][1])

                        regionDict = {"name":regionOfInterest[0], \
                             "priority":regionOfInterest[1], \
                             "ratio":regionOfInterest[2], \
                             "cycleName":cycleName, \
                             "observationName":observationName, \
                             "et":ets[i], "utc":et2utc(ets[i]), \
                             "lon":lons[i], "lat":lats[i], \
                             "incidenceAngle":incidence_angles[i], "lst":lst[i]}
                        if "daysideRegions" not in orbit.keys():
                            orbit["daysideRegions"] = []
                        orbit["daysideRegions"].append(regionDict)
                    else:
                        if not silent: print("Match found on orbit %i but incidence angle %0.1f is above %0.0f" %(orbit["orbitNumber"], incidence_angles[i], MAXIMUM_SEARCH_INCIDENCE_ANGLE))
    return orbit_list




def regionsOfInterestOccultation(orbit_list, regions_of_interest, observationCycles, silent=True):
    """check for occultation observations near regions of interest"""
    #loop through each observation, making lat/lon steps and check against regions of interest
    for orbit in orbit_list:
#        print(orbit["orbitNumber"])
        for occultation_type in orbit["allowedObservationTypes"]:
#            print(occultation_type)
            
            if occultation_type in ["ingress", "egress", "merged", "grazing"]:
                occultation = orbit[occultation_type]
                
                etStart = occultation["etStart"]
                etEnd = occultation["etEnd"]
                ets = np.arange(etStart, etEnd, OCCULTATION_SEARCH_STEP_SIZE)
                occultationData = np.asfarray([getLonLatLst(et) for et in ets])
                alts = np.asfarray([getTangentAltitude(et) for et in ets])
                
                
                lons = occultationData[:, 0]
                lats = occultationData[:, 1]
                lst = occultationData[:, 2]
                
                warning_1_given = False
                warning_2_given = False
                for regionOfInterest in regions_of_interest:
                    matches = np.logical_and(
                            np.logical_and((regionOfInterest[4] < lats), (regionOfInterest[5] > lats)),
                            np.logical_and((regionOfInterest[6] < lons), (regionOfInterest[7] > lons))
                            )
                    if np.any(matches): #if match found
                        #for merged occultation, check altitude to determine if real or viewing planet
                        if np.all(alts[matches] == 0.0):
                            if not silent and not warning_1_given:
                                if not silent: 
                                    print("Match found on orbit %i but all tangent altitudes are negative" %orbit["orbitNumber"])
                                    warning_1_given = True
        
                        #for grazing, check if altitude is good or not. Don't add if too high
                        elif np.all(alts[matches] > MAXIMUM_GRAZING_ALTITUDE):
                            if not silent and not warning_2_given:
                                print("Match found on orbit %i but all tangent altitudes are above %ikm" %(orbit["orbitNumber"], MAXIMUM_GRAZING_ALTITUDE))
                                warning_2_given = True
         
                        else:
                            min_altitude = np.nanmin(alts[matches]) #find minimum valid altitude
#                            print(min_altitude)
                            i = int(np.where(alts[matches] == min_altitude)[0][0]) #find index corresponding to minimum altitude
                            #i = int(np.mean(np.where(matches)[0])) #find centre index
                            
                            #get random observation name from cycleName:
                            cycleName = regionOfInterest[3]
                            observationName = random.choice(observationCycles[cycleName][1])
                            
                            #get data for minimum altitude point
                            regionDict = {"occultationType":occultation_type,
                                     "name":regionOfInterest[0], \
                                     "priority":regionOfInterest[1], \
                                     "ratio":regionOfInterest[2], \
                                     "cycleName":cycleName, \
                                     "observationName":observationName, \
                                     "et":ets[i], "utc":et2utc(ets[i]), \
                                     "lon":lons[i], "lat":lats[i], \
                                     "lst":lst[i]}
                            if "occultationRegions" not in orbit.keys():
                                orbit["occultationRegions"] = []
                            orbit["occultationRegions"].append(regionDict)
    return orbit_list



    

def findMatchingRegions(orbit_list, silent=True):
    """add flag to file where obsevations match a region of interest"""
    for orbit in orbit_list:
        if "daysideRegions" in orbit.keys():
            priority = 999 #start with large number = lowest priority
            for region in orbit["daysideRegions"]:
                    
                if not silent: 
                    print("Match found: %s, orbit %i, incidence angle %0.1f at %s" %(region["name"], orbit["orbitNumber"], region["incidenceAngle"], region["utc"]))
    
                if region["priority"] < priority: #if region has higher priority, write to orbit list
                    priority = region["priority"] #save new priority for checking against next region
                    orbit["dayside"]["observationName"] = region["observationName"]
                    if not silent: 
                        print("%s observation added" %orbit["dayside"]["observationName"])
                else:
                    print("Matching region of interest found (%s), but superseded by higher priority region (%s)" %(region["name"], orbit["dayside"]["observationName"]))

    
        if "occultationRegions" in orbit.keys():
            priority = 999 #start with large number = lowest priority
            for region in orbit["occultationRegions"]:
                matchingOccultationType = region["occultationType"]

                if not silent: 
                    print("Match found: %s, orbit %i, %s occultation at %s" %(region["name"], orbit["orbitNumber"], matchingOccultationType, region["utc"]))
    
                if region["priority"] < priority: #if region has higher priority, write to orbit list
                    priority = region["priority"] #save new priority for checking against next region
                    orbit[matchingOccultationType]["observationName"] = region["observationName"]
                    if not silent: 
                        print("%s observation added" %orbit["dayside"]["observationName"])
                else:
                    print("Matching region of interest found (%s), but superseded by higher priority region (%s)" %(region["name"], orbit[matchingOccultationType]["observationName"]))

    return orbit_list


