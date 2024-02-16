# -*- coding: utf-8 -*-
"""
Created on Mon Apr 27 12:26:09 2020

@author: iant
"""
import os
import numpy as np

from nomad_obs.config.paths import COP_TABLE_DIRECTORY
from nomad_obs.other.generic_functions import findIndex, stop




def outputCopTable(copVersion,channel,cop):
    """function to read in cop tables, given channel and name"""

    if channel=="so" or channel=="lno":
        csvFilename=COP_TABLE_DIRECTORY+os.sep+"%s" %copVersion+os.sep+"%s_%s_table.csv" %(channel,cop)
    elif channel=="uvis":
        csvFilename=COP_TABLE_DIRECTORY+os.sep+"%s" %copVersion+os.sep+"uvis_table.csv"
    with open(csvFilename) as f:
        copList=[]
        for index,line in enumerate(f):
            content = line.strip('\n').split(',')
            if index==0: #if first line
                copHeaders=content #record header data
                copHeaders.append("comments")
            else:
                if content[len(content)-1].find('#') != -1: #if comment line
                    temp=content[len(content)-1].split('#') #split last field into value and comment
                    content[len(content)-1]=temp[0].strip() #replace last column with value only
                    content.append(temp[1].strip()) #add new column on end for the comment
                else:
                    content.append("NONE")
                copList.append(content)
    return copHeaders,copList




    

def getCopTables(mtpConstants):
    """read in COP tables from file"""
    copVersion = mtpConstants["copVersion"]


    soAotfHeaders,soAotfList = outputCopTable(copVersion,"so",'aotf')
    soFixedHeaders,soFixedList = outputCopTable(copVersion,"so",'fixed')
    soScienceHeaders,soScienceList = outputCopTable(copVersion,"so",'science')
    soSteppingHeaders,soSteppingList = outputCopTable(copVersion,"so",'stepping')
    soSubdomainHeaders,soSubdomainList = outputCopTable(copVersion,"so",'sub_domain')
    
    lnoAotfHeaders,lnoAotfList = outputCopTable(copVersion,"lno",'aotf')
    lnoFixedHeaders,lnoFixedList = outputCopTable(copVersion,"lno",'fixed')
    lnoScienceHeaders,lnoScienceList = outputCopTable(copVersion,"lno",'science')
    lnoSteppingHeaders,lnoSteppingList = outputCopTable(copVersion,"lno",'stepping')
    lnoSubdomainHeaders,lnoSubdomainList = outputCopTable(copVersion,"lno",'sub_domain')
    
    uvisHeaders,uvisList = outputCopTable(copVersion,"uvis","")
        
    copTableDict = {
            "soAotfHeaders":soAotfHeaders, "soAotfList":soAotfList, \
            "soFixedHeaders":soFixedHeaders, "soFixedList":soFixedList, \
            "soScienceHeaders":soScienceHeaders, "soScienceList":soScienceList, \
            "soSteppingHeaders":soSteppingHeaders, "soSteppingList":soSteppingList, \
            "soSubdomainHeaders":soSubdomainHeaders, "soSubdomainList":soSubdomainList, \
            "lnoAotfHeaders":lnoAotfHeaders, "lnoAotfList":lnoAotfList, \
            "lnoFixedHeaders":lnoFixedHeaders, "lnoFixedList":lnoFixedList, \
            "lnoScienceHeaders":lnoScienceHeaders, "lnoScienceList":lnoScienceList,  \
            "lnoSteppingHeaders":lnoSteppingHeaders, "lnoSteppingList":lnoSteppingList, \
            "lnoSubdomainHeaders":lnoSubdomainHeaders, "lnoSubdomainList":lnoSubdomainList, \
            "uvisHeaders":uvisHeaders, "uvisList":uvisList, \
            }

    return copTableDict


