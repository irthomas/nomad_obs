# -*- coding: utf-8 -*-
"""
Created on Tue Jun  4 14:25:48 2019

@author: iant


TEST WRITING CURRENT COP TABLES TO WEBPAGE

"""

import numpy as np
import os


from obs_config import BASE_DIRECTORY, COP_TABLE_DIRECTORY
from obs_inputs import getMtpConstants


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





def findIndex(valueIn,listIn):
    
    if valueIn in listIn:
        indexOut = [index for index,value in enumerate(listIn) if value == valueIn]
        if len(indexOut) > 1:
            print("Error: Multiple values found")
        else:
            return indexOut[0]
    else:
        print("Error: Not found")
    




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




def calcExecutionTime(number_accumulations, window_height, integration_time): #real number of rows (16, 20, 24), int time in milliseconds
    return ((number_accumulations+1.0) * ((integration_time * 1000.0) + 71.0 + 320.0 * window_height + 1000.0) + 337.0) / 1000.0



def uniqueDiffractionOrders(aotf_order_list):
    tuples = [tuple(i) for i in aotf_order_list]
    uniqueTuples = set(tuples)
    unique_orders = [list(i) for i in uniqueTuples]
    return unique_orders




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
    sbsfAll = []
    
#    subdomainRow = subdomainList[1000]
    for rowIndex, subdomainRow in enumerate(subdomainList):
        nSubdomains = 6 - subdomainRow.count("0")
        
        steppingIndices = []
        accumulations = []
        binningFactors = []
        integrationTimes = []
        sbsfs = []
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

            sbsf = int(scienceRow[2])
            sbsfs.append(sbsf)
        
            aotfIndex = int(scienceRow[3])
            
            if scienceIndex == 0: #if subdomain selection blank:
                aotfOrder = -1
            else:
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

        if len(set(sbsfs)) == 1: #if more than one integration time in the observation
            sbsfSingle = sbsfs[0]
        else:
            if not silent: print("Sbsf error row %i" %rowIndex)
            if not silent: print(sbsf)
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
            sbsfAll.append(sbsfSingle)
            
    copTableCombinations = {"index":subdomainIndices, "orders":aotfOrdersAll, "integrationTime":integrationTimesAll, "rhythm":rhythmAll, "windowHeight":windowHeightAll, "sbsf":sbsfAll}
    return copTableCombinations






mtpNumber = 21

for channelCode in [0,1]:
    mtpConstants = getMtpConstants(mtpNumber)
    copTableDict = getCopTables(mtpConstants)
    
    channel = {0:"so", 1:"lno"}[channelCode]
    
    html_title = "%s channel COP row combinations" %channel.upper()
    html_header = ["Order 1", "Order 2", "Order 3", "Order 4", "Order 5", "Order 6", "Options (integration time, rhythm, window height)"]
    html_page_name = html_title.replace(" ","_").lower()
    
    copTableCombinationDict = {
            0:makeCopTableDict(0, copTableDict), \
            1:makeCopTableDict(1, copTableDict)
            }
    
    allowedIntegrationTimeDict = {
            0:[2.0, 4.0, 6.0, 10.0, 20.0, 40.0], \
            1:range(1000)}
    
    allowedIntegrationTimes = allowedIntegrationTimeDict[channelCode]
    
    defaultColour = "FFFFFF"
    colourDict = {119:"FF8F8F", 120:"FF5656", 121:"FF0000", 122:"D90000", 123:"BE0000",
                  130:"FAFAFA", 131:"E9E9E9", 132:"DADADA", 133:"BCBCBC", 134:"9C9C9C", 135:"838383", 136:"6D6D6D",
                  146:"FFFFA0", 147:"FFFF6F", 148:"FFFF21", 149:"E9E900", 150:"D8D800",
                  163:"FFD4FF", 164:"FFA4FE", 165:"FF5FFD", 166:"FF00FC",
                  167:"CEFFA8", 168:"B4FF7A", 169:"92FF3F", 170:"5BD300", 171:"4FB800",
                  186:"BDE4FF", 187:"7CC9FF", 188:"2CA8FF", 189:"0083DF", 190:"006FBD", 191:"2835FF", 192:"000DDE",
                  193:"FFDBA9", 194:"FFC87C", 195:"FFB349", 196:"FF9500", 197:"E68600", 198:"C47200"}
    
    
    def getMolecule(order):
        
        if 119 <= order <= 123:
            molecule = "HDO/CO2 (SO <60km)"
        elif 130 <= order <=136:
            molecule = "CH4/H2O (SO <60km)"
        elif 146 <= order <= 150:
            molecule = "CO2 (SO 60-100km)"
        elif 163 <= order <= 166:
            molecule = "CO2 (SO >100km)"
        elif 167 <= order <= 171:
            molecule = "H2O (SO >60km)"
        elif 186 <= order <= 192:
            molecule = "CO"
        else:
            molecule = "Nadir dust/surface"
        return molecule
    
    copTableCombinations = copTableCombinationDict[channelCode]
    
    ordersList = copTableCombinations["orders"]
    
    #remove single orders e.g. special darks, SO limbs, or calibrations (not those where 5x darks)
    #ordersList = [orders for orders in ordersList if len(orders)>2]
    
    ordersList = [sorted(orders + [-1]*(6 - len(orders))) for orders in ordersList]
    
    uniqueOrdersList = uniqueDiffractionOrders(ordersList)
    
    uniqueOrdersListSorted = sorted(uniqueOrdersList, key=lambda x: (x[5], x[4], x[3], x[2], x[1], x[0]))
    
    
    #next move the observations where all orders the same to the bottom of the list
    singleOrders = []
    uniqueOrdersListSorted2 = []
    
    for listIndex, uniqueOrders in enumerate(uniqueOrdersListSorted):
        if uniqueOrders[1] == uniqueOrders[2] == uniqueOrders[5]: #all same order
