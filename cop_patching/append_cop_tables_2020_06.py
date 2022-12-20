# -*- coding: utf-8 -*-
"""
Created on Thu Jun  4 14:39:11 2020

@author: iant

SCRIPT TO READ IN THE EXISTING SCIENCE TABLES AND GENERATE A FEW SUBDOMAIN ROWS FOR A MINOR PATCH
"""
import os
import re

from cop_patching.generate_cop_tables_v05 import readScienceComments, writeTable
from cop_patching.generate_cop_tables_v05 import read_in_cop_table, getWindowHeight, exec_time, checkExecTime

from nomad_obs.config.paths import BASE_DIRECTORY


PREVIOUS_COP_TABLE_DIRECTORY_NAME = "mtp031_proposed"
COP_TABLE_PATH = os.path.join(BASE_DIRECTORY, "cop_tables", PREVIOUS_COP_TABLE_DIRECTORY_NAME)



channels = ["so", "lno"]

#Patch at end of MTP030 (made June 2020)
newLnoObservationDict = {
"H2O CO 3SUBD #2":[[168,189,190], 205, 15, 144, 1], 
"H2O CO 3SUBD #3":[[169,189,190], 205, 15, 144, 1], 
"CH4 CO 2SUBD #3":[[189,136], 200, 15, 144, 1], 
"CH4 CO 2SUBD #4":[[189,134], 200, 15, 144, 1], 
"Surface 3SUBD #3":[[189,194,196], 205, 15, 144, 1], 
"Ice CO 2SUBD #2":[[193,189], 200, 15, 144, 1], 
"Night Limb #2":[[158,158], 200, 15, 144, 1],
"Nominal 4SUBD #3":[[168,134,190,189], 195, 15, 144, 1], #GOOD
"Nominal 4SUBD #4":[[168,136,190,189], 195, 15, 144, 1], #GOOD
"Nominal 4SUBD #5":[[169,134,190,189], 195, 15, 144, 1], #GOOD
"Nominal 4SUBD #6":[[169,136,190,189], 195, 15, 144, 1], #GOOD
}


