# -*- coding: utf-8 -*-
"""
Created on Mon Apr 27 12:17:50 2020

@author: iant
"""

import numpy as np
import spiceypy as sp



from nomad_obs.planning.spice_functions import et2utc, getLonLatIncidenceLst
from nomad_obs.config.constants import SPICE_OBSERVER, SPICE_TARGET, SPICE_ABCORR
from nomad_obs.other.generic_functions import stop





def getNadirData(orbit_list, mtpConstants):
    """get all nadir data, add to orbit list"""
    utc_string_start = mtpConstants["utcStringStart"]
    utc_string_end = mtpConstants["utcStringEnd"]
    copVersion = mtpConstants["copVersion"]

    adjust = 0
    nintvals = 500
    stepSize = 1.0
    
    if utc_string_start == "" or utc_string_end == "" or copVersion == "":
        print("Error: Either utc_string_start, utc_string_end or copVersion have not been defined in obs_inputs.py. Please update and try again")
        stop()
    
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