def makeCopTableDict(channelCode, copTableDict, silent=True):

    subdomainList = {0:copTableDict["soSubdomainList"], 1:copTableDict["lnoSubdomainList"]}[channelCode]
    scienceList = {0:copTableDict["soScienceList"], 1:copTableDict["lnoScienceList"]}[channelCode]
    aotfList = {0:copTableDict["soAotfList"], 1:copTableDict["lnoAotfList"]}[channelCode]
    
    #degf	dvaf	sbsf	aotfPointer	steppingPointer	accumulationCount	binningFactor	integrationTime
    
    subdomainIndices = []
    aotfOrdersAll = []
    integrationTimesAll = []
    windowHeightAll = []
    rhythmAll = []
    
#    subdomainRow = subdomainList[1000]
    for rowIndex, subdomainRow in enumerate(subdomainList):
        nSubdomains = 6 - subdomainRow.count("0")
        
        steppingIndices = []
        accumulations = []
        binningFactors = []
        integrationTimes = []
        aotfOrders = []
        
        errorFound = False
        calibration = False

        if nSubdomains == 0:
            calibration = True       
        
        for index in range(nSubdomains):
            scienceIndex = int(subdomainRow[index])
            scienceRow = scienceList[scienceIndex]
        
            steppingIndex = int(scienceRow[4])
            steppingIndices.append(steppingIndex)
            
            accumulation = int(scienceRow[5])
            accumulations.append(accumulation)
        
            binningFactor = int(scienceRow[6])
            binningFactors.append(binningFactor)
        
            integrationTime = int(scienceRow[7]) / 1000.0
            integrationTimes.append(integrationTime)
        
            aotfIndex = int(scienceRow[3])
            aotfRow = aotfList[aotfIndex]
            if "ORDER_" in aotfRow[2]:
                aotfOrder = int(aotfRow[2].replace("ORDER_",""))
            elif aotfIndex == 0:
                aotfOrder = 0
    
            if steppingIndices[0] > 0:
                calibration = True
        
            aotfOrders.append(aotfOrder)
        
        aotfOrdersSorted = sorted(aotfOrders)
                
            
        if len(set(binningFactors)) == 1: #if more than one binning factor in the observation
            binningFactorSingle = binningFactors[0]
            windowHeightTotal = 24.0 / nSubdomains * (binningFactorSingle + 1)
            if np.round(windowHeightTotal) == windowHeightTotal:
                windowHeightTotal = int(windowHeightTotal)
            else:
                print("Binning rounding error row %i" %rowIndex)
        else:
            if not silent: print("Binning error row %i" %rowIndex)
            if not silent: print(binningFactors)
            errorFound = True
        
        
        if len(set(accumulations)) == 1: #if n accumulations is the same for all observations
            accumulationSingle = accumulations[0]
        else:
            if not silent: print("Accumulation error row %i" %rowIndex)
            if not silent: print(accumulations)
            errorFound = True
        
        
        if len(set(integrationTimes)) == 1: #if more than one integration time in the observation
            integrationTimeSingle = integrationTimes[0]
        else:
            if not silent: print("Int time error row %i" %rowIndex)
            if not silent: print(integrationTimes)
            errorFound = True
        
            
        if nSubdomains > 1: 
            if sum(steppingIndices[1:6]) > 0:
                if not silent: print("Stpping error row %i" %rowIndex)
                errorFound = True
        
        if not calibration:
            executionTime = calcExecutionTime(accumulationSingle, windowHeightTotal, integrationTimeSingle)
            executionTimeTotal = executionTime * nSubdomains
        
            if 650.0 < executionTimeTotal < 1000.0:
                rhythm = 1
            elif 1700.0 < executionTimeTotal < 2000.0:
                rhythm = 2
            elif 3400.0 < executionTimeTotal < 4000.0:
                rhythm = 4
            elif 7000.0 < executionTimeTotal < 8000.0:
                rhythm = 8
            elif 14000.0 < executionTimeTotal < 15000.0:
                rhythm = 15
            else:
                if not silent: print("Exec time error row %i" %rowIndex)
                errorFound = True
        
        if not errorFound and not calibration:
            subdomainIndices.append(rowIndex)
            aotfOrdersAll.append(aotfOrdersSorted)
            integrationTimesAll.append(integrationTimeSingle)
            windowHeightAll.append(windowHeightTotal)
            rhythmAll.append(rhythm)
            
    copTableCombinations = {"index":subdomainIndices, "orders":aotfOrdersAll, "integrationTime":integrationTimesAll, "rhythm":rhythmAll, "windowHeight":windowHeightAll}
    return copTableCombinations




    

