# -*- coding: utf-8 -*-
"""
Created on Mon Apr 27 12:15:46 2020

@author: iant
"""
import os
import numpy as np
import spiceypy as sp

from nomad_obs.event_file.event_file_codes import \
NOMAD_INGRESS_START_CODES, NOMAD_INGRESS_END_CODES, \
NOMAD_EGRESS_START_CODES, NOMAD_EGRESS_END_CODES, \
NOMAD_MERGED_START_CODES, NOMAD_MERGED_END_CODES, \
NOMAD_GRAZING_START_CODES, NOMAD_GRAZING_END_CODES, \
NOMAD_LIMB_START_CODES, NOMAD_LIMB_END_CODES, \
NOMAD_NIGHT_LIMB_START_CODES, NOMAD_NIGHT_LIMB_END_CODES, \
ACS_INGRESS_START_CODES, ACS_INGRESS_END_CODES, \
ACS_EGRESS_START_CODES, ACS_EGRESS_END_CODES, \
ACS_MERGED_START_CODES, ACS_MERGED_END_CODES, \
ACS_GRAZING_START_CODES, ACS_GRAZING_END_CODES, \
NOMAD_SOLAR_CALIBRATION_START_CODES, NOMAD_SOLAR_CALIBRATION_END_CODES, \
ACS_SOLAR_CALIBRATION_START_CODES, ACS_SOLAR_CALIBRATION_END_CODES
from nomad_obs.config.constants import ACCEPTABLE_MTP_OCCULTATION_TIME_ERROR





def readMappsEventFile(instrument, mappsObservationType, mtpConstants, paths):
    """read in the LTP  planning file from the SOC and find NOMAD or ACS events (occultations) or terminator crossings (nadir)"""

    mappsEventFilename = mtpConstants["mappsEventFilename"]
    mappsEventFilepath = os.path.join(paths["EVENT_FILE_PATH"], mappsEventFilename)
#    lines = [line.rstrip('\n').split()[0:3] for line in open(mappsEventFilepath) if line[0] != "#"]
    lines = [line.rstrip('\n').split()[0:3] for line in open(mappsEventFilepath)]

    if mappsObservationType == "occultation":
        mappsEvent = []

        ingressStartFound = False
        ingressEndFound = False
        egressStartFound = False
        egressEndFound = False
        mergedStartFound = False
        mergedEndFound = False
        grazingStartFound = False
        grazingEndFound = False
        eventIndex = 0

        if instrument == "NOMAD":
            EVENT_CODES = NOMAD_INGRESS_START_CODES + NOMAD_INGRESS_END_CODES + NOMAD_EGRESS_START_CODES + NOMAD_EGRESS_END_CODES + \
                          NOMAD_MERGED_START_CODES + NOMAD_MERGED_END_CODES + NOMAD_GRAZING_START_CODES + NOMAD_GRAZING_END_CODES
        elif instrument == "ACS":
            EVENT_CODES = ACS_INGRESS_START_CODES + ACS_INGRESS_END_CODES + ACS_EGRESS_START_CODES + ACS_EGRESS_END_CODES + \
                          ACS_MERGED_START_CODES + ACS_MERGED_END_CODES + ACS_GRAZING_START_CODES + ACS_GRAZING_END_CODES

        for eventTime, eventName, eventCount in lines:
            if eventName in EVENT_CODES:
                eventTime = eventTime[0:-1] #remove Z
                eventCount = eventName + "-%i" %int(eventCount.split("COUNT=")[1].strip(r")"))
        
                if eventName in NOMAD_INGRESS_START_CODES + ACS_INGRESS_START_CODES:
                    mappsIngressStart = sp.str2et(eventTime)
                    ingressStartFound = True
                elif eventName in NOMAD_INGRESS_END_CODES + ACS_INGRESS_END_CODES:
                    mappsIngressEnd = sp.str2et(eventTime)
                    ingressEndFound = True
                if ingressStartFound and ingressEndFound:
                    mappsEvent.append([eventIndex, "Ingress", mappsIngressStart, mappsIngressEnd, eventCount])
                    eventIndex += 1
                    ingressStartFound = False
                    ingressEndFound = False
                    
                if eventName in NOMAD_EGRESS_START_CODES + ACS_EGRESS_START_CODES:
                    mappsEgressStart = sp.str2et(eventTime)
                    egressStartFound = True
                elif eventName in NOMAD_EGRESS_END_CODES + ACS_EGRESS_END_CODES:
                    mappsEgressEnd = sp.str2et(eventTime)
                    egressEndFound = True
                if egressStartFound and egressEndFound:
                    mappsEvent.append([eventIndex, "Egress", mappsEgressStart, mappsEgressEnd, eventCount])
                    eventIndex += 1
                    egressStartFound = False
                    egressEndFound = False
        
                if eventName in NOMAD_MERGED_START_CODES + ACS_MERGED_START_CODES:
                    mappsMergedStart = sp.str2et(eventTime)
                    mergedStartFound = True
                elif eventName in NOMAD_MERGED_END_CODES + ACS_MERGED_END_CODES:
                    mappsMergedEnd = sp.str2et(eventTime)
                    mergedEndFound = True
                if mergedStartFound and mergedEndFound:
                    mappsEvent.append([eventIndex, "Merged", mappsMergedStart, mappsMergedEnd, eventCount])
                    eventIndex += 1
                    mergedStartFound = False
                    mergedEndFound = False
        
                if eventName in NOMAD_GRAZING_START_CODES + ACS_GRAZING_START_CODES:
                    mappsGrazingStart = sp.str2et(eventTime)
                    grazingStartFound = True
                elif eventName in NOMAD_GRAZING_END_CODES + ACS_GRAZING_END_CODES:
                    mappsGrazingEnd = sp.str2et(eventTime)
                    grazingEndFound = True
                if grazingStartFound and grazingEndFound:
                    mappsEvent.append([eventIndex, "Grazing", mappsGrazingStart, mappsGrazingEnd, eventCount])
                    eventIndex += 1
                    grazingStartFound = False
                    grazingEndFound = False
    

