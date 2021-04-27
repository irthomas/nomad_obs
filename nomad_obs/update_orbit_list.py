# -*- coding: utf-8 -*-
"""
Created on Mon Apr 27 17:03:29 2020

@author: iant

SOMETIMES THE OPS TEAM'S OCCULTATION CALCULATIONS DIFFER
THIS CAN LEAD TO INCORRECT OCCULTATION TYPE E.G. MERGED INSTEAD OF GRAZING
THEREFORE COP ROWS CAN BE INSERTED INTO WRONG OUTPUT FILE AND UVIS INPUTS
HAVE INCORRECT LENGTH.

MANUALLY UPDATE SPECIFIC ORBITS TO MATCH BOJAN/CLADIO'S ORBIT TYPE ASSIGNMENT
"""


def updateWrongOrbitTypes(orbit_list, mtpConstants):
    """fudges for certain MTPs where grazing occultation is now a merged occ or vice versa
    find correct orbit and set allowedObservationTypes to that specified by ops team"""
    #TODO: come up with better way of doing this
    
    mtpNumber = mtpConstants["mtpNumber"]


    """note that index here is one less than the orbit number => orbit 228 is at index 226
    the index here is two less than the row number in the excel spreadsheet => row 188 is at index 186"""
    if mtpNumber == 10:
        orbit_list[227]["allowedObservationTypes"] = ["dayside", "grazing"]
        orbit_list[227]["grazing"] = orbit_list[227].pop("merged")

    elif mtpNumber == 20:
        orbit_list[150]["allowedObservationTypes"] = ["dayside", "merged"]

    elif mtpNumber == 21:
        orbit_list[4]["allowedObservationTypes"] = ["dayside", "grazing"]
        orbit_list[4]["grazing"] = orbit_list[4].pop("merged")

    elif mtpNumber == 25:
        orbit_list[6]["allowedObservationTypes"] = ["dayside", "grazing"]
        orbit_list[6]["grazing"] = orbit_list[6].pop("merged")

    elif mtpNumber == 26:
        orbit_list[167]["allowedObservationTypes"] = ["dayside", "grazing"]
        orbit_list[167]["grazing"] = orbit_list[167].pop("merged")

    elif mtpNumber == 34:
        orbit_list[29]["allowedObservationTypes"] = ["dayside", "grazing"]
        orbit_list[29]["grazing"] = orbit_list[29].pop("merged")
        orbit_list[232]["allowedObservationTypes"] = ["dayside", "grazing"]
        orbit_list[232]["grazing"] = orbit_list[232].pop("merged")

    elif mtpNumber == 36:
        orbit_list[186]["allowedObservationTypes"] = ["dayside", "grazing"]
        orbit_list[186]["grazing"] = orbit_list[186].pop("merged")

    elif mtpNumber == 40:
        orbit_list[33]["allowedObservationTypes"] = ["dayside", "grazing"]
        orbit_list[33]["grazing"] = orbit_list[33].pop("merged")
           
    return orbit_list



