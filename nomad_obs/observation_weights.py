# -*- coding: utf-8 -*-
"""
Created on Mon Apr 27 09:59:55 2020

@author: iant

ALLOCATE WEIGHTS TO EACH OBSERVATION NAME FOR EACH OBSERVATION TYPE

"""

# observation name and weighting


OCCULTATION_WEIGHTS = [

    # only for southern summer
    ["179 only #2"] * 16,  # order 179 only, priority v high only during southern summer MTPs 80-82 (HF search)

    # new MTP073+
    ["Fullscan fast step4 all #1"] * 16,  # 124(128)-168, priority v high
    ["Fullscan fast step5 all #1"] * 16,  # 114(119)-189, priority v high

    # new MTP073+
    ["6SUBD Nominal #54"] * 8,  # Nominal with 148, priority high
    ["6SUBD CO2 CO #34"] * 8,  # T, CO2 iso low, CO low, priority high
    ["6SUBD CO #6"] * 8,  # CO iso + Temp, priority high

    ["CO2 Fullscan Fast #5"] * 8,  # CO2 orders 141-150, priority high for GL


    # after prioritisation exercise
    ["6SUBD Nominal #53"] * 8,  # H #148 instead of 149 #121, 136, 169, 129, 148, 165
    ["6SUBD Nominal #52"] * 8,  # H #148 instead of 149 #121, 134, 169, 129, 148, 165
    ["6SUBD Nominal #51"] * 8,  # H #nominal + 129 #121, 136, 129, 169, 186, 190
    ["6SUBD Nominal #48"] * 8,  # H #nominal + 129 #121, 134, 129, 169, 186, 190
    ["6SUBD Nominal #45"] * 8,  # H #nominal + 129 #121, 136, 169, 129, 149, 165
    ["6SUBD Nominal #42"] * 8,  # H #nominal + 129 #121, 134, 169, 129, 149, 165
    ["6SUBD Nominal #12"] * 8,  # H #nominal + 126/129 #121, 134, 127, 129, 169, 190
    ["6SUBD Nominal #2"] * 8,  # H #119, 136, 149, 169, 186, 189
    ["6SUBD Nominal #1"] * 8,  # H #121, 134, 149, 169, 186, 190

    ["6SUBD CO2 H2O #14"] * 8,  # H #121, 134, 148, 132, 165, 169
    ["6SUBD CO2 H2O #13"] * 8,  # H
    ["6SUBD CO2 H2O #12"] * 8,  # H
    ["6SUBD CO2 H2O #11"] * 8,  # H
    ["6SUBD CO2 H2O CO #15"] * 8,  # H
    ["6SUBD CO2 CO #28"] * 8,  # H #co isotopes and temperature
    ["6SUBD CO2 #24"] * 8,  # H
    ["6SUBD CO2 #23"] * 8,  # H
    ["6SUBD CO2 #19"] * 8,  # H

    ["6SUBD Nom CO #7"] * 8,  # H #Mike Smith orders 148+186 together
    ["6SUBD Nom CO #6"] * 8,  # H #Mike Smith orders 148+186 together
    ["6SUBD CO #1"] * 8,  # H #Shohei

    ["Dust H2O 01"] * 8,  # H





    # after prioritisation exercise
    ["6SUBD Nom CO #1"] * 4,  # M

    ["6SUBD CO2 CO #29"] * 4,  # M #co isotopes and temperature
    ["6SUBD CO2 CO #27"] * 4,  # M
    ["6SUBD CO2 CO #25"] * 4,  # M
    ["6SUBD CO #2"] * 4,  # M

    ["HCL #10"] * 4,  # M #all HCL

    ["CO Fullscan Fast #2"] * 4,  # M 185-195









    # after prioritisation exercise
    ["6SUBD Nominal #11"] * 2,  # L #nominal + 126/129 #121, 134, 126, 129, 169, 190
    ["6SUBD Nom CO2 #1"] * 2,  # L #121, 134, 149, 164, 165, 169
    ["6SUBD Nom CH4 #2"] * 2,  # L #134, 136, 164, 169, 186, 190

    ["6SUBD CO2 #18"] * 2,  # L
    ["6SUBD CO2 #13"] * 2,  # L
    ["6SUBD CO2 #21"] * 2,  # L
    ["6SUBD CO2 Dipole #1"] * 2,  # L

    ["6SUBD CO #3"] * 2,  # L
    ["6SUBD CH4 H2O #1"] * 2,  # L #169, 132, 133, 134, 136, 137

    ["All Fullscan Fast #2"] * 2,  # L all
    ["All Fullscan Slow #2"] * 2,  # L all
    ["LNO Occultation Fullscan Fast #2"] * 2,  # L all

    ["CO2 Fullscan Fast #2"] * 2,  # L 160-170
    ["CO2 Fullscan Fast #3"] * 2,  # L 125-135
    ["CO2 Fullscan Fast #4"] * 2,  # L 165-175
]


