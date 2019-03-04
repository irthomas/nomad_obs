# -*- coding: utf-8 -*-
"""
Created on Thu Feb 21 14:41:19 2019

@author: iant

OBS PLANNING USING SPICE WINDOWS
"""


import numpy as np
import os

#import numpy as np
#import os
from datetime import datetime
#import matplotlib.pyplot as plt
import xlsxwriter
import xlrd
#import spiceypy as sp

from obs_config import BASE_DIRECTORY, COP_TABLE_DIRECTORY, KERNEL_DIRECTORY, OBS_DIRECTORY, METAKERNEL_NAME
from run_planning import mtpNumber
#from obs_inputs import mtpNumber, MAKE_MAPPS_EVENT_FILE, MAKE_OBSERVATION_PLAN, ADD_UVIS_COP_ROWS, STOP_ON_ERROR
#from obs_inputs import JOINT_OBSERVATION_NAMES_TO_FIND, SOC_JOINT_OBSERVATION_NAMES, SOC_JOINT_OBSERVATION_TYPES
from obs_inputs import getMtpConstants
from obs_inputs import nadirObservationDict, nadirRegionsOfInterest, occultationObservationDict, occultationRegionsOfInterest, nadirRegionsObservations, occultationRegionsObservations
from obs_inputs import OCCULTATION_KEYS, OCCULTATION_MERGED_KEYS, OCCULTATION_GRAZING_KEYS, USE_TWO_SCIENCES
from obs_inputs import NADIR_KEYS, NADIR_LIMB_KEYS, NADIR_NIGHTSIDE_KEYS



__project__   = "NOMAD Observation Planning"
__author__    = "Ian Thomas"
__contact__   = "ian.thomas@aeronomie.be"



if not os.path.exists("/bira-iasb/data/SATELLITE/TRACE-GAS-ORBITER/NOMAD"):# and not os.path.exists(os.path.normcase(r"X:\linux\Data")):
    print("Running on windows")
    import spiceypy as sp
#    load spiceypy kernels if required
#    KERNEL_DIRECTORY = os.path.normcase(r"C:\Users\iant\Documents\DATA\local_spice_kernels\kernels\mk")
#    METAKERNEL_NAME = "em16_plan_win.tm"
#    METAKERNEL_NAME = "em16_ops_win.tm"
    sp.furnsh(KERNEL_DIRECTORY+os.sep+METAKERNEL_NAME)
    print(sp.tkvrsn("toolkit"))
    print("KERNEL_DIRECTORY=%s" %KERNEL_DIRECTORY)


"""set up paths to output files"""
#LOG_FILE_PATH = os.path.join(BASE_DIRECTORY, "observations", "mtps")
#HTML_FILE_PATH = os.path.join(BASE_DIRECTORY, "observations", "mtps")
INPUT_FILE_PATH = os.path.join(OBS_DIRECTORY, "input")
#OUTPUT_FILE_PATH = os.path.join(BASE_DIRECTORY, "observations", "output")

#MERGED_OBSERVATION_PLAN_PATH = os.path.join(BASE_DIRECTORY, "observations", "mtps", "nomad_mtp%03d_merged.txt" %mtpNumber)




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





def getNadirData(orbit_list, utc_string_start, utc_string_end):
    """get all nadir data, add to orbit list"""
    #Dayside Nadir Index	UTC Start Time	UTC End Time UTC Minimum Incidence Angle Time	Duration (s)	Start Longitude	Centre Longitude	End Longitude	Start Latitude	Centre Latitude	End Latitude	Centre Local Time (hrs)

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
        
        orbit_list.append({"orbitNumber":index, "etOrbitStart":orbit_start, "etOrbitEnd":orbit_end, \
                           "utcOrbitStart":orbit_start_str, "utcOrbitEnd":orbit_end_str, \
                           
                           
                           "daysideNadir":{"utcStart":start_str, "utcEnd":end_str, "utcMidpoint":midpoint_str, \
                                           "etStart":start, "etEnd":end, "etMidpoint":midpoint, \
                                           "lonStart":start_lon, "lonEnd":end_lon, "lonMidpoint":midpoint_lon, 
                                           "latStart":start_lat, "latEnd":end_lat, "latMidpoint":midpoint_lat, 
                                           "incidenceStart":start_incidence, "incidenceEnd":end_incidence, "incidenceMidpoint":midpoint_incidence, 
                                           "lstStart":start_lst, "lstEnd":end_lst, "lstMidpoint":midpoint_lst, 
                                           "duration":duration}, \

                           "nightsideNadir":{"utcStart":orbit_start_str, "utcEnd":start_str, \
                                           "etStart":orbit_start, "etEnd":start}})
        
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




