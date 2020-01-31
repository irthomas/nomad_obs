# -*- coding: utf-8 -*-
"""
Created on Mon Apr 24 10:30:58 2017

@author: iant

SCRIPT TO GENERATE COP TABLES


VERSION=5  2019 VERSION


REMOVE ALL 2 SECOND OCCULTATIONS
REMOVE VARIABLE INT TIME


PRIORITISE MAX NUMBER OF DIFFRACTION ORDERS


ADD LNO FIXED ROWS FOR 16 LINE OCCULTATIONS







"""
import numpy as np
import os
from datetime import datetime
import xlrd
from generate_cop_tables_dictionaries_v05 import MAX_EXECUTION_TIME, MAX_ROWS, MIN_EXECUTION_TIME, MINISCAN_ROWS
from generate_cop_tables_dictionaries_v05 import MINISCAN_STARTING_ORDERS, FIXED_ROWS, FULLSCAN_ROWS, WINDOW_STEPPING_ROWS
from generate_cop_tables_dictionaries_v05 import INTEGRATION_TIME_STEPPING_ROWS, SCIENCE_ROWS, STEPPING_ROWS
from generate_cop_tables_dictionaries_v05 import DEFAULT_FIXED_ROWS, SUBDOMAIN_SCIENCE_ROWS


ORDER_COMBINATION_FILE = "EXM-NO-SNO-AER-00028-iss0rev4-SO_LNO_COP_Table_Order_Combinations-180528.xlsx"

BASE_DIRECTORY = os.path.normcase(r"C:\Users\iant\Dropbox\NOMAD\Python")
AUXILIARY_DIRECTORY = os.path.join(BASE_DIRECTORY, "data", "pfm_auxiliary_files")


MODEL = "PFM"

#channels=["so","lno"]
channels=["so"]

#PRINT_FLAG=True
PRINT_FLAG=False


folder_name = datetime.now().strftime("%Y%m%d_%H%M%S")
OUTPUT_DIRECTORY = os.path.join(BASE_DIRECTORY, "data", "cop_tables", folder_name)




"""FUNCTIONS"""
def exec_time(n_acc, window_height, int_time):
    """input COP table values, return microseconds"""
    return int(((n_acc+1.0) * (int_time + 71.0 + 320.0 * (window_height + 1.0) + 1000.0) + 337.0) )

def executionTime(accumulation_count, n_rows, n_subd, integration_time):
    """use real number of rows"""
    window_height = np.float32(n_rows - 1.0)
    return int(np.ceil(exec_time(accumulation_count, window_height, integration_time) * np.float32(n_subd)))



def n_acc(max_exec_time, window_height, int_time):
    n_accs_float = (max_exec_time - 337.0) / (int_time + 71.0 + 320.0 * (window_height + 1.0) + 1000.0) - 1.0
    n_accs = int(np.floor(n_accs_float/2.0) * 2.0) #make even for all observations, sbsf 0 or 1
    return n_accs

def getAccumulationCount(max_exec_time, n_rows, int_time):
    """use real number of rows"""
    window_height = np.float32(n_rows - 1.0)
    return n_acc(max_exec_time, window_height, int_time)



def getBinningFactor(n_rows, n_subdomains, rows=24):
    """use real number of rows, return COP table style binning factor (-1)"""
    n_bins = np.float(n_rows) / (np.float(rows)/np.float(n_subdomains))
    if np.round(n_bins) == n_bins:
        return int(n_bins)-1
    else:
        print("Error: n_bins is not an integer: %0.2f, %i" %(n_bins,int(n_bins)))
        print(n_rows, n_subdomains, rows)
        stop()


def getWindowHeight(binning_factor, n_subdomains, rows=24):
    """use COP table binning_factor, output COP table window height"""
    n_rows_per_subdomain = rows / n_subdomains
    if np.round(n_rows_per_subdomain) == n_rows_per_subdomain:
        window_height = (n_rows_per_subdomain * (binning_factor+1)) - 1
        return int(window_height)
    else:
        print("Error: n_rows_per_subdomain is not an integer: %0.2f, %i" %(n_rows_per_subdomain,int(n_rows_per_subdomain)))
        print(n_subdomains, rows)
        stop()
    


