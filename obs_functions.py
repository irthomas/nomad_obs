# -*- coding: utf-8 -*-
"""
Created on Thu Feb 21 14:41:19 2019

@author: iant

OBS PLANNING USING SPICE WINDOWS
"""


import numpy as np
import os
import sys

#import numpy as np
#import os
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import xlsxwriter
import xlrd
import spiceypy as sp

from obs_config import BASE_DIRECTORY, COP_TABLE_DIRECTORY, OBS_DIRECTORY
#from run_planning import mtpNumber
from obs_inputs import SOC_JOINT_OBSERVATION_NAMES, SOC_JOINT_OBSERVATION_TYPES, getMtpConstants
from obs_inputs import nadirObservationDict, nadirRegionsOfInterest, occultationObservationDict, occultationRegionsOfInterest, nadirRegionsObservations, occultationRegionsObservations
from obs_inputs import OCCULTATION_KEYS, OCCULTATION_MERGED_KEYS, OCCULTATION_GRAZING_KEYS, USE_TWO_SCIENCES
from obs_inputs import NADIR_KEYS, NADIR_LIMB_KEYS, NADIR_NIGHTSIDE_KEYS


__project__   = "NOMAD Observation Planning"
__author__    = "Ian Thomas"
__contact__   = "ian.thomas@aeronomie.be"



#for orbit in orbitList:
#    irDescription = orbit["finalOrbitPlan"]["irDaysideCopRows"]["copRowDescription"]
#    uvisDescription = orbit["finalOrbitPlan"]["uvisDaysideCopRows"]["copRowDescription"]
##    if "ingress" in orbit.keys():
##        print(orbit["ingress"]["duration"])
#
#
#stop()





#spice constants
SPICE_ABCORR = "None"
SPICE_TARGET = "MARS"
SPICE_METHOD = "Intercept: ellipsoid"
SPICE_FORMATSTR = "C"
SPICE_PRECISION = 0
SPICE_SHAPE = "Ellipsoid"
SPICE_OBSERVER = "-143"
SPICE_REF = "IAU_MARS"
SPICE_MARS_AXES = sp.bodvrd("MARS", "RADII", 3)[1] #get mars axis values
SPICE_DATETIME_FORMAT = "%Y %b %d %H:%M:%S"


#output file channel codes
SO_CHANNEL_CODE = 0
LNO_CHANNEL_CODE = 1

#tc20 parameters
PRECOOLING_COP_ROW = 1
OFF_COP_ROW = -1

#universal constants
INITIALISATION_TIME = 10 #s
MINIMUM_TELECOMMAND_INTERVAL = 5 #s
PRECOOLING_TIME = 600 #s
THERMAL_RULE_ON_TIME = 80 * 60 #s

#detector constants
LNO_CENTRE_DETECTOR_LINE = 152

#occultation constants
OCCULTATION_SEARCH_STEP_SIZE = 2.0 #s
MAXIMUM_SO_ALTITUDE = 250.0 #km
SO_TRANSITION_ALTITUDE = 50.0 #km
MAXIMUM_GRAZING_ALTITUDE = 100.0 #km also for searching for region of interest matches
MINIMUM_TIME_BETWEEN_OCCULTATIONS = 675 #s define as merged occ if less than this
SO_REFERENCE_DURATION = 30 #s
ACCEPTABLE_MTP_OCCULTATION_TIME_ERROR = 20.0 #s

#nadir constants
NADIR_SEARCH_STEP_SIZE = 30.0 #s
MAXIMUM_SOLAR_INCIDENCE_ANGLE_ROUGH = 92.0 #deg
TIME_TO_START_DAYSIDE_BEFORE_TERMINATOR = 120 #s
TIME_TO_END_DAYSIDE_AFTER_TERMINATOR = 120 #s
ACCEPTABLE_MTP_NADIR_TIME_ERROR = 20.0 #s

MAXIMUM_SEARCH_INCIDENCE_ANGLE = 60.0 #max solar incidence angle when searching for nadir regions of interest. Higher value = lower quality data but more matches.



#orbit types. Remember to add type numbers to functions if more are created!
UVIS_MULTIPLE_TC_NADIR_ORBIT_TYPES = [2, 4, 6]
LIMB_ORBIT_TYPES = [8, 28]
UVIS_DEFAULT_ORBIT_TYPE = 14 #14 = UVIS 1xTC per dayside. 4 = 3xTCs per dayside


#plot constants
FIG_X = 10
FIG_Y = 6



"""see https://issues.cosmos.esa.int/exomarswiki/display/OE/Event+Names
These must be manually inserted into the SOC event file"""
NOMAD_INGRESS_START_CODES = ["NOMAD_OCCIN_START", "NOMAD_OCCIN_ST_START", "NOMAD_UVIS_OCCIN_START", "NOMAD_UV_OCCIN_ST_START"]
NOMAD_INGRESS_END_CODES = ["NOMAD_OCCIN_END", "NOMAD_OCCIN_ST_END", "NOMAD_UVIS_OCCIN_END", "NOMAD_UV_OCCIN_ST_END"]
NOMAD_EGRESS_START_CODES = ["NOMAD_OCCEG_START", "NOMAD_OCCEG_ST_START", "NOMAD_UVIS_OCCEG_START", "NOMAD_UV_OCCEG_ST_START"]
NOMAD_EGRESS_END_CODES = ["NOMAD_OCCEG_END", "NOMAD_OCCEG_ST_END", "NOMAD_UVIS_OCCEG_END", "NOMAD_UV_OCCEG_ST_END"]
NOMAD_MERGED_START_CODES = ["NOMAD_OCCME_START"]
NOMAD_MERGED_END_CODES = ["NOMAD_OCCME_END"]
NOMAD_GRAZING_START_CODES = ["NOMAD_OCCGR_START"]
NOMAD_GRAZING_END_CODES = ["NOMAD_OCCGR_END"]
NOMAD_LIMB_START_CODES = ["NOMAD_LIMB_START"]
NOMAD_LIMB_END_CODES = ["NOMAD_LIMB_END"]

"""Old list - new list for MTP008 onwards is below"""
#ACS_INGRESS_START_CODES = ["ACS_MIR_OCCIN_START", "ACS_NIR_OCCIN_RA_START", "ACS_TIRSUN_OCCIN_START"]
#ACS_INGRESS_END_CODES = ["ACS_MIR_OCCIN_END", "ACS_NIR_OCCIN_RA_END", "ACS_TIRSUN_OCCIN_END"]
#ACS_EGRESS_START_CODES = ["ACS_MIR_OCCEG_START", "ACS_NIR_OCCEG_RA_START", "ACS_TIRSUN_OCCEG_START"]
#ACS_EGRESS_END_CODES = ["ACS_MIR_OCCEG_END", "ACS_NIR_OCCEG_RA_END", "ACS_TIRSUN_OCCEG_END"]
#ACS_MERGED_START_CODES = ["ACS_MIR_OCCME_START", "ACS_NIR_OCCME_RA_START", "ACS_TIRSUN_OCCME_START"]
#ACS_MERGED_END_CODES = ["ACS_MIR_OCCME_END", "ACS_NIR_OCCME_RA_END", "ACS_TIRSUN_OCCME_END"]
#ACS_GRAZING_START_CODES = ["ACS_MIR_OCCGR_START", "ACS_NIR_OCCGR_RA_START", "ACS_TIRSUN_OCCGR_START"]
#ACS_GRAZING_END_CODES = ["ACS_MIR_OCCGR_END", "ACS_NIR_OCCGR_RA_END", "ACS_TIRSUN_OCCGR_END"]

ACS_INGRESS_START_CODES = ["ACS_MIR_OCCIN_ST_START", "ACS_MIR_OCCIN_START", "ACS_TIRSUN_OCCIN_START", "ACS_TIRSCA_OCCIN_START"]
ACS_INGRESS_END_CODES = ["ACS_MIR_OCCIN_ST_END", "ACS_MIR_OCCIN_END", "ACS_TIRSUN_OCCIN_END", "ACS_TIRSCA_OCCIN_END"]
ACS_EGRESS_START_CODES = ["ACS_MIR_OCCEG_ST_START", "ACS_MIR_OCCEG_START", "ACS_TIRSUN_OCCEG_START", "ACS_TIRSCA_OCCEG_START"]
ACS_EGRESS_END_CODES = ["ACS_MIR_OCCEG_ST_END", "ACS_MIR_OCCEG_END", "ACS_TIRSUN_OCCEG_END", "ACS_TIRSCA_OCCEG_END"]
ACS_MERGED_START_CODES = ["ACS_MIR_OCCME_START", "ACS_NIR_OCCME_START", "ACS_TIRSUN_OCCME_START", "ACS_TIRSCA_OCCME_START"]
ACS_MERGED_END_CODES = ["ACS_MIR_OCCME_END", "ACS_NIR_OCCME_END", "ACS_TIRSUN_OCCME_END", "ACS_TIRSCA_OCCME_END"]
ACS_GRAZING_START_CODES = ["ACS_MIR_OCCGR_START", "ACS_TIRSUN_OCCGR_START", "ACS_TIRSCA_OCCGR_START"]
ACS_GRAZING_END_CODES = ["ACS_MIR_OCCGR_END", "ACS_TIRSUN_OCCGR_END", "ACS_TIRSCA_OCCGR_END"]

TERMINATOR_D2N_CODES = ["EXMGEO_TD2N"]
TERMINATOR_N2D_CODES = ["EXMGEO_TN2D"]



def stop():
    import sys
    print("**********Fatal Error********")
#    halt
    sys.exit() #breaks program
    return 0




def et2utc(et):
    """function to convert et to utc if float is not -"""
    if et == "-":
        return "-"
    else:
        return sp.et2utc(et, SPICE_FORMATSTR, SPICE_PRECISION)




def getLonLatIncidenceLst(et):
    """get nadir data for a given time"""
    coords = sp.subpnt(SPICE_METHOD, SPICE_TARGET, et, SPICE_REF, SPICE_ABCORR, SPICE_OBSERVER)[0]
    lon, lat = sp.reclat(coords)[1:3] * np.asfarray([sp.dpr(),sp.dpr()])
    lst = sp.et2lst(et, 499, (lon / sp.dpr()), "PLANETOCENTRIC")[3]
    incidence = sp.ilumin(SPICE_SHAPE, SPICE_TARGET, et, SPICE_REF, SPICE_ABCORR, SPICE_OBSERVER, coords)[3] * sp.dpr()
    lst_hours = np.float(lst[0:2]) + np.float(lst[3:5])/60.0 + np.float(lst[6:8])/3600.0
    return lon, lat, incidence, lst_hours





def getNadirData(orbit_list, mtpConstants):
    """get all nadir data, add to orbit list"""
    utc_string_start = mtpConstants["utcStringStart"]
    utc_string_end = mtpConstants["utcStringEnd"]

    adjust = 0
    nintvals = 500
    stepSize = 1.0
    
    daysideConfinementWindow = sp.stypes.SPICEDOUBLE_CELL(2)
    sp.wninsd(sp.utc2et(utc_string_start), sp.utc2et(utc_string_end), daysideConfinementWindow)
    daysideResultWindow = sp.stypes.SPICEDOUBLE_CELL(1000)
    sp.gfpa(SPICE_TARGET, "SUN", SPICE_ABCORR, SPICE_OBSERVER, "<", (np.pi / 2), adjust, stepSize, nintvals,  daysideConfinementWindow, daysideResultWindow)

    nightsideConfinementWindow = sp.stypes.SPICEDOUBLE_CELL(2)
    sp.wninsd(sp.utc2et(utc_string_start) - 30.0 * 60.0, sp.utc2et(utc_string_end) - 30.0 * 60.0, nightsideConfinementWindow)
    nightsideResultWindow = sp.stypes.SPICEDOUBLE_CELL(1000)
    sp.gfpa(SPICE_TARGET, "SUN", SPICE_ABCORR, SPICE_OBSERVER, ">", (np.pi / 2), adjust, stepSize, nintvals,  nightsideConfinementWindow, nightsideResultWindow)
    
    count = sp.wncard(daysideResultWindow)
    
    for index in range(count):
        orbit_start, _ = sp.wnfetd(nightsideResultWindow, index)
        start, end = sp.wnfetd(daysideResultWindow, index)
        midpoint = np.mean((start, end))
        duration = end - start
        
        orbit_start_str = et2utc(orbit_start)
        start_str = et2utc(start)
        end_str = et2utc(end)
        midpoint_str = et2utc(midpoint)

        orbit_end = end
        orbit_end_str = end_str

        start_lon, start_lat, start_incidence, start_lst = getLonLatIncidenceLst(start)
        end_lon, end_lat, end_incidence, end_lst = getLonLatIncidenceLst(end)
        midpoint_lon, midpoint_lat, midpoint_incidence, midpoint_lst = getLonLatIncidenceLst(midpoint)

        nightside_start_str = orbit_start_str
        nightside_end_str = start_str
        nightside_start = orbit_start
        nightside_end = start
        nightside_midpoint = np.mean((nightside_start, nightside_end))
        nightside_midpoint_str = et2utc(nightside_midpoint)
        nightside_duration = nightside_end - nightside_start

        nightside_start_lon, nightside_start_lat, nightside_start_incidence, nightside_start_lst = getLonLatIncidenceLst(nightside_start)
        nightside_end_lon, nightside_end_lat, nightside_end_incidence, nightside_end_lst = getLonLatIncidenceLst(nightside_end)
        nightside_midpoint_lon, nightside_midpoint_lat, nightside_midpoint_incidence, nightside_midpoint_lst = getLonLatIncidenceLst(nightside_midpoint)
        
        orbit_list.append({"orbitNumber":index+1, "etOrbitStart":orbit_start, "etOrbitEnd":orbit_end, \
                           "utcOrbitStart":orbit_start_str, "utcOrbitEnd":orbit_end_str, \
                           
                           
                           "dayside":{"utcStart":start_str, "utcEnd":end_str, "utcMidpoint":midpoint_str, \
                                           "etStart":start, "etEnd":end, "etMidpoint":midpoint, \
                                           "lonStart":start_lon, "lonEnd":end_lon, "lonMidpoint":midpoint_lon, 
                                           "latStart":start_lat, "latEnd":end_lat, "latMidpoint":midpoint_lat, 
                                           "incidenceStart":start_incidence, "incidenceEnd":end_incidence, "incidenceMidpoint":midpoint_incidence, 
                                           "lstStart":start_lst, "lstEnd":end_lst, "lstMidpoint":midpoint_lst, 
                                           "duration":duration}, \

                           "nightside":{"utcStart":nightside_start_str, "utcEnd":nightside_end_str, "utcMidpoint":nightside_midpoint_str, \
                                           "etStart":nightside_start, "etEnd":nightside_end, "etMidpoint":nightside_midpoint, \
                                           "lonStart":nightside_start_lon, "lonEnd":nightside_end_lon, "lonMidpoint":nightside_midpoint_lon, 
                                           "latStart":nightside_start_lat, "latEnd":nightside_end_lat, "latMidpoint":nightside_midpoint_lat, 
                                           "incidenceStart":nightside_start_incidence, "incidenceEnd":nightside_end_incidence, "incidenceMidpoint":nightside_midpoint_incidence, 
                                           "lstStart":nightside_start_lst, "lstEnd":nightside_end_lst, "lstMidpoint":nightside_midpoint_lst, 
                                           "duration":nightside_duration}})
    return orbit_list




def getTangentAltitude(et): #returns zero if viewing planet
    """get occultation tangent altitude for a given time"""
    mars2tgoPos = sp.spkpos("-143", et, SPICE_REF, SPICE_ABCORR, "MARS")[0] #get tgo pos in mars frame
    tgo2sunPos = sp.spkpos("SUN", et, SPICE_REF, SPICE_ABCORR, "-143")[0] #get sun pos in mars frame

    #calculate tangent point altitude
    tangentAltitude = sp.npedln(SPICE_MARS_AXES[0], SPICE_MARS_AXES[1], SPICE_MARS_AXES[2], mars2tgoPos, tgo2sunPos)[1]
    return tangentAltitude




def findTangentAltitudeTime(desired_altitude, start_time, step_size):
    """find time where tangent altitude matches a given value"""
    calculated_altitude = 0.0
    time = start_time
    
    while calculated_altitude < desired_altitude:
        time = time + step_size
        calculated_altitude = getTangentAltitude(time)
    return time




def getLonLatLst(et):
    """get occultation data for a given time"""
    mars2tgoPos = sp.spkpos("-143", et, SPICE_REF, SPICE_ABCORR, "MARS")[0] #get tgo pos in mars frame
    tgo2sunPos = sp.spkpos("SUN", et, SPICE_REF, SPICE_ABCORR, "-143")[0] #get sun pos in mars frame

    coords = sp.npedln(SPICE_MARS_AXES[0], SPICE_MARS_AXES[1], SPICE_MARS_AXES[2], mars2tgoPos, tgo2sunPos)[0]
    lon, lat = sp.reclat(coords)[1:3] * np.asfarray([sp.dpr(),sp.dpr()])
    lst = sp.et2lst(et, 499, (lon / sp.dpr()), "PLANETOCENTRIC")[3]
    lst_hours = np.float(lst[0:2]) + np.float(lst[3:5])/60.0 + np.float(lst[6:8])/3600.0
    return lon, lat, lst_hours




def getOccultationData(orbit_list, mtpConstants):
    """get all occultation data (except grazing), add to orbit list"""
    utc_string_start = mtpConstants["utcStringStart"]
    utc_string_end = mtpConstants["utcStringEnd"]
    acs_start_altitude = mtpConstants["acsStartAltitude"]

    orbit_starts = np.asfarray([orbit["etOrbitStart"] for orbit in orbit_list])
    
    frontBody="MARS"
    frontShape="ELLIPSOID"
    frontFrame="IAU_MARS"
    
    backBody="SUN"
#    backShape="ELLIPSOID"
    backShape="POINT"
    backFrame="IAU_SUN"
    stepSize=1
    
