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


    """note that index here is one less than the orbit number => orbit 227 is at index 226
    the index here is two less than the row number in the excel spreadsheet => row 188 is at index 186"""
    if mtpNumber == 7:
        orbit_list[195]["allowedObservationTypes"] = ["dayside", "grazing"]
        orbit_list[195]["grazing"] = orbit_list[195].pop("merged")

    if mtpNumber == 10:
        #switch a merged for a grazing
        orbit_list[227]["allowedObservationTypes"] = ["dayside", "grazing"]
        orbit_list[227]["grazing"] = orbit_list[227].pop("merged")

    elif mtpNumber == 20:
        #add merged occultation
        orbit_list[150]["allowedObservationTypes"] = ["dayside", "merged"]

    elif mtpNumber == 21:
        #switch a merged for a grazing
        orbit_list[4]["allowedObservationTypes"] = ["dayside", "grazing"]
        orbit_list[4]["grazing"] = orbit_list[4].pop("merged")

    elif mtpNumber == 25:
        #switch a merged for a grazing
        orbit_list[6]["allowedObservationTypes"] = ["dayside", "grazing"]
        orbit_list[6]["grazing"] = orbit_list[6].pop("merged")

    elif mtpNumber == 26:
        #switch a merged for a grazing
        orbit_list[167]["allowedObservationTypes"] = ["dayside", "grazing"]
        orbit_list[167]["grazing"] = orbit_list[167].pop("merged")

    elif mtpNumber == 34:
        #switch a merged for a grazing
        orbit_list[29]["allowedObservationTypes"] = ["dayside", "grazing"]
        orbit_list[29]["grazing"] = orbit_list[29].pop("merged")
        #switch a merged for a grazing
        orbit_list[232]["allowedObservationTypes"] = ["dayside", "grazing"]
        orbit_list[232]["grazing"] = orbit_list[232].pop("merged")

    elif mtpNumber == 36:
        #switch a merged for a grazing
        orbit_list[186]["allowedObservationTypes"] = ["dayside", "grazing"]
        orbit_list[186]["grazing"] = orbit_list[186].pop("merged")

    elif mtpNumber == 40:
        #switch a merged for a grazing
        orbit_list[33]["allowedObservationTypes"] = ["dayside", "grazing"]
        orbit_list[33]["grazing"] = orbit_list[33].pop("merged")

    elif mtpNumber == 44:
        #switch a merged for a grazing
        orbit_list[50]["allowedObservationTypes"] = ["dayside", "grazing"]
        orbit_list[50]["grazing"] = orbit_list[50].pop("merged")

    elif mtpNumber == 49:
        #switch a merged for a grazing
        index = 13
        orbit_list[index]["allowedObservationTypes"] = ["dayside", "grazing"]
        orbit_list[index]["grazing"] = orbit_list[index].pop("merged")

    elif mtpNumber == 51:
        #switch a merged for a grazing
        xlsx_row = 44 #row number of the observation in the excel spreadsheet
        orbit_list[xlsx_row - 2]["allowedObservationTypes"] = ["dayside", "grazing"]
        orbit_list[xlsx_row - 2]["grazing"] = orbit_list[xlsx_row - 2].pop("merged")

    elif mtpNumber == 52:
        #switch a merged for a grazing
        xlsx_row = 297 #row number of the observation in the excel spreadsheet
        orbit_list[xlsx_row - 2]["allowedObservationTypes"] = ["dayside", "grazing"]
        orbit_list[xlsx_row - 2]["grazing"] = orbit_list[xlsx_row - 2].pop("merged")

    elif mtpNumber == 55:
        #switch a merged for a grazing
        xlsx_row = 116 #row number of the observation in the excel spreadsheet
        orbit_list[xlsx_row - 2]["allowedObservationTypes"] = ["dayside", "grazing"]
        orbit_list[xlsx_row - 2]["grazing"] = orbit_list[xlsx_row - 2].pop("merged")
        
    elif mtpNumber == 59:
        #switch a merged for a grazing
        xlsx_row = 147 #row number of the observation in the excel spreadsheet
        orbit_list[xlsx_row - 2]["allowedObservationTypes"] = ["dayside", "grazing"]
        orbit_list[xlsx_row - 2]["grazing"] = orbit_list[xlsx_row - 2].pop("merged")

    elif mtpNumber == 61:
        #switch a merged for a grazing
        xlsx_row = 168 #row number of the observation in the excel spreadsheet
        orbit_list[xlsx_row - 2]["allowedObservationTypes"] = ["dayside", "grazing"]
        orbit_list[xlsx_row - 2]["grazing"] = orbit_list[xlsx_row - 2].pop("merged")
        
    return orbit_list