#    elif mappsObservationType == "nadir":
#        mappsEvent = []
#        
#        daysideStartFound = False
#        daysideEndFound = False
#        eventIndex = 0
#        
#        EVENT_CODES = TERMINATOR_N2D_CODES + TERMINATOR_D2N_CODES
#        
#        for eventTime, eventName, eventCount in lines:
#            if eventName in EVENT_CODES:
#                eventTime = eventTime[0:-1]
#                eventCount = eventName + "-%i" %int(eventCount.split("COUNT=")[1].strip(r")"))
#        
#                if eventName in TERMINATOR_N2D_CODES:
#                    mappsDaysideStart = sp.str2et(eventTime)
#                    daysideStartFound = True
#                elif eventName in TERMINATOR_D2N_CODES:
#                    mappsDaysideEnd = sp.str2et(eventTime)
#                    daysideEndFound = True
#                if daysideStartFound and daysideEndFound:
#                    mappsEvent.append([eventIndex, "Dayside", mappsDaysideStart, mappsDaysideEnd, eventCount])
#                    eventIndex += 1
#                    daysideStartFound = False
#                    daysideEndFound = False

    elif mappsObservationType == "limb":
        mappsEvent = []
        
        limbStartFound = False
        limbEndFound = False
        eventIndex = 0
        
        EVENT_CODES = NOMAD_LIMB_START_CODES + NOMAD_LIMB_END_CODES
        
        for eventTime, eventName, eventCount in lines:
            if eventName in EVENT_CODES:
                eventTime = eventTime[0:-1] #remove Z
                if eventName in NOMAD_LIMB_START_CODES:
                    mappsLimbStart = sp.str2et(eventTime)
                    limbStartFound = True
                elif eventName in NOMAD_LIMB_END_CODES:
                    mappsLimbEnd = sp.str2et(eventTime)
                    limbEndFound = True
                if limbStartFound and limbEndFound:
                    mappsEvent.append([eventIndex, "Limb", mappsLimbStart, mappsLimbEnd, eventCount])
                    eventIndex += 1
                    limbStartFound = False
                    limbEndFound = False

    elif mappsObservationType == "nightlimb":
        mappsEvent = []
        
        nightLimbStartFound = False
        nightLimbEndFound = False
        eventIndex = 0
        
        EVENT_CODES = NOMAD_NIGHT_LIMB_START_CODES + NOMAD_NIGHT_LIMB_END_CODES
        
        for eventTime, eventName, eventCount in lines:
            if eventName in EVENT_CODES:
                eventTime = eventTime[0:-1] #remove Z
                if eventName in NOMAD_NIGHT_LIMB_START_CODES:
                    mappsNightLimbStart = sp.str2et(eventTime)
                    nightLimbStartFound = True
                elif eventName in NOMAD_NIGHT_LIMB_END_CODES:
                    mappsNightLimbEnd = sp.str2et(eventTime)
                    nightLimbEndFound = True
                if nightLimbStartFound and nightLimbEndFound:
                    mappsEvent.append([eventIndex, "NightLimb", mappsNightLimbStart, mappsNightLimbEnd, eventCount])
                    eventIndex += 1
                    nightLimbStartFound = False
                    nightLimbEndFound = False

    elif mappsObservationType == "solarCalibration":
        mappsEvent = []
                
        solarCalibrationStartFound = False
        solarCalibrationEndFound = False
        eventIndex = 0

        if instrument == "NOMAD":
            EVENT_CODES = NOMAD_SOLAR_CALIBRATION_START_CODES + NOMAD_SOLAR_CALIBRATION_END_CODES
        elif instrument == "ACS":
            EVENT_CODES = ACS_SOLAR_CALIBRATION_START_CODES + ACS_SOLAR_CALIBRATION_END_CODES
        
        
        for eventTime, eventName, eventCount in lines:
            if eventName in EVENT_CODES:
                eventTime = eventTime[0:-1] #remove Z
                if eventName in NOMAD_SOLAR_CALIBRATION_START_CODES:
                    mappsSolarCalibrationStart = sp.str2et(eventTime)
                    solarCalibrationStartFound = True
                elif eventName in NOMAD_SOLAR_CALIBRATION_END_CODES:
                    mappsSolarCalibrationEnd = sp.str2et(eventTime)
                    solarCalibrationEndFound = True
                if solarCalibrationStartFound and solarCalibrationEndFound:
                    mappsEvent.append([eventIndex, "SolarCalibration", mappsSolarCalibrationStart, mappsSolarCalibrationEnd, eventCount])
                    eventIndex += 1
                    solarCalibrationStartFound = False
                    solarCalibrationEndFound = False

    return mappsEvent



    