def findCopRowData(channel, copTableDict, columnNames, row, table=""):
#    channel="so"
#    columnName = "science_3"
#    row=1000
    

    
    if isinstance(row, list):
        if len(row)==1:
            row = int(row[0])
        else:
            print("Error: row number is a list")

    if channel in ["so","lno"]:
        aotfHeaders = {"so":copTableDict["soAotfHeaders"], "lno":copTableDict["lnoAotfHeaders"]}[channel]
        aotfList = {"so":copTableDict["soAotfList"], "lno":copTableDict["lnoAotfList"]}[channel]
        fixedHeaders = {"so":copTableDict["soFixedHeaders"], "lno":copTableDict["lnoFixedHeaders"]}[channel]
        fixedList = {"so":copTableDict["soFixedList"], "lno":copTableDict["lnoFixedList"]}[channel]
        scienceHeaders = {"so":copTableDict["soScienceHeaders"], "lno":copTableDict["lnoScienceHeaders"]}[channel]
        scienceList = {"so":copTableDict["soScienceList"], "lno":copTableDict["lnoScienceList"]}[channel]
        steppingHeaders = {"so":copTableDict["soSteppingHeaders"], "lno":copTableDict["lnoSteppingHeaders"]}[channel]
        steppingList = {"so":copTableDict["soSteppingList"], "lno":copTableDict["lnoSteppingList"]}[channel]
        subdomainHeaders = {"so":copTableDict["soSubdomainHeaders"], "lno":copTableDict["lnoSubdomainHeaders"]}[channel]
        subdomainList = {"so":copTableDict["soSubdomainList"], "lno":copTableDict["lnoSubdomainList"]}[channel]
    
    if table != "": #not used
        if table=="aotf":
            copTable = aotfList
            copTableHeader = aotfHeaders
        elif table=="fixed":
            copTable = fixedList
            copTableHeader = fixedHeaders
        elif table=="science":
            copTable = scienceList
            copTableHeader = scienceHeaders
        elif table=="stepping":
            copTable = steppingList
            copTableHeader = steppingHeaders
        elif table=="subdomain":
            copTable = subdomainList
            copTableHeader = subdomainHeaders
        else:
            print("Error: table unknown")

        valuesOut = []
        for columnName in columnNames:
            columnIndex = findIndex(columnName,copTableHeader)
            valuesOut.append(copTable[int(row)][columnIndex])
            
        if len(valuesOut)==1:
            valuesOut = valuesOut[0]
        return valuesOut
    
    else:
        if channel in ["so","lno"]:
            headers = [aotfHeaders,fixedHeaders,scienceHeaders,steppingHeaders,subdomainHeaders]
            lists = [aotfList,fixedList,scienceList,steppingList,subdomainList]
        elif channel == "uvis":
            headers = [copTableDict["uvisHeaders"]]
            lists = [copTableDict["uvisList"]]
        
        valuesOut = []
        for columnName in columnNames:
            value = []
            for headerIndex,header in enumerate(headers):
                if columnName in header:
                    columnIndex = findIndex(columnName,header)
    #                print(headerIndex)
    #                print(columnIndex)
                    value.append(lists[headerIndex][int(row)][columnIndex])
                    
            if len(value) == 1:
                valuesOut.append(value[0])
            else:
                print("Error finding COP row")
                    
        if len(valuesOut)==1:
            valuesOut = valuesOut[0]
        return valuesOut