def getOccultationData(orbit_list, utc_string_start, utc_string_end):
    """get all occultation data (except grazing), add to orbit list"""
    #Instrument	Occultation Index	 Occultation Type	 UTC Start Time	UTC End Time	UTC Transition Time	Duration (s)	Tangent Centre Longitude	Tangent Centre Latitude	Tangent Centre Local Time (hrs)

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
        obs_egress_start = egress_start - INITIALISATION_TIME - PRECOOLING_TIME - SO_REFERENCE_DURATION
        obs_egress_end = egress_end + SO_REFERENCE_DURATION

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

            occultation_dict = {"occultationNumber":index, \
                                "merged":{"utcStart":merged_start_str, "utcEnd":merged_end_str, "utcMidpoint":merged_midpoint_str, "utcTransition":merged_transition_str, \
                                          "etStart":merged_start, "etEnd":merged_end, "etMidpoint":merged_midpoint, "etTransition":merged_transition, \
                                           "lonStart":merged_start_lon, "lonEnd":merged_end_lon, "lonMidpoint":merged_midpoint_lon, "lonTransition":merged_transition_lon, \
                                           "latStart":merged_start_lat, "latEnd":merged_end_lat, "latMidpoint":merged_midpoint_lat, "latTransition":merged_transition_lat, \
                                           "altitudeStart":merged_start_altitude, "altitudeEnd":merged_end_altitude, "altitudeMidpoint":merged_midpoint_altitude, "altitudeTransition":merged_transition_altitude, \
                                           "lstStart":merged_start_lst, "lstEnd":merged_end_lst, "lstMidpoint":merged_midpoint_lst, "lstTransition":merged_transition_lst, \
                                           "obsStart":obs_merged_start, "obsEnd":obs_merged_end, \
                                           "duration":merged_duration}}
        else:
            occultation_dict = {"occultationNumber":index, \
                                "ingress":{"utcStart":ingress_start_str, "utcEnd":ingress_end_str, "utcMidpoint":ingress_midpoint_str, "utcTransition":ingress_transition_str, \
                                           "etStart":ingress_start, "etEnd":ingress_end, "etMidpoint":ingress_midpoint, "etTransition":ingress_transition, \
                                           "lonStart":ingress_start_lon, "lonEnd":ingress_end_lon, "lonMidpoint":ingress_midpoint_lon, "lonTransition":ingress_transition_lon, \
                                           "latStart":ingress_start_lat, "latEnd":ingress_end_lat, "latMidpoint":ingress_midpoint_lat, "latTransition":ingress_transition_lat, \
                                           "altitudeStart":ingress_start_altitude, "altitudeEnd":ingress_end_altitude, "altitudeMidpoint":ingress_midpoint_altitude, "altitudeTransition":ingress_transition_altitude, \
                                           "lstStart":ingress_start_lst, "lstEnd":ingress_end_lst, "lstMidpoint":ingress_midpoint_lst, "lstTransition":ingress_transition_lst, \
                                           "obsStart":obs_ingress_start, "obsEnd":obs_ingress_end, \
                                           "duration":ingress_duration},  

                                 "egress":{"utcStart":egress_start_str, "utcEnd":egress_end_str, "utcMidpoint":egress_midpoint_str, "utcTransition":egress_transition_str, \
                                           "etStart":egress_start, "etEnd":egress_end, "etMidpoint":egress_midpoint, "etTransition":egress_transition, \
                                           "lonStart":egress_start_lon, "lonEnd":egress_end_lon, "lonMidpoint":egress_midpoint_lon, "lonTransition":egress_transition_lon, \
                                           "latStart":egress_start_lat, "latEnd":egress_end_lat, "latMidpoint":egress_midpoint_lat, "latTransition":egress_transition_lat, \
                                           "altitudeStart":egress_start_altitude, "altitudeEnd":egress_end_altitude, "altitudeMidpoint":egress_midpoint_altitude, "altitudeTransition":egress_transition_altitude, \
                                           "lstStart":egress_start_lst, "lstEnd":egress_end_lst, "lstMidpoint":egress_midpoint_lst, "lstTransition":egress_transition_lst, \
                                           "obsStart":obs_egress_start, "obsEnd":obs_egress_end, \
                                           "duration":egress_duration}}
        orbit_index = (ingress_start > orbit_starts).argmin() - 1
        orbit_list[orbit_index].update(occultation_dict)

    return orbit_list        