def addMappsEvents(orbit_list, mtpConstants, paths):
    """compare timings in event file to calculated orbits"""
    mappsNomadOccEvents = readMappsEventFile("NOMAD", "occultation", mtpConstants, paths)
    mappsNomadOccEventStartTimes = [eventTime for _, eventName, eventTime, _, _ in mappsNomadOccEvents if eventName in ["Ingress", "Egress", "Merged", "Grazing"]]
    mappsNomadOccEventStartNames = [eventName for _, eventName, _, _, _ in mappsNomadOccEvents if eventName in ["Ingress", "Egress", "Merged", "Grazing"]]
    mappsNomadOccEventStartCounts = [eventCount for _, eventName, _, _, eventCount in mappsNomadOccEvents if eventName in ["Ingress", "Egress", "Merged", "Grazing"]]
    
    mappsAcsOccEvents = readMappsEventFile("ACS", "occultation", mtpConstants, paths)
    mappsAcsOccEventStartTimes = [eventTime for _, eventName, eventTime, _, _ in mappsAcsOccEvents if eventName in ["Ingress", "Egress", "Merged", "Grazing"]]
#    mappsAcsOccEventStartNames = [eventName for _, eventName, _, _, _ in mappsAcsOccEvents if eventName in ["Ingress", "Egress", "Merged", "Grazing"]]
#    mappsAcsOccEventStartCounts = [eventCount for _, eventName, _, _, eventCount in mappsAcsOccEvents if eventName in ["Ingress", "Egress", "Merged", "Grazing"]]
    
#    mappsDaysideEvents = readMappsEventFile("", "nadir")
#    mappsDaysideEventsStartTimes = [eventTime for _, eventName, eventTime, _, _ in mappsDaysideEvents if eventName in ["Dayside"]]
#    mappsDaysideEventStartNames = [eventName for _, eventName, _, _, _ in mappsDaysideEvents if eventName in ["Dayside"]]
#    mappsDaysideEventStartCounts = [eventCount for _, eventName, _, _, eventCount in mappsDaysideEvents if eventName in ["Dayside"]]
    

    mappsLimbEvents = readMappsEventFile("", "limb", mtpConstants, paths)
    mappsLimbEventStartTimes = [eventTime for _, eventName, eventTime, _, _ in mappsLimbEvents if eventName in ["Limb"]]

    mappsNightLimbEvents = readMappsEventFile("", "nightlimb", mtpConstants, paths)
    mappsNightLimbEventStartTimes = [eventTime for _, eventName, eventTime, _, _ in mappsNightLimbEvents if eventName in ["NightLimb"]]

    mappsNomadSolarCalibrationEvents = readMappsEventFile("NOMAD", "solarCalibration", mtpConstants, paths)
    mappsNomadSolarCalibrationEventStartTimes = [eventTime for _, eventName, eventTime, _, _ in mappsNomadSolarCalibrationEvents if eventName in ["SolarCalibration"]]

    mappsAcsSolarCalibrationEvents = readMappsEventFile("ACS", "solarCalibration", mtpConstants, paths)
    mappsAcsSolarCalibrationEventStartTimes = [eventTime for _, eventName, eventTime, _, _ in mappsAcsSolarCalibrationEvents if eventName in ["SolarCalibration"]]

    for orbit in orbit_list:
