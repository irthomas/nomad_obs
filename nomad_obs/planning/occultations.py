# -*- coding: utf-8 -*-
"""
Created on Mon Apr 27 12:18:44 2020

@author: iant
"""

import numpy as np
import spiceypy as sp



from nomad_obs.planning.spice_functions import et2utc, getLonLatLst
from nomad_obs.config.constants import SPICE_OBSERVER, SPICE_ABCORR
from nomad_obs.planning.spice_functions import findTangentAltitudeTime, getTangentAltitude

from nomad_obs.config.constants import INITIALISATION_TIME, PRECOOLING_TIME
from nomad_obs.config.constants import OCCULTATION_SEARCH_STEP_SIZE, MAXIMUM_SO_ALTITUDE, SO_TRANSITION_ALTITUDE, MAXIMUM_GRAZING_ALTITUDE, MINIMUM_TIME_BETWEEN_OCCULTATIONS, SO_REFERENCE_DURATION



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


