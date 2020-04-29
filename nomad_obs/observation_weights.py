# -*- coding: utf-8 -*-
"""
Created on Mon Apr 27 09:59:55 2020

@author: iant

ALLOCATE WEIGHTS TO EACH OBSERVATION NAME FOR EACH OBSERVATION TYPE

"""

#observation name and weighting
OCCULTATION_WEIGHTS = [

    ["6SUBD Nominal #1"] * 20, 
    ["6SUBD Nominal #2"] * 20, 
    ["6SUBD Nominal #3"] * 20, 
    ["6SUBD Nom CO2 #1"] * 5,
    ["6SUBD Nom CO2 #2"] * 5,
    ["6SUBD Nom CH4 #1"] * 5,
    ["6SUBD Nom CH4 #2"] * 5,
    ["6SUBD Nom CO #1"] * 5,
    ["6SUBD Nom CO #2"] * 5,
    ["6SUBD Nom CO #3"] * 5,
    ["6SUBD Nom CO #4"] * 5,
    ["6SUBD Nom CO #5"] * 5,
     
    ["CO2 100km #1"] * 10,
     
    ["6SUBD CH4 #1"] * 3,
    ["6SUBD CO H2O #1"] * 3,
    ["6SUBD CO H2O #2"] * 3,
    ["6SUBD CO2 CO #1"] * 3,
    ["6SUBD CH4 H2O #1"] * 3,
    ["All Fullscan Fast #2"] * 3,
    ["All Fullscan Slow #2"] * 1,
    ["CO2 Fullscan Fast #2"] * 1,
    ["CO Fullscan Fast #2"] * 1,
    ["LNO Occultation Fullscan Fast #2"] * 3,
    ["119 only #2"] * 1,
    ["120 only #2"] * 1,
    ["121 only #2"] * 1,

    ["BgSubTest 03"] * 3, #reduce by one in MTP029
    ["BgSubTest 04"] * 3,
    ["BgSubTest 05"] * 3,
    ["BgSubTest 06"] * 3,
    ["Nominal Science 1xCO2 LA05"] * 2, #reduce by one in MTP029
    ["Nominal Science 1xCO2 LA06"] * 2,
    ["Nominal Science 1xCO2 LA01"] * 2,
    ["Nominal Science 1xCO2 HA01"] * 2,
    ["Nominal Science 1xCO2 LA02"] * 2,
    ["Nominal Science 1xCO2 HA02"] * 2,
    ["Nominal Science 1xCO2 LA03"] * 2,
    ["Nominal Science 1xCO2 HA03"] * 2,
    ["Nominal Science 1xCO2 LA04"] * 2,
    ["Nominal Science 1xCO2 HA04"] * 2,
    ["Dust H2O 01"] * 1,
    ["Water Ice 01"] * 1,
    ["CO 01"] * 1,
    ["HDO 01"] * 1,
    ["AER 01"] * 1,
    
    #new MTP025+
    ["6SUBD CO2 #1"] * 9, #reduce at MTP029
    ["6SUBD CO2 #10"] * 9, #reduce at MTP029

    #MTP028+ CO2 M1/E2 and HCl
    ["126 only #2"] * 9,
    ["127 only #2"] * 9,
    ["129 only #2"] * 9,

     
    ["132 only #2"] * 3,
    ["133 only #2"] * 4,
    ["134 only #2"] * 5,
    ["6SUBD CO2 Dipole #1"] * 4,
    ["CO2 Fullscan Fast #3"] * 4,

]

        
OCCULTATION_MERGED_WEIGHTS = [
#        ["Nominal Science 1xCO2 LA05"] * 1,
#        ["BgSubTest 05"] * 1,
#        ["Nominal Science 1xCO2 LA05"] * 1,
#        ["BgSubTest 06"] * 1,
#        ["All Fullscan Fast"] * 1,
#        ["CH4 01"] * 1,
#        ["134 with 1xDark"] * 1, #special calibration

    ["6SUBD Nominal #1"] * 2, 
    ["6SUBD Nominal #2"] * 2, 
    ["6SUBD Nominal #3"] * 2, 
    ["6SUBD CH4 #1"] * 1,
    ["All Fullscan Fast #2"] * 1,
    ["134 only #2"] * 1,
    ["136 only #2"] * 1,
    
    
]

        
OCCULTATION_GRAZING_WEIGHTS = [
    ["6SUBD Nominal #1"] * 2, 
    ["6SUBD Nominal #2"] * 2, 
    ["6SUBD Nominal #3"] * 2, 
    ["6SUBD CH4 #1"] * 1,
    ["All Fullscan Fast #2"] * 1,
    ["134 only #2"] * 1,
    ["136 only #2"] * 1,
]