#            print(uniqueOrders)
            singleOrders.append(uniqueOrders)
        else:
            uniqueOrdersListSorted2.append(uniqueOrders)
    uniqueOrdersListSorted = uniqueOrdersListSorted2 + singleOrders
    
    
    #prepare tables for each number of diffraction orders (0 = calibration if used in future)
    tables = {0:"", 1:"", 2:"", 3:"", 4:"", 5:"", 6:""}
    
    #make table in html and add to all tables
    h = r"<div style='white-space:pre;overflow:auto;width:2000px;padding:10px;'>"
    h += r"<table border=1 style='width:1600px;'>"+"\n"
    h += r"<tr>"+"\n"
    for headerColumn in html_header:
        h += r"<th>%s</th>" %headerColumn +"\n"
    h += r"</tr>"+"\n"
    
    for numberOfOrders in [0,1,2,3,4,5,6]:
        tables[numberOfOrders] += h
    
    
    #search for unique order combinations in list of all, to find different obs parameters for each order combination
    for uniqueOrders in uniqueOrdersListSorted:
        integrationTimes = []
        rhythms = []
        windowHeights = []
        sbsfs = []
        comment = ""
        found = False
        for index, orders in enumerate(ordersList):
            if uniqueOrders == orders:
                
                integrationTime = copTableCombinations["integrationTime"][index]
                rhythm = copTableCombinations["rhythm"][index]
                windowHeight = copTableCombinations["windowHeight"][index]
                sbsf = copTableCombinations["sbsf"][index]
                
                if integrationTime in allowedIntegrationTimes:
    #            if integrationTime in [4.0] and windowHeight in [16, 20] and rhythm in [1]:
                    found = True
                
                    integrationTimes.append(integrationTime)
                    rhythms.append(rhythm)
                    windowHeights.append(windowHeight)
                    sbsfs.append(sbsf)
                    
    #                comment += "IT=%0.1f, rhythm=%i, wHeight=%i; " %(integrationTime, rhythm, windowHeight)
                    comment += "(%0.1fms, %is, %ipx, bg%s); " %(integrationTime, rhythm, windowHeight, {0:"OFF", 1:"ON"}[sbsf])
                else:
                    print("IT=%0.1f, rhythm=%i, wHeight=%i; bg=%s; " %(integrationTime, rhythm, windowHeight, {0:"OFF", 1:"ON"}[sbsf]))
    
    
        if found:
            nOrders = np.sum([1 for order in uniqueOrders if order>0])
            h = r"<tr>" +"\n"
            for order in uniqueOrders[::-1]:
                if order == 0:
                    h += r"<td>Dark</td>" +"\n"
                elif order == -1:
                    h += r"<td>---</td>" +"\n"
                else:
                    if order in colourDict.keys(): #if order has a colour, get it
                        colour = colourDict[order]
                    else: #if not, use white background
                        colour = defaultColour
                    h += r"<td bgcolor='#%s'>%s</td>" %(colour, order) +"\n"
                    
            h += r"<td>%s</td>" %comment +"\n" #add comment with different obs parameter combinations
            h += r"</tr>" +"\n"
            
            for numberOfOrders in [0,1,2,3,4,5,6]: #add table row to correct table, based on number of orders
                if nOrders == numberOfOrders:
                    tables[numberOfOrders] += h
            
    h = r"</table>" +"\n"
    h += r"</div>" +"\n"
    
    for numberOfOrders in [0,1,2,3,4,5,6]:
        tables[numberOfOrders] += h
    
    
    
    h = r""
    h += r"<h1>%s</h1>" %html_title +"\n"
    
    h += r"<div style='white-space:pre;overflow:auto;width:2000px;padding:10px;'>"
    h += r"<table border=1 style='width:1600px;'>"+"\n"
    h += r"<tr>"+"\n"
    for headerColumn in ["Order", "Molecule(s)"]:
        h += r"<th>%s</th>" %headerColumn +"\n"
    for order, colour in colourDict.items():
        h += r"</tr>" +"\n"
        h += r"<td bgcolor='#%s'>%s</td><td bgcolor='#%s'>%s</td>" %(colour, order, colour, getMolecule(order)) +"\n"
        h += r"</tr>"+"\n"
    h += r"</table>" +"\n"
    h += r"</div>" +"\n"
        
    
    for numberOfOrders in [1,2,3,4,5,6]:
        h += r"<h2>%s diffraction orders</h2>" %numberOfOrders +"\n"
        h += tables[numberOfOrders]
        h += "<br><br>" +"\n"

    
    f = open(os.path.join(BASE_DIRECTORY, html_page_name+".html"), 'w')
    f.write(h)
    f.close()
    