def checkExecTime(exec_time_microsecs, rhythm, silent=False):
    """check if execution time is between min and max values"""    
    min_exec_time = MIN_EXECUTION_TIME[rhythm]
    max_exec_time = MAX_EXECUTION_TIME[rhythm]
    if exec_time_microsecs < min_exec_time:
        if not silent: print(f"Error: execution time too small (exec_time={exec_time_microsecs}, min_exec_time={min_exec_time}, rhythm={rhythm}")
#        stop()
        return 0
    else:
        if exec_time_microsecs > max_exec_time:
            if not silent: print(f"Error: Execution time too large (exec_time={exec_time_microsecs}, max_exec_time={max_exec_time}, rhythm={rhythm}")
#            stop()
            return 0
        else:
            return 1





"""read in order combinations from excel spreadsheet"""
def load_order_combinations(channel,nsubd):
    global OUTPUT_DIRECTORY

    book = xlrd.open_workbook(OUTPUT_DIRECTORY.split("\\2")[0]+os.sep+ORDER_COMBINATION_FILE)
    sheet = book.sheet_by_index(0) #get first sheet from spreadsheet
    
    if channel == "lno":
        if nsubd == 2:
            columns = [1,2]
        elif nsubd == 3:
            columns = [4,5,6]
        elif nsubd == 4:
            columns = [8,9,10,11]
        elif nsubd == 6:
            columns = [13,14,15,16,17,18]
        elif nsubd == 5: #OCCULTATION
            columns = [20,21,22,23,24,25]
        else:
            print("Error: combination of channel and nsubd not found")
            stop()
    elif channel == "so":
        if nsubd == 5:
            columns = [27,28,29,30,31,32]
        elif nsubd == 6:
            columns = [34,35,36,37,38,39]
        else:
            print("Error: combination of channel and nsubd not found")
            stop()
    else:
        print("Error: combination of channel and nsubd not found")
        stop()
    
    data_in = []
    for column in columns:
        data_in.append(sheet.col_values(column))
        
    if nsubd == 2:
        data_zipped_all = list(zip(data_in[0],data_in[1]))
    if nsubd == 3:
        data_zipped_all = list(zip(data_in[0],data_in[1],data_in[2]))
    if nsubd == 4:
        data_zipped_all = list(zip(data_in[0],data_in[1],data_in[2],data_in[3]))
    if nsubd == 5 or nsubd ==6:
        data_zipped_all = list(zip(data_in[0],data_in[1],data_in[2],data_in[3],data_in[4],data_in[5]))
 
    data_out = [data_line for data_line in data_zipped_all if data_line[0] != ""]
    
    return data_out



def readScienceComments(scienceLines, nScienceCalRows):
    """get science lines from list, remove calibration lines. Extract data from comments"""
    import re

    newScienceTable = []
    NA_LINE = ["-999"]*4
    for rowIndex, scienceLine in enumerate(scienceLines[1:]):
        if rowIndex in range(nScienceCalRows):
            newScienceTable.append(["-999"]*12)
        else:
            scienceValues = scienceLine.split(" #")[0].split(",")

            scienceComment = scienceLine.split("#")[1]
            regex = re.findall("(\d+)ROWS.*_(\d+)SECS.*_(\d+)SUBD.*EXECTIME=(\d+)MS.*", scienceComment)
            if len(regex) == 1:
                if len(regex[0]) == 4:
#                    nrows, rhythm, nsubd, exectime = regex[0]
                    newScienceTable.append(scienceValues + list(regex[0]))
                else:
                    newScienceTable.append(scienceValues + NA_LINE)
            else:
                newScienceTable.append(scienceValues + NA_LINE)
            
    return newScienceTable
    



def writeTable(channel, table_name, lines):
    """write cop csv file"""
    os.makedirs(OUTPUT_DIRECTORY, exist_ok=True)
    with open(OUTPUT_DIRECTORY+os.sep+"%s_%s_table.csv" %(channel,table_name), "w") as f:
        for line in lines:
            f.write(line+"\n")


