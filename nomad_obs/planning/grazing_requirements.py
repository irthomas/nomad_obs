# -*- coding: utf-8 -*-
"""
Created on Mon Jul 29 17:08:14 2024

@author: iant

GRAZING OCCULTATION CONSTRAINTS BY ALTITUDE, LATITUDE, ETC.
"""

from nomad_obs.config.constants import GRAZING_GEOMETRY


def check_grazing_geometry(mtp_constants, ir_or_uvis, lat, max_alt):

    mtpNumber = mtp_constants["mtpNumber"]

    if ir_or_uvis not in GRAZING_GEOMETRY.keys():
        print("Error: must choose ir or uvis to select grazing geometry requirements")

    lat_min_req = -999

    for (mtp_start, mtp_end), geom_reqs in GRAZING_GEOMETRY[ir_or_uvis].items():
        if mtpNumber >= mtp_start and mtpNumber <= mtp_end:
            lat_min_req = geom_reqs["lat_min"]
            lat_max_req = geom_reqs["lat_max"]
            max_altitude_req = geom_reqs["max_altitude"]

    if lat_min_req == -999:
        print("Error: mtp not in list of grazing requirement dictionary")

    # if geometry conditions met, return True, else False
    if max_alt <= max_altitude_req and lat >= lat_min_req and lat <= lat_max_req:
        return True
    else:
        return False


def get_max_grazing_altitude(mtp_constants):

    mtpNumber = mtp_constants["mtpNumber"]

    ir_max_altitude_req = -999
    uvis_max_altitude_req = -999

    # get max altitudes for both ir and uvis obs
    for (mtp_start, mtp_end), geom_reqs in GRAZING_GEOMETRY["ir"].items():
        if mtpNumber >= mtp_start and mtpNumber <= mtp_end:
            ir_max_altitude_req = geom_reqs["max_altitude"]

    for (mtp_start, mtp_end), geom_reqs in GRAZING_GEOMETRY["uvis"].items():
        if mtpNumber >= mtp_start and mtpNumber <= mtp_end:
            uvis_max_altitude_req = geom_reqs["max_altitude"]

    if ir_max_altitude_req == -999:
        print("Error: mtp not in list of ir grazing requirement dictionary")
        return -999

    if uvis_max_altitude_req == -999:
        print("Error: mtp not in list of uvis grazing requirement dictionary")
        return -999

    max_grazing_altitude = max(ir_max_altitude_req, uvis_max_altitude_req)
    return max_grazing_altitude