def findGrazingOccultations(orbit_list):
    """find all grazing occultations in MTP, add to orbit list"""
    grazing_index = 0
    for orbit in orbitList:
        if orbit["daysideNadir"]["incidenceMidpoint"] > 60.0: #if high beta angle
            if "merged" not in orbit.keys():
                et_start = orbit["nightsideNadir"]["etStart"] + 500
                et_end = orbit["nightsideNadir"]["etEnd"] - 500
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
                    
                    grazing_duration = grazing_end - grazing_start
                    
                    occultation_dict = {"occultationNumber":grazing_index, \
                        "grazing":{"utcStart":grazing_start_str, "utcEnd":grazing_end_str, "utcMidpoint":grazing_midpoint_str, "utcTransition":"-", \
                                  "etStart":grazing_start, "etEnd":grazing_end, "etMidpoint":grazing_midpoint, "etTransition":"-", \
                                   "lonStart":grazing_start_lon, "lonEnd":grazing_end_lon, "lonMidpoint":grazing_midpoint_lon, "lonTransition":"-", \
                                   "latStart":grazing_start_lat, "latEnd":grazing_end_lat, "latMidpoint":grazing_midpoint_lat, "latTransition":"-", \
                                   "altitudeStart":grazing_start_altitude, "altitudeEnd":grazing_end_altitude, "altitudeMidpoint":grazing_midpoint_altitude, "altitudeTransition":"-", \
                                   "lstStart":grazing_start_lst, "lstEnd":grazing_end_lst, "lstMidpoint":grazing_midpoint_lst, "lstTransition":"-", \
                                   "obsStart":obs_grazing_start, "obsEnd":obs_grazing_end, \
                                   "duration":grazing_duration}}
    
    
                    
                    orbit.update(occultation_dict)
    return orbit_list




def readMappsEventFile(instrument, mappsObservationType):
    """read in the LTP  planning file from the SOC and find NOMAD or ACS events (occultations) or terminator crossings (nadir)"""
    MAPPS_EVENT_FILEPATH = os.path.join(INPUT_FILE_PATH, MAPPS_EVENT_FILENAME)
    lines = [line.rstrip('\n').split()[0:3] for line in open(MAPPS_EVENT_FILEPATH) if line[0] != "#"]

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
                eventTime = eventTime[0:-1]
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
    

    elif mappsObservationType == "nadir":
        mappsEvent = []
        
        daysideStartFound = False
        daysideEndFound = False
        eventIndex = 0
        
        EVENT_CODES = TERMINATOR_N2D_CODES + TERMINATOR_D2N_CODES
        
        for eventTime, eventName, eventCount in lines:
            if eventName in EVENT_CODES:
                eventTime = eventTime[0:-1]
                eventCount = eventName + "-%i" %int(eventCount.split("COUNT=")[1].strip(r")"))
        
                if eventName in TERMINATOR_N2D_CODES:
                    mappsDaysideStart = sp.str2et(eventTime)
                    daysideStartFound = True
                elif eventName in TERMINATOR_D2N_CODES:
                    mappsDaysideEnd = sp.str2et(eventTime)
                    daysideEndFound = True
                if daysideStartFound and daysideEndFound:
                    mappsEvent.append([eventIndex, "Dayside", mappsDaysideStart, mappsDaysideEnd, eventCount])
                    eventIndex += 1
                    daysideStartFound = False
                    daysideEndFound = False

    return mappsEvent



    






def addMappsEvents(orbit_list):
    """compare timings in event file to calculated orbits"""
    for orbit in orbit_list:
#        orbit["obsTypes"] = []
        orbit["allowedOccultationTypes"] = []
        
        for obstype in ["ingress","egress","merged","grazing"]:
            if obstype in orbit.keys():
                mappsNomadEventIndex = np.abs(np.asfarray(mappsNomadOccEventStartTimes) - orbit[obstype]["etStart"]).argmin()
                mappsAcsEventIndex = np.abs(np.asfarray(mappsAcsOccEventStartTimes) - orbit[obstype]["etStart"]).argmin()
        
                if np.abs(mappsNomadOccEventStartTimes[mappsNomadEventIndex] - orbit[obstype]["etStart"]) < ACCEPTABLE_MTP_OCCULTATION_TIME_ERROR:
                    orbit["allowedOccultationTypes"].append(obstype)
                    orbit[obstype]["rowColour"] = "98fab4"
                    orbit[obstype]["primeInstrument"] = "NOMAD"
    
                    orbit[obstype]["occultationEventFileCounts"] = mappsNomadOccEventStartCounts[mappsNomadEventIndex]
                    orbit[obstype]["mappsStartTime"] = mappsNomadOccEventStartTimes[mappsNomadEventIndex]
                    orbit[obstype]["mappsStartName"] = mappsNomadOccEventStartNames[mappsNomadEventIndex]
                    orbit[obstype]["mappsStartTimeDelta"] = mappsNomadOccEventStartTimes[mappsNomadEventIndex] - orbit[obstype]["etStart"]
    
    
                elif np.abs(mappsAcsOccEventStartTimes[mappsAcsEventIndex] - orbit[obstype]["etStart"]) < ACCEPTABLE_MTP_OCCULTATION_TIME_ERROR:
                    orbit[obstype]["rowColour"] = "97c9f9"
                    orbit[obstype]["primeInstrument"] = "ACS"
    
                else:
                    orbit[obstype]["rowColour"] = "f99797"
                    orbit[obstype]["primeInstrument"] = "N/A"
    return orbit_list