def stop():
#    import sys
    print("**********Fatal Error********")
    halt
#    sys.exit() #breaks program
    return 0







def makeSteppingTable(channel):

    """STEPPING COP TABLE"""
    #write EMTPY rows everywhere first
    steppingHeaders = ["stepValue","steppingParameter","stepCount","stepSpeed"]
    steppingLines = [",".join(steppingHeaders)]
    #channel, code [stepping pointer, value, parameter, count, speed]
    for rowNumber in range(256):
        stepValue, steppingParameter, stepCount, stepSpeed = STEPPING_ROWS[channel]["EMPTY ROW"][1:]
        comment = "EMPTY ROW"
        steppingLines.append(f"{stepValue},{steppingParameter},{stepCount},{stepSpeed} # {comment}")
        
    #then add real data
    #channel, code [stepping pointer, value, parameter, count, speed]
    for comment in STEPPING_ROWS[channel].keys():
        rowNumber = STEPPING_ROWS[channel][comment][0] + 1 #header in row 0, row 1 must be empty
        stepValue, steppingParameter, stepCount, stepSpeed = STEPPING_ROWS[channel][comment][1:]
        steppingLines[rowNumber] = f"{stepValue},{steppingParameter},{stepCount},{stepSpeed} # {comment}"
    
    return steppingLines


def makeFixedTable(channel):
    """FIXED COP TABLE"""
    detectorSupply=1
    aotfDelay=1
    dataSource=0
    dataValidSource=0
    fixed_headers = ["windowLineCount","windowLeftTop","detectorSupply","aotfDelay","dataSource","dataValidSource","rythm"]
    
    
    fixedLines = [",".join(fixed_headers)]
    #channel nrows rhythm [windowtops, comment]
    for nrows in DEFAULT_FIXED_ROWS[channel].keys():
        windowLineCount = nrows - 1
        for rythm in DEFAULT_FIXED_ROWS[channel][nrows].keys():
            windowLeftTops, comment = DEFAULT_FIXED_ROWS[channel][nrows][rythm]
            for windowLeftTop in windowLeftTops:
                fixedLines.append(f"{windowLineCount},{windowLeftTop},{detectorSupply},{aotfDelay},{dataSource},{dataValidSource},{rythm} # {comment}")
    
    for nrows in FIXED_ROWS[channel].keys():
        windowLineCount = nrows - 1
        for rythm in FIXED_ROWS[channel][nrows].keys():
            windowLeftTops, comment = FIXED_ROWS[channel][nrows][rythm]
            for windowLeftTop in windowLeftTops:
                fixedLines.append(f"{windowLineCount},{windowLeftTop},{detectorSupply},{aotfDelay},{dataSource},{dataValidSource},{rythm} # {comment}")

    print("Number of %s fixed lines = %i" %(channel, len(fixedLines)))
    while len(fixedLines) < 257:
        windowLineCount = windowLeftTop = detectorSupply = aotfDelay = dataSource = dataValidSource = rythm = 0
        comment = "EMPTY ROW"
        fixedLines.append(f"{windowLineCount},{windowLeftTop},{detectorSupply},{aotfDelay},{dataSource},{dataValidSource},{rythm} # {comment}")


    return fixedLines