newSoObservationDict = {
"HCL #1":[[121, 134, 126, 126, 126, 126], 4, 1, 16, 0],
"HCL #2":[[121, 134, 127, 127, 127, 127], 4, 1, 16, 0],
"HCL #4":[[121, 134, 129, 129, 129, 129], 4, 1, 16, 0],
"HCL #5":[[121, 134, 130, 130, 130, 130], 4, 1, 16, 0],

"HCL #6":[[121, 136, 126, 126, 126, 126], 4, 1, 16, 0],
"HCL #7":[[121, 136, 127, 127, 127, 127], 4, 1, 16, 0],
"HCL #8":[[121, 136, 129, 129, 129, 129], 4, 1, 16, 0],
"HCL #9":[[121, 136, 130, 130, 130, 130], 4, 1, 16, 0],

"HCL #10":[[121, 134, 126, 127, 129, 130], 4, 1, 16, 0],
"HCL #11":[[121, 136, 126, 127, 129, 130], 4, 1, 16, 0],


"HCL #12":[[134, 126, 126, 126, 126, 126], 4, 1, 16, 0],
"HCL #13":[[134, 127, 127, 127, 127, 127], 4, 1, 16, 0],
"HCL #14":[[134, 129, 129, 129, 129, 129], 4, 1, 16, 0],
"HCL #15":[[134, 130, 130, 130, 130, 130], 4, 1, 16, 0],

"HCL #16":[[136, 126, 126, 126, 126, 126], 4, 1, 16, 0],
"HCL #17":[[136, 127, 127, 127, 127, 127], 4, 1, 16, 0],
"HCL #18":[[136, 129, 129, 129, 129, 129], 4, 1, 16, 0],
"HCL #19":[[136, 130, 130, 130, 130, 130], 4, 1, 16, 0],




"HCL CO #1":[[186, 189, 190, 126, 127, 129], 4, 1, 16, 0],

"Nom HCL #1":[[121, 134, 169, 126, 127, 129], 4, 1, 16, 0],
"Nom HCL #2":[[121, 136, 169, 126, 127, 129], 4, 1, 16, 0],

"Nom HCL #3":[[119, 134, 169, 126, 127, 129], 4, 1, 16, 0],
"Nom HCL #4":[[119, 136, 169, 126, 127, 129], 4, 1, 16, 0],

"HCL CO2 #1":[[121, 149, 165, 126, 127, 129], 4, 1, 16, 0],
"HCL CO2 #2":[[121, 149, 164, 126, 127, 129], 4, 1, 16, 0],



"6SUBD Nominal #4":[[121, 134, 126, 127, 169, 186], 4, 1, 16, 0],
"6SUBD Nominal #5":[[121, 134, 126, 129, 169, 186], 4, 1, 16, 0],
"6SUBD Nominal #6":[[121, 134, 127, 129, 169, 186], 4, 1, 16, 0],

"6SUBD Nominal #7":[[121, 136, 126, 127, 169, 186], 4, 1, 16, 0],
"6SUBD Nominal #8":[[121, 136, 126, 129, 169, 186], 4, 1, 16, 0],
"6SUBD Nominal #9":[[121, 136, 127, 129, 169, 186], 4, 1, 16, 0],

"6SUBD Nominal #10":[[121, 134, 126, 127, 169, 190], 4, 1, 16, 0],
"6SUBD Nominal #11":[[121, 134, 126, 129, 169, 190], 4, 1, 16, 0],
"6SUBD Nominal #12":[[121, 134, 127, 129, 169, 190], 4, 1, 16, 0],

"6SUBD Nominal #13":[[121, 136, 126, 127, 169, 190], 4, 1, 16, 0],
"6SUBD Nominal #14":[[121, 136, 126, 129, 169, 190], 4, 1, 16, 0],
"6SUBD Nominal #15":[[121, 136, 127, 129, 169, 190], 4, 1, 16, 0],

"6SUBD Nominal #16":[[121, 149, 126, 127, 169, 186], 4, 1, 16, 0],
"6SUBD Nominal #17":[[121, 149, 126, 129, 169, 186], 4, 1, 16, 0],
"6SUBD Nominal #18":[[121, 149, 127, 129, 169, 186], 4, 1, 16, 0],

"6SUBD Nominal #22":[[121, 149, 126, 127, 169, 190], 4, 1, 16, 0],
"6SUBD Nominal #23":[[121, 149, 126, 129, 169, 190], 4, 1, 16, 0],
"6SUBD Nominal #24":[[121, 149, 127, 129, 169, 190], 4, 1, 16, 0],

"6SUBD Nominal #28":[[134, 126, 127, 169, 186, 190], 4, 1, 16, 0],
"6SUBD Nominal #29":[[134, 126, 129, 169, 186, 190], 4, 1, 16, 0],
"6SUBD Nominal #30":[[134, 127, 129, 169, 186, 190], 4, 1, 16, 0],

"6SUBD Nominal #31":[[136, 126, 127, 169, 186, 190], 4, 1, 16, 0],
"6SUBD Nominal #32":[[136, 126, 129, 169, 186, 190], 4, 1, 16, 0],
"6SUBD Nominal #33":[[136, 127, 129, 169, 186, 190], 4, 1, 16, 0],

"6SUBD Nominal #34":[[134, 126, 127, 169, 149, 165], 4, 1, 16, 0],
"6SUBD Nominal #35":[[134, 126, 129, 169, 149, 165], 4, 1, 16, 0],
"6SUBD Nominal #36":[[134, 127, 129, 169, 149, 165], 4, 1, 16, 0],

"6SUBD Nominal #37":[[136, 126, 127, 169, 149, 165], 4, 1, 16, 0],
"6SUBD Nominal #38":[[136, 126, 129, 169, 149, 165], 4, 1, 16, 0],
"6SUBD Nominal #39":[[136, 127, 129, 169, 149, 165], 4, 1, 16, 0],

"6SUBD Nominal #40":[[121, 134, 169, 126, 149, 165], 4, 1, 16, 0],
"6SUBD Nominal #41":[[121, 134, 169, 127, 149, 165], 4, 1, 16, 0],
"6SUBD Nominal #42":[[121, 134, 169, 129, 149, 165], 4, 1, 16, 0],

"6SUBD Nominal #43":[[121, 136, 169, 126, 149, 165], 4, 1, 16, 0],
"6SUBD Nominal #44":[[121, 136, 169, 127, 149, 165], 4, 1, 16, 0],
"6SUBD Nominal #45":[[121, 136, 169, 129, 149, 165], 4, 1, 16, 0],

"6SUBD Nominal #46":[[121, 134, 126, 169, 186, 190], 4, 1, 16, 0],
"6SUBD Nominal #47":[[121, 134, 127, 169, 186, 190], 4, 1, 16, 0],
"6SUBD Nominal #48":[[121, 134, 129, 169, 186, 190], 4, 1, 16, 0],

"6SUBD Nominal #49":[[121, 136, 126, 169, 186, 190], 4, 1, 16, 0],
"6SUBD Nominal #50":[[121, 136, 127, 169, 186, 190], 4, 1, 16, 0],
"6SUBD Nominal #51":[[121, 136, 129, 169, 186, 190], 4, 1, 16, 0],




"6SUBD CO HCL #6":[[126, 134, 186, 187, 189, 190], 4, 1, 16, 0],
"6SUBD CO HCL #7":[[127, 134, 186, 187, 189, 190], 4, 1, 16, 0],
"6SUBD CO HCL #8":[[129, 134, 186, 187, 189, 190], 4, 1, 16, 0],
"6SUBD CO HCL #9":[[126, 136, 186, 187, 189, 190], 4, 1, 16, 0],
"6SUBD CO HCL #10":[[127, 136, 186, 187, 189, 190], 4, 1, 16, 0],
"6SUBD CO HCL #11":[[129, 136, 186, 187, 189, 190], 4, 1, 16, 0],



"6SUBD CH4 HCL #1":[[121, 126, 133, 134, 135, 136], 4, 1, 16, 0],
"6SUBD CH4 HCL #2":[[121, 127, 133, 134, 135, 136], 4, 1, 16, 0],
"6SUBD CH4 HCL #3":[[121, 129, 133, 134, 135, 136], 4, 1, 16, 0],

"6SUBD CH4 HCL #4":[[169, 126, 133, 134, 135, 136], 4, 1, 16, 0],
"6SUBD CH4 HCL #5":[[169, 127, 133, 134, 135, 136], 4, 1, 16, 0],
"6SUBD CH4 HCL #6":[[169, 129, 133, 134, 135, 136], 4, 1, 16, 0],



"6SUBD CO2 HCL #1":[[119, 149, 164, 165, 126, 127], 4, 1, 16, 0],
"6SUBD CO2 HCL #2":[[119, 149, 164, 165, 126, 129], 4, 1, 16, 0],
"6SUBD CO2 HCL #3":[[119, 149, 164, 165, 127, 129], 4, 1, 16, 0],




}