OCCULTATION_ACS_RIDEALONG_WEIGHTS = [
    ["ACS Ridealong Science 2SUBD 01"] * 1,
]




OCCULTATION_CH4_REGION_WEIGHTS = [
    ["134 only #2"] * 1, 
    ["136 only #2"] * 3, 
    ["6SUBD CH4 #1"] * 1,
]


OCCULTATION_H2O_REGION_WEIGHTS = [
    ["6SUBD Nominal #1"] * 3, 
    ["6SUBD Nominal #2"] * 1, 
    ["6SUBD Nominal #3"] * 1, 
]

        
#IN GENERAL, USE LESS CH4 ORDERS AS THESE ARE NORMALLY ADDED WHEN CROSSING OVER INTERESTING REGIONS
NADIR_WEIGHTS = [
#        ["LNO Ice Index 2SUBD 01"] * 1, #MTP013+ F.SCHMIDT
#        ["H2O 2SUBD 01"] * 1, #167 & 169
#        ["HDO H2O 2SUBD 02"] * 1, #168 & 124 S.AOKI
#        ["AER H2Oi 3SUBD 01"] * 1, #127, 131, 169 AEROSOLS
#        ["CH4 3SUBD 01"] * 1, #134, 136, 168
#        ["HDO H2O 2SUBD 03"] * 1, #121 & 168 
#        ["Nominal 6SUBD 01"] * 1, #6 ORDERS DUST
#        ["H2O CO 2SUBD 01"] * 1, #168, 190
#        ["CO H2O 3SUBD 01"] * 1, #191, 190, 168
#        ["CH4 2SUBD 03"] * 1, #136 x 2
#        ["Nominal 4SUBD 01"] * 1, #121, 134, 168, 190

    ["Nominal 6SUBD 01"] * 10,
    ["Nominal 4SUBD 01"] * 10,
    ["Nominal 3SUBD 01"] * 10,
    ["H2O 2SUBD 01"] * 6,
    ["H2O CO 2SUBD 01"] * 6,
    ["CO H2O 3SUBD 01"] * 6,

    ["HDO CO 3SUBD 02"] * 4,
    ["CH4 3SUBD 01"] * 4,
    ["CH4 H2O 2SUBD 02"] * 4,
    ["CH4 H2O 2SUBD 01"] * 4,
    ["CH4 2SUBD 03"] * 4,
    ["CH4 2SUBD 02"] * 4,
    ["CH4 CO 2SUBD 01"] * 4,
    ["CH4 CO 2SUBD 02"] * 4,
    ["HDO H2O 2SUBD 02"] * 4,
    ["HDO H2O 2SUBD 03"] * 4,
    ["CO Fullscan #2"] * 1,
    ["H2O Fullscan #2"] * 1,

    ["Ice CH4 2SUBD #1"] * 5,
    ["Ice H2O 2SUBD #1"] * 5,
    ["Ice CO 2SUBD #1"] * 5,

    ["Surface Ice 4SUBD 01"] * 1, #increase when beta angle high
    ["Surface Ice 6SUBD 01"] * 1,
    ["Surface Ice 4SUBD 02"] * 1,
    ["Surface Ice 3SUBD 01"] * 1,
     
]


        
#limb 3 and 4 are more important than the others
#ORDER 164 FOR LIMBS > 50KM, CONTINUE 163-165 COMBINATIONS FOR CASSIS LIMBS
NADIR_LIMB_WEIGHTS = [
    ["Limb 2SUBD 07"] * 3,
    ["Nominal Limb 01"] * 1,
]

NADIR_NIGHT_LIMB_WEIGHTS = [
    ["Limb 2SUBD 07"] * 3,
    ["Nominal Limb 01"] * 1,
]
        
NADIR_NIGHTSIDE_WEIGHTS = [
    ["Limb 2SUBD 07"] * 1,
]

        
        
        
        