def makeScienceTable(channel):
    """MAKE SCIENCE CALIBRATION TABLE"""
    science_headers = ["degf","dvaf","sbsf","aotfPointer","steppingPointer","accumulationCount","binningFactor","integrationTime"]
    degf = 0
    dvaf = 1
    sbsf = 1
    
    nScienceCalRows = 0
    scienceLines = [",".join(science_headers)]
    
    #first line must be 0
    aotfPointer = steppingPointer = accumulationCount = binningFactor = integrationTime = 0
    comment = "EMPTY_ROW"
    scienceLines.append(f"{degf},{dvaf},{sbsf},{aotfPointer},{steppingPointer},{accumulationCount},{binningFactor},{integrationTime} # {comment}")
    nScienceCalRows += 1
    
    
    """WINDOW STEPPING"""
    for steppingCode in WINDOW_STEPPING_ROWS[channel].keys():
        aotfPointers, integrationTime, rythm = WINDOW_STEPPING_ROWS[channel][steppingCode]
        
        #channel, code [stepping pointer, stepValue, stepParameter, stepCount, stepSpeed]
        steppingPointer, nrows, _, _, stepSpeed = STEPPING_ROWS[channel][steppingCode]
        
        nsubd = stepSpeed + 1
        
        maxExecTimeRhythm = MAX_EXECUTION_TIME[rythm]
        maxExecTime = np.float32(maxExecTimeRhythm) / np.float32(nsubd)
        accumulationCount = getAccumulationCount(maxExecTime, nrows, integrationTime)
        binningFactor = getBinningFactor(nrows, nsubd)
        execTime = executionTime(accumulationCount, nrows, nsubd, integrationTime)
        execTimeText = "%i" %(execTime/1000.0)
    
        for aotfPointer in aotfPointers:
            comment = f"{steppingCode}_{nrows}ROWS -- EXECTIME={execTimeText}MS"
            scienceLines.append(f"{degf},{dvaf},{sbsf},{aotfPointer},{steppingPointer},{accumulationCount},{binningFactor},{integrationTime} # {comment}")
            nScienceCalRows += 1
    
    """INT TIME STEPPING"""
    sbsf = 0
    for steppingCode in INTEGRATION_TIME_STEPPING_ROWS[channel].keys():
        aotfPointers, nrows, integrationTime, accumulationCount, rythm = INTEGRATION_TIME_STEPPING_ROWS[channel][steppingCode]
    
        #channel, code [stepping pointer, stepValue, stepParameter, stepCount, stepSpeed]
        steppingPointer, integrationTimeStep, _, integrationTimeSteps, stepSpeed = STEPPING_ROWS[channel][steppingCode]
    
        nsubd = stepSpeed + 1
    
        maxExecTimeRhythm = MAX_EXECUTION_TIME[rythm]
        maxExecTime = np.float32(maxExecTimeRhythm) / np.float32(nsubd)
        binningFactor = getBinningFactor(nrows, nsubd)
        maxIntegrationTime = integrationTime + integrationTimeStep * integrationTimeSteps
        execTime = executionTime(accumulationCount, nrows, nsubd, maxIntegrationTime)
        execTimeText = "%i" %(execTime/1000.0)
    
        for aotfPointer in aotfPointers:
            comment = f"{steppingCode}_{nrows}ROWS_{integrationTimeStep}MS -- EXECTIME={execTimeText}MS"
            scienceLines.append(f"{degf},{dvaf},{sbsf},{aotfPointer},{steppingPointer},{accumulationCount},{binningFactor},{integrationTime} # {comment}")
            nScienceCalRows += 1
    
    
           
    sbsf = 1
    #channel nrows stepspeed nsteps [starting orders, inttime, comment]
    for nrows in FULLSCAN_ROWS[channel].keys():
        for nsubd in FULLSCAN_ROWS[channel][nrows].keys(): #nsubd = stepSpeed
            for stepSizeOrder in FULLSCAN_ROWS[channel][nrows][nsubd].keys():
                aotfPointers, integrationTime, rythm, base_comment = FULLSCAN_ROWS[channel][nrows][nsubd][stepSizeOrder]
    
                steppingCode = "FULLSCAN_%iORDERS_%iSUBDS" %(stepSizeOrder, nsubd)
                steppingPointer = STEPPING_ROWS[channel][steppingCode][0]
    
                maxExecTimeRhythm = MAX_EXECUTION_TIME[rythm]
                maxExecTime = np.float32(maxExecTimeRhythm) / np.float32(nsubd)
                accumulationCount = getAccumulationCount(maxExecTime, nrows, integrationTime)
                binningFactor = getBinningFactor(nrows, nsubd)
                execTime = executionTime(accumulationCount, nrows, nsubd, integrationTime)
                execTimeText = "%i" %(execTime/1000.0)
    
                comment = base_comment
                comment += f"_{stepSizeOrder}ORDERS_{nrows}ROWS_{rythm}SECS_{nsubd}SUBDS -- EXECTIME={execTimeText}MS"
                checkExecTime(execTime, rythm)
                
                for aotfPointer in aotfPointers:
                    scienceLines.append(f"{degf},{dvaf},{sbsf},{aotfPointer},{steppingPointer},{accumulationCount},{binningFactor},{integrationTime} # {comment}")
                    nScienceCalRows += 1
                    
    
    
    #channel nrows rhythm nsubd [step, inttime, comment]
    for nrows in MINISCAN_ROWS[channel].keys():
        for rythm in MINISCAN_ROWS[channel][nrows].keys():
            for nsubd in MINISCAN_ROWS[channel][nrows][rythm].keys():
                stepsKhz, integrationTime, base_comment = MINISCAN_ROWS[channel][nrows][rythm][nsubd]
                for stepSizeKhz in stepsKhz:
                    
                    steppingCode = "MINISCAN_%iKHZ_%iSUBDS" %(stepSizeKhz, nsubd)
                    steppingPointer = STEPPING_ROWS[channel][steppingCode][0]
                    
                    #look in other dictionary for matching step sizes / diffraction orders
                    #khzstep [starting orders]
                    if stepSizeKhz in MINISCAN_STARTING_ORDERS[channel].keys():
                        aotfPointers = MINISCAN_STARTING_ORDERS[channel][stepSizeKhz]
                    
                        maxExecTimeRhythm = MAX_EXECUTION_TIME[rythm]
                        maxExecTime = np.float32(maxExecTimeRhythm) / np.float32(nsubd)
                        accumulationCount = getAccumulationCount(maxExecTime, nrows, integrationTime)
                        
                        #code to fudge accumulation count reduction:
                        if base_comment == "OCCULTATION_MINISCAN_SLOW" and stepSizeKhz == 4:
                                accumulationCounts = [accumulationCount-20, accumulationCount-10, accumulationCount]
                        else:
                            accumulationCounts = [accumulationCount]
                        
                        for accumulationCount in accumulationCounts:
                            binningFactor = getBinningFactor(nrows, nsubd)
                            execTime = executionTime(accumulationCount, nrows, nsubd, integrationTime)
                            execTimeText = "%i" %(execTime/1000.0)
                            
                            comment = base_comment
                            comment += f"_{stepSizeKhz}KHZ_{nrows}ROWS_{rythm}SECS_{nsubd}SUBDS -- EXECTIME={execTimeText}MS"
                            checkExecTime(execTime, rythm)
        
                            
                            for aotfPointer in aotfPointers:
                                scienceLines.append(f"{degf},{dvaf},{sbsf},{aotfPointer},{steppingPointer},{accumulationCount},{binningFactor},{integrationTime} # {comment}")
                                nScienceCalRows += 1
                    else:
                        print("Error: stepSize not found in dictionary")
    


            
    
    """MAKE SCIENCE TABLE"""
    degf = 0
    dvaf = 1
    sbsfs = [0,1]
    #accumulationCount = 0
    #binningFactor = 0
    steppingPointer = 0
    
    
    
    #channel nrows rhythm nsubd [inttimes, comment]
    for sbsf in sbsfs:
        for nrows in SCIENCE_ROWS[channel].keys():
            for rythm in SCIENCE_ROWS[channel][nrows].keys():
                for nsubd in SCIENCE_ROWS[channel][nrows][rythm].keys(): #steps
    
                    integrationTimes, aotfPointers, validSbsfs, base_comment = SCIENCE_ROWS[channel][nrows][rythm][nsubd]
                    if sbsf in validSbsfs:

                        for integrationTime in integrationTimes:
    
                            maxExecTimeRhythm = MAX_EXECUTION_TIME[rythm]
                            maxExecTime = np.float32(maxExecTimeRhythm) / np.float32(nsubd)
                            accumulationCount = getAccumulationCount(maxExecTime, nrows, integrationTime)
                            binningFactor = getBinningFactor(nrows, nsubd)
                            execTime = executionTime(accumulationCount, nrows, nsubd, integrationTime)
                            execTimeText = "%i" %(execTime/1000.0)
        
                            comment = base_comment
                            comment += f"_{nrows}ROWS_{rythm}SECS_{nsubd}SUBDS -- EXECTIME={execTimeText}MS"
                            checkExecTime(execTime, rythm)
                            
                            for aotfPointer in aotfPointers:
                                scienceLines.append(f"{degf},{dvaf},{sbsf},{aotfPointer},{steppingPointer},{accumulationCount},{binningFactor},{integrationTime} # {comment}")


    print("Number of %s science lines = %i" %(channel, len(scienceLines)))
    while len(scienceLines) < 4097:
        degf = dvaf = sbsf = aotfPointer = steppingPointer = accumulationCount = binningFactor = integrationTime = 0
        comment = "EMPTY ROW"
        scienceLines.append(f"{degf},{dvaf},{sbsf},{aotfPointer},{steppingPointer},{accumulationCount},{binningFactor},{integrationTime} # {comment}")


    return scienceLines, nScienceCalRows