"""find matching cop rows"""
def findCopRows(channel,copTableDict, orders,integrationTime,nRows,silent=False): #IntTime in ms!!
    
    subdomainList = {"so":copTableDict["soSubdomainList"], "lno":copTableDict["lnoSubdomainList"]}[channel]
    
    otherRows = []
    found=False
    for rowIndex,subdomainRow in enumerate(subdomainList):
        subdomainComment = subdomainRow[6]
        nFound = 0
        nSubdomains = 6 - subdomainRow.count("0")
        for order in orders:
            if subdomainComment.find(" %s " %str(order)) > -1:
                nFound += 1
    
            if nFound == len(orders) and nSubdomains == len(orders):
                found=True
                if subdomainComment.find("=%sMS" %str(integrationTime)) > -1:
                    
                    if subdomainComment.find("NROWS=%s" %str(nRows)) > -1:
                        if not silent: print("Matching row found: %i" %rowIndex)
                        if not silent: print(subdomainRow)
                        return rowIndex
                    else:
                         otherRows.append(subdomainRow)
                else:
                     otherRows.append(subdomainRow)
    
    if found:
        print("Orders found but integration time and/or number of rows not. Possible options are:")
        for otherRow in otherRows:
            print(otherRow)
        return -1 #wrong integration time
    else:
        print("Orders not found")
        print(orders)
        return -2 #order combination not found




"""find matching cop rows"""
def findFixedCopRow(channel,copTableDict, centreRow,nRows,rhythm,silent=False): #IntTime in ms!!
    
    fixedList = {"so":copTableDict["soFixedList"], "lno":copTableDict["lnoFixedList"]}[channel]
    
    foundRows = []
    found=False
    for rowIndex,fixedRow in enumerate(fixedList):
        nFound = 0
        fixedHeight = int(fixedRow[0]) + 1
        fixedTop = int(fixedRow[1])
        fixedRhythm = int(fixedRow[6])
        
        if fixedHeight == nRows and fixedTop == centreRow - nRows/2 and fixedRhythm == rhythm:
            if not silent: print("Matching fixed row found: %i" %rowIndex)
            if not silent: print(fixedRow)
            found=True
            nFound += 1
            foundRows.append(rowIndex)
                
    if found and len(foundRows)==1:
        return foundRows[0] #return the correct row
    elif found:
        if foundRows[0] == 0 and foundRows[1] == 9: #fudge to stop error when default values (at top of fixed cop table) are copies of other rows
            return foundRows[0] #return the first matching row
        elif foundRows[0] == 1 and foundRows[1] == 72: #fudge to stop error when default values (at top of fixed cop table) are copies of other rows
            return foundRows[0] #return the first matching row
        elif foundRows[0] == 2 and foundRows[1] == 81: #fudge to stop error when default values (at top of fixed cop table) are copies of other rows
            return foundRows[0] #return the first matching row

        elif foundRows[0] == 0 and foundRows[1] == 21: #fudge to stop error when default values (at top of fixed cop table) are copies of other rows
            return foundRows[0] #return the first matching row
        elif foundRows[0] == 1 and foundRows[1] == 11: #fudge to stop error when default values (at top of fixed cop table) are copies of other rows
            return foundRows[0] #return the first matching row
        elif foundRows[0] == 2 and foundRows[1] == 80: #fudge to stop error when default values (at top of fixed cop table) are copies of other rows
            return foundRows[0] #return the first matching row

        else:
            print("Warning: Multiple matching fixed rows found:")
            for row in foundRows:
                print(row)
                print(fixedList[row][7])
            return foundRows[0] #
    else:
        print("Error: Fixed row not found")
        return -999