#    occultationType="ANNULAR"
    occultationType="ANY"
    
    
    confinementWindow = sp.stypes.SPICEDOUBLE_CELL(2)
    sp.wninsd(sp.utc2et(utc_string_start), sp.utc2et(utc_string_end), confinementWindow)
    resultWindow = sp.stypes.SPICEDOUBLE_CELL(1000)
    sp.gfoclt(occultationType, frontBody, frontShape, frontFrame, backBody, backShape, backFrame, SPICE_ABCORR, SPICE_OBSERVER, stepSize, confinementWindow, resultWindow)

    count = sp.wncard(resultWindow)
    
    for index in range(count):
        
        #start when the ingress ends
        #end is when the egress starts
        ingress_end, egress_start = sp.wnfetd(resultWindow, index) 
        
        ingress_start_altitude = MAXIMUM_SO_ALTITUDE
        ingress_end_altitude = 0
        ingress_transition_altitude = SO_TRANSITION_ALTITUDE
        egress_end_altitude = MAXIMUM_SO_ALTITUDE
        egress_start_altitude = 0
        egress_transition_altitude = SO_TRANSITION_ALTITUDE

        ingress_start = findTangentAltitudeTime(ingress_start_altitude, ingress_end, -1.0)
        
        ingress_start_acs = findTangentAltitudeTime(acs_start_altitude, ingress_end, -1.0)
        
        ingress_start_str = et2utc(ingress_start)
        ingress_end_str = et2utc(ingress_end)
        ingress_duration = ingress_end - ingress_start
        ingress_transition = findTangentAltitudeTime(ingress_transition_altitude, ingress_end, -1.0)
        ingress_transition_str = et2utc(ingress_transition)
        ingress_midpoint = np.mean((ingress_start, ingress_end))
        ingress_midpoint_str = et2utc(ingress_midpoint)
        ingress_start_lon, ingress_start_lat, ingress_start_lst = getLonLatLst(ingress_start)
        ingress_end_lon, ingress_end_lat, ingress_end_lst = getLonLatLst(ingress_end)
        ingress_midpoint_lon, ingress_midpoint_lat, ingress_midpoint_lst = getLonLatLst(ingress_midpoint)
        ingress_transition_lon, ingress_transition_lat, ingress_transition_lst = getLonLatLst(ingress_transition)
        ingress_midpoint_altitude = getTangentAltitude(ingress_midpoint)

        egress_end = findTangentAltitudeTime(egress_end_altitude, egress_start, 1.0)
        egress_start_str = et2utc(egress_start)
        egress_end_str = et2utc(egress_end)
        egress_duration = egress_end - egress_start
        egress_transition = findTangentAltitudeTime(egress_transition_altitude, egress_start, 1.0)
        egress_transition_str = et2utc(egress_transition)
        egress_midpoint = np.mean((egress_start, egress_end))
        egress_midpoint_str = et2utc(egress_midpoint)
        egress_start_lon, egress_start_lat, egress_start_lst = getLonLatLst(egress_start)
        egress_end_lon, egress_end_lat, egress_end_lst = getLonLatLst(egress_end)
        egress_midpoint_lon, egress_midpoint_lat, egress_midpoint_lst = getLonLatLst(egress_midpoint)
        egress_transition_lon, egress_transition_lat, egress_transition_lst = getLonLatLst(egress_transition)
        egress_midpoint_altitude = getTangentAltitude(egress_midpoint)

        obs_ingress_start = ingress_start - INITIALISATION_TIME - PRECOOLING_TIME - SO_REFERENCE_DURATION
        obs_ingress_end = ingress_end + SO_REFERENCE_DURATION
        obs_ingress_duration = obs_ingress_end - obs_ingress_start
        obs_egress_start = egress_start - INITIALISATION_TIME - PRECOOLING_TIME - SO_REFERENCE_DURATION
        obs_egress_end = egress_end + SO_REFERENCE_DURATION
        obs_egress_duration = obs_egress_end - obs_egress_start

        if egress_start - ingress_end < MINIMUM_TIME_BETWEEN_OCCULTATIONS:
            
            merged_start = ingress_start
            merged_start_str = ingress_start_str
            merged_end = egress_end
            merged_end_str = egress_end_str

            merged_start_altitude = ingress_start_altitude
            merged_end_altitude = egress_end_altitude
            merged_transition_altitude = "-"

            merged_duration = merged_end - merged_start
            merged_transition = "-"
            merged_transition_str = "-"
            merged_midpoint = "-"
            merged_midpoint_str = "-"
            merged_start_lon, merged_start_lat, merged_start_lst = getLonLatLst(merged_start)
            merged_end_lon, merged_end_lat, merged_end_lst = getLonLatLst(merged_end)
            merged_midpoint_lon = merged_midpoint_lat = merged_midpoint_lst = "-"
            merged_transition_lon = merged_transition_lat = merged_transition_lst = "-"
            merged_midpoint_altitude = "-"
            
            obs_merged_start = obs_ingress_start
            obs_merged_end = obs_egress_end
            obs_merged_duration = obs_merged_end - obs_merged_start

            occultation_dict = {"occultationNumber":index+1, \
                                "merged":{"utcStart":merged_start_str, "utcEnd":merged_end_str, "utcMidpoint":merged_midpoint_str, "utcTransition":merged_transition_str, \
                                          "etStart":merged_start, "etEnd":merged_end, "etMidpoint":merged_midpoint, "etTransition":merged_transition, \
                                           "lonStart":merged_start_lon, "lonEnd":merged_end_lon, "lonMidpoint":merged_midpoint_lon, "lonTransition":merged_transition_lon, \
                                           "latStart":merged_start_lat, "latEnd":merged_end_lat, "latMidpoint":merged_midpoint_lat, "latTransition":merged_transition_lat, \
                                           "altitudeStart":merged_start_altitude, "altitudeEnd":merged_end_altitude, "altitudeMidpoint":merged_midpoint_altitude, "altitudeTransition":merged_transition_altitude, \
                                           "lstStart":merged_start_lst, "lstEnd":merged_end_lst, "lstMidpoint":merged_midpoint_lst, "lstTransition":merged_transition_lst, \
                                           "obsStart":obs_merged_start, "obsEnd":obs_merged_end, "obsDuration":obs_merged_duration, \
                                           "duration":merged_duration, \
                                           "etStartAcs":ingress_start_acs}}
        else:
            occultation_dict = {"occultationNumber":index+1, \
                                "ingress":{"utcStart":ingress_start_str, "utcEnd":ingress_end_str, "utcMidpoint":ingress_midpoint_str, "utcTransition":ingress_transition_str, \
                                           "etStart":ingress_start, "etEnd":ingress_end, "etMidpoint":ingress_midpoint, "etTransition":ingress_transition, \
                                           "lonStart":ingress_start_lon, "lonEnd":ingress_end_lon, "lonMidpoint":ingress_midpoint_lon, "lonTransition":ingress_transition_lon, \
                                           "latStart":ingress_start_lat, "latEnd":ingress_end_lat, "latMidpoint":ingress_midpoint_lat, "latTransition":ingress_transition_lat, \
                                           "altitudeStart":ingress_start_altitude, "altitudeEnd":ingress_end_altitude, "altitudeMidpoint":ingress_midpoint_altitude, "altitudeTransition":ingress_transition_altitude, \
                                           "lstStart":ingress_start_lst, "lstEnd":ingress_end_lst, "lstMidpoint":ingress_midpoint_lst, "lstTransition":ingress_transition_lst, \
                                           "obsStart":obs_ingress_start, "obsEnd":obs_ingress_end, "obsDuration":obs_ingress_duration, \
                                           "duration":ingress_duration, \
                                           "etStartAcs":ingress_start_acs}, 

                                 "egress":{"utcStart":egress_start_str, "utcEnd":egress_end_str, "utcMidpoint":egress_midpoint_str, "utcTransition":egress_transition_str, \
                                           "etStart":egress_start, "etEnd":egress_end, "etMidpoint":egress_midpoint, "etTransition":egress_transition, \
                                           "lonStart":egress_start_lon, "lonEnd":egress_end_lon, "lonMidpoint":egress_midpoint_lon, "lonTransition":egress_transition_lon, \
                                           "latStart":egress_start_lat, "latEnd":egress_end_lat, "latMidpoint":egress_midpoint_lat, "latTransition":egress_transition_lat, \
                                           "altitudeStart":egress_start_altitude, "altitudeEnd":egress_end_altitude, "altitudeMidpoint":egress_midpoint_altitude, "altitudeTransition":egress_transition_altitude, \
                                           "lstStart":egress_start_lst, "lstEnd":egress_end_lst, "lstMidpoint":egress_midpoint_lst, "lstTransition":egress_transition_lst, \
                                           "obsStart":obs_egress_start, "obsEnd":obs_egress_end, "obsDuration":obs_egress_duration, \
                                           "duration":egress_duration}}
        orbit_index = (ingress_start > orbit_starts).argmin() - 1
        orbit_list[orbit_index].update(occultation_dict)

        #finally, print note if occultations are merged, or almost merged
        if (egress_start - ingress_end) < (MINIMUM_TIME_BETWEEN_OCCULTATIONS + 30.0):
            print("Time between occultations is %0.1f seconds for orbit list index %i" %((egress_start - ingress_end), orbit_index))
        


    return orbit_list        




def findGrazingOccultations(orbit_list):
    """find all grazing occultations in MTP, add to orbit list"""
    grazing_index = 0
    for orbit in orbit_list:
        if orbit["dayside"]["incidenceMidpoint"] > 60.0: #if high beta angle
            if "merged" not in orbit.keys():
                et_start = orbit["nightside"]["etStart"] + 500
                et_end = orbit["nightside"]["etEnd"] - 500
                step_size = OCCULTATION_SEARCH_STEP_SIZE
                ets = np.arange(et_start, et_end, step_size)
                alts = np.asfarray([getTangentAltitude(et) for et in ets])
                minimum_altitude = np.min(alts)
                if 0.0 < minimum_altitude < MAXIMUM_GRAZING_ALTITUDE: #if grazing and below 
                    grazing_index += 1
                    grazing_start_altitude = MAXIMUM_SO_ALTITUDE
                    grazing_end_altitude = MAXIMUM_SO_ALTITUDE
    
                    alt_ingress = alts[0:int(len(alts)/2)] #ingress altitudes
                    alt_ingress_index = (alt_ingress > MAXIMUM_SO_ALTITUDE).argmin()
    
                    grazing_start = ets[alt_ingress_index]
                    grazing_start_str = et2utc(grazing_start)
                    grazing_start_lon, grazing_start_lat, grazing_start_lst =  getLonLatLst(grazing_start)
                    
                    alt_egress = np.copy(alts)
                    alt_egress[0:int(len(alts)/2)] = -100.0
                    alt_egress_index = (alt_egress > MAXIMUM_SO_ALTITUDE).argmax()
    
                    grazing_end = ets[alt_egress_index]
                    grazing_end_str = et2utc(grazing_end)
                    grazing_end_lon, grazing_end_lat, grazing_end_lst =  getLonLatLst(grazing_start)
                    
                    grazing_midpoint_altitude = minimum_altitude
                    grazing_midpoint_index = np.where(alts == grazing_midpoint_altitude)[0][0]
                    grazing_midpoint = ets[grazing_midpoint_index]
                    grazing_midpoint_str = et2utc(grazing_midpoint)
                    grazing_midpoint_lon, grazing_midpoint_lat, grazing_midpoint_lst =  getLonLatLst(grazing_midpoint)
    
                    obs_grazing_start = grazing_start - INITIALISATION_TIME - PRECOOLING_TIME - SO_REFERENCE_DURATION
                    obs_grazing_end = grazing_end + SO_REFERENCE_DURATION
                    obs_duration = obs_grazing_end - obs_grazing_start
                    
                    grazing_duration = grazing_end - grazing_start
                    
                    occultation_dict = {"occultationNumber":grazing_index, \
                        "grazing":{"utcStart":grazing_start_str, "utcEnd":grazing_end_str, "utcMidpoint":grazing_midpoint_str, "utcTransition":"-", \
                                  "etStart":grazing_start, "etEnd":grazing_end, "etMidpoint":grazing_midpoint, "etTransition":"-", \
                                   "lonStart":grazing_start_lon, "lonEnd":grazing_end_lon, "lonMidpoint":grazing_midpoint_lon, "lonTransition":"-", \
                                   "latStart":grazing_start_lat, "latEnd":grazing_end_lat, "latMidpoint":grazing_midpoint_lat, "latTransition":"-", \
                                   "altitudeStart":grazing_start_altitude, "altitudeEnd":grazing_end_altitude, "altitudeMidpoint":grazing_midpoint_altitude, "altitudeTransition":"-", \
                                   "lstStart":grazing_start_lst, "lstEnd":grazing_end_lst, "lstMidpoint":grazing_midpoint_lst, "lstTransition":"-", \
                                   "obsStart":obs_grazing_start, "obsEnd":obs_grazing_end, "obsDuration":obs_duration, \
                                   "duration":grazing_duration}}
    
    
                    
                    orbit.update(occultation_dict)
    return orbit_list




def readMappsEventFile(instrument, mappsObservationType, mtpConstants, paths):
    """read in the LTP  planning file from the SOC and find NOMAD or ACS events (occultations) or terminator crossings (nadir)"""
    mappsEventFilename = mtpConstants["mappsEventFilename"]
    
    
    mappsEventFilepath = os.path.join(paths["EVENT_FILE_PATH"], mappsEventFilename)
    lines = [line.rstrip('\n').split()[0:3] for line in open(mappsEventFilepath) if line[0] != "#"]

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
            
    return orbit_list




def regionsOfInterestNadir(orbit_list, regions_of_interest, silent=True):
    """check for nadir observations near regions of interest"""
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
            
            for regionOfInterest in regions_of_interest:
                matches = np.logical_and(
                        np.logical_and((regionOfInterest[1] < lats), (regionOfInterest[2] > lats)),
                        np.logical_and((regionOfInterest[3] < lons), (regionOfInterest[4] > lons))
                        )
                if np.any(matches):
                    i = int(np.mean(np.where(matches)[0])) #find centre index
                    if incidence_angles[i] < MAXIMUM_SEARCH_INCIDENCE_ANGLE: #check if solar angle too low
                        regionDict = {"name":regionOfInterest[0], \
                             "et":ets[i], "utc":et2utc(ets[i]), \
                             "lon":lons[i], "lat":lats[i], \
                             "incidenceAngle":incidence_angles[i], "lst":lst[i]}
                        if "daysideRegions" not in orbit.keys():
                            orbit["daysideRegions"] = []
                        orbit["daysideRegions"].append(regionDict)
                    else:
                        if not silent: print("Match found on orbit %i but incidence angle %0.1f is above %0.0f" %(orbit["orbitNumber"], incidence_angles[i], MAXIMUM_SEARCH_INCIDENCE_ANGLE))
    return orbit_list