for channel in channels:


    """MAKE SUBDOMAIN TABLE"""
    steppingLines = makeSteppingTable(channel)
    fixedLines = makeFixedTable(channel)
    scienceLines, nScienceCalRows = makeScienceTable(channel)
    
    
    """WRITE TABLES"""
        
    tableNames = {"fixed":fixedLines, "science":scienceLines, "stepping":steppingLines}
    
    for tableName, tableLines in tableNames.items():
        max_rows = MAX_ROWS[tableName]
        if len(tableLines) > max_rows:
            print("Error: too many lines in table!")
            stop()
        writeTable(channel, tableName, tableLines)
    

    
    if channel == "so":
        from generate_cop_tables_order_combinations_v05 import newSoObservationDict as newObservationDict
        from generate_cop_tables_order_combinations_v05 import specialSoObservationDict as specialObservationDict
    elif channel == "lno":
        from generate_cop_tables_order_combinations_v05 import newLnoObservationDict as newObservationDict
        from generate_cop_tables_order_combinations_v05 import specialLnoObservationDict as specialObservationDict
    
    
    nSubdomainRows = 0
    subdomain_headers = ["science_1","science_2","science_3","science_4","science_5","science_6"]
    subdomainLines = [",".join(subdomain_headers)]

#    #first line must be 0 already accounted for in science table copy

    
    for sciencePointer in range(0, nScienceCalRows, 1):
        comment = scienceLines[sciencePointer +1].split("#")[1]
        subdomainLines.append(f"{sciencePointer},0,0,0,0,0 # {comment}")
    
        
        
    scienceTable = readScienceComments(scienceLines, nScienceCalRows)
        
    #set up dictionary
    nsubdomains = {
            "so":[1, 2, 6], #5 orders + dark = 6SUBD
            "lno":[1, 2, 3, 4, 5, 6],
            }
    orderCombinationDict = {}
    orderCombinationDict[channel] = {}
    for nsubd in nsubdomains[channel]:
        orderCombinationDict[channel][nsubd] = {}
    
    
    
    """NOTE: int times, nrows, etc given in observationDict are ignored"""
    #sort obs by nsubd and add to output dictionary
    for obsName, obsData in newObservationDict.items():
        nOrders = len(obsData[0])
        orderCombinationDict[channel][nOrders][obsName] = obsData[0] #get orders only
    
    """NOTE: int times, nrows, etc given in observationDict are ignored"""
    #get order combinations from existing and new dictionaries, then combine with all options to make 
    for nsubdRequired, observations in orderCombinationDict[channel].items():
        for obsName, orderCombination in observations.items():
            nLightOrders = sum([1 for order in orderCombination if order>0])
            nDarkOrders = sum([1 for order in orderCombination if order == 0])
            if nDarkOrders > 0:
                sbsfRequired = 0
            else:
                sbsfRequired = 1
            
            #loop through science row parameters, finding each in scienceTable
            #channel nrows rhythm nsubd sbsf [inttimes]
            for nrowsRequired in SUBDOMAIN_SCIENCE_ROWS[channel].keys():
                for rhythmRequired in SUBDOMAIN_SCIENCE_ROWS[channel][nrowsRequired].keys():
                    if nsubdRequired in SUBDOMAIN_SCIENCE_ROWS[channel][nrowsRequired][rhythmRequired].keys():
                        inttimesRequired = SUBDOMAIN_SCIENCE_ROWS[channel][nrowsRequired][rhythmRequired][nsubdRequired]
                        for inttimeRequired in inttimesRequired:
                            sciencePointers = []
                            for diffractionOrder in orderCombination:
                                #search science lines for data
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
                                