"""output text description of measurement given input rows"""
def getObservationDescription(channel, copTableDict, fixedRow, copRow, silent=False):
    if copRow == -1:
        return "%s off" %channel.upper()
    
    
    if channel in ["so","lno"]:

        fixedRhythm = findCopRowData(channel,copTableDict, ["rythm"],fixedRow)
        fixedTop = findCopRowData(channel,copTableDict, ["windowLeftTop"],fixedRow)
        fixedHeight = findCopRowData(channel,copTableDict, ["windowLineCount"],fixedRow)
        
        sciencePointers = findCopRowData(channel,copTableDict, ["science_1","science_2","science_3","science_4","science_5","science_6"],copRow)
            
        nSubdomains = 6 - sciencePointers.count("0")
        if not silent: print(nSubdomains)
        
        if nSubdomains == 1: #check for stepping
            sciencePointer = sciencePointers[0]
            steppingPointer = findCopRowData(channel,copTableDict, ["steppingPointer"],sciencePointer)
            if steppingPointer != "0":
                steppingType,steppingSpeed,steppingCount,steppingValue = findCopRowData(channel,copTableDict, ["steppingParameter","stepSpeed","stepCount","stepValue"],steppingPointer)
                aotfOrder = findCopRowData(channel,copTableDict, ["aotfPointer"],sciencePointer)
                aotfFrequency = findCopRowData(channel,copTableDict, ["frequency"],aotfOrder)
                integrationTime = int(findCopRowData(channel,copTableDict, ["integrationTime"],sciencePointer)) / 1000
                if steppingType=="AOTF_IX":
                    observationText = "Diffraction order stepping (fullscan): %i orders from %i to %i in steps of %s (%s order(s) per %s second(s))" %(int(steppingCount),int(aotfOrder),int(aotfOrder)+int(steppingCount),int(steppingValue),int(steppingSpeed)+1,int(fixedRhythm))
                elif steppingType=="WINDOW_TOP":
                    observationText = "Detector window stepping: %i step(s) covering detector lines %i to %i (%s step(s) per %s second(s))" %(int(steppingCount),int(fixedTop),int(fixedTop)+int(steppingCount)*int(steppingValue),int(steppingSpeed)+1,int(fixedRhythm))
                elif steppingType=="INTEGRATION_TIME":
                    observationText = "Detector integration time stepping: %i integration times from %i to %ims in steps of %ims for detector lines %i to %i (%s step(s) per %s second(s))" %(int(steppingCount),int(integrationTime),int(integrationTime)*int(steppingCount)*int(steppingValue),int(steppingValue),int(fixedTop),int(fixedTop)+int(fixedHeight)+1,int(steppingSpeed)+1,int(fixedRhythm))
                elif steppingType=="AOTF_FREQ":
                    observationText = "AOTF frequency stepping (miniscan): %i frequencies from %i to %ikHz in steps of %ikHz (%s step(s) per %s second(s))" %(int(steppingCount),int(aotfFrequency)/1000,int(aotfFrequency)/1000+int(steppingCount)*np.round(int(steppingValue)*8e4/2**32),np.round(int(steppingValue)*8e4/2**32),int(steppingSpeed)+1,int(fixedRhythm))
        elif nSubdomains == 0:
            print("Error: no subdomains")
            stop()
        else:
            observationText = "Science: orders " 
            integrationTimes = []
            for sciencePointer in sciencePointers[0:nSubdomains]:
                aotfOrder = findCopRowData(channel,copTableDict, ["aotfPointer"],sciencePointer)
                integrationTimes.append(findCopRowData(channel,copTableDict, ["integrationTime"],sciencePointer))
                observationText += "#%s, " %([int(aotfOrder) if aotfOrder != "0" else "dark"][0])
            if integrationTimes.count(integrationTimes[0]) == len(integrationTimes):
                observationText += "with %ius integration time " %int(integrationTimes[0])
            else:
                observationText += "with variable integration times "
            observationText += "(%i orders per %i second(s) for detector lines %i to %i)" %(nSubdomains,int(fixedRhythm),int(fixedTop),int(fixedTop)+int(fixedHeight)+1)
        if not silent: print(observationText)

    elif channel == "uvis":
       num_acqs, flag_register, binning_size, comments = findCopRowData(channel,copTableDict, ["num_acqs", "flag_register", "binning_size", "comments"],copRow)