def regionsOfInterestNadir(orbit_list, regions_of_interest, silent=True):
    """check for nadir observations near regions of interest"""
    #loop through each observation, making lat/lon steps and check against regions of interest
    for orbit in orbit_list:
        if "daysideNadir" in orbit.keys():
            daysideNadir = orbit["daysideNadir"]
            
            etStart = daysideNadir["etStart"]
            etEnd = daysideNadir["etEnd"]
            ets = np.arange(etStart, etEnd, NADIR_SEARCH_STEP_SIZE)
            daysideNadirData = np.asfarray([getLonLatIncidenceLst(et) for et in ets])
            
            lons = daysideNadirData[:, 0]
            lats = daysideNadirData[:, 1]
            incidence_angles = daysideNadirData[:, 2]
            lst = daysideNadirData[:, 3]
            
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
                        if "daysideNadirRegions" not in orbit.keys():
                            orbit["daysideNadirRegions"] = []
                        orbit["daysideNadirRegions"].append(regionDict)
                    else:
                        if not silent: print("Match found on orbit %i but incidence angle %0.1f is above %0.0f" %(orbit["orbitNumber"], incidence_angles[i], MAXIMUM_SEARCH_INCIDENCE_ANGLE))
    return orbit_list




def regionsOfInterestOccultation(orbit_list, regions_of_interest, silent=False):
    """check for occultation observations near regions of interest"""
    #loop through each observation, making lat/lon steps and check against regions of interest
    for orbit in orbit_list:
        for occultation_type in orbit["allowedOccultationTypes"]:
#            print(occultation_type)
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
        if "daysideNadirRegions" in orbit.keys():
            for region in orbit["daysideNadirRegions"]:
                if not silent: 
                    print("Match found: %s, orbit %i, incidence angle %0.1f at %s" %(region["name"], orbit["orbitNumber"], region["incidenceAngle"], region["utc"]))
    
                if region["name"] in nadirRegionsObservations.keys():
                    orbit["daysideNadir"]["observationName"] = nadirRegionsObservations[region["name"]]
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

    #inputs for defining generic orbit plan
    LNO_CYCLE = ["ON", "OFF"] * 200 #i.e. 50% duty cycle for orbits without occultations. 
    #This should begin with a 3 so that first observation after OCM is an LNO
    #The script automatically starts with a 4 if the preceding orbit has a measurement to avoid scheduling too many consecutive observations.
    
    lno_cycle = -1
    for orbit in orbit_list:

        generic_orbit = {}
        generic_orbit_type = 14
        generic_orbit_comment = ""
        
        generic_orbit["irNightside"] = "" #irNightside not defined in generic plan
        generic_orbit["uvisNightside"] = "" #uvisNightside not defined in generic plan

        """check for possible OCMs (Saturday afternoons, 11 - 4pm)"""
        timeStringOut = orbit["daysideNadir"]["utcStart"]
        orbitNumber = orbit["orbitNumber"]
    
        ocm = False
        if datetime.strptime(timeStringOut, SPICE_DATETIME_FORMAT).isoweekday() == 6:
            if orbitNumber != 0: #if not first orbit
                if orbitNumber != (len(orbit_list)-1): #if not last orbit
                    if 11 < datetime.strptime(timeStringOut, SPICE_DATETIME_FORMAT).hour < 16:
                        generic_orbit_comment += "&PossibleOCM; "
                        ocm = True



    
        for occultation_type in orbit["allowedOccultationTypes"]:
            if occultation_type == "ingress":
                generic_orbit["irIngressHigh"] = "irIngress"
                generic_orbit["irIngressLow"] = "irIngress"
                generic_orbit["uvisIngress"] = "uvisIngress"
    
                generic_orbit_type = 1
                if "egress" in orbit["allowedOccultationTypes"]: #if 2 occultations in same orbit
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
                if "ingress" in orbit["allowedOccultationTypes"]: #if 2 occultations in same orbit
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
            if "occultationRegions" in orbit.keys(): #if nadir obs matches region of interest, set LNO on
                for region in orbit["occultationRegions"]:
                    generic_orbit_comment += "%sMatch:%s; " %(region["occultationType"], region["name"])

    
        if generic_orbit_type == 14: #if no occultations
    
            generic_orbit["irIngressHigh"] = ""
            generic_orbit["irIngressLow"] = ""
            generic_orbit["uvisIngress"] = ""
            generic_orbit["irEgressHigh"] = ""
            generic_orbit["irEgressLow"] = ""
            generic_orbit["uvisEgress"] = ""
    
            if ocm: #NOMAD must be off during correction maneouvres
                generic_orbit["irDayside"] = ""
                generic_orbit["uvisDayside"] = "uvisOnlyDayside"
                lno_cycle = -1 #reset lno to on

            else:
                #check nadir regions of interest
                if "daysideNadirRegions" in orbit.keys(): #if nadir obs matches region of interest, set LNO on
                    lno_on_off = "ON"
                    lno_cycle = 0 #reset lno to off
                    
                    for region in orbit["daysideNadirRegions"]:
                        generic_orbit_comment += "&daysideMatch:%s; " %(region["name"])
                else:
                    lno_cycle += 1
                    lno_on_off = LNO_CYCLE[lno_cycle]
                
                if lno_on_off == "ON":
                    generic_orbit_type = 3
                    generic_orbit["irDayside"] = "irLongDayside"
                    generic_orbit["uvisDayside"] = "uvisDayside"
            
                else: #if lno off and no occultations
                    generic_orbit["irDayside"] = ""
                    generic_orbit["uvisDayside"] = "uvisOnlyDayside"



        
    
        orbit["genericOrbitPlanOut"] = {"orbitTypeNumber":generic_orbit_type, "orbitTypes":generic_orbit, "comment":generic_orbit_comment}
    return orbit_list



