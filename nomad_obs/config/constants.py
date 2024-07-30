# -*- coding: utf-8 -*-
"""
Created on Mon Apr 27 12:12:25 2020

@author: iant
"""
import spiceypy as sp

# ignore missing files? E.g. when running very old MTPs
# IGNORE_MISSING = True
IGNORE_MISSING = False


# spice constants
SPICE_ABCORR = "None"
SPICE_TARGET = "MARS"
SPICE_METHOD = "Intercept: ellipsoid"
SPICE_FORMATSTR = "C"
SPICE_PRECISION = 0
SPICE_SHAPE = "Ellipsoid"
SPICE_OBSERVER = "-143"
SPICE_REF = "IAU_MARS"
SPICE_MARS_AXES = sp.bodvrd("MARS", "RADII", 3)[1]  # get mars axis values
SPICE_DATETIME_FORMAT = "%Y %b %d %H:%M:%S"


# output file channel codes
SO_CHANNEL_CODE = 0
LNO_CHANNEL_CODE = 1
OFF_CHANNEL_CODE = -1

# tc20 parameters
PRECOOLING_COP_ROW = 1
OFF_COP_ROW = -1

# universal constants
INITIALISATION_TIME = 10  # s
MINIMUM_TELECOMMAND_INTERVAL = 5  # s
# PRECOOLING_TIME = 600 #s #see mtp inputs
THERMAL_RULE_ON_TIME = 80 * 60  # s

# detector constants
LNO_CENTRE_DETECTOR_LINE = 152

# occultation constants
OCCULTATION_SEARCH_STEP_SIZE = 2.0  # s
MAXIMUM_SO_ALTITUDE = 250.0  # km
SO_TRANSITION_ALTITUDE = 50.0  # km


MINIMUM_TIME_BETWEEN_OCCULTATIONS = {440: 519, 600: 675}  # s define as merged occ if less than this. Dict key is the precooling time
SO_REFERENCE_DURATION = 30  # s
ACCEPTABLE_MTP_OCCULTATION_TIME_ERROR = 20.0  # s

# if checking whether a limb is correctly on the dayside or nightside, apply this mergin
EVENT_TIMING_MARGIN = 30.0  # s

# nadir constants
NADIR_SEARCH_STEP_SIZE = 30.0  # s
MAXIMUM_SOLAR_INCIDENCE_ANGLE_ROUGH = 92.0  # deg
TIME_TO_START_DAYSIDE_BEFORE_TERMINATOR = 120  # s
TIME_TO_END_DAYSIDE_AFTER_TERMINATOR = 120  # s
ACCEPTABLE_MTP_NADIR_TIME_ERROR = 20.0  # s

# max solar incidence angle when searching for nadir regions of interest. Higher value = lower quality data but more matches.
MAXIMUM_SEARCH_INCIDENCE_ANGLE = 85.0


# MRO overlap constraints
MRO_OVERLAP_LATLON_CONSTRAINT = 5
MRO_OVERLAP_LST_CONSTRAINT = 30


# orbit types. Remember to add type numbers to functions if more are created!
UVIS_MULTIPLE_TC_NADIR_ORBIT_TYPES = [2, 4, 6]
LIMB_ORBIT_TYPES = [8, 28]
UVIS_DEFAULT_ORBIT_TYPE = 14  # 14 = UVIS 1xTC per dayside. 4 = 3xTCs per dayside

# for no ir or uvis occultation, e.g. for grazings under the max altitude requirement but not matching the geometry requirements
IR_OFF_CODE = "irOFF"
UVIS_OFF_CODE = "uvisOFF"

# plot constants
FIG_X = 10
FIG_Y = 6


# diffraction orders for specific observations, for writing orbits where they are measured
# channel / observation type / objective
OBJECTIVE_ORDERS = {
    "SO": {},
    "LNO": {"irDayside":
            {"H2O": [167, 168, 169], "CO": [189, 190, 191]},
            }
}

# MAXIMUM_GRAZING_ALTITUDE = 100.0  # km also for searching for region of interest matches #replaced by function
# (MTP start, MTP end) : "ir" or "uvis": minimum and maximum tangent point latitude and maximum altitude
GRAZING_GEOMETRY = {
    "ir": {
        (1, 83): {"lat_min": -90.0, "lat_max": 90.0, "max_altitude": 100.0},
        (84, 999): {"lat_min": -15.0, "lat_max": 15.0, "max_altitude": 50.0},
    },
    "uvis": {
        (1, 83): {"lat_min": -90.0, "lat_max": 90.0, "max_altitude": 100.0},
        (84, 999): {"lat_min": -45.0, "lat_max": 45.0, "max_altitude": 70.0},
    }
}


if IGNORE_MISSING:
    print("Warning: IGNORE_MISSING = True. Don't run like this for planning new MTPs!")
