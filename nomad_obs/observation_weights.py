# -*- coding: utf-8 -*-
"""
Created on Mon Apr 27 09:59:55 2020

@author: iant

ALLOCATE WEIGHTS TO EACH OBSERVATION NAME FOR EACH OBSERVATION TYPE

"""

#observation name and weighting
OCCULTATION_WEIGHTS = [

    ["6SUBD CO2 H2O #11"] * 6,
    ["6SUBD CO2 #12"] * 4,
    ["6SUBD CO2 #13"] * 4,
    ["6SUBD CO2 H2O #14"] * 6,
    ["6SUBD CO2 H2O CO #15"] * 6,
    ["6SUBD CO2 #16"] * 4, #Miguel
    ["6SUBD CO2 #17"] * 4,
    ["6SUBD CO2 #18"] * 2,
    ["6SUBD CO2 #19"] * 4,
    ["6SUBD CO2 #20"] * 4,
    ["6SUBD CO2 #21"] * 2,
    ["6SUBD CO2 #22"] * 4,
    ["6SUBD CO2 #23"] * 4,
    ["6SUBD CO2 #24"] * 4,
    ["6SUBD CO2 CO #25"] * 4,
    ["6SUBD CO2 CO #26"] * 2,
    ["6SUBD CO2 CO #27"] * 4,
    ["6SUBD CO2 H2O #12"] * 6,
    ["6SUBD CO2 H2O #13"] * 6,
    ["6SUBD CO #1"] * 4, #Shohei
    ["6SUBD CO #2"] * 4 ,#Shohei
    ["6SUBD CO #3"] * 4, #Shohei
    ["6SUBD CO #4"] * 4, #Shohei
    ["6SUBD CO #5"] * 4, #Shohei  



    ["6SUBD Nominal #1"] * 4, 
    ["6SUBD Nominal #2"] * 4, 
    ["6SUBD Nominal #3"] * 4, 
    ["6SUBD Nom CO2 #1"] * 4,
    ["6SUBD Nom CO2 #2"] * 4,
    ["6SUBD Nom CH4 #1"] * 4,
    ["6SUBD Nom CH4 #2"] * 4,

    ["6SUBD Nominal #42"] * 8, #nominal + 129
    ["6SUBD Nominal #45"] * 8, #nominal + 129
    ["6SUBD Nominal #48"] * 8, #nominal + 129
    ["6SUBD Nominal #51"] * 8, #nominal + 129
    ["6SUBD Nominal #11"] * 8, #nominal + 126/129
    ["6SUBD Nominal #12"] * 8, #nominal + 127/129


    ["6SUBD Nom CO #1"] * 2,
    ["6SUBD Nom CO #2"] * 2,
    ["6SUBD Nom CO #3"] * 2,
    ["6SUBD Nom CO #4"] * 2,
    ["6SUBD Nom CO #5"] * 2,

    ["6SUBD Nom CO #6"] * 10, #Mike Smith orders 148+186 together
    ["6SUBD Nom CO #7"] * 10, #Mike Smith orders 148+186 together

     
    ["CO2 100km #1"] * 8,
     
    ["6SUBD CH4 #1"] * 3,
    ["6SUBD CO H2O #1"] * 3,
    ["6SUBD CO H2O #2"] * 3,
    ["6SUBD CO2 CO #1"] * 3,
    ["6SUBD CH4 H2O #1"] * 3,


    ["All Fullscan Fast #2"] * 10,
    ["All Fullscan Slow #2"] * 5,
    ["CO2 Fullscan Fast #2"] * 3,
    ["CO2 Fullscan Fast #4"] * 7, #orders 165-175 #reduce gradually
    ["CO Fullscan Fast #2"] * 3,
    ["LNO Occultation Fullscan Fast #2"] * 5,
    
    #new MTP025+
    ["6SUBD CO2 #1"] * 3, #reduce from MTP029 onwards to 3
    ["6SUBD CO2 #10"] * 3, #reduce from MTP029 onwards to 3

    #MTP028+ CO2 M1/E2 and HCl. reduce as new patches become available.
    ["129 only #2"] * 3,
    ["HDO 01"] * 3,
    ["Dust H2O 01"] * 3,


    ["132 only #2"] * 3,
    ["133 only #2"] * 3,
    ["134 only #2"] * 3,
    ["6SUBD CO2 Dipole #1"] * 3,
    ["CO2 Fullscan Fast #3"] * 3,

    ["HCL #4"] * 3, #129 + others
    ["HCL #5"] * 3, #130 + others
    ["HCL #8"] * 3, #129 + others
    ["HCL #9"] * 3, #130 + others
    ["HCL #10"] * 3, #all HCL
    ["HCL #11"] * 3, #all HCL



]

        
OCCULTATION_MERGED_WEIGHTS = [
    ["6SUBD CO2 H2O #11"] * 1,
    ["6SUBD CO2 H2O #14"] * 1,
    ["6SUBD CO2 H2O CO #15"] * 1,
    ["6SUBD CO2 H2O #12"] * 1,
    ["6SUBD CO2 H2O #13"] * 1,

    ["All Fullscan Fast #2"] * 2,
    ["CO2 Fullscan Fast #4"] * 2, #orders 165-175 reduce gradually

    ["6SUBD Nominal #42"] * 1, #nominal + 129
    ["6SUBD Nominal #45"] * 1, #nominal + 129
    ["6SUBD Nominal #48"] * 1, #nominal + 129
    ["6SUBD Nominal #51"] * 1, #nominal + 129
    ["6SUBD Nominal #11"] * 1, #nominal + 126/129
    ["6SUBD Nominal #12"] * 1, #nominal + 127/129
    
]

        
OCCULTATION_GRAZING_WEIGHTS = [
    ["6SUBD CO2 H2O #11"] * 1,
    ["6SUBD CO2 H2O #14"] * 1,
    ["6SUBD CO2 H2O CO #15"] * 1,
    ["6SUBD CO2 H2O #12"] * 1,
    ["6SUBD CO2 H2O #13"] * 1,

    ["All Fullscan Fast #2"] * 2,
    ["CO2 Fullscan Fast #4"] * 2, #orders 165-175 reduce gradually

    ["6SUBD Nominal #42"] * 1, #nominal + 129
    ["6SUBD Nominal #45"] * 1, #nominal + 129
    ["6SUBD Nominal #48"] * 1, #nominal + 129
    ["6SUBD Nominal #51"] * 1, #nominal + 129
    ["6SUBD Nominal #11"] * 1, #nominal + 126/129
    ["6SUBD Nominal #12"] * 1, #nominal + 127/129
     
]