"""check for repeated orders in lines"""
for searchIndex, (searchObsName, searchObsData) in enumerate(newSoObservationDict.items()):
    searchOrders, _, _, _, _ = searchObsData
    for eachIndex, (eachObsName, eachObsData) in enumerate(newSoObservationDict.items()):
        eachOrders, _, _, _, _ = eachObsData
        if sorted(searchOrders) == sorted(eachOrders):
            if searchIndex != eachIndex:
                print("######SO Repeats#####")
                print("Match found:", searchObsName, "matches", eachObsName, searchObsData, eachObsData)

for searchIndex, (searchObsName, searchObsData) in enumerate(newLnoObservationDict.items()):
    searchOrders, _, _, _, _ = searchObsData
    for eachIndex, (eachObsName, eachObsData) in enumerate(newLnoObservationDict.items()):
        eachOrders, _, _, _, _ = eachObsData
        if sorted(searchOrders) == sorted(eachOrders):
            if searchIndex != eachIndex:
                print("######LNO Repeats#####")
                print("Match found:", searchObsName, "matches", eachObsName, searchObsData, eachObsData)



"""write orders to new subdomain file"""
for channel in channels:


    if channel == "so":
        newObservationDict = newSoObservationDict
        nScienceCalRows = 582
    elif channel == "lno":
        newObservationDict = newLnoObservationDict
        nScienceCalRows = 629
    

    cop = "science"
    csv_filename = COP_TABLE_PATH + os.sep + "%s_%s_table.csv" %(channel, cop)
    with open(csv_filename) as f:
        scienceLines = f.readlines()
    scienceTable = readScienceComments(scienceLines, nScienceCalRows)
        
    
    
    
    #get order combinations from new dictionaries
    subdomainLines = []
    for obsName, obsParameters in newObservationDict.items():
        nsubdRequired = len(obsParameters[0])
    
        orderCombination = obsParameters[0]
        nrowsRequired = obsParameters[3]
        rhythmRequired = obsParameters[2]
        inttimeRequired = obsParameters[1] * 1000

        nLightOrders = sum([1 for order in orderCombination if order>0])
        nDarkOrders = sum([1 for order in orderCombination if order == 0])
        if nDarkOrders > 0:
            sbsfRequired = 0
        else:
            sbsfRequired = 1
            
        
        sciencePointers = []
        for diffractionOrder in orderCombination:
            #search science lines for matching order, binning, int time etc.
            matchingLine = []
            for lineNumber, scienceLine in enumerate(scienceTable):
                _,_,sbsf,aotfPointer,steppingPointer,accumulationCount,binningFactor,integrationTime,nrows,rhythm,nsubd,exectime = scienceLine
                if int(steppingPointer) == 0:
                    if int(aotfPointer) == diffractionOrder:
                        if inttimeRequired == int(integrationTime):
                            if nrowsRequired == int(nrows):
                                if sbsfRequired == int(sbsf):
                                    if rhythmRequired == int(rhythm):
                                        if nsubdRequired == int(nsubd):
                                            matchingLine.append(lineNumber)
            if len(matchingLine) == 1: #check only 1 line found
                sciencePointers.append(matchingLine[0])
            elif len(matchingLine) > 1:
                print("Error: too many lines found (%i)" %len(matchingLine))
                for index in matchingLine:
                    print(scienceTable[index])
            else:
                print("Error: line not found order=%i nsubd=%i it=%i nrows=%i bg=%i rhy=%i" %(diffractionOrder, nsubdRequired, inttimeRequired, nrowsRequired, sbsfRequired, rhythmRequired))
        while len(sciencePointers) != 6:
            sciencePointers.append(0)
            
        longComment = scienceLines[sciencePointers[0]+1].split("#")[1].strip()
        comment = "ORDERS " + " ".join([str(i) for i in orderCombination]) + " -- " + longComment
        
        
        subdomainLines.append(f"{sciencePointers[0]},{sciencePointers[1]},{sciencePointers[2]},{sciencePointers[3]},{sciencePointers[4]},{sciencePointers[5]} # {comment}")


    writeTable(channel, "sub_domain", subdomainLines, output_directory=COP_TABLE_PATH)