def writeObservationPlan(worksheet, row, row_to_write):
    """function to write observation plan"""
    for column, row_item in enumerate(row_to_write):
        worksheet.write(row, column, row_item)



def writeGenericPlanXlsx(mtp_number, orbit_list):
    """write generic observation plan to file"""
    with xlsxwriter.Workbook(BASE_DIRECTORY+os.sep+"nomad_mtp%03d_plan_generic.xlsx" %mtp_number) as workbook:
        worksheet = workbook.add_worksheet()
        
        rowCounter = 0
        writeObservationPlan(worksheet, rowCounter, ["#orbitType","irIngressHigh","irIngressLow","uvisIngress","irEgressHigh","irEgressLow","uvisEgress","irDayside","uvisDayside","irNightside","uvisNightside","night2dayTerminator","comment"])
        
        for orbit in orbit_list:
            genericOrbitPlan = orbit["genericOrbitPlanOut"]
            row_to_write = [genericOrbitPlan["orbitTypeNumber"]]
            
            for genericObsType in ["irIngressHigh","irIngressLow","uvisIngress","irEgressHigh","irEgressLow","uvisEgress","irDayside","uvisDayside","irNightside","uvisNightside"]:
                row_to_write.append(genericOrbitPlan["orbitTypes"][genericObsType])
            
            row_to_write.append(orbit["daysideNadir"]["utcStart"])
            row_to_write.append(genericOrbitPlan["comment"])
            
            rowCounter += 1
            writeObservationPlan(worksheet, rowCounter, row_to_write)






def getMtpPlanXlsx(mtp_number):
    """read back in orbit plan after iteration by OU/BIRA"""
    with xlrd.open_workbook(os.path.join(INPUT_FILE_PATH, "nomad_mtp%03d_plan_generic.xlsx" %mtp_number)) as workbook:
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


def mergeMtpPlan(orbit_list, mtp_plan):
    """merge iterated orbit plan into orbit list"""    
    if len(mtp_plan) != len(orbit_list):
        print("Error")
    
    for orbit, orbit_plan in zip(orbit_list, mtp_plan):
        orbit["genericOrbitTypesIn"] = {}
        for key, value in orbit_plan.items():
            if value != "":
                orbit[key] = value
                if key in ["orbitType", "irIngressHigh", "irIngressLow", "uvisIngress", "irEgressHigh", "irEgressLow", "uvisEgress", "irDayside", \
                          "uvisDayside", "irNightside", "uvisNightside"]:
                    orbit["genericOrbitTypesIn"][key] = value
                elif key == "comment":
                    orbit["genericOrbitTypesIn"]["comment"] = value
                    #TODO: check ingress/egresses match in orbit list and mtp plan, check timings match
                    #TODO: check that genericOrbitTypesIn = genericOrbitTypesOut
    return orbit_list