#                            longComments = "(" + " & ".join([scienceLines[index+1][4:].replace(","," ") for index in sciencePointers if index>0]) + ")"
#                            comment = "ORDERS " + " ".join([str(i) for i in orderCombination]) + ": " + longComments
                            
                            longComment = scienceLines[sciencePointers[0]+1].split("#")[1].strip()
                            comment = "ORDERS " + " ".join([str(i) for i in orderCombination]) + " -- " + longComment
                            
                            
                            subdomainLines.append(f"{sciencePointers[0]},{sciencePointers[1]},{sciencePointers[2]},{sciencePointers[3]},{sciencePointers[4]},{sciencePointers[5]} # {comment}")
                            
    #make special observations
    """here we take the int times, rhythm and nrows directly from the dictionary. Ignore so/lno flag"""
    for obsName, obsData in specialObservationDict.items():
        orderCombination, inttimeRequired, rhythmRequired, nrowsRequired, _ = obsData

        inttimeRequired *= 1000 #stored in ms in dictionary
        nsubdRequired = len(orderCombination)
        nLightOrders = sum([1 for order in orderCombination if order>0])
        nDarkOrders = sum([1 for order in orderCombination if order == 0])
        if nDarkOrders > 0:
            sbsfRequired = 0
        else:
            sbsfRequired = 1


        sciencePointers = []
        for diffractionOrder in orderCombination:
            #search science lines for data
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
            
