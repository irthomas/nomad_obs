# -*- coding: utf-8 -*-
"""
Created on Tue Jun  2 16:26:17 2020

@author: iant
"""
import os

from nomad_obs.config.constants import MRO_OVERLAP_LATLON_CONSTRAINT, MRO_OVERLAP_LST_CONSTRAINT


def getMroOverlaps(paths):
    """read in list of orbits from MRO overlap summary files"""
    
    dir_name = "%ideg_latlon_%imin_LST" %(MRO_OVERLAP_LATLON_CONSTRAINT, MRO_OVERLAP_LST_CONSTRAINT)

    with open(os.path.join(paths["SUMMARY_FILE_PATH"], dir_name, "TGO_AND_MRO_OVERLAP_IN_ONE_MTP_%ideg.txt" %MRO_OVERLAP_LATLON_CONSTRAINT)) as f:
        lines = f.readlines()
        
    overlap_orbit_numbers = []
    for line in lines[1:]:
        line_split = line.strip().split(",")
        overlap_orbit_numbers.append(int(line_split[2])) #orbits start at 1 in the dictionary list

    return overlap_orbit_numbers





# mroOverlapOrbits = getMroOverlaps(paths)