print("Starting program (%s)" %(datetime.strftime(datetime.now(), SPICE_DATETIME_FORMAT)))
orbitList = []
print("Reading in initialisation data and inputs from mapps event file (%s)" %(datetime.strftime(datetime.now(), SPICE_DATETIME_FORMAT)))
utcstringStart, utcstringEnd, copVersion, MAPPS_EVENT_FILENAME, SO_CENTRE_DETECTOR_LINE = getMtpConstants(mtpNumber)

mappsNomadOccEvents = readMappsEventFile("NOMAD", "occultation")
mappsNomadOccEventStartTimes = [eventTime for _, eventName, eventTime, _, _ in mappsNomadOccEvents if eventName in ["Ingress", "Egress", "Merged", "Grazing"]]
mappsNomadOccEventStartNames = [eventName for _, eventName, _, _, _ in mappsNomadOccEvents if eventName in ["Ingress", "Egress", "Merged", "Grazing"]]
mappsNomadOccEventStartCounts = [eventCount for _, eventName, _, _, eventCount in mappsNomadOccEvents if eventName in ["Ingress", "Egress", "Merged", "Grazing"]]

mappsAcsOccEvents = readMappsEventFile("ACS", "occultation")
mappsAcsOccEventStartTimes = [eventTime for _, eventName, eventTime, _, _ in mappsAcsOccEvents if eventName in ["Ingress", "Egress", "Merged", "Grazing"]]
mappsAcsOccEventStartNames = [eventName for _, eventName, _, _, _ in mappsAcsOccEvents if eventName in ["Ingress", "Egress", "Merged", "Grazing"]]
mappsAcsOccEventStartCounts = [eventCount for _, eventName, _, _, eventCount in mappsAcsOccEvents if eventName in ["Ingress", "Egress", "Merged", "Grazing"]]

mappsDaysideEvents = readMappsEventFile("", "nadir")
mappsDaysideEventsStartTimes = [eventTime for _, eventName, eventTime, _, _ in mappsDaysideEvents if eventName in ["Dayside"]]
mappsDaysideEventStartNames = [eventName for _, eventName, _, _, _ in mappsDaysideEvents if eventName in ["Dayside"]]
mappsDaysideEventStartCounts = [eventCount for _, eventName, _, _, eventCount in mappsDaysideEvents if eventName in ["Dayside"]]


print("Getting nadir data (%s)" %(datetime.strftime(datetime.now(), SPICE_DATETIME_FORMAT)))
orbitList = getNadirData(orbitList, utcstringStart, utcstringEnd)
print("Getting occultation data (%s)" %(datetime.strftime(datetime.now(), SPICE_DATETIME_FORMAT)))
orbitList = getOccultationData(orbitList, utcstringStart, utcstringEnd)
print("Finding grazing occultations (%s)" %(datetime.strftime(datetime.now(), SPICE_DATETIME_FORMAT)))
orbitList = findGrazingOccultations(orbitList)
print("Checking for corresponding MAPPS events (%s)" %(datetime.strftime(datetime.now(), SPICE_DATETIME_FORMAT)))
orbitList = addMappsEvents(orbitList)
print("Finding dayside nadir observations in regions of interest (%s)" %(datetime.strftime(datetime.now(), SPICE_DATETIME_FORMAT)))
orbitList = regionsOfInterestNadir(orbitList, nadirRegionsOfInterest)
print("Finding occultation observations in regions of interest (%s)" %(datetime.strftime(datetime.now(), SPICE_DATETIME_FORMAT)))
orbitList = regionsOfInterestOccultation(orbitList, occultationRegionsOfInterest)
print("Adding flags to file where obsevations match a region of interest (%s)" %(datetime.strftime(datetime.now(), SPICE_DATETIME_FORMAT)))
orbitList = findMatchingRegions(orbitList)
print("Writing generic plan in orbit list (no nightsides or limbs, to be added manually) (%s)" %(datetime.strftime(datetime.now(), SPICE_DATETIME_FORMAT)))
orbitList = makeGenericOrbitPlan(orbitList)
print("Writing generic observation plan to file (%s)" %(datetime.strftime(datetime.now(), SPICE_DATETIME_FORMAT)))
writeGenericPlanXlsx(mtpNumber, orbitList)
print("Getting iterated mtp plan and merging with orbit list (%s)" %(datetime.strftime(datetime.now(), SPICE_DATETIME_FORMAT)))
mtpPlan = getMtpPlanXlsx(mtpNumber)
orbitList = mergeMtpPlan(orbitList, mtpPlan)


"""check for clashing start/end times"""
#TODO: check for clashes

"""fill in generic plan with real observations"""
#TODO: fill in generic plan with real observations