OCCULTATION_MERGED_WEIGHTS = [
    # new MTP073+
    ["6SUBD Nominal #54"] * 8,  # Nominal with 148, priority high

    ["6SUBD Nominal #53"] * 8,  # H #148 instead of 149
    ["6SUBD Nominal #52"] * 8,  # H #148 instead of 149
    ["6SUBD Nominal #51"] * 8,  # H #nominal + 129
    ["6SUBD Nominal #48"] * 8,  # H #nominal + 129
    ["6SUBD Nominal #45"] * 8,  # H #nominal + 129
    ["6SUBD Nominal #42"] * 8,  # H #nominal + 129
    ["6SUBD Nominal #12"] * 8,  # H #nominal + 126/129
    ["6SUBD Nominal #2"] * 8,  # H
    ["6SUBD Nominal #1"] * 8,  # H

    ["All Fullscan Fast #2"] * 2,  # L all
    ["Fullscan fast step4 all #1"] * 4,  # 124(128)-168, priority v high
    ["Fullscan fast step5 all #1"] * 4,  # 114(119)-189, priority v high

]


OCCULTATION_GRAZING_WEIGHTS = [
    # new MTP073+
    ["6SUBD Nominal #54"] * 8,  # Nominal with 148, priority high

    ["6SUBD Nominal #53"] * 8,  # H #148 instead of 149
    ["6SUBD Nominal #52"] * 8,  # H #148 instead of 149
    ["6SUBD Nominal #51"] * 8,  # H #nominal + 129
    ["6SUBD Nominal #48"] * 8,  # H #nominal + 129
    ["6SUBD Nominal #45"] * 8,  # H #nominal + 129
    ["6SUBD Nominal #42"] * 8,  # H #nominal + 129
    ["6SUBD Nominal #12"] * 8,  # H #nominal + 126/129
    ["6SUBD Nominal #2"] * 8,  # H
    ["6SUBD Nominal #1"] * 8,  # H

    # ["All Fullscan Fast #2"] * 2,  # L all
    ["Fullscan fast step4 all #1"] * 4,  # 124(128)-168, priority v high
    ["Fullscan fast step5 all #1"] * 4,  # 114(119)-189, priority v high

]


# OCCULTATION_ACS_RIDEALONG_WEIGHTS = [
#     ["ACS Ridealong Science 2SUBD 01"] * 1,
# ]


OCCULTATION_CH4_REGION_WEIGHTS = [
    # ["6SUBD Nom CH4 #2"] * 1,  # L #134, 136, 164, 169, 186, 190
    # ["6SUBD CH4 H2O #1"] * 1,  # L #169, 132, 133, 134, 136, 137
    ["6SUBD Nominal #54"] * 2,  # Nominal with 148, priority high
    ["6SUBD Nominal #53"] * 2,  # H #148 instead of 149 #121, 136, 169, 129, 148, 165
    ["6SUBD Nominal #45"] * 2,  # H #nominal + 129 #121, 136, 169, 129, 149, 165
]