#        orbit["obsTypes"] = []
        orbit["allowedObservationTypes"] = []
        
        for obstype in ["ingress","egress","merged","grazing"]:
            if obstype in orbit.keys():
                mappsNomadEventIndex = np.abs(np.asfarray(mappsNomadOccEventStartTimes) - orbit[obstype]["etStart"]).argmin()
                mappsAcsEventIndex = np.abs(np.asfarray(mappsAcsOccEventStartTimes) - orbit[obstype]["etStart"]).argmin()
        
                if np.abs(mappsNomadOccEventStartTimes[mappsNomadEventIndex] - orbit[obstype]["etStart"]) < ACCEPTABLE_MTP_OCCULTATION_TIME_ERROR:
                    orbit["allowedObservationTypes"].append(obstype)
                    orbit[obstype]["rowColour"] = "98fab4"
                    orbit[obstype]["primeInstrument"] = "NOMAD"
    
                    orbit[obstype]["occultationEventFileCounts"] = mappsNomadOccEventStartCounts[mappsNomadEventIndex]
                    orbit[obstype]["mappsStartTime"] = mappsNomadOccEventStartTimes[mappsNomadEventIndex]
                    orbit[obstype]["mappsStartName"] = mappsNomadOccEventStartNames[mappsNomadEventIndex]
                    orbit[obstype]["mappsStartTimeDelta"] = mappsNomadOccEventStartTimes[mappsNomadEventIndex] - orbit[obstype]["etStart"]
    
    
                elif np.abs(mappsAcsOccEventStartTimes[mappsAcsEventIndex] - orbit[obstype]["etStart"]) < ACCEPTABLE_MTP_OCCULTATION_TIME_ERROR:
                    orbit[obstype]["rowColour"] = "97c9f9"
                    orbit[obstype]["primeInstrument"] = "ACS"

                #ACS changed their starting altitude - check new altitude for ingress or merged
                elif obstype in ["ingress", "merged"]:
                        if np.abs(mappsAcsOccEventStartTimes[mappsAcsEventIndex] - orbit[obstype]["etStartAcs"]) < ACCEPTABLE_MTP_OCCULTATION_TIME_ERROR:
                            orbit[obstype]["rowColour"] = "97c9f9"
                            orbit[obstype]["primeInstrument"] = "ACS"
                        else: #occultation not used
                            orbit[obstype]["rowColour"] = "f99797"
                            orbit[obstype]["primeInstrument"] = "N/A"
                else: #occultation not used
                    orbit[obstype]["rowColour"] = "f99797"
                    orbit[obstype]["primeInstrument"] = "N/A"
                
        #check if limb measurement lies within the dayside nadir of this orbit
        for limbStartTime in mappsLimbEventStartTimes:
            if orbit["dayside"]["etStart"] < limbStartTime < orbit["dayside"]["etEnd"]:
                orbit["allowedObservationTypes"].append("trueLimb")

        #check if night limb measurement lies within the nightside nadir of this orbit
        for nightLimbStartTime in mappsNightLimbEventStartTimes:
            if orbit["nightside"]["etStart"] < nightLimbStartTime < orbit["nightside"]["etEnd"]:
                print("Night limb timing found")
                orbit["allowedObservationTypes"].append("trueNightLimb")

        #check if solar calibration lies within this orbit
        for nomadSolarCalibrationStartTime in mappsNomadSolarCalibrationEventStartTimes:
            if orbit["nightside"]["etStart"] < nomadSolarCalibrationStartTime < orbit["dayside"]["etEnd"]:
                print("NOMAD solar calibration timing found")
                orbit["allowedObservationTypes"].append("nomadSolarCalibration")
        for acsSolarCalibrationStartTime in mappsAcsSolarCalibrationEventStartTimes:
            if orbit["nightside"]["etStart"] < acsSolarCalibrationStartTime < orbit["dayside"]["etEnd"]:
                print("ACS solar calibration timing found")
                orbit["allowedObservationTypes"].append("acsSolarCalibration")

            
    return orbit_list

