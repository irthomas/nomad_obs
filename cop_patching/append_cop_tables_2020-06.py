# -*- coding: utf-8 -*-
"""
Created on Thu Jun  4 14:39:11 2020

@author: iant

SCRIPT TO READ IN THE EXISTING SCIENCE TABLES AND GENERATE A FEW SUBDOMAIN ROWS FOR A MINOR PATCH
"""
read_in_cop_table

#Patch at end of MTP030 (made June 2020)
newLnoObservationDict = {
"H2O CO 3SUBD #2":[[168,189,190], 205, 15, 144, 1], 
"CH4 CO 2SUBD #3":[[189,136], 200, 15, 144, 1], 
"CH4 CO 2SUBD #4":[[189,134], 200, 15, 144, 1], 
"Surface 3SUBD #3":[[189,194,196], 205, 15, 144, 1], 
"Ice CO 2SUBD #2":[[193,189], 200, 15, 144, 1], 
"Night Limb #2":[[158,158], 200, 15, 144, 1],
}


newSoObservationDict = {
"HCl #1":[[121, 134, 126, 126, 126, 126], 4, 1, 16, 0],
"HCl #2":[[121, 134, 127, 127, 127, 127], 4, 1, 16, 0],
"HCl #3":[[121, 134, 128, 128, 128, 128], 4, 1, 16, 0],
"HCl #4":[[121, 134, 129, 129, 129, 129], 4, 1, 16, 0],
"HCl #5":[[121, 134, 130, 130, 130, 130], 4, 1, 16, 0],


}


for channel in channels:

    subdomainHeaders, subdomainList = read_in_cop_table(channel, "sub_domain")
    scienceHeaders, scienceList = read_in_cop_table(channel, "science")
    fixedHeaders, fixedList = read_in_cop_table(channel, "fixed")
    
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