#First check if all keys above can be found in the observation dictionaries
for key_file in [OCCULTATION_KEYS, OCCULTATION_MERGED_KEYS, OCCULTATION_GRAZING_KEYS]:
    for observation_name in key_file:
        if observation_name not in list(occultationObservationDict.keys()):
            print("Error: %s not found in occultation dictionary!" %observation_name)

for key_file in [NADIR_KEYS, NADIR_LIMB_KEYS]:
    for observation_name in key_file:
        if observation_name not in list(nadirObservationDict.keys()):
            print("Error: %s not found in nadir dictionary!" %observation_name)



def getObsParameters(observation_name, dictionary):
    if observation_name in list(dictionary.keys()):
        orders_out, inttime_out, rhythm_out, rows_out = dictionary[observation_name]
        return orders_out, inttime_out, rhythm_out, rows_out
    else:
        print("Observation name %s not found in dictionary" %observation_name)
        





occultationCounter = -1
occultationMergedCounter = -1
occultationGrazingCounter = -1
occultationRidealongCounter = -1
nadirCounter = -1
nadirLimbCounter = -1
nadirNightsideCounter = -1

for orbit in orbitList:

    genericObsTypes = orbit["genericOrbitTypesIn"]
    orbitType = genericObsTypes["orbitType"]

    irIngressHigh = "******ERROR******" #to be replaced in loop
    irIngressLow = "******ERROR******" #to be replaced in loop
    irEgressHigh = "******ERROR******" #to be replaced in loop
    irEgressLow = "******ERROR******" #to be replaced in loop
    irDayside = "******ERROR******" #to be replaced in loop
    irNightside = "******ERROR******" #to be replaced in loop




    if orbitType in [1]:
        if genericObsTypes["irIngressHigh"] == "irIngress":
            occultationCounter += 1
            irIngressHigh = OCCULTATION_KEYS[occultationCounter]
            irIngressLow = OCCULTATION_KEYS[occultationCounter]
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
            irIngressHigh = ""
            irIngressLow = ""



        if genericObsTypes["irEgressHigh"] == "irEgress":
            occultationCounter += 1
            irEgressHigh = OCCULTATION_KEYS[occultationCounter]
            irEgressLow = OCCULTATION_KEYS[occultationCounter]
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
            irEgressHigh = ""
            irEgressLow = ""

        if genericObsTypes["irDayside"] != "": #if dayside nadir not blank, add the observation
            nadirCounter += 1
            irDayside = NADIR_KEYS[nadirCounter]
        else:
            irDayside = ""
        irNightside="" #never nightside with occultations



    if orbitType in [5]:
        if genericObsTypes["irIngressHigh"] in ["irMerged"]:
            occultationMergedCounter += 1
            irIngressHigh = OCCULTATION_MERGED_KEYS[occultationMergedCounter]
            irIngressLow = OCCULTATION_MERGED_KEYS[occultationMergedCounter]
        elif genericObsTypes["irIngressHigh"] in ["irGrazing"]:
            occultationGrazingCounter += 1
            irIngressHigh = OCCULTATION_GRAZING_KEYS[occultationGrazingCounter]
            irIngressLow = OCCULTATION_GRAZING_KEYS[occultationGrazingCounter]

        irEgressHigh = ""
        irEgressLow = ""
        nadirCounter += 1
        irDayside = NADIR_KEYS[nadirCounter]
        irNightside=""


    if orbitType in [6]:
        if genericObsTypes["irIngressHigh"] in ["irMerged"]:
            occultationMergedCounter += 1
            irIngressHigh = OCCULTATION_MERGED_KEYS[occultationMergedCounter]
            irIngressLow = OCCULTATION_MERGED_KEYS[occultationMergedCounter]
        elif genericObsTypes["irIngressHigh"] in ["irGrazing"]:
            occultationGrazingCounter += 1
            irIngressHigh = OCCULTATION_GRAZING_KEYS[occultationGrazingCounter]
            irIngressLow = OCCULTATION_GRAZING_KEYS[occultationGrazingCounter]

        irEgressHigh = ""
        irEgressLow = ""
        irDayside = ""
        irNightside=""




    if orbitType in [3]:
        irIngressHigh=""
        irIngressLow=""
        irEgressHigh=""
        irEgressLow=""
        nadirCounter += 1
        irDayside = NADIR_KEYS[nadirCounter]
        irNightside=""

    if orbitType in [4, 14]:
        irIngressHigh=""
        irIngressLow=""
        irEgressHigh=""
        irEgressLow=""
        irDayside=""
        irNightside=""



    if orbitType in [7]:
        irIngressHigh=""
        irIngressLow=""
        irEgressHigh=""
        irEgressLow=""

        if genericObsTypes["irDayside"] == "irDayside": #dayside nadir
            nadirCounter += 1
            irDayside = NADIR_KEYS[nadirCounter]
        else:
            irDayside = ""

        if genericObsTypes["irNightside"] == "irNightside": #nightside nadir
            nadirNightsideCounter += 1
            irNightside = NADIR_NIGHTSIDE_KEYS[nadirNightsideCounter]
        else:
            irNightside = ""
            print("Warning: orbit type 7 found with blank nightside nadir")


    if orbitType in [17]:
        irIngressHigh=""
        irIngressLow=""
        irEgressHigh=""
        irEgressLow=""

        if genericObsTypes["irDayside"] == "irDayside": #dayside nadir
            nadirCounter += 1
            irDayside = NADIR_KEYS[nadirCounter]
        else:
            irDayside = ""

        if genericObsTypes["irNightside"] == "irNightside": #nightside nadir
            nadirNightsideCounter += 1
            irNightside = NADIR_NIGHTSIDE_KEYS[nadirNightsideCounter]
        else:
            irNightside = ""


    if orbitType in [8]:
        irIngressHigh=""
        irIngressLow=""
        irEgressHigh=""
        irEgressLow=""


        if genericObsTypes["irDayside"] == "irLimb": #limb
            nadirLimbCounter += 1
            irDayside = NADIR_LIMB_KEYS[nadirLimbCounter]
        else:
            irDayside = ""
            print("Warning: orbit type 8 found with blank limb observation")
        irNightside = ""