#        longComments = "(" + " & ".join([scienceLines[index+1][4:].replace(","," ") for index in sciencePointers if index>0]) + ")"
#        comment = "ORDERS " + " ".join([str(i) for i in orderCombination]) + ": " + longComments
            
        longComment = scienceLines[sciencePointers[0]+1].split("#")[1].strip()
        comment = "ORDERS " + " ".join([str(i) for i in orderCombination]) + " -- " + longComment

        subdomainLines.append(f"{sciencePointers[0]},{sciencePointers[1]},{sciencePointers[2]},{sciencePointers[3]},{sciencePointers[4]},{sciencePointers[5]} # {comment}")
        
    
    print("Number of %s subdomain lines = %i" %(channel, len(subdomainLines)))
    while len(subdomainLines) < 4097:
        sciencePointers = [0] * 6
        comment = "EMPTY ROW"
        subdomainLines.append(f"{sciencePointers[0]},{sciencePointers[1]},{sciencePointers[2]},{sciencePointers[3]},{sciencePointers[4]},{sciencePointers[5]} # {comment}")
    
    
    
    """WRITE TABLES"""
            
    tableNames = {"sub_domain":subdomainLines}
    
    for tableName, tableLines in tableNames.items():
        max_rows = MAX_ROWS[tableName]
        if len(tableLines) > max_rows:
            print("Error: too many lines in table!")
            stop()
        writeTable(channel, tableName, tableLines)
    





"""CHECK TABLES"""


#stop()