OCCULTATION_ACS_RIDEALONG_WEIGHTS = [
    ["ACS Ridealong Science 2SUBD 01"] * 1,
]




OCCULTATION_CH4_REGION_WEIGHTS = [
    ["6SUBD CO2 H2O #11"] * 1,
    ["6SUBD CO2 H2O #14"] * 1,
    ["6SUBD CO2 H2O CO #15"] * 1,
    ["6SUBD CO2 H2O #12"] * 1,
    ["6SUBD CO2 H2O #13"] * 1,

    ["134 only #2"] * 3, 
    ["136 only #2"] * 3, 
    ["6SUBD CH4 #1"] * 3,
]


OCCULTATION_H2O_REGION_WEIGHTS = [
    ["6SUBD CO2 H2O #11"] * 1,
    ["6SUBD CO2 H2O #14"] * 1,
    ["6SUBD CO2 H2O CO #15"] * 1,
    ["6SUBD CO2 H2O #12"] * 1,
    ["6SUBD CO2 H2O #13"] * 1,

    ["6SUBD Nominal #42"] * 1, #nominal + 129
    ["6SUBD Nominal #45"] * 1, #nominal + 129
    ["6SUBD Nominal #48"] * 1, #nominal + 129
    ["6SUBD Nominal #51"] * 1, #nominal + 129
    ["6SUBD Nominal #11"] * 1, #nominal + 126/129
    ["6SUBD Nominal #12"] * 1, #nominal + 127/129
]

        
#IN GENERAL, USE LESS CH4 ORDERS AS THESE ARE NORMALLY ADDED WHEN CROSSING OVER INTERESTING REGIONS
NADIR_WEIGHTS = [

    ["Nominal 6SUBD #2"] * 8, #WITH ORDER 189
    ["Nominal 4SUBD #2"] * 8, #WITH ORDER 189
    ["H2O CO 2SUBD #1"] * 15, #WITH ORDER 189. BEST OBSERVATION
    ["H2O CO 3SUBD #2"] * 15, #PATCHED FOR MTP031+
    ["CH4 CO 2SUBD #3"] * 4, #PATCHED FOR MTP031+
    ["CH4 CO 2SUBD #4"] * 4, #PATCHED FOR MTP031+
    ["H2O 2SUBD 01"] * 5,
    ["CH4 3SUBD 01"] * 4,
    ["Surface 3SUBD #3"] * 5,

    ["Nominal 6SUBD 01"] * 2, #REDUCE, REPLACE WITH ORDER 189
    ["Nominal 4SUBD 01"] * 2,
    ["Nominal 3SUBD 01"] * 2,


    ["HDO H2O 2SUBD 02"] * 2,
    ["HDO H2O 2SUBD 03"] * 2,
    ["CO Fullscan #2"] * 1,
    ["H2O Fullscan #2"] * 1,


    ["Ice CH4 2SUBD #1"] * 4,
    ["Ice H2O 2SUBD #1"] * 4,
    ["Ice CO 2SUBD #2"] * 4, #PATCHED FOR MTP031+

    ["Surface Ice 4SUBD 01"] * 4, #increase when beta angle high
    ["Surface Ice 6SUBD 01"] * 4,
    ["Surface Ice 4SUBD 02"] * 4,
    ["Surface Ice 3SUBD 01"] * 4,


     
]


        
#limb 3 and 4 are more important than the others
#ORDER 164 FOR LIMBS > 50KM, CONTINUE 163-165 COMBINATIONS FOR CASSIS LIMBS
NADIR_LIMB_WEIGHTS = [
    ["Limb 2SUBD 07"] * 3,
    ["Nominal Limb 01"] * 1,
    
]

NADIR_NIGHT_LIMB_WEIGHTS = [
    ["Night Limb #2"] * 5, #PATCHED FOR MTP031+

]
        
NADIR_NIGHTSIDE_WEIGHTS = [
    ["Night Limb #2"] * 5, #PATCHED FOR MTP031+

]

        
        
        
        
NADIR_CH4_REGION_WEIGHTS = [
    ["CH4 H2O 2SUBD 02"] * 3, #WITH 136
    ["CH4 H2O 2SUBD 01"] * 1, #WITH 134
    ["CH4 2SUBD 03"] * 1, #136 ONLY
    ["CH4 CO 2SUBD #3"] * 4, #PATCHED FOR MTP031+
    
]        

NADIR_H2O_REGION_WEIGHTS = [
    ["H2O 2SUBD 01"] * 2,        
    ["H2O CO 2SUBD #1"] * 1, #OPTIMAL OBSERVATION
]        


NADIR_SURFACE_REGION_WEIGHTS = [
    ["H2O CO 2SUBD #1"] * 2,
    ["Surface 3SUBD 02"] * 1,
    ["Surface 3SUBD #3"] * 3, #PATCHED FOR MTP031+
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
    
    