OCCULTATION_H2O_REGION_WEIGHTS = [
    ["6SUBD Nominal #54"] * 1,  # Nominal with 148, priority high
    ["6SUBD Nominal #53"] * 1,  # H #148 instead of 149 #121, 136, 169, 129, 148, 165
    ["6SUBD Nominal #52"] * 1,  # H #148 instead of 149 #121, 134, 169, 129, 148, 165
    ["6SUBD Nominal #51"] * 1,  # H #nominal + 129 #121, 136, 129, 169, 186, 190
    ["6SUBD Nominal #48"] * 1,  # H #nominal + 129 #121, 134, 129, 169, 186, 190
    ["6SUBD Nominal #45"] * 1,  # H #nominal + 129 #121, 136, 169, 129, 149, 165
    ["6SUBD Nominal #42"] * 1,  # H #nominal + 129 #121, 134, 169, 129, 149, 165
    ["6SUBD Nominal #12"] * 1,  # H #nominal + 126/129 #121, 134, 127, 129, 169, 190
]


# IN GENERAL, USE LESS CH4 ORDERS AS THESE ARE NORMALLY ADDED WHEN CROSSING OVER INTERESTING REGIONS
NADIR_WEIGHTS = [

    ["H2O CO 2SUBD #1"] * 32,  # VERY HIGH #168, 189

    ["H2O CO 3SUBD #2"] * 8,  # H #168, 189, 190
    ["Ice CO 2SUBD #2"] * 8,  # H #193, 189
    # ["Surface Ice 2SUBD #1"] * 32,  # H #132, 133

    ["Nominal 6SUBD #2"] * 8,  # H #196, 189, 168, 149, 134, 121
    ["Nominal 3SUBD 01"] * 8,  # H #167, 169, 190
    ["Ice H2O 2SUBD #1"] * 8,  # H #193, 168



    ["Surface Ice 3SUBD #2"] * 4,  # H #189, 132, 133
    ["Surface Ice 3SUBD #3"] * 4,  # H #193, 132, 133
    ["Nominal 4SUBD #2"] * 4,  # M #168, 134, 121, 189
    ["Nominal 4SUBD 01"] * 4,  # M #168, 134, 121, 190
    ["CH4 H2O 2SUBD 02"] * 4,  # M #168, 136
    ["CH4 3SUBD 01"] * 4,  # M #168, 134, 136
    ["Ice CH4 2SUBD #1"] * 4,  # M #193, 136
    ["Surface Ice 4SUBD 01"] * 4,  # M #199, 194, 193, 187
    ["Surface Ice 6SUBD 01"] * 4,  # M #199, 198, 194, 193, 187, 186




    ["H2O 2SUBD 01"] * 2,  # L #167, 169
    ["CH4 CO 2SUBD #3"] * 2,  # L #189, 136
    ["CH4 H2O 2SUBD 01"] * 2,  # L #168, 134
    ["Surface 3SUBD #3"] * 2,  # L #189, 194, 196

]


# limb 3 and 4 are more important than the others
# ORDER 164 FOR LIMBS > 50KM, CONTINUE 163-165 COMBINATIONS FOR CASSIS LIMBS
NADIR_LIMB_WEIGHTS = [
    ["Limb 2SUBD 07"] * 3,  # 164 x2
    ["Nominal Limb 01"] * 1,  # 164, 169
]

NADIR_NIGHT_LIMB_WEIGHTS = [
    ["Night Limb #2"] * 1,  # PATCHED FOR MTP031+
]

NADIR_NIGHTSIDE_WEIGHTS = [
    ["Night Limb #2"] * 1,  # PATCHED FOR MTP031+
]

NADIR_CH4_REGION_WEIGHTS = [
    ["H2O CO 2SUBD #1"] * 32,  # VERY HIGH #168, 189
    ["H2O CO 3SUBD #2"] * 8,
    ["CH4 CO 2SUBD #3"] * 1,  # L #189, 136
    ["CH4 H2O 2SUBD 01"] * 1,  # L #168, 134
]

NADIR_H2O_REGION_WEIGHTS = [
    ["H2O CO 2SUBD #1"] * 8,  # H #168, 189
]

NADIR_SURFACE_REGION_WEIGHTS = [
    ["H2O CO 2SUBD #1"] * 2,  # VERY HIGH #168, 189
    # ["Surface 3SUBD #3"] * 1,  # L #189, 194, 196
    ["Ice CO 2SUBD #2"] * 1,  # H #193, 189
    ["Ice H2O 2SUBD #1"] * 1,  # H #193, 168
]