#       observationText = "%s -NumAcqsBetweenDarks=%s -FlagRegister=%s -BinningSize=%s" %(comments, num_acqs, flag_register, binning_size)
       observationText = "%s, Binning=%s" %(comments.replace(" - ",",").replace(" -","," ).replace("-",", "), binning_size)
    
    return observationText





def getObsParameters(observation_name, dictionary):
    if observation_name in list(dictionary.keys()):
        orders_out, inttime_out, rhythm_out, rows_out, channel_code = dictionary[observation_name]
        return sorted(orders_out), inttime_out, rhythm_out, rows_out, channel_code
    else:
        return [-999], -1, -1, -1, -1
        
        

def calcExecutionTime(number_accumulations, window_height, integration_time): #real number of rows (16, 20, 24), int time in milliseconds
    return ((number_accumulations+1.0) * ((integration_time * 1000.0) + 71.0 + 320.0 * window_height + 1000.0) + 337.0) / 1000.0


def uniqueDiffractionOrders(aotf_order_list):
    tuples = [tuple(i) for i in aotf_order_list]
    uniqueTuples = set(tuples)
    unique_orders = [list(i) for i in uniqueTuples]
    return unique_orders



"""return dictionary containing COP rows and description of measurement given input dictionary containing observation parameters"""
def getCopRows(observationName, observationDict, copTableDict, copTableCombinationDict, centreDetectorLines, silent=False):

    diffractionOrders, integrationTime, rhythm, windowHeight, channelCode = getObsParameters(observationName, observationDict)
    if diffractionOrders[0] == -999:
        print("Observation name %s not found in dictionary" %(observationName))
        return {}, [], -1, -1, -1, -1


    detectorCentreLine = centreDetectorLines[channelCode]
    copTableCombinations = copTableCombinationDict[channelCode]

    if channelCode in [0,1]:
        channel = {0:"so", 1:"lno"}[channelCode]
    else:
        print("Error: channel %i not defined" %channelCode)


    """do fixed table first"""
    fixedCopRow = findFixedCopRow(channel, copTableDict, detectorCentreLine, windowHeight, rhythm, silent=silent)
    if fixedCopRow == -999:
        print("Error: incorrect fixed row")
        stop()
    
    
    """then do subdomain table"""
    scienceCopRow = -999
    
    if type(diffractionOrders[0]) != int:
        if "COP#" in diffractionOrders[0]:
            scienceCopRow = int(diffractionOrders[0].split("#")[1])
#            print("Manual mode: COP row %i" %(scienceCopRow))
        else:
            print("Error: COP rows must be integers or must be specified manually e.g. COP#1")
            stop()
    else:
        #look in cop tables for correct subdomain rows
        found = [0]
        for indexCop, diffractionOrdersCop, integrationTimeCop, rhythmCop, windowHeightCop in zip(copTableCombinations["index"], copTableCombinations["orders"], copTableCombinations["integrationTime"], copTableCombinations["rhythm"], copTableCombinations["windowHeight"]):
            if diffractionOrders == diffractionOrdersCop:
                found.append(1)
                if integrationTime == integrationTimeCop:
                    found.append(2)
                    if rhythm == rhythmCop:
                        found.append(3)
                        if windowHeight == windowHeightCop:
                            scienceCopRow = indexCop
                            found.append(4)

                
    
    if scienceCopRow < 0:
        print("Error: COP row 1 not found. ", {0:"Orders not found", 1:"Int time not found", 2:"Rhythm not found", 3:"Window height not found"}[max(found)])
        print(diffractionOrders)
        stop()
    
    #find description of observation
    description = getObservationDescription(channel, copTableDict, fixedCopRow, scienceCopRow, silent=True)
    outputDict = {"scienceCopRow":scienceCopRow, "fixedCopRow":fixedCopRow, "copRowDescription":description}
    
    return outputDict, diffractionOrders, integrationTime, rhythm, windowHeight, channelCode





        