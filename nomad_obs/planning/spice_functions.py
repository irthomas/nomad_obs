# -*- coding: utf-8 -*-
"""
Created on Mon Apr 27 12:14:37 2020

@author: iant
"""


import numpy as np
import spiceypy as sp


from nomad_obs.config.constants import SPICE_METHOD, SPICE_FORMATSTR, SPICE_PRECISION, SPICE_SHAPE, SPICE_OBSERVER, SPICE_REF, SPICE_MARS_AXES
from nomad_obs.config.constants import SPICE_TARGET, SPICE_ABCORR



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
    lst_hours = float(lst[0:2]) + float(lst[3:5])/60.0 + float(lst[6:8])/3600.0
    return lon, lat, incidence, lst_hours


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
    lst_hours = float(lst[0:2]) + float(lst[3:5])/60.0 + float(lst[6:8])/3600.0
    return lon, lat, lst_hours