NADIR_ICE_REGION_WEIGHTS = [
    # ["H2O CO 3SUBD #2"] * 1, #168,189,190
    ["Surface Ice 2SUBD #1"] * 1,  # 132, 133
    ["Ice CO 2SUBD #2"] * 1,  # 189, 193
    ["Ice CO 2SUBD #3"] * 1,  # 193, 193
]


observationCycles = {
    "OccultationCycleNominal": ["Occultation", [item for sublist in OCCULTATION_WEIGHTS for item in sublist]],
    "OccultationCycleMerged": ["Occultation", [item for sublist in OCCULTATION_MERGED_WEIGHTS for item in sublist]],
    "OccultationCycleGrazing": ["Occultation", [item for sublist in OCCULTATION_GRAZING_WEIGHTS for item in sublist]],

    "NadirCycleNominal": ["Nadir", [item for sublist in NADIR_WEIGHTS for item in sublist]],
    "NadirCycleLimb": ["Nadir", [item for sublist in NADIR_LIMB_WEIGHTS for item in sublist]],
    "NadirCycleNightside": ["Nadir", [item for sublist in NADIR_NIGHTSIDE_WEIGHTS for item in sublist]],
    "NadirCycleNightLimb": ["Nadir", [item for sublist in NADIR_NIGHT_LIMB_WEIGHTS for item in sublist]],

    "OccultationCycleCH4": ["Occultation", [item for sublist in OCCULTATION_CH4_REGION_WEIGHTS for item in sublist]],
    "OccultationCycleH2O": ["Occultation", [item for sublist in OCCULTATION_H2O_REGION_WEIGHTS for item in sublist]],
    "NadirCycleCH4": ["Nadir", [item for sublist in NADIR_CH4_REGION_WEIGHTS for item in sublist]],
    "NadirCycleH2O": ["Nadir", [item for sublist in NADIR_H2O_REGION_WEIGHTS for item in sublist]],
    "NadirCycleSurface": ["Nadir", [item for sublist in NADIR_SURFACE_REGION_WEIGHTS for item in sublist]],
    "NadirCycleIce": ["Nadir", [item for sublist in NADIR_ICE_REGION_WEIGHTS for item in sublist]],
}


"""list NOMAD ACS joint occultations"""
# for obsLists in SOC_JOINT_OBSERVATION_NAMES.values():
#    for obs in obsLists:
#        orders = occultationObservationDict[obs][0]
#        print ("%s;" %obs + " %i," * len(orders) % tuple(orders))


"""list observation cycles"""
# cycleName = "OccultationCycleNominal"
# cycleName = "NadirCycleNominal"
# cycleName = "NadirCycleCH4"
#
# obsNames = observationCycles[cycleName][1]
#
# uniqueObsNames = list(set(obsNames))
# uniqueObsData = [{"Occultation": occultationObservationDict, "Nadir": nadirObservationDict}[observationCycles[cycleName][0]][obsName]
#                  for obsName in uniqueObsNames]
#
# counts = []
# for uniqueObsName in uniqueObsNames:
#    counts.append(obsNames.count(uniqueObsName))
#
# sort by number of counts
# countsSorted = [x for x,_,_ in reversed(sorted(zip(counts,uniqueObsNames,uniqueObsData)))]
# uniqueObsNamesSorted = [x for _,x,_ in reversed(sorted(zip(counts,uniqueObsNames,uniqueObsData)))]
# uniqueObsDataSorted = [x for _,_,x in reversed(sorted(zip(counts,uniqueObsNames,uniqueObsData)))]
#
# totalCounts = sum(counts)
# print("Frequency,Name,Orders")
# for count, obsName, obsData in zip(countsSorted, uniqueObsNamesSorted, uniqueObsDataSorted):
#    print("%0.1f%%,%s,%s" %((count/totalCounts)*100.0, obsName, ("%s" %obsData[0]).replace("[","").replace("]","").replace(" ","")))