#        print("Limb obs found. Observation name = %s" %irDayside)
            
        
    orbit["completeOrbitPlan"] = \
        {
        "irIngressHigh":irIngressHigh,
        "irIngressLow":irIngressLow,
        "irEgressHigh":irEgressHigh,
        "irEgressLow":irEgressLow,
        "irDayside":irDayside,
        "irNightside":irNightside,
        
        "uvisIngress":"uvisIngress",
        "uvisEgress":"uvisEgress",
        "uvisDayside":"uvisDayside",
        "uvisNightside":"uvisNightside",
        
        "comment":genericObsTypes["comment"],
        }
    

    

def writeCompletePlanXlsx(mtp_number, orbit_list):
    """write complete observation plan to file"""
    with xlsxwriter.Workbook(BASE_DIRECTORY+os.sep+"nomad_mtp%03d_plan.xlsx" %mtp_number) as workbook:
        worksheet = workbook.add_worksheet()
        
        rowCounter = 0
        writeObservationPlan(worksheet, rowCounter, ["#orbitType","irIngressHigh","irIngressLow","uvisIngress","irEgressHigh","irEgressLow","uvisEgress","irDayside","uvisDayside","irNightside","uvisNightside","night2dayTerminator","comment"])
        
        for orbit in orbit_list:
            completeOrbitPlan = orbit["completeOrbitPlan"]
            row_to_write = [completeOrbitPlan["orbitTypeNumber"]]
            
            for genericObsType in ["irIngressHigh","irIngressLow","uvisIngress","irEgressHigh","irEgressLow","uvisEgress","irDayside","uvisDayside","irNightside","uvisNightside"]:
                row_to_write.append(completeOrbitPlan[genericObsType])
            
            row_to_write.append(orbit["daysideNadir"]["utcStart"])
            row_to_write.append(completeOrbitPlan["comment"])
            
            rowCounter += 1
            writeObservationPlan(worksheet, rowCounter, row_to_write)

    
writeCompletePlanXlsx(mtpNumber, orbitList)

    
#    #find cop table data
#    lnoObservationOrders, lnoIntegrationTime, lnoRhythm, lnoDetectorRows = getObsParameters(lnoObservationName,nadirObservationDict)
#
#    
#    inputDict = {"observationName":lnoObservationName, \
#                 "integrationTime":lnoIntegrationTime, \
#                 "orders":lnoObservationOrders, \
#                 "centreDetectorLine":LNO_CENTRE_DETECTOR_LINE, \
#                 "nRows":lnoDetectorRows, \
#                 "rhythm":lnoRhythm, \
#                 }
#    outputDict = getCopRows("lno", observationType, inputDict, silent=True)
#    fixedRow = outputDict["fixedRow"]
#    copRow1 = outputDict["copRow1"]
#    copRow2 = outputDict["copRow2"]
#    copRow1Description = outputDict["copRow1Description"]
#    copRow2Description = outputDict["copRow2Description"]            







#for orbit in orbitList: 
#    if "occultationRegions" in orbit.keys():
#        print(orbit["orbitNumber"])


print("Done! (%s)" %(datetime.strftime(datetime.now(), SPICE_DATETIME_FORMAT)))


