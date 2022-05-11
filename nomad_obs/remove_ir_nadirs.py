# -*- coding: utf-8 -*-
"""
Created on Wed May 11 10:17:41 2022

@author: iant

PARSE ORBIT PLAN AND REMOVE SELECTED NADIRS

"""
import os
import shutil
import numpy as np
from openpyxl import load_workbook

from nomad_obs.mtp_inputs import getMtpConstants
from nomad_obs.config.paths import setupPaths, BASE_DIRECTORY

from nomad_obs.regions_of_interest import nadirRegionsOfInterest

from nomad_obs.io.orbit_plan_xlsx import getMtpPlanXlsx


mtpNumber = 55
mtpConstants = getMtpConstants(mtpNumber)
paths = setupPaths(mtpConstants)



def get_adjacent_indices(indices, n_orbits):
    out = []
    for index in indices:
        if index > 0:
            out.append(index - 1)
        out.append(index)
        if index < n_orbits - 1:
            out.append(index + 1)
        
    return sorted(list(set(out)))



#copy generic plan to orbit_plans
src = os.path.join(BASE_DIRECTORY, "nomad_mtp%03d_%s.xlsx" %(mtpNumber, "plan_generic"))
dest = os.path.join(paths["ORBIT_PLAN_PATH"], "nomad_mtp%03d_%s.xlsx" %(mtpNumber, "plan_generic"))
shutil.copyfile(src, dest)


#get data from spreadsheet
mtpPlan = getMtpPlanXlsx(mtpConstants, paths, "plan_generic")

irDaysides = [d["irDayside"] for d in mtpPlan]
irNightsides = [d["irNightside"] for d in mtpPlan]
comments = [d["comment"] for d in mtpPlan]


n_orbits = len(comments)

orbit_mask = np.zeros((n_orbits, 2))

#add MRO overlaps
indices_mro = [i for i,s in enumerate(comments) if "&mroOverlap" in s]
orbit_mask[indices_mro, 0] = 2


#add nadir regions
region_comments = ["&daysideMatch:%s" %s[0] for s in nadirRegionsOfInterest]
region_ratios = [s[2] for s in nadirRegionsOfInterest]

for i, comment in enumerate(comments):
    for region_comment, region_ratio in zip(region_comments, region_ratios):
        if region_comment in comment:
            orbit_mask[i, 0] = region_ratio



"""add forbidden"""
#find indices of orbits where daysides are not allowed
#during OCMs
#during ACS calibrations
#during NOMAD calibrations

#after nightside limbs
#before and after CaSSIS calibrations
#before and after Phobos/Deimos tracking

indices_day_limbs = [i for i,s in enumerate(irDaysides) if "irLimb" in s]
indices_night_limbs = [i for i,s in enumerate(irNightsides) if "irNightLimb" in s]
indices_cassis_cals = [i for i,s in enumerate(comments) if "&cassisSolarCalibration" in s]
indices_phobos = [i for i,s in enumerate(comments) if "&nomadPhobos" in s]
indices_deimos = [i for i,s in enumerate(comments) if "&nomadDeimos" in s]

#also add nomad cals - don't want to run nadirs on adjacent orbits
indices_nomad_cals = [i for i,s in enumerate(comments) if "&nomadSolarCalibration" in s]


indices_dict = {
    "ocm":[i for i,s in enumerate(comments) if "&possibleOCM" in s],
    "acs_cals":[i for i,s in enumerate(comments) if "&acsSolarCalibration" in s],
    "day_limbs":get_adjacent_indices(indices_day_limbs, n_orbits),
    "night_limbs":get_adjacent_indices(indices_night_limbs, n_orbits),
    "cassis_cals":get_adjacent_indices(indices_cassis_cals, n_orbits),
    "phobos":get_adjacent_indices(indices_phobos, n_orbits),
    "deimos":get_adjacent_indices(indices_deimos, n_orbits),
    "nomad_cals":get_adjacent_indices(indices_nomad_cals, n_orbits),
}

indices_off = []
for key, key_indices in indices_dict.items():
    for index in key_indices:
        if index not in indices_off:
            indices_off.append(index)
indices_off = sorted(indices_off)

#set orbit masks to -1 (not allowed)
orbit_mask[indices_off, 0] = -1



#overwrite irLimbs (slews with UVIS) with a different value (to be added to irDaysides at end)
orbit_mask[indices_day_limbs, 0] = 3



            

#fill in generic nadirs where no other observations
orbit_mask[0, 1] = 1
for i in range(3, n_orbits-2):
    #if all surrounding orbits are not allowed or unknown
    if np.all(orbit_mask[i-3:i+3, 0] < 1.0):
        if orbit_mask[i, 0] == 0:
            orbit_mask[i, 0] = 1
            orbit_mask[i, 1] = 1


#remove adjacent mro overlaps            
for i in range(0, n_orbits-1):
    if orbit_mask[i, 0] == 2:
        #if not mro overlap on previous orbit
        if orbit_mask[i-1, 0] != 2:
            orbit_mask[i, 1] = 1
        
        #if mro overlap on previous orbit but nadir not run
        elif orbit_mask[i-1, 1] == 0:
            orbit_mask[i, 1] = 1

#check regions, add probability
for i in range(0, n_orbits):
    if 0.0 < orbit_mask[i, 0] < 1.0:
        
        #if ratio > randomly generated number, add nadir
        rand = np.random.random()
        if orbit_mask[i, 0] > rand:
            orbit_mask[i, 1] = 1
            
            #remove adjacent nadirs
            if i not in [0, n_orbits-1]:
                if orbit_mask[i-1, 1] == 1:
                    orbit_mask[i-1, 1] = 0
                if orbit_mask[i+1, 1] == 1:
                    orbit_mask[i+1, 1] = 0

#finally add all irLimbs, Phobos, Deimos as switched on
for i in range(0, n_orbits):
    if orbit_mask[i, 0] == 3:
        orbit_mask[i, 1] = 1

        #remove adjacent nadirs
        if i not in [0, n_orbits-1]:
            if orbit_mask[i-1, 1] == 1:
                orbit_mask[i-1, 1] = 0
            if orbit_mask[i+1, 1] == 1:
                orbit_mask[i+1, 1] = 0
        

#now overwrite irDaysides with new list
nadirs = []
count = 0.0
for i in range(n_orbits):
    if orbit_mask[i, 1] == 1:
        if irDaysides[i] == "":
            nadirs.append("irDayside")
            count += 1.0
        else:
            nadirs.append(irDaysides[i])
            count += 1.0
    else:
        nadirs.append("")


print("Ratio of dayside limbs/nadirs in MTP: %0.1f%%" %(100.*count/n_orbits))


#update irDaysides in spreadsheet
wb = load_workbook(dest, data_only=True)
sheets = wb.sheetnames
Sheet1 = wb["Sheet1"]

row_number = 0

for nadir in nadirs:
    #copy to cell
    Sheet1.cell(row_number+2, 7+1).value = nadir #add 2, one for header, one for 1-indexing
    
    #change orbit type 3 to 14 if no nadir in 1st column
    if nadir == "":
        if Sheet1.cell(row_number+2, 0+1).value == 3:
            Sheet1.cell(row_number+2, 0+1).value = 14

    #change orbit type 14 to 3 if nadir in 1st column
    if nadir != "":
        if Sheet1.cell(row_number+2, 0+1).value == 14:
            Sheet1.cell(row_number+2, 0+1).value = 3
    row_number += 1


#save and close file
wb.save(dest) 
print("Generic orbit plan saved to %s" %dest)