NADIR_CH4_REGION_WEIGHTS = [
    ["CH4 3SUBD 01"] * 1,
    ["CH4 H2O 2SUBD 02"] * 2,
    ["CH4 H2O 2SUBD 01"] * 1,
    ["CH4 2SUBD 03"] * 2,
    ["CH4 2SUBD 02"] * 1,
    ["CH4 CO 2SUBD 01"] * 2,
    ["CH4 CO 2SUBD 02"] * 1,        
]        

NADIR_H2O_REGION_WEIGHTS = [
    ["H2O 2SUBD 01"] * 4,        
    ["Nominal 3SUBD 01"] * 1,
]        
        

NADIR_SURFACE_REGION_WEIGHTS = [
    ["Surface 3SUBD 02"] * 3,
    ["Nominal 3SUBD 01"] * 1,
]
    
observationCycles = {
        "OccultationCycleNominal":["Occultation", [item for sublist in OCCULTATION_WEIGHTS for item in sublist]],
        "OccultationCycleMerged":["Occultation", [item for sublist in OCCULTATION_MERGED_WEIGHTS for item in sublist]],
        "OccultationCycleGrazing":["Occultation", [item for sublist in OCCULTATION_GRAZING_WEIGHTS for item in sublist]],

        "NadirCycleNominal":["Nadir", [item for sublist in NADIR_WEIGHTS for item in sublist]],
        "NadirCycleLimb":["Nadir", [item for sublist in NADIR_LIMB_WEIGHTS for item in sublist]],
        "NadirCycleNightside":["Nadir", [item for sublist in NADIR_NIGHTSIDE_WEIGHTS for item in sublist]],
        "NadirCycleNightLimb":["Nadir", [item for sublist in NADIR_NIGHT_LIMB_WEIGHTS for item in sublist]],

        "OccultationCycleCH4":["Occultation", [item for sublist in OCCULTATION_CH4_REGION_WEIGHTS for item in sublist]],
        "OccultationCycleH2O":["Occultation", [item for sublist in OCCULTATION_H2O_REGION_WEIGHTS for item in sublist]],
        "NadirCycleCH4":["Nadir", [item for sublist in NADIR_CH4_REGION_WEIGHTS for item in sublist]],
        "NadirCycleH2O":["Nadir", [item for sublist in NADIR_H2O_REGION_WEIGHTS for item in sublist]],
        "NadirCycleSurface":["Nadir", [item for sublist in NADIR_SURFACE_REGION_WEIGHTS for item in sublist]],
}


        
        
        




"""list NOMAD ACS joint occultations"""
#for obsLists in SOC_JOINT_OBSERVATION_NAMES.values():
#    for obs in obsLists:
#        orders = occultationObservationDict[obs][0]
#        print ("%s;" %obs + " %i," * len(orders) % tuple(orders))



"""list observation cycles"""
#cycleName = "OccultationCycleNominal"
#cycleName = "NadirCycleNominal"
#cycleName = "NadirCycleCH4"
#
#obsNames = observationCycles[cycleName][1]
#
#uniqueObsNames = list(set(obsNames))
#uniqueObsData = [{"Occultation":occultationObservationDict, "Nadir":nadirObservationDict}[observationCycles[cycleName][0]][obsName] for obsName in uniqueObsNames]
#
#counts = []
#for uniqueObsName in uniqueObsNames:
#    counts.append(obsNames.count(uniqueObsName))
#
##sort by number of counts
#countsSorted = [x for x,_,_ in reversed(sorted(zip(counts,uniqueObsNames,uniqueObsData)))]
#uniqueObsNamesSorted = [x for _,x,_ in reversed(sorted(zip(counts,uniqueObsNames,uniqueObsData)))]
#uniqueObsDataSorted = [x for _,_,x in reversed(sorted(zip(counts,uniqueObsNames,uniqueObsData)))]
#
#totalCounts = sum(counts)
#print("Frequency,Name,Orders")
#for count, obsName, obsData in zip(countsSorted, uniqueObsNamesSorted, uniqueObsDataSorted):
#    print("%0.1f%%,%s,%s" %((count/totalCounts)*100.0, obsName, ("%s" %obsData[0]).replace("[","").replace("]","").replace(" ","")))
    
    