"""function to read in cop tables, given channel and name"""
def read_in_cop_table(channel,cop):
    csv_filename=OUTPUT_DIRECTORY+os.sep+"%s_%s_table.csv" %(channel,cop)
    with open(csv_filename) as f:
        cop_list=[]
        for index,line in enumerate(f):
            content = line.strip('\n').split(',')
            if index==0: #if first line
                cop_headers=content #record header data
                cop_headers.append("comments")
            else:
                if content[len(content)-1].find('#') != -1: #if comment line
                    temp=content[len(content)-1].split('#') #split last field into value and comment
                    content[len(content)-1]=temp[0].strip() #replace last column with value only
                    content.append(temp[1].strip()) #add new column on end for the comment
                else:
                    content.append("NONE")
                cop_list.append(content)
    return cop_headers,cop_list




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





#        
#def calculate_best_inttimes(base_inttime, rhythm, nsubdomains, windowheight, sbsf, order_combinations=[[]], fix_inttime=False):
#    if rhythm > 1000000:
#        max_exec_time = rhythm - 400000
#    else:
#        max_exec_time = rhythm - 150000
#    
#    best_inttime = base_inttime
#    best_accumulations = 0
#    smallest_lost_time = 10000.0 #ms
#    best_execution_time = 0
#    
#    if fix_inttime:
#        possible_inttimes = [base_inttime]
#    else:
#        possible_inttimes = np.arange(base_inttime - 20000, base_inttime + 30000, 5000)
#
#    for inttime in possible_inttimes:
#        bins = n_bin(windowheight, nsubdomains, rows=24)
#        accumulations = n_acc(max_exec_time/nsubdomains, windowheight, inttime, sbsf)
#        execution_time = exec_time(accumulations, windowheight, inttime) * 1000
#        lost_time = (max_exec_time - execution_time * nsubdomains)/1000.0 #ms
#        if lost_time < smallest_lost_time:
#            smallest_lost_time = lost_time
#            best_inttime = inttime
#            best_accumulations = accumulations
#            best_execution_time = np.int(execution_time / 1000.0)
#        if not fix_inttime:
#            print("int time %i us = lost time %0.1f" %(inttime, lost_time))
#    print("Printing for NSUBD=%i, RHYTHM=%i" %(nsubdomains, rhythm/1000000))
#    
#    if fix_inttime:
#        print("Fixed inttime: %i us, %i accs, binning = %i. lost time %0.1f ms" %(best_inttime, best_accumulations, bins, smallest_lost_time))
#    else:
#        print("Best: %i us, %i accs, %i bins. lost time %0.1f ms" %(best_inttime, best_accumulations, bins, smallest_lost_time))
#    print("%i # NADIR_SCIENCE_%iSUBD -- EXECTIME=%iMS -- RHYTHM=%iMS -- NROWS=%i" 
#          %(best_inttime, nsubdomains, best_execution_time, rhythm/1000, windowheight))
#    for order_combination in order_combinations:
#        print("0 # NADIR_SCIENCE -- ORDERS "+"%i "*len(order_combination) %tuple(order_combination)+"-- INTTIME=%iMS -- EXECTIME=%iMS -- NROWS=%i"
#              %(best_inttime/1000, best_execution_time*nsubdomains, windowheight))
#


#write_cop_tables(channels)


#
#
##calculate_best_inttimes(base_inttime, rhythm, nsubdomains, windowheight, sbsf, order_combinations=orders, fix_inttime=True)
##calculate_best_inttimes(base_inttime, rhythm, nsubdomains, windowheight, sbsf, fix_inttime=True)
#
#
#"""CHANGE LNO OCC FROM 20 TO 16 ROWS"""
#rhythm = 1000000
#nsubdomains = 6
#windowheight = 16
#sbsf = 1
#
#orders = [
#[1,2,3,4,5,6],
#]
#    
#for base_inttime in [1000,2000,3000]:
#    print("Int time = %0.0fms" %(base_inttime/1000))
#  
#    calculate_best_inttimes(base_inttime, rhythm, nsubdomains, windowheight, sbsf, order_combinations=orders, fix_inttime=True)
##calculate_best_inttimes(base_inttime, rhythm, nsubdomains, windowheight, sbsf, fix_inttime=True)
#
#
#
#
#
#