def regionsOfInterestOccultation(orbit_list, regions_of_interest, silent=True):
    """check for occultation observations near regions of interest"""
    #loop through each observation, making lat/lon steps and check against regions of interest
    for orbit in orbit_list:
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
                for region_of_interest in regions_of_interest:
                    matches = np.logical_and(
                            np.logical_and((region_of_interest[1] < lats), (region_of_interest[2] > lats)),
                            np.logical_and((region_of_interest[3] < lons), (region_of_interest[4] > lons))
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
                            i = int(np.where(alts[matches] == min_altitude)[0]) #find index corresponding to minimum altitude
                            #i = int(np.mean(np.where(matches)[0])) #find centre index
                            
                            #get data for minimum altitude point
                            regionDict = {"occultationType":occultation_type, "name":region_of_interest[0], \
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
            for region in orbit["daysideRegions"]:
                if not silent: 
                    print("Match found: %s, orbit %i, incidence angle %0.1f at %s" %(region["name"], orbit["orbitNumber"], region["incidenceAngle"], region["utc"]))
    
                if region["name"] in nadirRegionsObservations.keys():
                    orbit["dayside"]["observationName"] = nadirRegionsObservations[region["name"]]
                    if not silent: 
                        print("%s observation added" %nadirRegionsObservations[region["name"]])
                else:
                    print("Warning: %s not found in observation list" %region["name"])
    
        if "occultationRegions" in orbit.keys():
            for region in orbit["occultationRegions"]:
                matchingOccultationType = region["occultationType"]
                if not silent: 
                    print("Match found: %s, orbit %i, %s occultation at %s" %(region["name"], orbit["orbitNumber"], matchingOccultationType, region["utc"]))
    
                if region["name"] in occultationRegionsObservations.keys():
                    orbit[matchingOccultationType]["observationName"] = occultationRegionsObservations[region["name"]]
                    if not silent: 
                        print("%s observation added" %occultationRegionsObservations[region["name"]])
                else:
                    print("Warning: %s not found in observation list" %region["name"])
    return orbit_list




def makeGenericOrbitPlan(orbit_list, silent=True):
    """save generic plan to orbit list. This doesn't have nightsides or limbs, just occs and dayside nadirs"""
    """baseline orbit plan orbit types: 1 or 5 if occultations, 14 if not, 3 if nadir region of interest detected"""
    # Potential improvment: automatically add some limbs and nightsides to fill in the times when occultations cannot be performed


    #inputs for defining generic orbit plan
    LNO_CYCLE = ["ON", "OFF"] * 200 #i.e. 50% duty cycle for orbits without occultations. 
    #This should begin with a 3 so that first observation after OCM is an LNO
    #The script automatically starts with a 4 if the preceding orbit has a measurement to avoid scheduling too many consecutive observations.
 
    lno_cycle = -1
    for orbit in orbit_list:

        generic_orbit = {}
        generic_orbit_type = UVIS_DEFAULT_ORBIT_TYPE
        generic_orbit_comment = ""
        
        generic_orbit["irNightside"] = "" #irNightside not defined in generic plan
        generic_orbit["uvisNightside"] = "" #uvisNightside not defined in generic plan

        """check for possible OCMs (Saturday afternoons, 11 - 4pm)"""
        timeStringOut = orbit["dayside"]["utcStart"]
        orbitNumber = orbit["orbitNumber"]
    
        #first check for OCMs
        ocm = False
        if datetime.strptime(timeStringOut, SPICE_DATETIME_FORMAT).isoweekday() == 6:
            if orbitNumber != 1: #if not first orbit
                if orbitNumber != len(orbit_list): #if not last orbit
                    if 11 < datetime.strptime(timeStringOut, SPICE_DATETIME_FORMAT).hour < 16:
                        generic_orbit_comment += "&possibleOCM; "
                        ocm = True

        #next check for true (UVIS+LNO) limbs
        if "trueLimb" in orbit["allowedObservationTypes"]:
            generic_orbit_type = 28
            generic_orbit["irDayside"] = "irLimb"
            generic_orbit["uvisDayside"] = "uvisLimb"
            generic_orbit["irIngressHigh"] = ""
            generic_orbit["irIngressLow"] = ""
            generic_orbit["uvisIngress"] = ""
            generic_orbit["irEgressHigh"] = ""
            generic_orbit["irEgressLow"] = ""
            generic_orbit["uvisEgress"] = ""

    
        for occultation_type in orbit["allowedObservationTypes"]:
            if occultation_type == "ingress":
                generic_orbit["irIngressHigh"] = "irIngress"
                generic_orbit["irIngressLow"] = "irIngress"
                generic_orbit["uvisIngress"] = "uvisIngress"
    
                generic_orbit_type = 1
                if "egress" in orbit["allowedObservationTypes"]: #if 2 occultations in same orbit
                    generic_orbit["irDayside"] = "irShortDayside"
                else:
                    generic_orbit["irDayside"] = "irDayside"
                    generic_orbit["irEgressHigh"] = ""
                    generic_orbit["irEgressLow"] = ""
                    generic_orbit["uvisEgress"] = ""
    
                generic_orbit["uvisDayside"] = "uvisDayside"
                
            elif occultation_type == "egress":
                generic_orbit["irEgressHigh"] = "irEgress"
                generic_orbit["irEgressLow"] = "irEgress"
                generic_orbit["uvisEgress"] = "uvisEgress"
    
                generic_orbit_type = 1
                if "ingress" in orbit["allowedObservationTypes"]: #if 2 occultations in same orbit
                    generic_orbit["irDayside"] = "irShortDayside"
                else:
                    generic_orbit["irDayside"] = "irDayside"
                    generic_orbit["irIngressHigh"] = ""
                    generic_orbit["irIngressLow"] = ""
                    generic_orbit["uvisIngress"] = ""
    
                generic_orbit["uvisDayside"] = "uvisDayside"
                
            elif occultation_type == "merged":
                generic_orbit["irIngressHigh"] = "irMerged"
                generic_orbit["irIngressLow"] = "irMerged"
                generic_orbit["uvisIngress"] = "uvisMerged"
    
                generic_orbit["irEgressHigh"] = ""
                generic_orbit["irEgressLow"] = ""
                generic_orbit["uvisEgress"] = ""
    
                generic_orbit_type = 5
                generic_orbit["irDayside"] = "irShortDayside"
                generic_orbit["uvisDayside"] = "uvisDayside"
                
            elif occultation_type == "grazing":
                generic_orbit["irIngressHigh"] = "irGrazing"
                generic_orbit["irIngressLow"] = "irGrazing"
                generic_orbit["uvisIngress"] = "uvisGrazing"
    
                generic_orbit["irEgressHigh"] = ""
                generic_orbit["irEgressLow"] = ""
                generic_orbit["uvisEgress"] = ""
    
                generic_orbit_type = 5
                generic_orbit["irDayside"] = "irDayside"
                generic_orbit["uvisDayside"] = "uvisDayside"
    
            lno_cycle = 0 #reset lno to off

            #check for occultation regions of interest
            if "occultationRegions" in orbit.keys(): #if occ obs matches region of interest, set SO on and override generic comment with specific obs
                for region in orbit["occultationRegions"]:
                    generic_orbit_comment += "%sMatch:%s; " %(region["occultationType"], region["name"])
                    matchingOccultationType = region["occultationType"]
                    if "observationName" in orbit[matchingOccultationType].keys(): #if dedicated obs type found, overwrite generic obs
                        if matchingOccultationType == "ingress":
                            generic_orbit["irIngressHigh"] = orbit[matchingOccultationType]["observationName"]
                            generic_orbit["irIngressLow"] = orbit[matchingOccultationType]["observationName"]
                        if matchingOccultationType == "egress":
                            generic_orbit["irEgressHigh"] = orbit[matchingOccultationType]["observationName"]
                            generic_orbit["irEgressLow"] = orbit[matchingOccultationType]["observationName"]
                        if matchingOccultationType == "merged":
                            generic_orbit["irIngressHigh"] = orbit[matchingOccultationType]["observationName"]
                            generic_orbit["irIngressLow"] = orbit[matchingOccultationType]["observationName"]
                        if matchingOccultationType == "grazing":
                            generic_orbit["irIngressHigh"] = orbit[matchingOccultationType]["observationName"]
                            generic_orbit["irIngressLow"] = orbit[matchingOccultationType]["observationName"]
                        
                    else:
                        print("Warning: region of interest found but no dedicated observation type has been specified")


    
        if generic_orbit_type in [4, 14]: #if no occultations
    
            generic_orbit["irIngressHigh"] = ""
            generic_orbit["irIngressLow"] = ""
            generic_orbit["uvisIngress"] = ""
            generic_orbit["irEgressHigh"] = ""
            generic_orbit["irEgressLow"] = ""
            generic_orbit["uvisEgress"] = ""
    
            if ocm: #NOMAD must be off during correction maneouvres
                generic_orbit["irDayside"] = ""
                generic_orbit["uvisDayside"] = ""
                lno_cycle = -1 #reset lno to on

            else:
                #check nadir regions of interest
                if "daysideRegions" in orbit.keys(): #if nadir obs matches region of interest, set LNO on
                    lno_on_off = "ON"
                    lno_cycle = 0 #reset lno to off
                    
                    for region in orbit["daysideRegions"]:
                        generic_orbit_comment += "&daysideMatch:%s; " %(region["name"])
                        
                else:
                    lno_cycle += 1
                    lno_on_off = LNO_CYCLE[lno_cycle]
                
                if lno_on_off == "ON":
                    generic_orbit_type = 3
                    generic_orbit["irDayside"] = "irLongDayside"
                    generic_orbit["uvisDayside"] = "uvisDayside"

                    #check nadir regions of interest in orbit list
                    if "observationName" in orbit["dayside"].keys(): #if dedicated obs type found, overwrite generic obs
                        generic_orbit["irDayside"] = orbit["dayside"]["observationName"]

            
                else: #if lno off and no occultations
                    generic_orbit["irDayside"] = ""
                    if generic_orbit_type == 4: #if 3x UVIS TCs
                        generic_orbit["uvisDayside"] = "uvisDayside"
                        
                    elif generic_orbit_type == 14: #if 1x UVIS TCs
                        generic_orbit["uvisDayside"] = "uvisDayside"

        else: #if not orbit type 14, still check for nadir regions
            #check nadir regions of interest
            if "daysideRegions" in orbit.keys(): #if nadir obs matches region of interest, set LNO on
                for region in orbit["daysideRegions"]:
                    generic_orbit_comment += "&daysideMatch:%s; " %(region["name"])
    
            #check nadir regions of interest in orbit list
            if "observationName" in orbit["dayside"].keys(): #if dedicated obs type found, overwrite generic obs
                generic_orbit["irDayside"] = orbit["dayside"]["observationName"]

            
        #special section for true limbs
        if "trueLimb" in orbit["allowedObservationTypes"]:
            generic_orbit_type = 28
            generic_orbit["irIngressHigh"] = ""
            generic_orbit["irIngressLow"] = ""
            generic_orbit["uvisIngress"] = ""
            generic_orbit["irEgressHigh"] = ""
            generic_orbit["irEgressLow"] = ""
            generic_orbit["uvisEgress"] = ""
            generic_orbit["irDayside"] = "irLimb"
            generic_orbit["uvisDayside"] = "uvisLimb"
            generic_orbit_comment = "&trueLimb"
        
    
        orbit["genericOrbitPlanOut"] = {"orbitType":generic_orbit_type, "orbitTypes":generic_orbit, "comment":generic_orbit_comment}
    return orbit_list





def writeObservationPlan(worksheet, row, row_to_write):
    """function to write observation plan"""
    for column, row_item in enumerate(row_to_write):
        worksheet.write(row, column, row_item)





def writeOrbitPlanXlsx(orbit_list, mtpConstants, paths, version):
    """write generic observation plan to file if the file doesn't exist """
    mtp_number = mtpConstants["mtpNumber"]
    
    #check if file has already been placed in correct directory. If so, don't generate again
    fileExists = os.path.isfile(os.path.join(paths["ORBIT_PLAN_PATH"], "nomad_mtp%03d_%s.xlsx" %(mtp_number, version)))
        
    if not fileExists:    
        with xlsxwriter.Workbook(os.path.join(BASE_DIRECTORY, "nomad_mtp%03d_%s.xlsx" %(mtp_number, version))) as workbook:
            worksheet = workbook.add_worksheet()
            
            if version == "plan_generic": #find name of the orbit plan
                orbitPlanName = "genericOrbitPlanOut"
            elif version == "plan":
                orbitPlanName = "completeOrbitPlan"
            else:
                print("Error: unknown version %s. Exiting..." %version)
                sys.exit()
            
            rowCounter = 0
            writeObservationPlan(worksheet, rowCounter, ["#orbitType","irIngressHigh","irIngressLow","uvisIngress","irEgressHigh","irEgressLow","uvisEgress","irDayside","uvisDayside","irNightside","uvisNightside","night2dayTerminator","comment"])
    
            for orbit in orbit_list:
                orbitPlan = orbit[orbitPlanName]
                row_to_write = [orbitPlan["orbitType"]]
                
                for genericObsType in ["irIngressHigh","irIngressLow","uvisIngress","irEgressHigh","irEgressLow","uvisEgress","irDayside","uvisDayside","irNightside","uvisNightside"]:
                    if version == "plan_generic": #find name of the orbit plan. Information is in a different format in the generic orbit plan
                        row_to_write.append(orbitPlan["orbitTypes"][genericObsType])
                    elif version == "plan":
                        row_to_write.append(orbitPlan[genericObsType])
                
                row_to_write.append(orbit["dayside"]["utcStart"])
                row_to_write.append(orbitPlan["comment"])
                
                rowCounter += 1
                writeObservationPlan(worksheet, rowCounter, row_to_write)






def getMtpPlanXlsx(mtpConstants, paths, version):
    """read back in orbit plan after iteration by OU/BIRA"""
    mtp_number = mtpConstants["mtpNumber"]
    
    workbookPath = os.path.join(paths["ORBIT_PLAN_PATH"], "nomad_mtp%03d_%s.xlsx" %(mtp_number, version))
    
    if not os.path.exists(workbookPath):
        if version == "plan_generic": #write message depending on which orbit plan was not found, then exit program
            print("Iterated orbit plan (%s) not found. Exiting..." %workbookPath)
        elif version == "plan":
            print("Final orbit plan (%s) not found. Exiting..." %workbookPath)
        else:
            print("Orbit plan (%s) not found. Exiting..." %workbookPath)
        sys.exit()
    
    #if plan found, open it and list contents
    with xlrd.open_workbook(workbookPath) as workbook:
        worksheet = workbook.sheet_by_index(0)
        
        mtp_plan_list = []
        mtpPlanColumns = ["orbitType", "irIngressHigh", "irIngressLow", "uvisIngress", "irEgressHigh", "irEgressLow", "uvisEgress", "irDayside", \
                          "uvisDayside", "irNightside", "uvisNightside", "night2dayTerminator","comment"]
        for row_index in range(worksheet.nrows):
            if row_index > 0:
                row = worksheet.row(row_index)
                cells = {}
                for column_index in range(len(mtpPlanColumns)):
                    cell_obj = row[column_index]
                    if column_index == 0:
                        cell = int(cell_obj.value)
                    else:
                        cell = str(cell_obj.value)
                    cells[mtpPlanColumns[column_index]] = cell
                mtp_plan_list.append(cells)
        
    return mtp_plan_list




def mergeMtpPlan(orbit_list, mtp_plan, new_dict_name, old_dict_name):
    """merge iterated orbit plan into orbit list, check that they match each other"""    
    if len(mtp_plan) != len(orbit_list):
        print("Error: length of plan read in from file does not match number of orbits calculated")
    
    for orbit, orbit_plan in zip(orbit_list, mtp_plan):
        orbit[new_dict_name] = {}
        
        if orbit_plan["orbitType"] == 1 and orbit[old_dict_name]["orbitType"] != 1:
            print("Error: occultation mismatch between orbit plan written and orbit plan read in for orbit number %i" %orbit["orbitNumber"])
            
        #do checks to ensure that ingress/egresses match in orbit list and mtp plan
        occultationFound = [True for value in orbit["allowedObservationTypes"] if value in ["ingress", "egress", "merged", "grazing"]]
        if orbit_plan["orbitType"] in [1, 5, 6] and not occultationFound:
            print("Error: occultation detected in orbit that shouldn't have occultations")
        
        for key, value in orbit_plan.items():
            if key in ["orbitType", "irIngressHigh", "irIngressLow", "uvisIngress", "irEgressHigh", "irEgressLow", "uvisEgress", "irDayside", \
                      "uvisDayside", "irNightside", "uvisNightside", "comment"]:
                orbit[new_dict_name][key] = value
            if value != "":
                orbit[key] = value


    return orbit_list




def checkKeys(occultationObservationDict, nadirObservationDict):
    """check if all keys above can be found in the observation dictionaries"""
    for key_file in [OCCULTATION_KEYS, OCCULTATION_MERGED_KEYS, OCCULTATION_GRAZING_KEYS]:
        for observation_name in key_file:
            if observation_name not in list(occultationObservationDict.keys()):
                print("Error: %s not found in occultation dictionary!" %observation_name)
    
    for key_file in [NADIR_KEYS, NADIR_LIMB_KEYS]:
        for observation_name in key_file:
            if observation_name not in list(nadirObservationDict.keys()):
                print("Error: %s not found in nadir dictionary!" %observation_name)






def makeCompleteOrbitPlan(orbit_list):
    """fill in generic plan with real observation names"""
    occultationCounter = -1
    occultationMergedCounter = -1
    occultationGrazingCounter = -1
#    occultationRidealongCounter = -1
    nadirCounter = -1
    nadirLimbCounter = -1
    nadirNightsideCounter = -1
    
    for orbit in orbit_list:
    
        genericObsTypes = orbit["genericOrbitPlanIn"]
        orbitType = genericObsTypes["orbitType"]
    
        irIngressHigh = "******ERROR******" #to be replaced in loop
        irIngressLow = "******ERROR******" #to be replaced in loop
        irEgressHigh = "******ERROR******" #to be replaced in loop
        irEgressLow = "******ERROR******" #to be replaced in loop
        irDayside = "******ERROR******" #to be replaced in loop
        irNightside = "******ERROR******" #to be replaced in loop
    
    #    uvisIngress = genericObsTypes["uvisIngress"]
    #    uvisEgress = genericObsTypes["uvisEgress"]
    #    uvisDayside = genericObsTypes["uvisDayside"]
    
    
    
        if orbitType in [1]:
            if genericObsTypes["irIngressHigh"] == "": #no observation
                irIngressHigh = ""
                irIngressLow = ""
                uvisIngress = ""
            elif genericObsTypes["irIngressHigh"] == "irIngress": #generic observation
                occultationCounter += 1
                irIngressHigh = OCCULTATION_KEYS[occultationCounter]
                irIngressLow = OCCULTATION_KEYS[occultationCounter]
                uvisIngress = "uvisIngress"
                #special obs where high and low altitude obs are different
                if USE_TWO_SCIENCES:
                    if OCCULTATION_KEYS[occultationCounter]=="Nominal Science 1xCO2 LA01":
                        irIngressHigh = "Nominal Science 1xCO2 HA01"
                        irIngressLow = "Nominal Science 1xCO2 LA01"
                    elif OCCULTATION_KEYS[occultationCounter]=="Nominal Science 1xCO2 LA02":
                        irIngressHigh = "Nominal Science 1xCO2 HA02"
                        irIngressLow = "Nominal Science 1xCO2 LA02"
                    elif OCCULTATION_KEYS[occultationCounter]=="Nominal Science 1xCO2 LA03":
                        irIngressHigh = "Nominal Science 1xCO2 HA03"
                        irIngressLow = "Nominal Science 1xCO2 LA03"
                    elif OCCULTATION_KEYS[occultationCounter]=="Nominal Science 1xCO2 LA04":
                        irIngressHigh = "Nominal Science 1xCO2 HA04"
                        irIngressLow = "Nominal Science 1xCO2 LA04"
    #        elif occ1High in ["Ingress_ACS","Egress_ACS"]:
    #            occultationRidealongCounter += 1
    #            irIngressHigh = OCCULTATION_ACS_RIDEALONG_KEYS[occultationRidealongCounter]
    #            irIngressLow = OCCULTATION_ACS_RIDEALONG_KEYS[occultationRidealongCounter]
    
            else:
                irIngressHigh = genericObsTypes["irIngressHigh"] #use preselected targeted obs
                irIngressLow = genericObsTypes["irIngressLow"] #use preselected targeted obs
                uvisIngress = "uvisIngress"
    
    
            if genericObsTypes["irEgressHigh"] == "": #no observation
                irEgressHigh = ""
                irEgressLow = ""
                uvisEgress = ""
            elif genericObsTypes["irEgressHigh"] == "irEgress": #generic observation
                occultationCounter += 1
                irEgressHigh = OCCULTATION_KEYS[occultationCounter]
                irEgressLow = OCCULTATION_KEYS[occultationCounter]
                uvisEgress = "uvisEgress"
                #special obs where high and low altitude obs are different
                if USE_TWO_SCIENCES:
                    if OCCULTATION_KEYS[occultationCounter]=="Nominal Science 1xCO2 LA01":
                        irEgressHigh = "Nominal Science 1xCO2 HA01"
                        irEgressLow = "Nominal Science 1xCO2 LA01"
                    elif OCCULTATION_KEYS[occultationCounter]=="Nominal Science 1xCO2 LA02":
                        irEgressHigh = "Nominal Science 1xCO2 HA02"
                        irEgressLow = "Nominal Science 1xCO2 LA02"
                    elif OCCULTATION_KEYS[occultationCounter]=="Nominal Science 1xCO2 LA03":
                        irEgressHigh = "Nominal Science 1xCO2 HA03"
                        irEgressLow = "Nominal Science 1xCO2 LA03"
                    elif OCCULTATION_KEYS[occultationCounter]=="Nominal Science 1xCO2 LA04":
                        irEgressHigh = "Nominal Science 1xCO2 HA04"
                        irEgressLow = "Nominal Science 1xCO2 LA04"
    #        elif occ2High in ["Ingress_ACS","Egress_ACS"]:
    #            occultationRidealongCounter += 1
    #            irEgressHigh = OCCULTATION_ACS_RIDEALONG_KEYS[occultationRidealongCounter]
    #            irEgressLow = OCCULTATION_ACS_RIDEALONG_KEYS[occultationRidealongCounter]
            else:
                irEgressHigh = genericObsTypes["irEgressHigh"] #use preselected targeted obs
                irEgressLow = genericObsTypes["irEgressLow"] #use preselected targeted obs
                uvisEgress = "uvisEgress"
    
    
            if genericObsTypes["irDayside"] == "": #if LNO off
                irDayside = ""
                uvisDayside = "uvisDayside"
            elif genericObsTypes["irDayside"] in ["irDayside", "irShortDayside", "irLongDayside"]: #generic observation
                nadirCounter += 1
                irDayside = NADIR_KEYS[nadirCounter]
                uvisDayside = "uvisDayside"
            else: #use preselected targeted obs
                irDayside = genericObsTypes["irDayside"]
                uvisDayside = "uvisDayside"
            orbit["allowedObservationTypes"].append("dayside")
    
            irNightside="" #never nightside with occultations
            uvisNightside = "" #never nightside with occultations
    
    
        if orbitType in [5, 6]: #merged/grazing with UVIS and/or LNO nadir
            if genericObsTypes["irIngressHigh"] == "irMerged": #generic observation
                occultationMergedCounter += 1
                irIngressHigh = OCCULTATION_MERGED_KEYS[occultationMergedCounter]
                irIngressLow = OCCULTATION_MERGED_KEYS[occultationMergedCounter]
                uvisIngress = "uvisMerged"
            elif genericObsTypes["irIngressHigh"] == "irGrazing": #generic observation
                occultationGrazingCounter += 1
                irIngressHigh = OCCULTATION_GRAZING_KEYS[occultationGrazingCounter]
                irIngressLow = OCCULTATION_GRAZING_KEYS[occultationGrazingCounter]
                uvisIngress = "uvisGrazing"
            else:
                irIngressHigh = genericObsTypes["irIngressHigh"] #use preselected targeted obs
                irIngressLow = genericObsTypes["irIngressLow"] #use preselected targeted obs
            irEgressHigh = ""
            irEgressLow = ""
            uvisEgress = ""
    
    
    
            if genericObsTypes["irDayside"] in ["irDayside", "irShortDayside", "irLongDayside"]: #LNO generic dayside nadir
                if orbitType == 6:
                    print("Error: orbit type 6 cannot have LNO dayside")
                    irDayside = ""
                    uvisDayside = "uvisDayside"
                else:
                    nadirCounter += 1
                    irDayside = NADIR_KEYS[nadirCounter]
                    uvisDayside = "uvisDayside"
    
            elif genericObsTypes["irDayside"] == "": #LNO off
                if orbitType == 6:
                    irDayside = ""
                    uvisDayside = "uvisDayside"
                else:
                    uvisDayside = "uvisDayside"
            else: #use preselected targeted obs
                if orbitType == 6:
                    print("Error: orbit type 6 cannot have LNO dayside")
                    irDayside = ""
                    uvisDayside = "uvisDayside"
                else:
                    irDayside = genericObsTypes["irDayside"] #use preselected targeted obs
                    uvisDayside = "uvisDayside"
            orbit["allowedObservationTypes"].append("dayside")
    
            irNightside=""
            uvisNightside = ""
    
                
    
    
        if orbitType in [3, 4, 14]: #no occultations, dayside nadir only. Possible OCM here
            irIngressHigh=""
            irIngressLow=""
            uvisIngress = ""
            irEgressHigh=""
            irEgressLow=""
            uvisEgress = ""
    
            irNightside=""
            uvisNightside = ""

            if orbitType in [3, 14]:
                orbit["allowedObservationTypes"].append("dayside")
            elif orbitType == 4:
                orbit["allowedObservationTypes"].append("dayside")
                orbit["allowedObservationTypes"].append("dayside2")
                orbit["allowedObservationTypes"].append("dayside3")
            
            uvisDayside = genericObsTypes["uvisDayside"] #UVIS already off for OCM
    
    
            if genericObsTypes["irDayside"] in ["irDayside", "irShortDayside", "irLongDayside"]: #LNO generic dayside nadir
                if orbitType == 3:
                    nadirCounter += 1
                    irDayside = NADIR_KEYS[nadirCounter]
                elif orbitType == 4:
                    print("Error: orbit type 4 cannot have LNO dayside")
                    irDayside=""
                elif orbitType == 14:
                    print("Error: orbit type 14 cannot have LNO dayside")
                    irDayside=""
    
            elif genericObsTypes["irDayside"] == "": #LNO off
                if orbitType == 3:
                    irDayside=""
                elif orbitType == 4:
                    irDayside=""
                elif orbitType == 14:
                    irDayside=""
    
            else: #use preselected targeted obs
                if orbitType == 3:
                    irDayside = genericObsTypes["irDayside"]
                elif orbitType == 4:
                    print("Error: orbit type 4 cannot have LNO dayside")
                    irDayside=""
                elif orbitType == 14:
                    print("Error: orbit type 14 cannot have LNO dayside")
                    irDayside=""
    
    
    
    
    
        if orbitType in [7, 17]: #UVIS and/or LNO nightside
    
            irIngressHigh=""
            irIngressLow=""
            uvisIngress = ""
            irEgressHigh=""
            irEgressLow=""
            uvisEgress = ""

            orbit["allowedObservationTypes"].append("dayside") #nightsides also have daysides
            orbit["allowedObservationTypes"].append("nightside")
    
            if genericObsTypes["irDayside"] in ["irDayside", "irShortDayside", "irLongDayside"]: #dayside nadir
                nadirCounter += 1
                irDayside = NADIR_KEYS[nadirCounter]
                uvisDayside = "uvisDayside"
            elif genericObsTypes["irDayside"] == "": #LNO off
                irDayside = ""
                uvisDayside = "uvisDayside"
            else:
                irDayside = genericObsTypes["irDayside"] #use preselected targeted obs
                uvisDayside = "uvisDayside"
    
    
            if genericObsTypes["irNightside"] == "": #LNO off
                irNightside = ""
                uvisNightside = "uvisOnlyNightside"
                if orbitType == 7:
                    print("Warning: orbit type 7 found with blank nightside nadir")
    
            else: #if LNO nightside or preselected targeted obs
                if orbitType == 7:
                    if genericObsTypes["irNightside"] == "irNightside": #if generic obs
                        nadirNightsideCounter += 1
                        irNightside = NADIR_NIGHTSIDE_KEYS[nadirNightsideCounter]
                        uvisNightside = "uvisNightside"
                    else:
                        irNightside = genericObsTypes["irNightside"] #use preselected targeted obs
                        uvisNightside = "uvisNightside"
    
                else: #if LNO should be off
                    print("Error: orbit type 17 cannot have LNO nightside (orbit %i)" %orbit["orbitNumber"])
                    print(genericObsTypes["irNightside"])
                    irNightside = ""
                    uvisNightside = "uvisOnlyNightside"
    
    
    
        if orbitType in [8, 28]: #LNO and/or UVIS dayside limb
    
            irIngressHigh=""
            irIngressLow=""
            uvisIngress = ""
            irEgressHigh=""
            irEgressLow=""
            uvisEgress = ""

            orbit["allowedObservationTypes"].append("dayside")
    
            if genericObsTypes["irDayside"] == "": #LNO off
                irDayside = ""
                print("Warning: orbit type 8 found with blank limb observation")
    
                if orbitType == 8:
                    uvisDayside = "uvisDayside"
                else:
                    uvisDayside = "uvisOnlyLimb"
    
            elif genericObsTypes["irDayside"] == "irLimb": #LNO off
                nadirLimbCounter += 1
                irDayside = NADIR_LIMB_KEYS[nadirLimbCounter]
    
                if orbitType == 8:
                    uvisDayside = "uvisDayside"
                else:
                    uvisDayside = "uvisLimb"
    
            else: #use LNO limb preselected targeted obs
                irDayside = genericObsTypes["irDayside"]
                print("Warning: check that observation %s is suitable for an LNO limb measurement" %irDayside)
    
                if orbitType == 8:
                    uvisDayside = "uvisDayside"
                else:
                    uvisDayside = "uvisLimb"
                
            irNightside = ""
            uvisNightside = ""
    
            
        orbit["completeOrbitPlan"] = \
            {
            "orbitType":orbitType,
            "irIngressHigh":irIngressHigh,
            "irIngressLow":irIngressLow,
            "irEgressHigh":irEgressHigh,
            "irEgressLow":irEgressLow,
            "irDayside":irDayside,
            "irNightside":irNightside,
            
            "uvisIngress":uvisIngress,
            "uvisEgress":uvisEgress,
            "uvisDayside":uvisDayside,
            "uvisNightside":uvisNightside,
            
            "comment":genericObsTypes["comment"],
            }
    return orbit_list



def addCorrectNadirObservations(orbit_list):
    """add some final tweaks to ensure dayside/limb/nightside observations are correct e.g. include uvis 3 x TC20s, etc"""

    for orbit in orbit_list:    
        finalOrbitPlan = orbit["finalOrbitPlan"]
        
        #first, find all allowed occultation measurement types for orbit
        irMeasuredObsTypes = [occultationType for occultationType in orbit["allowedObservationTypes"][:] if occultationType in ["ingress", "egress", "merged", "grazing"]]
        uvisMeasuredObsTypes = [occultationType for occultationType in orbit["allowedObservationTypes"][:] if occultationType in ["ingress", "egress", "merged", "grazing"]]
        #add nadir types
        if finalOrbitPlan["irDayside"] != "": #limb is simply a dayside
            irMeasuredObsTypes.append("dayside")
        if finalOrbitPlan["irNightside"] != "":
            irMeasuredObsTypes.append("nightside")
        if finalOrbitPlan["uvisDayside"] != "":
            uvisMeasuredObsTypes.append("dayside")

            #some orbit types have 3 x uvis nadirs
            if finalOrbitPlan["orbitType"] in UVIS_MULTIPLE_TC_NADIR_ORBIT_TYPES:
                uvisMeasuredObsTypes.append("dayside2")
                uvisMeasuredObsTypes.append("dayside3")

        if finalOrbitPlan["uvisNightside"] != "":
            uvisMeasuredObsTypes.append("nightside")

        orbit["irMeasuredObsTypes"] = irMeasuredObsTypes
        orbit["uvisMeasuredObsTypes"] = uvisMeasuredObsTypes

    return orbit_list




"""function to read in cop tables, given channel and name"""
def outputCopTable(copVersion,channel,cop):
    if channel=="so" or channel=="lno":
        csvFilename=COP_TABLE_DIRECTORY+os.sep+"%s" %copVersion+os.sep+"%s_%s_table.csv" %(channel,cop)
    elif channel=="uvis":
        csvFilename=COP_TABLE_DIRECTORY+os.sep+"%s" %copVersion+os.sep+"uvis_table.csv"
    with open(csvFilename) as f:
        copList=[]
        for index,line in enumerate(f):
            content = line.strip('\n').split(',')
            if index==0: #if first line
                copHeaders=content #record header data
                copHeaders.append("comments")
            else:
                if content[len(content)-1].find('#') != -1: #if comment line
                    temp=content[len(content)-1].split('#') #split last field into value and comment
                    content[len(content)-1]=temp[0].strip() #replace last column with value only
                    content.append(temp[1].strip()) #add new column on end for the comment
                else:
                    content.append("NONE")
                copList.append(content)
    return copHeaders,copList




def findIndex(valueIn,listIn):
    
    if valueIn in listIn:
        indexOut = [index for index,value in enumerate(listIn) if value == valueIn]
        if len(indexOut) > 1:
            print("Error: Multiple values found")
        else:
            return indexOut[0]
    else:
        print("Error: Not found")
    

def getCopTables(mtpConstants):
    """read in COP tables from file"""
    copVersion = mtpConstants["copVersion"]


    soAotfHeaders,soAotfList = outputCopTable(copVersion,"so",'aotf')
    soFixedHeaders,soFixedList = outputCopTable(copVersion,"so",'fixed')
    soScienceHeaders,soScienceList = outputCopTable(copVersion,"so",'science')
    soSteppingHeaders,soSteppingList = outputCopTable(copVersion,"so",'stepping')
    soSubdomainHeaders,soSubdomainList = outputCopTable(copVersion,"so",'sub_domain')
    
    lnoAotfHeaders,lnoAotfList = outputCopTable(copVersion,"lno",'aotf')
    lnoFixedHeaders,lnoFixedList = outputCopTable(copVersion,"lno",'fixed')
    lnoScienceHeaders,lnoScienceList = outputCopTable(copVersion,"lno",'science')
    lnoSteppingHeaders,lnoSteppingList = outputCopTable(copVersion,"lno",'stepping')
    lnoSubdomainHeaders,lnoSubdomainList = outputCopTable(copVersion,"lno",'sub_domain')
    
    uvisHeaders,uvisList = outputCopTable(copVersion,"uvis","")
        
    copTableDict = {
            "soAotfHeaders":soAotfHeaders, "soAotfList":soAotfList, \
            "soFixedHeaders":soFixedHeaders, "soFixedList":soFixedList, \
            "soScienceHeaders":soScienceHeaders, "soScienceList":soScienceList, \
            "soSteppingHeaders":soSteppingHeaders, "soSteppingList":soSteppingList, \
            "soSubdomainHeaders":soSubdomainHeaders, "soSubdomainList":soSubdomainList, \
            "lnoAotfHeaders":lnoAotfHeaders, "lnoAotfList":lnoAotfList, \
            "lnoFixedHeaders":lnoFixedHeaders, "lnoFixedList":lnoFixedList, \
            "lnoScienceHeaders":lnoScienceHeaders, "lnoScienceList":lnoScienceList,  \
            "lnoSteppingHeaders":lnoSteppingHeaders, "lnoSteppingList":lnoSteppingList, \
            "lnoSubdomainHeaders":lnoSubdomainHeaders, "lnoSubdomainList":lnoSubdomainList, \
            "uvisHeaders":uvisHeaders, "uvisList":uvisList, \
            }

    return copTableDict


def makeCopTableDict(channelCode, copTableDict, silent=True):

    subdomainList = {0:copTableDict["soSubdomainList"], 1:copTableDict["lnoSubdomainList"]}[channelCode]
    scienceList = {0:copTableDict["soScienceList"], 1:copTableDict["lnoScienceList"]}[channelCode]
    aotfList = {0:copTableDict["soAotfList"], 1:copTableDict["lnoAotfList"]}[channelCode]
    
    #degf	dvaf	sbsf	aotfPointer	steppingPointer	accumulationCount	binningFactor	integrationTime
    
    subdomainIndices = []
    aotfOrdersAll = []
    integrationTimesAll = []
    windowHeightAll = []
    rhythmAll = []
    
#    subdomainRow = subdomainList[1000]
    for rowIndex, subdomainRow in enumerate(subdomainList):
        nSubdomains = 6 - subdomainRow.count("0")
        
        steppingIndices = []
        accumulations = []
        binningFactors = []
        integrationTimes = []
        aotfOrders = []
        
        errorFound = False
        calibration = False

        if nSubdomains == 0:
            calibration = True       
        
        for index in range(nSubdomains):
            scienceIndex = int(subdomainRow[index])
            scienceRow = scienceList[scienceIndex]
        
            steppingIndex = int(scienceRow[4])
            steppingIndices.append(steppingIndex)
            
            accumulation = int(scienceRow[5])
            accumulations.append(accumulation)
        
            binningFactor = int(scienceRow[6])
            binningFactors.append(binningFactor)
        
            integrationTime = int(scienceRow[7]) / 1000.0
            integrationTimes.append(integrationTime)
        
            aotfIndex = int(scienceRow[3])
            aotfRow = aotfList[aotfIndex]
            if "ORDER_" in aotfRow[2]:
                aotfOrder = int(aotfRow[2].replace("ORDER_",""))
            elif aotfIndex == 0:
                aotfOrder = 0
    
            if steppingIndices[0] > 0:
                calibration = True
        
            aotfOrders.append(aotfOrder)
        
        aotfOrdersSorted = sorted(aotfOrders)
                
            
        if len(set(binningFactors)) == 1: #if more than one binning factor in the observation
            binningFactorSingle = binningFactors[0]
            windowHeightTotal = 24.0 / nSubdomains * (binningFactorSingle + 1)
            if np.round(windowHeightTotal) == windowHeightTotal:
                windowHeightTotal = int(windowHeightTotal)
            else:
                print("Binning rounding error row %i" %rowIndex)
        else:
            if not silent: print("Binning error row %i" %rowIndex)
            if not silent: print(binningFactors)
            errorFound = True
        
        
        if len(set(accumulations)) == 1: #if n accumulations is the same for all observations
            accumulationSingle = accumulations[0]
        else:
            if not silent: print("Accumulation error row %i" %rowIndex)
            if not silent: print(accumulations)
            errorFound = True
        
        
        if len(set(integrationTimes)) == 1: #if more than one integration time in the observation
            integrationTimeSingle = integrationTimes[0]
        else:
            if not silent: print("Int time error row %i" %rowIndex)
            if not silent: print(integrationTimes)
            errorFound = True
        
            
        if nSubdomains > 1: 
            if sum(steppingIndices[1:6]) > 0:
                if not silent: print("Stpping error row %i" %rowIndex)
                errorFound = True
        
        if not calibration:
            executionTime = calcExecutionTime(accumulationSingle, windowHeightTotal, integrationTimeSingle)
            executionTimeTotal = executionTime * nSubdomains
        
            if 650.0 < executionTimeTotal < 1000.0:
                rhythm = 1
            elif 1700.0 < executionTimeTotal < 2000.0:
                rhythm = 2
            elif 3400.0 < executionTimeTotal < 4000.0:
                rhythm = 4
            elif 7000.0 < executionTimeTotal < 8000.0:
                rhythm = 8
            elif 14000.0 < executionTimeTotal < 15000.0:
                rhythm = 15
            else:
                if not silent: print("Exec time error row %i" %rowIndex)
                errorFound = True
        
        if not errorFound and not calibration:
            subdomainIndices.append(rowIndex)
            aotfOrdersAll.append(aotfOrdersSorted)
            integrationTimesAll.append(integrationTimeSingle)
            windowHeightAll.append(windowHeightTotal)
            rhythmAll.append(rhythm)
            
    copTableCombinations = {"index":subdomainIndices, "orders":aotfOrdersAll, "integrationTime":integrationTimesAll, "rhythm":rhythmAll, "windowHeight":windowHeightAll}
    return copTableCombinations




    

def findCopRowData(channel, copTableDict, columnNames, row, table=""):
#    channel="so"
#    columnName = "science_3"
#    row=1000
    

    
    if isinstance(row, list):
        if len(row)==1:
            row = int(row[0])
        else:
            print("Error: row number is a list")

    if channel in ["so","lno"]:
        aotfHeaders = {"so":copTableDict["soAotfHeaders"], "lno":copTableDict["lnoAotfHeaders"]}[channel]
        aotfList = {"so":copTableDict["soAotfList"], "lno":copTableDict["lnoAotfList"]}[channel]
        fixedHeaders = {"so":copTableDict["soFixedHeaders"], "lno":copTableDict["lnoFixedHeaders"]}[channel]
        fixedList = {"so":copTableDict["soFixedList"], "lno":copTableDict["lnoFixedList"]}[channel]
        scienceHeaders = {"so":copTableDict["soScienceHeaders"], "lno":copTableDict["lnoScienceHeaders"]}[channel]
        scienceList = {"so":copTableDict["soScienceList"], "lno":copTableDict["lnoScienceList"]}[channel]
        steppingHeaders = {"so":copTableDict["soSteppingHeaders"], "lno":copTableDict["lnoSteppingHeaders"]}[channel]
        steppingList = {"so":copTableDict["soSteppingList"], "lno":copTableDict["lnoSteppingList"]}[channel]
        subdomainHeaders = {"so":copTableDict["soSubdomainHeaders"], "lno":copTableDict["lnoSubdomainHeaders"]}[channel]
        subdomainList = {"so":copTableDict["soSubdomainList"], "lno":copTableDict["lnoSubdomainList"]}[channel]
    
    if table != "": #not used
        if table=="aotf":
            copTable = aotfList
            copTableHeader = aotfHeaders
        elif table=="fixed":
            copTable = fixedList
            copTableHeader = fixedHeaders
        elif table=="science":
            copTable = scienceList
            copTableHeader = scienceHeaders
        elif table=="stepping":
            copTable = steppingList
            copTableHeader = steppingHeaders
        elif table=="subdomain":
            copTable = subdomainList
            copTableHeader = subdomainHeaders
        else:
            print("Error: table unknown")

        valuesOut = []
        for columnName in columnNames:
            columnIndex = findIndex(columnName,copTableHeader)
            valuesOut.append(copTable[int(row)][columnIndex])
            
        if len(valuesOut)==1:
            valuesOut = valuesOut[0]
        return valuesOut
    
    else:
        if channel in ["so","lno"]:
            headers = [aotfHeaders,fixedHeaders,scienceHeaders,steppingHeaders,subdomainHeaders]
            lists = [aotfList,fixedList,scienceList,steppingList,subdomainList]
        elif channel == "uvis":
            headers = [copTableDict["uvisHeaders"]]
            lists = [copTableDict["uvisList"]]
        
        valuesOut = []
        for columnName in columnNames:
            value = []
            for headerIndex,header in enumerate(headers):
                if columnName in header:
                    columnIndex = findIndex(columnName,header)
    #                print(headerIndex)
    #                print(columnIndex)
                    value.append(lists[headerIndex][int(row)][columnIndex])
                    
            if len(value) == 1:
                valuesOut.append(value[0])
            else:
                print("Error finding COP row")
                    
        if len(valuesOut)==1:
            valuesOut = valuesOut[0]
        return valuesOut



"""find matching cop rows"""
def findCopRows(channel,copTableDict, orders,integrationTime,nRows,silent=False): #IntTime in ms!!
    
    subdomainList = {"so":copTableDict["soSubdomainList"], "lno":copTableDict["lnoSubdomainList"]}[channel]
    
    otherRows = []
    found=False
    for rowIndex,subdomainRow in enumerate(subdomainList):
        subdomainComment = subdomainRow[6]
        nFound = 0
        nSubdomains = 6 - subdomainRow.count("0")
        for order in orders:
            if subdomainComment.find(" %s " %str(order)) > -1:
                nFound += 1
    
            if nFound == len(orders) and nSubdomains == len(orders):
                found=True
                if subdomainComment.find("=%sMS" %str(integrationTime)) > -1:
                    
                    if subdomainComment.find("NROWS=%s" %str(nRows)) > -1:
                        if not silent: print("Matching row found: %i" %rowIndex)
                        if not silent: print(subdomainRow)
                        return rowIndex
                    else:
                         otherRows.append(subdomainRow)
                else:
                     otherRows.append(subdomainRow)
    
    if found:
        print("Orders found but integration time and/or number of rows not. Possible options are:")
        for otherRow in otherRows:
            print(otherRow)
        return -1 #wrong integration time
    else:
        print("Orders not found")
        print(orders)
        return -2 #order combination not found




"""find matching cop rows"""
def findFixedCopRow(channel,copTableDict, centreRow,nRows,rhythm,silent=False): #IntTime in ms!!
    
    fixedList = {"so":copTableDict["soFixedList"], "lno":copTableDict["lnoFixedList"]}[channel]
    
    foundRows = []
    found=False
    for rowIndex,fixedRow in enumerate(fixedList):
        nFound = 0
        fixedHeight = int(fixedRow[0]) + 1
        fixedTop = int(fixedRow[1])
        fixedRhythm = int(fixedRow[6])
        
        if fixedHeight == nRows and fixedTop == centreRow - nRows/2 and fixedRhythm == rhythm:
            if not silent: print("Matching fixed row found: %i" %rowIndex)
            if not silent: print(fixedRow)
            found=True
            nFound += 1
            foundRows.append(rowIndex)
                
    if found and len(foundRows)==1:
        return foundRows[0] #return the correct row
    elif found:
        if foundRows[0] == 0 and foundRows[1] == 9: #fudge to stop error when default values (at top of fixed cop table) are copies of other rows
            return foundRows[0] #return the first matching row
        elif foundRows[0] == 1 and foundRows[1] == 72: #fudge to stop error when default values (at top of fixed cop table) are copies of other rows
            return foundRows[0] #return the first matching row
        elif foundRows[0] == 2 and foundRows[1] == 81: #fudge to stop error when default values (at top of fixed cop table) are copies of other rows
            return foundRows[0] #return the first matching row

        elif foundRows[0] == 0 and foundRows[1] == 21: #fudge to stop error when default values (at top of fixed cop table) are copies of other rows
            return foundRows[0] #return the first matching row
        elif foundRows[0] == 1 and foundRows[1] == 11: #fudge to stop error when default values (at top of fixed cop table) are copies of other rows
            return foundRows[0] #return the first matching row
        elif foundRows[0] == 2 and foundRows[1] == 80: #fudge to stop error when default values (at top of fixed cop table) are copies of other rows
            return foundRows[0] #return the first matching row

        else:
            print("Warning: Multiple matching fixed rows found:")
            for row in foundRows:
                print(row)
                print(fixedList[row][7])
            return foundRows[0] #
    else:
        print("Error: Fixed row not found")
        return -999



"""output text description of measurement given input rows"""
def getObservationDescription(channel, copTableDict, fixedRow, copRow, silent=False):
    if copRow == -1:
        return "%s off" %channel.upper()
    
    
    if channel in ["so","lno"]:

        fixedRhythm = findCopRowData(channel,copTableDict, ["rythm"],fixedRow)
        fixedTop = findCopRowData(channel,copTableDict, ["windowLeftTop"],fixedRow)
        fixedHeight = findCopRowData(channel,copTableDict, ["windowLineCount"],fixedRow)
        
        sciencePointers = findCopRowData(channel,copTableDict, ["science_1","science_2","science_3","science_4","science_5","science_6"],copRow)
            
        nSubdomains = 6 - sciencePointers.count("0")
        if not silent: print(nSubdomains)
        
        if nSubdomains == 1: #check for stepping
            sciencePointer = sciencePointers[0]
            steppingPointer = findCopRowData(channel,copTableDict, ["steppingPointer"],sciencePointer)
            if steppingPointer != "0":
                steppingType,steppingSpeed,steppingCount,steppingValue = findCopRowData(channel,copTableDict, ["steppingParameter","stepSpeed","stepCount","stepValue"],steppingPointer)
                aotfOrder = findCopRowData(channel,copTableDict, ["aotfPointer"],sciencePointer)
                aotfFrequency = findCopRowData(channel,copTableDict, ["frequency"],aotfOrder)
                integrationTime = np.int(findCopRowData(channel,copTableDict, ["integrationTime"],sciencePointer)) / 1000
                if steppingType=="AOTF_IX":
                    observationText = "Diffraction order stepping (fullscan): %i orders from %i to %i in steps of %s (%s order(s) per %s second(s))" %(int(steppingCount),int(aotfOrder),int(aotfOrder)+int(steppingCount),int(steppingValue),int(steppingSpeed)+1,int(fixedRhythm))
                elif steppingType=="WINDOW_TOP":
                    observationText = "Detector window stepping: %i step(s) covering detector lines %i to %i (%s step(s) per %s second(s))" %(int(steppingCount),int(fixedTop),int(fixedTop)+int(steppingCount)*int(steppingValue),int(steppingSpeed)+1,int(fixedRhythm))
                elif steppingType=="INTEGRATION_TIME":
                    observationText = "Detector integration time stepping: %i integration times from %i to %ims in steps of %ims for detector lines %i to %i (%s step(s) per %s second(s))" %(int(steppingCount),int(integrationTime),int(integrationTime)*int(steppingCount)*int(steppingValue),int(steppingValue),int(fixedTop),int(fixedTop)+int(fixedHeight)+1,int(steppingSpeed)+1,int(fixedRhythm))
                elif steppingType=="AOTF_FREQ":
                    observationText = "AOTF frequency stepping (miniscan): %i frequencies from %i to %ikHz in steps of %ikHz (%s step(s) per %s second(s))" %(int(steppingCount),int(aotfFrequency)/1000,int(aotfFrequency)/1000+int(steppingCount)*np.round(int(steppingValue)*8e4/2**32),np.round(int(steppingValue)*8e4/2**32),int(steppingSpeed)+1,int(fixedRhythm))
        elif nSubdomains == 0:
            print("Error: no subdomains")
            stop()
        else:
            observationText = "Science: orders " 
            integrationTimes = []
            for sciencePointer in sciencePointers[0:nSubdomains]:
                aotfOrder = findCopRowData(channel,copTableDict, ["aotfPointer"],sciencePointer)
                integrationTimes.append(findCopRowData(channel,copTableDict, ["integrationTime"],sciencePointer))
                observationText += "#%s, " %([int(aotfOrder) if aotfOrder != "0" else "dark"][0])
            if integrationTimes.count(integrationTimes[0]) == len(integrationTimes):
                observationText += "with %ius integration time " %int(integrationTimes[0])
            else:
                observationText += "with variable integration times "
            observationText += "(%i orders per %i second(s) for detector lines %i to %i)" %(nSubdomains,int(fixedRhythm),int(fixedTop),int(fixedTop)+int(fixedHeight)+1)
        if not silent: print(observationText)

    elif channel == "uvis":
       num_acqs, flag_register, binning_size, comments = findCopRowData(channel,copTableDict, ["num_acqs", "flag_register", "binning_size", "comments"],copRow)
#       observationText = "%s -NumAcqsBetweenDarks=%s -FlagRegister=%s -BinningSize=%s" %(comments, num_acqs, flag_register, binning_size)
       observationText = "%s, Binning=%s" %(comments.replace(" - ",",").replace(" -","," ).replace("-",", "), binning_size)
    
    return observationText





def getObsParameters(observation_name, dictionary):
    if observation_name in list(dictionary.keys()):
        orders_out, inttime_out, rhythm_out, rows_out, channel_code = dictionary[observation_name]
        return sorted(orders_out), inttime_out, rhythm_out, rows_out, channel_code
    else:
        return [-999], -1, -1, -1, -1
#        print("Observation name %s not found in dictionary for orbit number %i" %(observation_name, orbitNumber))
        
        

def calcExecutionTime(number_accumulations, window_height, integration_time): #real number of rows (16, 20, 24), int time in milliseconds
    return ((number_accumulations+1.0) * ((integration_time * 1000.0) + 71.0 + 320.0 * window_height + 1000.0) + 337.0) / 1000.0


def uniqueDiffractionOrders(aotf_order_list):
    tuples = [tuple(i) for i in aotf_order_list]
    uniqueTuples = set(tuples)
    unique_orders = [list(i) for i in uniqueTuples]
    return unique_orders



"""return dictionary containing COP rows and description of measurement given input dictionary containing observation parameters"""
def getCopRows(observationName, observationDict, copTableDict, copTableCombinationDict, centreDetectorLines, silent=False):

    diffractionOrders, integrationTime, rhythm, windowHeight, channelCode = getObsParameters(observationName, observationDict)
    if diffractionOrders[0] == -999:
        print("Observation name %s not found in dictionary" %(observationName))


    detectorCentreLine = centreDetectorLines[channelCode]
    copTableCombinations = copTableCombinationDict[channelCode]

    if channelCode in [0,1]:
        channel = {0:"so", 1:"lno"}[channelCode]
    else:
        print("Error: channel %i not defined" %channelCode)


    """do fixed table first"""
    fixedCopRow = findFixedCopRow(channel, copTableDict, detectorCentreLine, windowHeight, rhythm, silent=silent)
    if fixedCopRow == -999:
        print("Error: incorrect fixed row")
        stop()
                
    
    
    """then do subdomain table"""
    scienceCopRow = -999
    
    if type(diffractionOrders[0]) != int:
        if "COP#" in diffractionOrders[0]:
            scienceCopRow = int(diffractionOrders[0].split("#")[1])
            print("Manual mode: COP row %i" %(scienceCopRow))
        else:
            print("Error: COP rows must be integers or must be specified manually e.g. COP#1")
            stop()
    else:
        #look in cop tables for correct subdomain rows
        for indexCop, diffractionOrdersCop, integrationTimeCop, rhythmCop, windowHeightCop in zip(copTableCombinations["index"], copTableCombinations["orders"], copTableCombinations["integrationTime"], copTableCombinations["rhythm"], copTableCombinations["windowHeight"]):
            if diffractionOrders == diffractionOrdersCop:
                if integrationTime == integrationTimeCop:
                    if rhythm == rhythmCop:
                        if windowHeight == windowHeightCop:
                            scienceCopRow = indexCop
                
    
    if scienceCopRow < 0:
        print("Error: COP row 1 not found")
        print(diffractionOrders)
        stop()
    
    #find description of observation
    description = getObservationDescription(channel, copTableDict, fixedCopRow, scienceCopRow, silent=True)
    outputDict = {"scienceCopRow":scienceCopRow, "fixedCopRow":fixedCopRow, "copRowDescription":description}
    
    return outputDict, diffractionOrders, integrationTime, rhythm, windowHeight, channelCode





        




def addIrCopRows(orbit_list, copTableDict, mtpConstants):
    """find cop rows that match observation names in final plan, add to orbit list"""
    centreDetectorLines = {
            0:mtpConstants["soCentreDetectorLine"], \
            1:LNO_CENTRE_DETECTOR_LINE #for lno occultations only
            }
    
    copTableCombinationDict = {
            0:makeCopTableDict(0, copTableDict), \
            1:makeCopTableDict(1, copTableDict)
            }
        
    
    for orbit in orbit_list:
        print(orbit["orbitNumber"])
        finalOrbitPlan = orbit["finalOrbitPlan"]
        irMeasuredObsTypes = orbit["irMeasuredObsTypes"]
        uvisMeasuredObsTypes = orbit["uvisMeasuredObsTypes"]


        #now check each allowed type and add cop rows
        if "ingress" in irMeasuredObsTypes or "merged" in irMeasuredObsTypes or "grazing" in irMeasuredObsTypes:
            for obsType in ["irIngressHigh","irIngressLow"]:
                
                
                observationName = finalOrbitPlan[obsType]
                observationDict = occultationObservationDict
                
                outputDict, diffractionOrders, integrationTime, rhythm, windowHeight, channelCode = getCopRows(observationName, observationDict, copTableDict, copTableCombinationDict, centreDetectorLines, silent=False)
                    
                finalOrbitPlan[obsType+"ObservationName"] = observationName
                finalOrbitPlan[obsType+"Orders"] = diffractionOrders
                finalOrbitPlan[obsType+"IntegrationTime"] = integrationTime
                finalOrbitPlan[obsType+"Rhythm"] = rhythm
                finalOrbitPlan[obsType+"DetectorRows"] = windowHeight
                finalOrbitPlan[obsType+"ChannelCode"] = channelCode
                finalOrbitPlan[obsType+"CopRows"] = outputDict


        if "egress" in irMeasuredObsTypes:
            for obsType in ["irEgressHigh","irEgressLow"]:

                observationName = finalOrbitPlan[obsType]
                observationDict = occultationObservationDict
                
                outputDict, diffractionOrders, integrationTime, rhythm, windowHeight, channelCode = getCopRows(observationName, observationDict, copTableDict, copTableCombinationDict, centreDetectorLines, silent=False)
                    
                finalOrbitPlan[obsType+"ObservationName"] = observationName
                finalOrbitPlan[obsType+"Orders"] = diffractionOrders
                finalOrbitPlan[obsType+"IntegrationTime"] = integrationTime
                finalOrbitPlan[obsType+"Rhythm"] = rhythm
                finalOrbitPlan[obsType+"DetectorRows"] = windowHeight
                finalOrbitPlan[obsType+"ChannelCode"] = channelCode
                finalOrbitPlan[obsType+"CopRows"] = outputDict

        if "dayside" in irMeasuredObsTypes:
            obsType  = "irDayside"
            
            observationName = finalOrbitPlan[obsType]
            observationDict = nadirObservationDict
            
            outputDict, diffractionOrders, integrationTime, rhythm, windowHeight, channelCode = getCopRows(observationName, observationDict, copTableDict, copTableCombinationDict, centreDetectorLines, silent=False)
                
            finalOrbitPlan[obsType+"ObservationName"] = observationName
            finalOrbitPlan[obsType+"Orders"] = diffractionOrders
            finalOrbitPlan[obsType+"IntegrationTime"] = integrationTime
            finalOrbitPlan[obsType+"Rhythm"] = rhythm
            finalOrbitPlan[obsType+"DetectorRows"] = windowHeight
            finalOrbitPlan[obsType+"ChannelCode"] = channelCode
            finalOrbitPlan[obsType+"CopRows"] = outputDict
            
        else: #if uvis operating, still write COP rows for nadirs
            if "dayside" in uvisMeasuredObsTypes: #if uvis operating, still write COP rows for nadirs
                obsType  = "irDayside"
                finalOrbitPlan[obsType+"CopRows"] = {"scienceCopRow":-1, "fixedCopRow":-1, "copRowDescription":""}
            if "dayside2" in uvisMeasuredObsTypes: #if uvis operating, still write COP rows for nadirs
                obsType  = "irDayside2"
                finalOrbitPlan[obsType+"CopRows"] = {"scienceCopRow":-1, "fixedCopRow":-1, "copRowDescription":""}
            if "dayside3" in uvisMeasuredObsTypes: #if uvis operating, still write COP rows for nadirs
                obsType  = "irDayside3"
                finalOrbitPlan[obsType+"CopRows"] = {"scienceCopRow":-1, "fixedCopRow":-1, "copRowDescription":""}
                
                
        #if orbit type not 12 (NOMAD OFF) then there should always be nadir COP rows specified
        if orbit["orbitType"] != 12 and "dayside" not in uvisMeasuredObsTypes:
            obsType  = "irDayside"
            finalOrbitPlan[obsType+"CopRows"] = {"scienceCopRow":-1, "fixedCopRow":-1, "copRowDescription":""}
            
        

        if "nightside" in irMeasuredObsTypes:
            obsType  = "irNightside"
            
            observationName = finalOrbitPlan[obsType]
            observationDict = nadirObservationDict
            
            outputDict, diffractionOrders, integrationTime, rhythm, windowHeight, channelCode = getCopRows(observationName, observationDict, copTableDict, copTableCombinationDict, centreDetectorLines, silent=False)
                
            finalOrbitPlan[obsType+"ObservationName"] = observationName
            finalOrbitPlan[obsType+"Orders"] = diffractionOrders
            finalOrbitPlan[obsType+"IntegrationTime"] = integrationTime
            finalOrbitPlan[obsType+"Rhythm"] = rhythm
            finalOrbitPlan[obsType+"DetectorRows"] = windowHeight
            finalOrbitPlan[obsType+"ChannelCode"] = channelCode
            finalOrbitPlan[obsType+"CopRows"] = outputDict
        else: #if uvis operating, still write COP rows for nadirs
            if "nightside" in uvisMeasuredObsTypes: #if uvis operating, still write COP rows for nadirs
                obsType  = "uvisNightside"
                finalOrbitPlan[obsType+"CopRows"] = {"scienceCopRow":-1, "copRowDescription":""}
                
                
        
            
        #for UVIS, add -1s to be replaced with real values later
        if "ingress" in uvisMeasuredObsTypes or "merged" in uvisMeasuredObsTypes or "grazing" in uvisMeasuredObsTypes:
            obsType = "uvisIngress"
            observationName = finalOrbitPlan[obsType]
            finalOrbitPlan[obsType+"ObservationName"] = observationName
            finalOrbitPlan[obsType+"CopRows"] = {"scienceCopRow":-1, "copRowDescription":""}

        if "egress" in uvisMeasuredObsTypes:
            obsType = "uvisEgress"
            observationName = finalOrbitPlan[obsType]
            finalOrbitPlan[obsType+"ObservationName"] = observationName
            finalOrbitPlan[obsType+"CopRows"] = {"scienceCopRow":-1, "copRowDescription":""}

        if "dayside" in uvisMeasuredObsTypes:
            obsType = "uvisDayside"
            observationName = finalOrbitPlan[obsType]
            finalOrbitPlan[obsType+"ObservationName"] = observationName
            finalOrbitPlan[obsType+"CopRows"] = {"scienceCopRow":-1, "copRowDescription":""}

        if "dayside2" in uvisMeasuredObsTypes:
            obsType = "uvisDayside2"
            observationName = finalOrbitPlan["uvisDayside"] #use same uvis dayside obs name for 3 x TC20s
            finalOrbitPlan[obsType+"ObservationName"] = observationName
            finalOrbitPlan[obsType+"CopRows"] = {"scienceCopRow":-1, "copRowDescription":""}

        if "dayside3" in uvisMeasuredObsTypes:
            obsType = "uvisDayside3"
            observationName = finalOrbitPlan["uvisDayside"] #use same uvis dayside obs name for 3 x TC20s
            finalOrbitPlan[obsType+"ObservationName"] = observationName
            finalOrbitPlan[obsType+"CopRows"] = {"scienceCopRow":-1, "copRowDescription":""}

        if "nightside" in uvisMeasuredObsTypes:
            obsType = "uvisNightside"
            observationName = finalOrbitPlan["uvisDayside"] #use same uvis dayside obs name for 3 x TC20s
            finalOrbitPlan[obsType+"ObservationName"] = observationName
            finalOrbitPlan[obsType+"CopRows"] = {"scienceCopRow":-1, "copRowDescription":""}

        #if orbit type not 12 (NOMAD OFF) then there should always be nadir COP rows specified
        if orbit["orbitType"] != 12 and "dayside" not in uvisMeasuredObsTypes:
            obsType  = "uvisDayside"
            finalOrbitPlan[obsType+"CopRows"] = {"scienceCopRow":-1, "copRowDescription":""}

    return orbit_list




def addUvisCopRows(orbit_list, copTableDict, mtpConstants, paths):
    """get UVIS COP rows from file (if they already exist)"""
    mtpNumber = mtpConstants["mtpNumber"]

    uvisFilesAvailable = os.path.isfile(os.path.join(paths["COP_ROW_PATH"], "mtp%03d_uvis_dayside_nadir.txt" %mtpNumber))
    uvisGrazingAvailable = os.path.isfile(os.path.join(paths["COP_ROW_PATH"], "mtp%03d_uvis_grazing_occultations.txt" %mtpNumber)) #grazing file only present if there are grazing occultations
    
    if uvisFilesAvailable:
        if uvisGrazingAvailable:
            uvisInputDict = {"uvis_dayside_nadir":[], \
                             "uvis_egress_occultations":[], "uvis_grazing_occultations":[], \
                             "uvis_ingress_occultations":[], "uvis_nightside_nadir":[]}
        else:
            uvisInputDict = {"uvis_dayside_nadir":[], \
                             "uvis_egress_occultations":[], \
                             "uvis_ingress_occultations":[], "uvis_nightside_nadir":[]}
        for uvisInputName in uvisInputDict.keys():
            with open(os.path.join(paths["COP_ROW_PATH"], "mtp%03d_%s.txt" %(mtpNumber, uvisInputName))) as f:
                for index, line in enumerate(f):
                    content = line.strip('\n')
                    if index > 0: #if first line
                        uvisInputDict[uvisInputName].append(int(content))

        if not uvisGrazingAvailable: #create empty grazing dictionary
            uvisInputDict["uvis_grazing_occultations"] = []
            
    
        
        daysideCounter = -1
        egressCounter = -1
        grazingCounter = -1
        ingressCounter = -1
        nightsideCounter = -1
        
        #fudge for mtp010, probably because with new kernels an old grazing occultation is now a merged occ
        if mtpNumber == 10:
            orbit_list[227]["allowedObservationTypes"] = ["dayside", "grazing"]
            
            
       
        for orbit in orbit_list:
            finalOrbitPlan = orbit["finalOrbitPlan"]
#            print(orbit["orbitNumber"])
            if "ingress" in orbit["allowedObservationTypes"]:
                ingressCounter += 1
                copRow = uvisInputDict["uvis_ingress_occultations"][ingressCounter]
                finalOrbitPlan["uvisIngressCopRows"]["scienceCopRow"] = copRow
                finalOrbitPlan["uvisIngressCopRows"]["copRowDescription"] = getObservationDescription("uvis", copTableDict, 0, copRow, silent=True)
        
            if "merged" in orbit["allowedObservationTypes"]: #merged is same as ingress
                ingressCounter += 1
                copRow = uvisInputDict["uvis_ingress_occultations"][ingressCounter]
                finalOrbitPlan["uvisIngressCopRows"]["scienceCopRow"] = copRow
                finalOrbitPlan["uvisIngressCopRows"]["copRowDescription"] = getObservationDescription("uvis", copTableDict, 0, copRow, silent=True)
        
            if "grazing" in orbit["allowedObservationTypes"]: #grazing is taken from a different file but added to ingress orbit plan
                grazingCounter += 1
                copRow = uvisInputDict["uvis_grazing_occultations"][grazingCounter]
                finalOrbitPlan["uvisIngressCopRows"]["scienceCopRow"] = copRow
                finalOrbitPlan["uvisIngressCopRows"]["copRowDescription"] = getObservationDescription("uvis", copTableDict, 0, copRow, silent=True)
        
            if "egress" in orbit["allowedObservationTypes"]:
                egressCounter += 1
                copRow = uvisInputDict["uvis_egress_occultations"][egressCounter]
                finalOrbitPlan["uvisEgressCopRows"]["scienceCopRow"] = copRow
                finalOrbitPlan["uvisEgressCopRows"]["copRowDescription"] = getObservationDescription("uvis", copTableDict, 0, copRow, silent=True)
        
            if "dayside" in orbit["allowedObservationTypes"]:
                daysideCounter += 1
                copRow = uvisInputDict["uvis_dayside_nadir"][daysideCounter]
                finalOrbitPlan["uvisDaysideCopRows"]["scienceCopRow"] = copRow
                copRowDescription = getObservationDescription("uvis", copTableDict, 0, copRow, silent=True)
                finalOrbitPlan["uvisDaysideCopRows"]["copRowDescription"] = copRowDescription
            
                #special case: UVIS can have 3 x TC20s in one dayside nadir
                if "dayside2" in orbit["allowedObservationTypes"]:
                    copRows = [copRow]
                    copRowDescriptions = [copRowDescription]
                    
                    daysideCounter += 1
                    copRow = uvisInputDict["uvis_dayside_nadir"][daysideCounter]
                    copRowDescription = getObservationDescription("uvis", copTableDict, 0, copRow, silent=True)
                    copRows.append(copRow)
                    copRowDescriptions.append(copRowDescription)
            
                    daysideCounter += 1
                    copRow = uvisInputDict["uvis_dayside_nadir"][daysideCounter]
                    copRowDescription = getObservationDescription("uvis", copTableDict, 0, copRow, silent=True)
                    copRows.append(copRow)
                    copRowDescriptions.append(copRowDescription)

                    finalOrbitPlan["uvisDaysideCopRows"]["scienceCopRow"] = copRows
                    finalOrbitPlan["uvisDaysideCopRows"]["copRowDescription"] = copRowDescriptions



            if "nightside" in orbit["allowedObservationTypes"]:
                nightsideCounter += 1
                copRow = uvisInputDict["uvis_dayside_nadir"][daysideCounter]
                finalOrbitPlan["uvisNightsideCopRows"]["scienceCopRow"] = copRow
                finalOrbitPlan["uvisNightsideCopRows"]["copRowDescription"] = getObservationDescription("uvis", copTableDict, 0, copRow, silent=True)
                
                
                
        #print stats#
        for name, counter, dictionary in zip(["dayside", "egress", "grazing", "ingress", "nightside"], \
                                             [daysideCounter, egressCounter, grazingCounter, ingressCounter, nightsideCounter], \
                                             [uvisInputDict["uvis_dayside_nadir"], uvisInputDict["uvis_egress_occultations"], uvisInputDict["uvis_grazing_occultations"], uvisInputDict["uvis_ingress_occultations"], uvisInputDict["uvis_nightside_nadir"]]):
            nRowsAdded = counter+1
            nRowsAvailable = len(dictionary)
            nRowsMissing = nRowsAvailable - nRowsAdded
            print("%i %s COP rows added to orbit list, %i were in file. %i have not been accounted for" %(nRowsAdded, name, nRowsAvailable, nRowsMissing))


    return orbit_list


def writeOutputTxt(filepath, lines_to_write):
    """function to write output to a log file"""
    with open(filepath+".txt", 'w') as txtFile:
        for line_to_write in lines_to_write:
            txtFile.write(line_to_write+'\n')

def writeOutputCsv(filepath, lines_to_write):
    """function to write output to a log file"""
    with open(filepath+".csv", 'w') as txtFile:
        for line_to_write in lines_to_write:
            txtFile.write(line_to_write+'\n')


def writeIrCopRowsTxt(orbit_list, mtpConstants, paths):
    """write cop rows to output files"""
    """rememeber: only the allowed ingresses and egresses allocated to NOMAD are written to file. 
                  for nadir, every orbit must be written to file, with -1s written in orbits without observations"""
    mtpNumber = mtpConstants["mtpNumber"]

    outputHeader = "TC20 FIXED,TC20 PRECOOLING,TC20 SCI1,TC20 SCI2,LNO_OBSERVING (1=YES;0=NO),OBSERVATION NUMBER,OBSERVATION TYPE,APPROX TC START TIME,COMMENTS"
    opsOutputDict = {"ir_dayside_nadir":[outputHeader], \
                     "ir_egress_occultations":[outputHeader], "ir_grazing_occultations":[outputHeader], \
                     "ir_ingress_occultations":[outputHeader], "ir_nightside_nadir":[outputHeader]}
    #which file to write cop rows to
    opsOutputNames = {"dayside":"ir_dayside_nadir", \
                      "dayside2":"ir_dayside_nadir", "dayside3":"ir_dayside_nadir", \
                      "egress":"ir_egress_occultations", "grazing":"ir_grazing_occultations", \
                      "ingress":"ir_ingress_occultations", "merged":"ir_ingress_occultations", \
                      "nightside":"ir_nightside_nadir"}

    for orbit in orbit_list:
        finalOrbitPlan = orbit["finalOrbitPlan"] #final version with cop rows and measurements specified
        irMeasuredObsTypes = orbit["irMeasuredObsTypes"][:]
        uvisMeasuredObsTypes = orbit["uvisMeasuredObsTypes"][:]

        #which variable contains cop row info
        lnoObsTypeNames = {"dayside":"irDayside", "nightside":"irNightside"} #matching ir daysides have been made for when UVIS has 3 x TCs per orbit
        for measuredObsType in lnoObsTypeNames.keys(): #loop through potential IR nadir types
            obsType = lnoObsTypeNames[measuredObsType]
            if measuredObsType in irMeasuredObsTypes: #if dayside or nightside is found, write COP rows. LNO cannot run multiple TCs
#                print(orbit["orbitNumber"])
                copRow1 = finalOrbitPlan[obsType+"CopRows"]["scienceCopRow"]
                copRow2 = copRow1 #lno nadir has only 1 science
                precoolingRow = PRECOOLING_COP_ROW
                fixedRow = finalOrbitPlan[obsType+"CopRows"]["fixedCopRow"]
                channelCode = finalOrbitPlan[obsType+"ChannelCode"]
                obsComment = "LNO ON"
                #special case for limb
                if "limb" in finalOrbitPlan["irDayside"].lower():
                    obsTypeOut = "limb"
                else:
                    obsTypeOut = measuredObsType


                outputLineToWrite = "%i,%i,%i,%i,%i,%i,%s,%s,%s" %(fixedRow, precoolingRow, copRow1, copRow2, channelCode, orbit["orbitNumber"], obsTypeOut, orbit[measuredObsType]["utcStart"], obsComment)
                opsOutputDict[opsOutputNames[measuredObsType]].append(outputLineToWrite)

        #special bit - we need to write a line of -1s for each orbit when LNO is not operating, and 3xlines if UVIS in 3xTCs mode
        uvisObsTypeNames = {"dayside":"uvisDayside", "dayside2":"uvisDayside2", "dayside3":"uvisDayside3", "nightside":"uvisNightside"} #matching ir daysides have been made for when UVIS has 3 x TCs per orbit
        for measuredObsType in uvisObsTypeNames.keys(): #loop through potential UVIS nadir types
            obsType = uvisObsTypeNames[measuredObsType]
            #if dayside, dayside2 or dayside3, or nightside is found in uvis list, but not in LNO list, write a line to corresponding LNO COP row file anyway
            if measuredObsType in uvisMeasuredObsTypes and measuredObsType not in irMeasuredObsTypes: 
                copRow1 = OFF_COP_ROW
                copRow2 = OFF_COP_ROW
                precoolingRow = OFF_COP_ROW
                fixedRow = OFF_COP_ROW
                channelCode = OFF_COP_ROW
                obsComment = "LNO OFF"
                obsTypeOut = measuredObsType
                
                if measuredObsType in ["dayside2","dayside3"]: #UVIS 3x TC20s not implemented. Using timings from dayside instead
                    measuredObsTypeOut = "dayside" 
                else:
                    measuredObsTypeOut = measuredObsType #otherwise just use the normal dayside/nightside

                outputLineToWrite = "%i,%i,%i,%i,%i,%i,%s,%s,%s" %(fixedRow, precoolingRow, copRow1, copRow2, channelCode, orbit["orbitNumber"], obsTypeOut, orbit[measuredObsTypeOut]["utcStart"], obsComment)
                opsOutputDict[opsOutputNames[measuredObsType]].append(outputLineToWrite)


        #if both LNO and UVIS off, write a single line anyway (only for dayside)
        measuredObsType = "dayside"
        if measuredObsType not in irMeasuredObsTypes and measuredObsType not in uvisMeasuredObsTypes:
            copRow1 = OFF_COP_ROW
            copRow2 = OFF_COP_ROW
            precoolingRow = OFF_COP_ROW
            fixedRow = OFF_COP_ROW
            channelCode = OFF_COP_ROW
            obsComment = "ALL OFF"
            obsTypeOut = measuredObsType

            outputLineToWrite = "%i,%i,%i,%i,%i,%i,%s,%s,%s" %(fixedRow, precoolingRow, copRow1, copRow2, channelCode, orbit["orbitNumber"], obsTypeOut, orbit[measuredObsType]["utcStart"], obsComment)
            opsOutputDict[opsOutputNames[measuredObsType]].append(outputLineToWrite)


        #find which variable name contains cop row info
        #remember order is reversed for egress
        obsTypeNames = {"ingress":["irIngressHigh","irIngressLow"], "merged":["irIngressHigh","irIngressLow"], "grazing":["irIngressHigh","irIngressLow"], "egress":["irEgressLow","irEgressHigh"]}
        for measuredObsType in obsTypeNames.keys():
            obsType1, obsType2 = obsTypeNames[measuredObsType]
            if measuredObsType in irMeasuredObsTypes:
                copRow1 = finalOrbitPlan[obsType1+"CopRows"]["scienceCopRow"]
                copRow2 = finalOrbitPlan[obsType2+"CopRows"]["scienceCopRow"]
                precoolingRow = PRECOOLING_COP_ROW
                fixedRow = finalOrbitPlan[obsType1+"CopRows"]["fixedCopRow"]
                channelCode = finalOrbitPlan[obsType1+"ChannelCode"]
                if channelCode == SO_CHANNEL_CODE:
                    obsComment = "SO ON"
                elif channelCode == LNO_CHANNEL_CODE:
                    obsComment = "LNO ON"
                obsTypeOut = measuredObsType

                outputLineToWrite = "%i,%i,%i,%i,%i,%i,%s,%s,%s" %(fixedRow, precoolingRow, copRow1, copRow2, channelCode, orbit["orbitNumber"], obsTypeOut, orbit[measuredObsType]["utcStart"], obsComment)
                opsOutputDict[opsOutputNames[measuredObsType]].append(outputLineToWrite)        


    for opsOutputName in opsOutputDict.keys():
        writeOutputTxt(os.path.join(paths["COP_ROW_PATH"], "mtp%03d_%s" %(mtpNumber, opsOutputName)), opsOutputDict[opsOutputName])

    return opsOutputDict







def writeHtmlTable(html_page_name, html_title, html_header, html_rows, paths, linkNameDesc="", extraComments=[]):
    """make html observation file"""
#    global HTML_PATHS

    h = r""
    h += r"<h1>%s</h1>" %html_title +"\n"
    if linkNameDesc != "":
        pagename = linkNameDesc[0]
        desc = linkNameDesc[1]
        h += r"<p><a href=%s>%s</a> - %s</p>" %(pagename, pagename, desc) +"\n"

    for extraComment in extraComments:
        h += r"<p>%s</p>" %(extraComment) +"\n"

    h += r"<div style='white-space:pre;overflow:auto;width:2000px;padding:10px;'>"
    h += r"<table border=1 style='width:2000px;'>"+"\n"

    h += r"<tr>"+"\n"
    for headerColumn in html_header:
        h += r"<th>%s</th>" %headerColumn +"\n"
    h += r"</tr>"+"\n"

    for row in html_rows:
        if row[-1] == "":
            h += r"<tr>"+"\n"
        else:
            h += r"<tr bgcolor='#%s'>" %row[-1]+"\n"

        for element in row[0:-1]:
            h += r"<td>%s</td>" %(element) +"\n"
        h += r"</tr>"+"\n"
    h += r"</table>"+"\n"
    h += r"</div>"

    f = open(os.path.join(paths["HTML_MTP_PATH"], html_page_name+".html"), 'w')
    f.write(h)
    f.close()






def writeNadirWebpage(orbit_list, mtpConstants, paths):
    """write nadir website page"""
    mtpNumber = mtpConstants["mtpNumber"]
    mappsEventFilename = mtpConstants["mappsEventFilename"]

    htmlHeader = ["Orbit Index", "UTC Start Time", "UTC Centre Time", "UTC End Time", "Duration (s)", \
                "Start Longitude", "Centre Longitude", "End Longitude", \
                "Start Latitude", "Centre Latitude", "End Latitude", \
                "Centre Incidence Angle", "Centre Local Time (hrs)", \
                "Orbit Type", "IR Observation Name", "IR Description", "UVIS Description", "Orbit Comment"]
    linesToWrite = ["".join(column+"\t" for column in htmlHeader)]
    
    htmlRows = []
    plotData = {"incidence":[], "et":[]}
    for orbit in orbit_list:
        orbitType = orbit["finalOrbitPlan"]["orbitType"]
        
        #nightside nadir
        nightside = orbit["nightside"]
        #get obs description from file (if it exists)
        if "irNightsideCopRows" in orbit["finalOrbitPlan"].keys():
            irDescription = orbit["finalOrbitPlan"]["irNightsideCopRows"]["copRowDescription"]
        else:
            irDescription = "-"
        if "uvisNightsideCopRows" in orbit["finalOrbitPlan"].keys():
            uvisDescription = "COP row %i: %s" %(orbit["finalOrbitPlan"]["uvisNightsideCopRows"]["scienceCopRow"], orbit["finalOrbitPlan"]["uvisNightsideCopRows"]["copRowDescription"])
        else:
            uvisDescription = "-"
            
        if "irNightsideObservationName" in orbit["finalOrbitPlan"].keys():
            irObservationName = orbit["finalOrbitPlan"]["irNightsideObservationName"]
        else:
            irObservationName = "-"
        comment = "" #no nightside nadir comment
    
        lineToWrite = [orbit["orbitNumber"], nightside["utcStart"], nightside["utcMidpoint"], nightside["utcEnd"], "%0.1f" %nightside["duration"], \
                       "%0.1f" %nightside["lonStart"], "%0.1f" %nightside["lonMidpoint"], "%0.1f" %nightside["lonEnd"], \
                       "%0.1f" %nightside["latStart"], "%0.1f" %nightside["latMidpoint"], "%0.1f" %nightside["latEnd"], \
                       "%0.1f" %nightside["incidenceMidpoint"], "%0.1f" %nightside["lstMidpoint"], \
                       
                       orbitType, irObservationName, irDescription, uvisDescription, comment
                       ]
        linesToWrite.append("".join(str(element)+"\t" for element in lineToWrite))
    
        rowColour = "b2b2b2"
        htmlRow = lineToWrite+[rowColour]
        htmlRows.append(htmlRow)
        





        #dayside nadir
        dayside = orbit["dayside"]
        
        #get obs description from file (if it exists)
        if "irDaysideCopRows" in orbit["finalOrbitPlan"].keys():
            irDescription = orbit["finalOrbitPlan"]["irDaysideCopRows"]["copRowDescription"]
        else:
            irDescription = "-"
        if "uvisDaysideCopRows" in orbit["finalOrbitPlan"].keys():
            
            #special case when UVIS has 3x TC20s in one nadir:
            if isinstance(orbit["finalOrbitPlan"]["uvisDaysideCopRows"]["scienceCopRow"], list):
                #first, check if all COP rows are the same (if so, just write info once)
                if len(set(orbit["finalOrbitPlan"]["uvisDaysideCopRows"]["scienceCopRow"])):
                    uvisDescription = "3x COP rows %i: %s" %(orbit["finalOrbitPlan"]["uvisDaysideCopRows"]["scienceCopRow"][0], orbit["finalOrbitPlan"]["uvisDaysideCopRows"]["copRowDescription"][0])
                else: #loop through COP rows
                    uvisDescription = ""
                    for copRow, copRowDescription in zip(orbit["finalOrbitPlan"]["uvisDaysideCopRows"]["scienceCopRow"], orbit["finalOrbitPlan"]["uvisDaysideCopRows"]["copRowDescription"]):
                        uvisDescription += "COP row %i: %s; " %(copRow, copRowDescription)
            else:
                uvisDescription = "COP row %i: %s" %(orbit["finalOrbitPlan"]["uvisDaysideCopRows"]["scienceCopRow"], orbit["finalOrbitPlan"]["uvisDaysideCopRows"]["copRowDescription"])
        else:
            uvisDescription = "-"
            
        if "irDaysideObservationName" in orbit["finalOrbitPlan"].keys():
            irObservationName = orbit["finalOrbitPlan"]["irDaysideObservationName"]
        else:
            irObservationName = "-"
        comment = orbit["finalOrbitPlan"]["comment"]
    
        lineToWrite = [orbit["orbitNumber"], dayside["utcStart"], dayside["utcMidpoint"], dayside["utcEnd"], "%0.1f" %dayside["duration"], \
                       "%0.1f" %dayside["lonStart"], "%0.1f" %dayside["lonMidpoint"], "%0.1f" %dayside["lonEnd"], \
                       "%0.1f" %dayside["latStart"], "%0.1f" %dayside["latMidpoint"], "%0.1f" %dayside["latEnd"], \
                       "%0.1f" %dayside["incidenceMidpoint"], "%0.1f" %dayside["lstMidpoint"], \
                       
                       orbitType, irObservationName, irDescription, uvisDescription, comment
                       ]
        linesToWrite.append("".join(str(element)+"\t" for element in lineToWrite))
    
        rowColour = "98fab4"
        htmlRow = lineToWrite+[rowColour]
        htmlRows.append(htmlRow)
        
        plotData["incidence"].append(dayside["incidenceMidpoint"])
        plotData["et"].append(dayside["etMidpoint"])
    





    linkName = "nomad_mtp%03d_nadir.txt" %mtpNumber
    linkDescription = "Table data in text format"
    extraComments = ["UTC Start Time = Terminator crossing time", \
                     "UTC End Time = Terminator crossing time", \
    #                 "Duration time includes extra time before and after terminator crossing", \
                     "Dayside nadir timings do not include 10 second initialisation time", \
                     "LTP file used for this analysis: %s" %mappsEventFilename, \
                     "Timings may vary from SOC by up to %i seconds, due to orbit differences" %ACCEPTABLE_MTP_NADIR_TIME_ERROR, \
                     "Colour code: Grey = nightside nadir; Green = dayside nadir"]
    #                "Note that observation start/end times here have not yet been checked for clashes with other NOMAD observations"]
    writeHtmlTable("nomad_mtp%03d_nadir" %mtpNumber, "NOMAD MTP%03d Nadir Observations" %mtpNumber, htmlHeader, htmlRows, paths, linkNameDesc=[linkName, linkDescription], extraComments=extraComments)
    writeOutputTxt(os.path.join(paths["HTML_MTP_PATH"], "nomad_mtp%03d_nadir" %mtpNumber), linesToWrite)
    
    
    plt.figure(figsize=(FIG_X, FIG_Y-2))
    plt.plot(plotData["et"], plotData["incidence"])
    xTickIndices = list(range(0, len(plotData["et"]), (np.int(len(plotData["et"])/4) -1)))
    xTickLabels = [et2utc(plotData["et"][x])[0:11] for x in xTickIndices]
    xTicks = [plotData["et"][x] for x in xTickIndices]
    plt.xticks(xTicks, xTickLabels)
    plt.xlabel("Observation Time")
    plt.ylabel("Dayside nadir Minimum Solar Incidence Angle (deg)")
    plt.title("MTP%03d Dayside Nadir Minimum Solar Incidence Angle" %mtpNumber)
    plt.savefig(os.path.join(paths["HTML_MTP_PATH"], "mtp%03d_nadir_minimum_incidence_angle.png" %mtpNumber))
    plt.close()







def writeOccultationWebpage(orbit_list, mtpConstants, paths):
    """write occultation website page"""
    mtpNumber = mtpConstants["mtpNumber"]
    mappsEventFilename = mtpConstants["mappsEventFilename"]

    def getValue(key):
        if occultation[key] != "-":
            return "%0.1f" %occultation[key]
        else:
            return "-"
    


    alt = "%0.0fkm" %SO_TRANSITION_ALTITUDE
    htmlHeader = ["Instrument", "Orbit Number", "Occultation Type", "UTC Start Time", "UTC Transition Time", "UTC End Time", "Duration (s)", \
                "Start Longitude", alt+" Longitude", "End Longitude", \
                "Start Latitude", alt+" Latitude", "End Latitude", alt+" Local Time (hrs)", \
                "Orbit Type", "IR Observation Name", "IR Description", "UVIS Description", "Orbit Comment"]
    linesToWrite = ["".join(column+"\t" for column in htmlHeader)]
    
    occultationNames = ["ingress","egress","merged","grazing"]
    irObsTypeNames = {"ingress":["irIngressHigh","irIngressLow"], "merged":["irIngressHigh","irIngressLow"], "grazing":["irIngressHigh","irIngressLow"], "egress":["irEgressLow","irEgressHigh"]}
    uvisObsTypeNames = {"ingress":"uvisIngress", "merged":"uvisIngress", "grazing":"uvisIngress", "egress":"uvisEgress"}
    
    
    htmlRows = []
    plotDataIngress = {"lon":[], "lat":[], "duration":[], "et":[]}
    plotDataEgress = {"lon":[], "lat":[], "duration":[], "et":[]}
    for orbit in orbit_list:
        orbitType = orbit["finalOrbitPlan"]["orbitType"]
    
        for occultationName in occultationNames:
            if occultationName in orbit.keys():
                occultation = orbit[occultationName]
    
                obsType1, obsType2 = irObsTypeNames[occultationName]
                
                #get obs description from file (if it exists)
                if obsType1+"CopRows" in orbit["finalOrbitPlan"].keys():
                    description1 = "%s" %(orbit["finalOrbitPlan"][obsType1+"CopRows"]["copRowDescription"])
                    description2 = "%s" %(orbit["finalOrbitPlan"][obsType2+"CopRows"]["copRowDescription"])
                    if description1 == description2: #if SCI1 = SCI2
                        irDescription = description1
                    else:
                        irDescription = description1 + "; " + description2
                    
                    name1 = "%s" %(orbit["finalOrbitPlan"][obsType1+"ObservationName"])
                    name2 = "%s" %(orbit["finalOrbitPlan"][obsType2+"ObservationName"])
                    if name1 == name2:
                        irObservationName = name1
                    else:
                        irObservationName = name1 + "; " + name2
                        
                else:
                    irDescription = "-"
                    irObservationName = "-"
                    
                uvisObsType = uvisObsTypeNames[occultationName]
                if uvisObsType+"CopRows" in orbit["finalOrbitPlan"].keys():
                    uvisDescription = "COP row %i: %s" %(orbit["finalOrbitPlan"][uvisObsType+"CopRows"]["scienceCopRow"], orbit["finalOrbitPlan"][uvisObsType+"CopRows"]["copRowDescription"])
                else:
                    uvisDescription = "-"
                    
                comment = orbit["finalOrbitPlan"]["comment"]
                    
        
                lineToWrite = [occultation["primeInstrument"], orbit["orbitNumber"], occultationName.capitalize(), \
                               occultation["utcStart"], occultation["utcTransition"], occultation["utcEnd"], "%0.1f" %occultation["duration"], \
                               "%0.1f" %occultation["lonStart"], getValue("lonTransition"), "%0.1f" %occultation["lonEnd"], \
                               "%0.1f" %occultation["latStart"], getValue("latTransition"), "%0.1f" %occultation["latEnd"], \
                               getValue("lstTransition"), 
                               
                               orbitType, irObservationName, irDescription, uvisDescription, comment
                               ]
                linesToWrite.append("".join(str(element)+"\t" for element in lineToWrite))
            
                rowColour = occultation["rowColour"]
                htmlRow = lineToWrite+[rowColour]
                htmlRows.append(htmlRow)
                
                if getValue("lonTransition") != "-": #igore merged or grazing
                    if occultationName == "ingress":
                        plotDataIngress["lon"].append(occultation["lonTransition"])
                        plotDataIngress["lat"].append(occultation["latTransition"])
                        plotDataIngress["duration"].append(occultation["duration"])
                        plotDataIngress["et"].append(occultation["etTransition"])
                    elif occultationName == "egress":
                        plotDataEgress["lon"].append(occultation["lonTransition"])
                        plotDataEgress["lat"].append(occultation["latTransition"])
                        plotDataEgress["duration"].append(occultation["duration"])
                        plotDataEgress["et"].append(occultation["etTransition"])
    
        
        
    linkName = "nomad_mtp%03d_occultation.txt" %mtpNumber
    linkDescription = "Table data in text format"
    extraComments = ["UTC Start Time = 0 or 250km tangent altitude", \
                     "UTC End Time = 0 or 250km tangent altitude", \
                     "UTC Transition Time = %i km tangent altitude" %SO_TRANSITION_ALTITUDE, \
                     "LTP file used for this analysis: %s" %mappsEventFilename, \
                     "Timings may vary from SOC by up to %i seconds, due to orbit differences" %ACCEPTABLE_MTP_OCCULTATION_TIME_ERROR, \
                     "Colour code: Green = occultation assigned to NOMAD in LTP; Blue = occultation assigned to ACS in LTP; Red = occultation unassigned in LTP; Yellow = unused observation e.g. tangent altitude too high"]
    #                     "Note that observation start/end times here have not yet been checked for clashes with other NOMAD observations"]
    writeHtmlTable("nomad_mtp%03d_occultation" %mtpNumber, "NOMAD MTP%03d Occultation Observations" %mtpNumber, htmlHeader, htmlRows, paths, linkNameDesc=[linkName, linkDescription], extraComments=extraComments)
    writeOutputTxt(os.path.join(paths["HTML_MTP_PATH"], "nomad_mtp%03d_occultation" %mtpNumber), linesToWrite)
    
    
    
    
    plt.figure(figsize=(FIG_X, FIG_Y-2))
    plt.scatter(plotDataIngress["et"], plotDataIngress["duration"], c="r", label="Ingress")
    plt.scatter(plotDataEgress["et"], plotDataEgress["duration"], c="b", label="Egress")
    xTickIndices = list(range(0, len(plotDataIngress["et"]), (np.int(len(plotDataIngress["et"])/4) -1)))
    xTickLabels = [et2utc(plotDataIngress["et"][x])[0:11] for x in xTickIndices]
    xTicks = [plotDataIngress["et"][x] for x in xTickIndices]
    plt.xticks(xTicks, xTickLabels)
    plt.xlabel("Observation Time")
    plt.ylabel("Occultation Duration (s)")
    plt.title("MTP%02d Solar Occultation Observation Durations" %mtpNumber)
    plt.legend()
    plt.savefig(os.path.join(paths["HTML_MTP_PATH"], "mtp%03d_occultation_duration.png" %mtpNumber))
    
    plt.close()
    
    plt.figure(figsize=(FIG_X, FIG_Y-2))
    plt.scatter(plotDataIngress["et"], plotDataIngress["lat"], c="r", label="Ingress")
    plt.scatter(plotDataEgress["et"], plotDataEgress["lat"], c="b", label="Egress")
    xTickIndices = list(range(0, len(plotDataIngress["et"]), (np.int(len(plotDataIngress["et"])/4) -1)))
    xTickLabels = [et2utc(plotDataIngress["et"][x])[0:11] for x in xTickIndices]
    xTicks = [plotDataIngress["et"][x] for x in xTickIndices]
    plt.xticks(xTicks, xTickLabels)
    plt.xlabel("Observation Time")
    plt.ylabel("Occultation Latitudes (deg)")
    plt.ylim([-90, 90])
    plt.title("MTP%02d Solar Occultation Observation Latitudes" %mtpNumber)
    plt.legend()
    plt.savefig(os.path.join(paths["HTML_MTP_PATH"], "mtp%03d_occultation_lat.png" %mtpNumber))
    plt.close()
    



def writeLnoUvisJointObsNumbers(orbit_list, mtpConstants, paths):
    """write LNO obs numbers for UVIS-LNO joint obs"""
    """irDayside field must contain text and must not be a limb measurement"""
    """note that a check is NOT made to see if this file arlready exists. It should be identical each time it is made and should never be edited by hand"""
    mtpNumber = mtpConstants["mtpNumber"]
    
    ORBIT_PLAN_NAME = "genericOrbitPlanIn"
    
    lnoOperatingOrbits = ["THERMAL ORBIT NUMBER WITH LNO NADIR"]
    for orbit in orbit_list:
        if "irDayside" in orbit[ORBIT_PLAN_NAME].keys():
            if orbit[ORBIT_PLAN_NAME]["orbitType"] not in LIMB_ORBIT_TYPES:
                if orbit[ORBIT_PLAN_NAME]["irDayside"] != "":
                    lnoOperatingOrbits.append("%s" %orbit["orbitNumber"])
    
    writeOutputTxt(os.path.join(paths["ORBIT_PLAN_PATH"], "nomad_mtp%03d_lno_orbits" %mtpNumber), lnoOperatingOrbits)


def writeLnoGroundAssetJointObsInfo(orbit_list, mtpConstants, paths, ground_asset_name):
    """ write NOMAD + SAM-TLS joint obs info - start/end time, incidence angle, COP rows used"""
    mtpNumber = mtpConstants["mtpNumber"]

    ORBIT_PLAN_NAME = "finalOrbitPlan"
    
    lnoGroundAssetJointObs = ["UTC TIME WHEN LNO OBSERVING CLOSE TO %s, INCIDENCE ANGLE, LOCAL SOLAR TIME, LNO DIFFRACTION ORDERS MEASURED" %ground_asset_name.upper()]
    for orbit in orbit_list:
        if "irDayside" in orbit[ORBIT_PLAN_NAME].keys(): #check if dayside
            if orbit[ORBIT_PLAN_NAME]["irDayside"] != "": #check if LNO observing
                if "daysideRegions" in orbit.keys(): #check if any regions of interest observed
                    for daysideRegion in orbit["daysideRegions"]: 
                        if ground_asset_name.upper() in daysideRegion["name"]: #check if curiosity
                            print(orbit["orbitNumber"])
                            ordersMeasured = orbit[ORBIT_PLAN_NAME]["irDaysideOrders"]
                            orders = "#"+" #".join(str(order) for order in ordersMeasured)
                            utcTimeMeasured = daysideRegion["utc"]
                            incidenceAngleMeasured = daysideRegion["incidenceAngle"]
                            lstMeasured = daysideRegion["lst"]
                            
                            outputText = "%s, %0.1f, %0.1f, %s" %(utcTimeMeasured, incidenceAngleMeasured, lstMeasured, orders)
                            lnoGroundAssetJointObs.append(outputText)
                            print(outputText)

    writeOutputTxt(os.path.join(paths["ORBIT_PLAN_PATH"], "nomad_mtp%03d_lno_%s_joint_obs" %(mtpNumber, ground_asset_name.lower())), lnoGroundAssetJointObs)


def writeAcsJointObsNumbers(orbit_list, mtpConstants, paths):
    """write ACS joint obs"""
    """note that a check is NOT made to see if this file arlready exists. It should be identical each time it is made and should never be edited by hand"""
    mtpNumber = mtpConstants["mtpNumber"]


    obsTypeNames = {"ingress":"irIngressLow", "merged":"irIngressLow", "grazing":"irIngressLow", "egress":"irEgressLow"}
    outputStrings = []
    for obsName, socObsName in SOC_JOINT_OBSERVATION_NAMES.items():
    
        for socObsType in SOC_JOINT_OBSERVATION_TYPES:
            outputString = "%s, %s" %(socObsName, socObsType)
            found = False
            
            for orbit in orbit_list:
                occultationObsTypes = [occultationType for occultationType in orbit["allowedObservationTypes"][:] if occultationType in ["ingress", "egress", "merged", "grazing"]]
                for occultationObsType in occultationObsTypes:
                    if occultationObsType in orbit.keys():
                        obsTypeName = obsTypeNames[occultationObsType]
                        if obsName == orbit["finalOrbitPlan"][obsTypeName]:
                            eventDescription = orbit[occultationObsType]["occultationEventFileCounts"]
                            if socObsType in eventDescription:
                                eventOrbitNumber = eventDescription.split("-")[-1]
                                outputString += ", %s" %eventOrbitNumber
                                found = True
            if found:
                outputStrings.append(outputString)

    writeOutputCsv(os.path.join(paths["COP_ROW_PATH"], "joint_occ_mtp%03d" %mtpNumber), outputStrings)




def writeOrbitPlanCsv(orbit_List, mtpConstants, paths):
    """write final orbit type numbers to csv file for ops team"""
    """note that a check is NOT made to see if this file arlready exists. It should be identical each time it is made and should never be edited by hand"""
    mtpNumber = mtpConstants["mtpNumber"]

    ORBIT_PLAN_NAME = "genericOrbitPlanIn"
    
    orbitTypeNumbers = ["#orbitType"]
    for orbit in orbit_List:
        orbitTypeNumbers.append("%i" %orbit[ORBIT_PLAN_NAME]["orbitType"])

    writeOutputCsv(os.path.join(paths["ORBIT_PLAN_PATH"], "nomad_mtp%03d_plan" %mtpNumber), orbitTypeNumbers)




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
        


def getMtpTimes(mtpNumber):
    """find mtp start/end times and ls for an mtp"""
    
    def lsubs(et):
        return sp.lspcn("MARS",et,SPICE_ABCORR) * sp.dpr()

    mtp0Start = datetime(2018, 3, 24)
    mtpTimeDelta = timedelta(days=28)
    
    mtpStart = mtp0Start + mtpTimeDelta * mtpNumber
    mtpEnd = mtpStart + mtpTimeDelta
    
    mtpStartString = datetime.strftime(mtpStart, SPICE_DATETIME_FORMAT[:8])
    mtpEndString = datetime.strftime(mtpEnd, SPICE_DATETIME_FORMAT[:8])
    
    mtpStartEt = sp.utc2et(mtpStartString)
    mtpEndEt = sp.utc2et(mtpEndString)
    
    mtpStartLs = lsubs(mtpStartEt)
    mtpEndLs = lsubs(mtpEndEt)
    
    return mtpStartString, mtpEndString, mtpStartLs, mtpEndLs




def makeOverviewPage(orbit_list, mtpConstants, paths):
    """plot occultation orders for mtp overview page"""
    mtpNumber = mtpConstants["mtpNumber"]
    obsTypeNames = {"ingress":"irIngressLow", "egress":"irEgressLow"}

    
    #loop through once to find list of all orders measured
    ordersAll = []
    for orbit in orbit_list:
        occultationObsTypes = [occultationType for occultationType in orbit["allowedObservationTypes"][:] if occultationType in ["ingress", "egress"]]    
        for occultationObsType in occultationObsTypes:
            if occultationObsType in orbit.keys():
                obsTypeName = obsTypeNames[occultationObsType]
    
                orders = orbit["finalOrbitPlan"][obsTypeName+"Orders"]
                if 0 in orders: #remove darks
                    orders.remove(0)
                if "COP#" in "%s" %orders[0]: #remove manual COP selection
                    orders = []
                ordersAll.extend(orders)
    uniqueOccultationOrders = sorted(list(set(ordersAll)))
    
    #loop through again to plot each order on a single graph
    for chosenOrder in uniqueOccultationOrders:
        title = "Solar occultations for diffraction order %s" %(chosenOrder)
        fig = plt.figure(figsize=(FIG_X, FIG_Y))
        ax = fig.add_subplot(111, projection="mollweide")
        ax.grid(True)
        plt.title(title)
    
        for orbit in orbit_list:
            occultationObsTypes = [occultationType for occultationType in orbit["allowedObservationTypes"][:] if occultationType in ["ingress", "egress"]]    
            for occultationObsType in occultationObsTypes:
                if occultationObsType in orbit.keys():
                    obsTypeName = obsTypeNames[occultationObsType]
        
                    orders = orbit["finalOrbitPlan"][obsTypeName+"Orders"]
                    if chosenOrder in orders:
                        occultation = orbit[occultationObsType]
                        
                        #if lats/lons/alts not yet in orbitList, find and write to list
                        if "alts" not in occultation.keys():
                            #just plot the half of the occultation closest to the surface, not the high altitude bits
                            #ignore merged or grazing occs at this point
                            if occultationObsType == "ingress":
                                ets = np.arange(occultation["etMidpoint"], occultation["etEnd"], OCCULTATION_SEARCH_STEP_SIZE)
                            elif occultationObsType == "egress":
                                ets = np.arange(occultation["etStart"], occultation["etMidpoint"], OCCULTATION_SEARCH_STEP_SIZE)
                            lonsLatsLsts = np.asfarray([getLonLatLst(et) for et in ets])
                            occultation["lons"] = lonsLatsLsts[:, 0]
                            occultation["lats"] = lonsLatsLsts[:, 1]
                            occultation["alts"] = np.asfarray([getTangentAltitude(et) for et in ets])
                        #else take lats/lons/alts from orbitList if already exists
                        
                        colours = occultation["alts"]
                        plot1 = ax.scatter(occultation["lons"]/sp.dpr(), occultation["lats"]/sp.dpr(), c=colours, cmap=plt.cm.jet, marker='o', linewidth=0)
    
        cbar = fig.colorbar(plot1, fraction=0.046, pad=0.04)
        cbar.set_label("Tangent Point Altitude (km)", rotation=270, labelpad=20)
        fig.tight_layout()
        plt.savefig(os.path.join(paths["IMG_MTP_PATH"], "occultations_mtp%03d_order%i_altitude.png" %(mtpNumber, chosenOrder)))
        plt.close()
    
    
    
    """plot nadir orders"""
    #find all orders measured
    ordersAll = []
    for orbit in orbit_list:
        if "dayside" in orbit["irMeasuredObsTypes"]:
            orders = orbit["finalOrbitPlan"]["irDaysideOrders"]
            if 0 in orders: #remove darks
                orders.remove(0)
            if "COP#" in "%s" %orders[0]: #remove manual COP selection
                orders = []
            ordersAll.extend(orders)
    uniqueNadirOrders = sorted(list(set(ordersAll)))
    
    #plot each order
    for chosenOrder in uniqueNadirOrders:
        title = "Dayside nadirs for diffraction order %s" %(chosenOrder)
        fig = plt.figure(figsize=(FIG_X, FIG_Y))
        ax = fig.add_subplot(111, projection="mollweide")
        ax.grid(True)
        plt.title(title)
    
        for orbit in orbit_list:
            if "dayside" in orbit["irMeasuredObsTypes"]:
                orders = orbit["finalOrbitPlan"]["irDaysideOrders"]
                if chosenOrder in orders:
                    nadir = orbit["dayside"]
                    
                    #if lats/lons/incidence angles not yet in orbitList, find and write to list
                    if "incidences" not in nadir.keys():
#                        print(orbit["orbitNumber"])
                        #nadir start/end times have been modified to fit thermal room
                        realStartTime = nadir["obsStart"] + PRECOOLING_TIME + INITIALISATION_TIME
                        realEndTime = nadir["obsEnd"]
                        ets = np.arange(realStartTime, realEndTime, NADIR_SEARCH_STEP_SIZE)
                        lonsLatsIncidencesLsts = np.asfarray([getLonLatIncidenceLst(et) for et in ets])
                        nadir["lons"] = lonsLatsIncidencesLsts[:, 0]
                        nadir["lats"] = lonsLatsIncidencesLsts[:, 1]
                        nadir["incidences"] = lonsLatsIncidencesLsts[:, 2]
                    #else take lats/lons/incidence angles from orbitList if already exists
                    
                    colours = nadir["incidences"]
                    plot1 = ax.scatter(nadir["lons"]/sp.dpr(), nadir["lats"]/sp.dpr(), c=colours, cmap=plt.cm.jet, marker='o', linewidth=0)
    
        cbar = fig.colorbar(plot1, fraction=0.046, pad=0.04)
        cbar.set_label("Incidence Angle (degrees)", rotation=270, labelpad=20)
        fig.tight_layout()
        plt.savefig(os.path.join(paths["IMG_MTP_PATH"], "dayside_nadirs_mtp%03d_order%i_incidence_angle.png" %(mtpNumber, chosenOrder)))
        plt.close()

    """write mtp overview page"""
    h = r""
    h += r"<h1>MTP%03d Overview</h1>" %(mtpNumber)
    h += r"<h2>Geometry</h2>"+"\n"
    
    imagename = "mtp%03d_occultation_duration.png" %(mtpNumber)
    h += r"<img src='%s'>" %imagename
    imagename = "mtp%03d_occultation_lat.png" %(mtpNumber)
    h += r"<img src='%s'>" %imagename
    imagename = "mtp%03d_nadir_minimum_incidence_angle.png" %(mtpNumber)
    h += r"<img src='%s'>" %imagename
    
    h += r"<p>UVIS typically operates on all dayside nadirs and all occultations</p>"+"\n"
    
    h += r"<h2>Solar Occultations</h2>"+"\n"
    
    h += r"Solar occultation diffraction orders measured this MTP: "+"\n"
    for chosenOrder in sorted(uniqueOccultationOrders):
        h += "%i, " %chosenOrder
    h += r"<br>"+"\n"
    
    for chosenOrder in sorted(uniqueOccultationOrders):
        h += "<h3>Solar occultations for diffraction order %i</h3>" %chosenOrder
        imagename = "img/occultations_mtp%03d_order%i_altitude.png" %(mtpNumber, chosenOrder)
        h += r"<img src='%s'>" %imagename
    
    h += r"<br>"+"\n"
    h += r"<br>"+"\n"
    h += r"<br>"+"\n"
    h += r"<br>"+"\n"
    h += r"<h2>Dayside Nadirs</h2>"+"\n"
    
    h += r"Dayside nadir diffraction orders measured this MTP: "+"\n"
    for chosenOrder in sorted(uniqueNadirOrders):
        h += "%i, " %chosenOrder
    h += r"<br>"+"\n"
    
    for chosenOrder in sorted(uniqueNadirOrders):
        h += "<h3>Dayside nadirs for diffraction order %i</h3>" %chosenOrder
        imagename = "img/dayside_nadirs_mtp%03d_order%i_incidence_angle.png" %(mtpNumber, chosenOrder)
        h += r"<img src='%s'>" %imagename
    
    
    
    h += r"<br>"+"\n"
    h += r"<br>"+"\n"
#    h += r"<h2>SO/LNO Observation Plan</h2>"+"\n"
    
        
    h += r"<br>"+"\n"
    h += r"<br>"+"\n"
    h += r"<h2>SO/LNO Observation Dictionaries</h2>"+"\n"
    h += r"<h3>Solar Occultation</h3>"+"\n"
    headers = ["Name", "Diffraction Order 1", "Diffraction Order 2", "Diffraction Order 3", "Diffraction Order 4", "Diffraction Order 5", "Diffraction Order 6", "Integration Time", "Rhythm", "Detector Height"]
    h += r"<table border=1>"+"\n"
    h += r"<tr>"+"\n"
    for header in headers:
        h += r"<th>%s</th>" %header
    h += r"</tr>"+"\n"
    for key in sorted(occultationObservationDict.keys()):
        orders, integrationTime, rhythm, detectorRows, channelCode = getObsParameters(key, occultationObservationDict)
    
        h += r"<tr>"+"\n"
        h += r"<td>%s</td>" %(key)
        if "COP" in orders:
            h += r"<td>%s (manual mode)</td>" %(orders)
            for order in range(5):
                h += r"<td>-</td>"+"\n"
        else:    
            for order in orders:
                h += r"<td>%s</td>" %(order)
            for order in range(6-len(orders)):
                h += r"<td>-</td>"+"\n"
                
        h += r"<td>%i</td>" %(integrationTime)
        h += r"<td>%i</td>" %(rhythm)
        h += r"<td>%i</td>" %(detectorRows)
        h += r"</tr>"+"\n"
    h += r"</table>"+"\n"
    
    
    h += r"<h3>Nadir/Limb</h3>"+"\n"
    headers = ["Name", "Diffraction Order 1", "Diffraction Order 2", "Diffraction Order 3", "Diffraction Order 4", "Diffraction Order 5", "Diffraction Order 6", "Integration Time", "Rhythm", "Detector Height"]
    h += r"<table border=1>"+"\n"
    h += r"<tr>"+"\n"
    for header in headers:
        h += r"<th>%s</th>" %header
    h += r"</tr>"
    for key in sorted(nadirObservationDict.keys()):
        orders, integrationTime, rhythm, detectorRows, channelCode = getObsParameters(key, nadirObservationDict)
    
        h += r"<tr>"+"\n"
        h += r"<td>%s</td>" %(key)
        if "COP" in orders:
            h += r"<td>%s (manual mode)</td>" %(orders)
            for order in range(5):
                h += r"<td>-</td>"+"\n"
        else:    
            for order in orders:
                h += r"<td>%s</td>" %(order)
            for order in range(6-len(orders)):
                h += r"<td>-</td>"+"\n"
                
        h += r"<td>%i</td>" %(integrationTime)
        h += r"<td>%i</td>" %(rhythm)
        h += r"<td>%i</td>" %(detectorRows)
        h += r"</tr>"+"\n"
    h += r"</table>"+"\n"
    
    
    
    
    h += r"<br>"+"\n"
    h += r"<br>"+"\n"
    h += r"<p>Page last modified: %s</p>" %(datetime.now().strftime('%a, %d %b %Y %H:%M:%S')) +"\n"
    
    with open(os.path.join(paths["HTML_MTP_PATH"], "nomad_mtp%03d_overview.html" %(mtpNumber)), 'w') as f:
        f.write(h)


    return uniqueOccultationOrders, uniqueNadirOrders




def writeMtpMasterPage(mtpConstants, paths):
    """write the master page up to the current mtp"""
    mtpNumber = mtpConstants["mtpNumber"]


    mtpStartString, mtpEndString, mtpStartLs, mtpEndLs = getMtpTimes(mtpNumber)
        
    """write mtp master page"""
    h = r""
    h += r"<h1>MTP%03d Planning (%s - %s, Ls: %0.0f - %0.0f)</h1>" %(mtpNumber, mtpStartString, mtpEndString, mtpStartLs, mtpEndLs)
    pagename = "nomad_mtp%03d_overview.html" %(mtpNumber); desc = "MTP Overview"
    h += r"<p><a href=%s>%s</a></p>" %(pagename, desc)
    pagename = "nomad_mtp%03d_occultation.html" %(mtpNumber); desc = "MTP Occultation Observations"
    h += r"<p><a href=%s>%s</a></p>" %(pagename, desc)
    pagename = "nomad_mtp%03d_nadir.html" %(mtpNumber); desc = "MTP Nadir Observations"
    h += r"<p><a href=%s>%s</a></p>" %(pagename, desc)
    #pagename = "nomad_mtp%03d_merged.html" %(mtpNumber); desc = "MTP Merged Observation Plan"
    #h += r"<p><a href=%s>%s</a></p>" %(pagename, desc)
    
#    pagename = "nomad_mtp%03d_uvis.html" %(mtpNumber); desc = "MTP UVIS Observation Plan"
#    h += r"<p><a href=%s>%s</a></p>" %(pagename, desc)
    h += r"<br>"+"\n"
    
    h += r"<br>"+"\n"
    h += r"<p>Page last modified: %s</p>" %(datetime.now().strftime('%a, %d %b %Y %H:%M:%S')) +"\n"
    pagename = "../../event_files/LEVF_M%03d_SOC_PLANNING.EVF" %(mtpNumber); desc = "."
    h += r"<p><a href=%s>%s</a></p>" %(pagename, desc)
    pagename = "../../itls/MITL_M%03d_NOMAD.ITL" %(mtpNumber); desc = "."
    h += r"<p><a href=%s>%s</a></p>" %(pagename, desc)
    
    with open(os.path.join(paths["HTML_MTP_PATH"], "nomad_mtp%03d.html" %(mtpNumber)), 'w') as f:
        f.write(h)



def writeIndexWebpage(mtpConstants, paths):
    """update website index page with latest mtp"""    
    mtpNumber = mtpConstants["mtpNumber"]



    MASTER_PAGE_NAMES = ["EXM-NO-SNO-AER-00028-iss0rev4-SO_LNO_COP_Table_Order_Combinations-180528.htm", \
              "EXM-NO-SNO-AER-00027-iss0rev8-Science_Orbit_Observation_Rules-180306.pdf", \
              "EXM-NO-PRS-AER-00172-iss0rev0-HDF5_Files_Description_180712.pdf"]

    MASTER_PAGE_DESCRIPTIONS = ["SO and LNO diffraction order combinations", \
                     "NOMAD Orbit Types and Observation Rules", \
                     "Description of NOMAD Data and Observations"]


    allMtps = range(1, mtpNumber+1)
    

    
    h = r""
    h += r"<h1>NOMAD Observation Page</h1>"+"\n"
    h += r"<h2>Miscellaneous Information</h2>"+"\n"

    pagename = "nomad_faqs.html"
    desc = "***Frequently Asked Questions***"
    h += r"<p><a href=%s>%s</a></p>" %("pages/"+pagename,desc)+"\n"

    for pageName,pageDescription in zip(MASTER_PAGE_NAMES,MASTER_PAGE_DESCRIPTIONS):
        h += r"<p><a href=%s>%s</a> - %s</p>" %("pages/"+pageName,pageName,pageDescription)+"\n"

   
    h += r"<h2>NOMAD Past Observations</h2>"+"\n"
    pagename = "nomad_ground_cal_obs.html"; desc="NOMAD Ground Calibration and Recalibration following LNO detector swap"
    h += r"<p><a href=%s>%s</a> - %s</p>" %("pages/"+pagename,pagename,desc)+"\n"
    pagename = "nomad_nec_obs.html"; desc="NOMAD Near Earth Commissioning"
    h += r"<p><a href=%s>%s</a> - %s</p>" %("pages/"+pagename,pagename,desc)+"\n"
    pagename = "nomad_mcc_obs.html"; desc="NOMAD Mid-Cruise Checkout"
    h += r"<p><a href=%s>%s</a> - %s</p>" %("pages/"+pagename,pagename,desc)+"\n"
    pagename = "nomad_mco_obs.html"; desc="NOMAD Mars Capture Orbit"
    h += r"<p><a href=%s>%s</a> - %s</p>" %(("pages/MCO/"+pagename),pagename,desc)+"\n"
    pagename = "nomad_mco2_obs.html"; desc="NOMAD Mars Capture Orbit Part 2"
    h += r"<p><a href=%s>%s</a> - %s</p>" %(("pages/MCO2/"+pagename),pagename,desc)+"\n"
    
    mtpStartString, mtpEndString, mtpStartLs, mtpEndLs = getMtpTimes(0)
    
    pagename = "nomad_commissioning.html"; desc="Post-Aerobraking Commissioning Phase (%s - %s, Ls: %0.0f - %0.0f)" %(mtpStartString, mtpEndString, mtpStartLs, mtpEndLs)
    h += r"<p><a href=%s>%s</a> - %s</p>" %("mtp_pages/mtp000/"+pagename,pagename,desc)+"\n"


    h += r"<h2>NOMAD Nominal Science Observations</h2>"+"\n"

    for mtpIndex in allMtps:
            
        mtpStartString, mtpEndString, mtpStartLs, mtpEndLs = getMtpTimes(mtpIndex)
        
        pagename = "nomad_mtp%03d.html" %(mtpIndex); desc="Medium Term Planning MTP%03d (%s - %s, Ls: %0.0f - %0.0f)" %(mtpIndex, mtpStartString, mtpEndString, mtpStartLs, mtpEndLs)
        h += r"<p><a href=%s>%s</a> - %s</p>" \
            %(("mtp_pages/mtp%03d" %mtpIndex +os.sep+pagename),pagename,desc)+"\n"

    h += r"<br>"+"\n"

    pagename = "science_calibrations.html"; desc="Calibrations During Nominal Science Period"
    h += r"<p><a href=%s>%s</a> - %s</p>" %("calibrations/"+pagename,pagename,desc)+"\n"
    h += r"<br>"+"\n"
    h += r"<br>"+"\n"
    h += r"<p>Page last modified: %s</p>" %(datetime.now().strftime('%a, %d %b %Y %H:%M:%S')) +"\n"

    with open(os.path.join(OBS_DIRECTORY, "index.html"), 'w') as f:
        f.write(h)




def printStatement(string_in):
    """write statement with current utc time"""
    print("%s (%s)" %(string_in, datetime.strftime(datetime.now(), SPICE_DATETIME_FORMAT)))







def writeCalibrationWebpage(paths):
    """write the science calibration webpage from Bojan's input file (place in OBS_DIRECTORY/calibrations)"""


    def readCalibrationsFromFile(paths):
        """read latest calibration file from Bojan/Claudio"""
        calibrationPath = paths["CALIBRATION_PATH"]
        calibrationFilePath = ""
        
        #check directory for calibration files
        #search for filename matching sequence
        lastMtps = []
        for fileName in os.listdir(calibrationPath):
            if "NOMAD_calibrations" in fileName:
                lastMtp = int(fileName.split("-")[1].replace(".txt",""))
                lastMtps.append(lastMtp)
        lastMtpInt = "-%03i.txt" %sorted(lastMtps)[-1] #get newest file from list of potential files
        
        for fileName in os.listdir(calibrationPath):
            if "NOMAD_calibrations" in fileName:
                if lastMtpInt in fileName:
                    calibrationFilePath = os.path.join(calibrationPath, fileName)
        
        #read lines
        if calibrationFilePath != "": #if file actually found
            with open(calibrationFilePath) as f:
                lines = []
                titles = []
                calibrations = []
                #remove unneeded lines
                for index, line in enumerate(f):
                    if line[0:3] == "MTP":
                        if index > 0:
                            calibrations.append(lines)
                            lines = []
                        content = line.strip().strip("%")
                        titles.append(content)
                    elif line[0] == "#":
                        lines.append(line.replace("# ",""))
        else:
            titles = []
            calibrations = []
    
        return titles, calibrations
    
    
    
    
    def textToNum(string):
        """convert string to int if possible"""
        try:
            return int(string)
        except ValueError:
            return -999
    
    h=r""
    h += r"<h1>NOMAD Science Phase Calibrations</h1>"+"\n"
    h += r"<h2>This page lists calibration observations only, and is maintained by hand (so may be out of date)</h2>"+"\n"
    h += r"<h2>Note that these are the predicted execution times. Real times could differ by up to 2 minutes</h2>"+"\n"
    h += r"<h2>Typically there are only 1 or 2 calibrations allowed per MTP</h2>"+"\n"
    
    
    titlesText, calibrationsText = readCalibrationsFromFile(paths)
    
    for title, calibration in zip(titlesText, calibrationsText):
        #find MTP
        calibrationMtpText = title.replace("MTP","").split("-")[0]
        calibrationMtp = textToNum(calibrationMtpText)
        
        if calibrationMtp > -1 and len(calibration) != 0:
            #get copVersion for each MTP
            mtpConstants = getMtpConstants(calibrationMtp)
            copVersion = mtpConstants["copVersion"]
            copTableDict = getCopTables(mtpConstants)
    
        
            
            
                    
            #get obs description from COP row
            soAotfHeaders,soAotfList = outputCopTable(copVersion,"so",'aotf')
            soFixedHeaders,soFixedList = outputCopTable(copVersion,"so",'fixed')
            soScienceHeaders,soScienceList = outputCopTable(copVersion,"so",'science')
            soSteppingHeaders,soSteppingList = outputCopTable(copVersion,"so",'stepping')
            soSubdomainHeaders,soSubdomainList = outputCopTable(copVersion,"so",'sub_domain')
            
            lnoAotfHeaders,lnoAotfList = outputCopTable(copVersion,"lno",'aotf')
            lnoFixedHeaders,lnoFixedList = outputCopTable(copVersion,"lno",'fixed')
            lnoScienceHeaders,lnoScienceList = outputCopTable(copVersion,"lno",'science')
            lnoSteppingHeaders,lnoSteppingList = outputCopTable(copVersion,"lno",'stepping')
            lnoSubdomainHeaders,lnoSubdomainList = outputCopTable(copVersion,"lno",'sub_domain')
            
            uvisHeaders,uvisList = outputCopTable(copVersion,"uvis","")
    
            
            soFixedRow = [int(value.replace("SO_COP_GENERAL = ","")) for value in calibration if "SO_COP_GENERAL" in value][0]
            lnoFixedRow = [int(value.replace("LNO_COP_GENERAL = ","")) for value in calibration if "LNO_COP_GENERAL" in value][0]
            
            soCopRow1 = [int(value.replace("SO_COP_SCIENCE_1 = ","")) for value in calibration if "SO_COP_SCIENCE_1" in value][0]
            soCopRow2 = [int(value.replace("SO_COP_SCIENCE_2 = ","")) for value in calibration if "SO_COP_SCIENCE_2" in value][0]
            lnoCopRow1 = [int(value.replace("LNO_COP_SCIENCE_1 = ","")) for value in calibration if "LNO_COP_SCIENCE_1" in value][0]
            lnoCopRow2 = [int(value.replace("LNO_COP_SCIENCE_2 = ","")) for value in calibration if "LNO_COP_SCIENCE_2" in value][0]
            
            uvisCopRow = [int(value.replace("UVIS_COP_ROW = ","")) for value in calibration if "UVIS_COP_ROW" in value][0]
            
            
            if soCopRow1 == soCopRow2:
                if soCopRow1 > 0:
                    soCopRows = [soCopRow1]
                else:
                    soCopRows = []
            else:
                soCopRows = [soCopRow1, soCopRow2]
    
            if lnoCopRow1 == lnoCopRow2:
                if lnoCopRow1 > 0:
                    lnoCopRows = [lnoCopRow1]
                else:
                    lnoCopRows = []
            else:
                lnoCopRows = [lnoCopRow1, lnoCopRow2]
                
            if uvisCopRow > 0:
                uvisCopRows = [uvisCopRow]
            else:
                uvisCopRows = []
    
    
            title = ""
            for soCopRow in soCopRows:
                channel = "so"
                description = getObservationDescription(channel, copTableDict, soFixedRow, soCopRow, silent=True)
                title += "<br>%s: %s" %(channel.upper(), description)
    
            for lnoCopRow in lnoCopRows:
                channel = "lno"
                description = getObservationDescription(channel, copTableDict, lnoFixedRow, lnoCopRow, silent=True)
                title += "<br>%s: %s" %(channel.upper(), description)
            
            for uvisCopRow in uvisCopRows:
                channel = "uvis"
                description = getObservationDescription(channel, copTableDict, 0, uvisCopRow, silent=True)
                title += "<br>%s: %s" %(channel.upper(), description)
    
    
            h += r"<h3>"+title+r"</h3>"+"\n"
            if len(calibration) > 0:
                h += r"<textarea rows=""38"" cols=""150"">"+"\n"
                for textLine in calibration:
                    h += textLine
                h += r"</textarea>"
    
    
    h += r"<br>"+"\n"
    h += r"<br>"+"\n"
    h += r"<p>Page last modified: %s</p>" %(datetime.now().strftime('%a, %d %b %Y %H:%M:%S')) +"\n"
    
    #write html page
    with open(os.path.join(paths["CALIBRATION_PATH"], "science_calibrations.html"), 'w') as f:
        f.write(h)
            
    







def step1(orbitList, mtpConstants, paths):
    printStatement("Starting program")
    printStatement("Reading in initialisation data and inputs from mapps event file")    
    printStatement("Getting nadir data")
    orbitList = getNadirData(orbitList, mtpConstants)
    printStatement("Getting occultation data")
    orbitList = getOccultationData(orbitList, mtpConstants)
    printStatement("Finding grazing occultations")
    orbitList = findGrazingOccultations(orbitList)
    printStatement("Checking for corresponding MAPPS events")
    orbitList = addMappsEvents(orbitList, mtpConstants, paths)
    printStatement("Finding dayside nadir observations in regions of interest")
    orbitList = regionsOfInterestNadir(orbitList, nadirRegionsOfInterest)
    printStatement("Finding occultation observations in regions of interest")
    orbitList = regionsOfInterestOccultation(orbitList, occultationRegionsOfInterest)
    printStatement("Adding flags to file where obsevations match a region of interest")
    orbitList = findMatchingRegions(orbitList)
    printStatement("Adding generic orbit plan to orbit list (no nightsides or limbs, to be added manually)")
    orbitList = makeGenericOrbitPlan(orbitList)
    printStatement("Writing generic observation plan to file")
    writeOrbitPlanXlsx(orbitList, mtpConstants, paths, "plan_generic")
    return orbitList



def step2(orbitList, mtpConstants, paths):


    printStatement("Getting iterated mtp plan from file and merging with orbit list")
    mtpPlan = getMtpPlanXlsx(mtpConstants, paths, "plan_generic")
    orbitList = mergeMtpPlan(orbitList, mtpPlan, "genericOrbitPlanIn", "genericOrbitPlanOut")
    printStatement("Writing joint observation number files for UVIS")
    writeLnoUvisJointObsNumbers(orbitList, mtpConstants, paths)
    printStatement("Writing final orbit plan to csv file")
    writeOrbitPlanCsv(orbitList, mtpConstants, paths)
    return orbitList



def step3(orbitList, mtpConstants, paths):


    printStatement("Checking that all observation keys are in dictionary")
    checkKeys(occultationObservationDict, nadirObservationDict)
    printStatement("Generating complete orbit plan (with real observation names) and adding to orbit list")
    orbitList = makeCompleteOrbitPlan(orbitList)
    printStatement("Writing complete observation plan to file")
    writeOrbitPlanXlsx(orbitList, mtpConstants, paths, "plan")
    return orbitList



def step4(orbitList, mtpConstants, paths):


    printStatement("Getting final mtp plan from file and merging with orbit list")
    finalMtpPlan = getMtpPlanXlsx(mtpConstants, paths, "plan")
    orbitList = mergeMtpPlan(orbitList, finalMtpPlan, "finalOrbitPlan", "completeOrbitPlan") #read in final plan, make finalOrbitPlan, checking it matches the previous completeOrbitPlan
    orbitList = addCorrectNadirObservations(orbitList)
    printStatement("Reducing LNO dayside nadir observations to fit thermal rule")
    fitNadirToThermalRule(orbitList)
    printStatement("Finding and adding COP rows to orbit list")
    copTableDict = getCopTables(mtpConstants)
    orbitList = addIrCopRows(orbitList, copTableDict, mtpConstants)
    orbitList = addUvisCopRows(orbitList, copTableDict, mtpConstants, paths)
    printStatement("Writing COP rows to text files")
    writeIrCopRowsTxt(orbitList, mtpConstants, paths)
    printStatement("Writing LNO and Curosity/SAM joint observation file")   
    writeLnoGroundAssetJointObsInfo(orbitList, mtpConstants, paths, "Curiosity")
    writeLnoGroundAssetJointObsInfo(orbitList, mtpConstants, paths, "Insight")
    writeLnoGroundAssetJointObsInfo(orbitList, mtpConstants, paths, "AEOLIS MENSAE MFF")
    printStatement("Writing mtp occultation webpage")
    writeOccultationWebpage(orbitList, mtpConstants, paths)
    printStatement("Writing mtp nadir webpage")
    writeNadirWebpage(orbitList, mtpConstants, paths)
    printStatement("Making order plots and writing mtp overview page")
    makeOverviewPage(orbitList, mtpConstants, paths)
    printStatement("Writing joint observation number files for ACS")
    writeAcsJointObsNumbers(orbitList, mtpConstants, paths)
    printStatement("Writing master page for this MTP and updating main index webpage")
    writeMtpMasterPage(mtpConstants, paths)
    writeIndexWebpage(mtpConstants, paths)
    printStatement("Updating science calibrations webpage")
    writeCalibrationWebpage(paths)
    printStatement("Done!")
    return orbitList




#for orbit in orbitList: 
#    if "occultationRegions" in orbit.keys():
#        print(orbit["orbitNumber"])