"""check that the new rows are correct"""
for channel in channels:

    subdomainHeaders, subdomainList = read_in_cop_table(channel, "sub_domain", output_directory=COP_TABLE_PATH)
    scienceHeaders, scienceList = read_in_cop_table(channel, "science", output_directory=COP_TABLE_PATH)
    fixedHeaders, fixedList = read_in_cop_table(channel, "fixed", output_directory=COP_TABLE_PATH)
    
    allWindowHeights = list(set([int(fixedLine[0]) for fixedLine in fixedList if fixedLine[0] != "0"]))
    
    for subdomainLine in subdomainList:
        sciencePointers = [int(subdomainLine[index]) for index in range(6) if subdomainLine[index] != "0"]
        scienceLineAll = [[int(scienceList[sciencePointer][index]) for index in range(8)]+[scienceList[sciencePointer][8]] for sciencePointer in sciencePointers]
        nSubdomains = len(scienceLineAll)
        if nSubdomains > 1:
            totalExecTime = 0
            comments = []
            for scienceLine in scienceLineAll:
                _,_,sbsf,aotfPointer,steppingPointer,accumulationCount,binningFactor,integrationTime,comment = scienceLine
                windowHeight = getWindowHeight(binningFactor, nSubdomains)
                
                if windowHeight not in allWindowHeights:
                    print("Error: window height not found in fixed table")
                totalExecTime += exec_time(accumulationCount, windowHeight, integrationTime)
                comments.append(comment)
                
            #check all comments identical
            nComments = len(list(set(comments)))
            if nComments > 1:
                print("Error: comments don't match")
    
            if not checkExecTime(totalExecTime, 1, silent=True):
                if not checkExecTime(totalExecTime, 2, silent=True):
                    if not checkExecTime(totalExecTime, 4, silent=True):
                        if not checkExecTime(totalExecTime, 8, silent=True):
                            if not checkExecTime(totalExecTime, 15, silent=True):
                                print("Error: bad execution time %i" %totalExecTime)



"""print order list. Superseded by the html writer"""
#for channel in channels:
#
#    cop = "sub_domain"
#    csv_filename = COP_TABLE_PATH + os.sep + "%s_%s_table.csv" %(channel, cop)
#    with open(csv_filename) as f:
#        subdomainLines = f.readlines()
#    subdomainLine = subdomainLines[0]
#    orderString = subdomainLine.split("ORDERS")[1].split("--")[0]
#    regex = re.findall("(\d+)", orderString)
#    
#    print("Orders", " ".join(regex))






