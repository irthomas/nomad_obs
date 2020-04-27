# -*- coding: utf-8 -*-
"""
Created on Mon Apr 27 12:34:12 2020

@author: iant
"""

import os
from datetime import datetime


from nomad_obs.mtp_inputs import getMtpConstants
from nomad_obs.cop_rows.cop_table_functions import getCopTables, outputCopTable, getObservationDescription




def writeCalibrationWebpage(paths):
    """write the science calibration webpage from Bojan's input file (place in OBS_DIRECTORY/calibrations)"""


    def readCalibrationsFromFile(paths):
        """read latest calibration file from Bojan/Claudio"""
        calibrationPath = paths["CALIBRATION_PATH"]
        calibrationFilePath = ""
        
        #check directory for calibration files
        #search for filename matching sequence
        lastMtps = []
        for fileName in os.listdir(calibrationPath):
            if "NOMAD_calibrations" in fileName:
                lastMtp = int(fileName.split("-")[1].replace(".txt",""))
                lastMtps.append(lastMtp)
        lastMtpInt = "-%03i.txt" %sorted(lastMtps)[-1] #get newest file from list of potential files
        
        for fileName in os.listdir(calibrationPath):
            if "NOMAD_calibrations" in fileName:
                if lastMtpInt in fileName:
                    calibrationFilePath = os.path.join(calibrationPath, fileName)
        
        #read lines
        if calibrationFilePath != "": #if file actually found
            with open(calibrationFilePath) as f:
                lines = []
                titles = []
                calibrations = []
                #remove unneeded lines
                for index, line in enumerate(f):
                    if line[0:3] == "MTP":
                        if index > 0:
                            calibrations.append(lines)
                            lines = []
                        content = line.strip().strip("%")
                        titles.append(content)
                    elif line[0] == "#":
                        lines.append(line.replace("# ",""))
        else:
            titles = []
            calibrations = []
    
        return titles, calibrations
    
    
    
    
    def textToNum(string):
        """convert string to int if possible"""
        try:
            return int(string)
        except ValueError:
            return -999
    
    h=r""
    h += r"<h1>NOMAD Science Phase Calibrations</h1>"+"\n"
    h += r"<h2>This page lists calibration observations only, and is maintained by hand (so may be out of date)</h2>"+"\n"
    h += r"<h2>Note that these are the predicted execution times. Real times could differ by up to 2 minutes</h2>"+"\n"
    h += r"<h2>Typically there are only 1 or 2 calibrations allowed per MTP</h2>"+"\n"
    
    
    titlesText, calibrationsText = readCalibrationsFromFile(paths)
    
    for title, calibration in zip(titlesText, calibrationsText):
        #find MTP
        calibrationMtpText = title.replace("MTP","").split("-")[0]
        calibrationMtp = textToNum(calibrationMtpText)
        
        if calibrationMtp > -1 and len(calibration) != 0:
            #get copVersion for each MTP
            mtpConstants = getMtpConstants(calibrationMtp)
            copVersion = mtpConstants["copVersion"]
            copTableDict = getCopTables(mtpConstants)
    
        
            
            
                    
            #get obs description from COP row
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
    
            
            soFixedRow = [int(value.replace("SO_COP_GENERAL = ","")) for value in calibration if "SO_COP_GENERAL" in value][0]
            lnoFixedRow = [int(value.replace("LNO_COP_GENERAL = ","")) for value in calibration if "LNO_COP_GENERAL" in value][0]
            
            soCopRow1 = [int(value.replace("SO_COP_SCIENCE_1 = ","")) for value in calibration if "SO_COP_SCIENCE_1" in value][0]
            soCopRow2 = [int(value.replace("SO_COP_SCIENCE_2 = ","")) for value in calibration if "SO_COP_SCIENCE_2" in value][0]
            lnoCopRow1 = [int(value.replace("LNO_COP_SCIENCE_1 = ","")) for value in calibration if "LNO_COP_SCIENCE_1" in value][0]
            lnoCopRow2 = [int(value.replace("LNO_COP_SCIENCE_2 = ","")) for value in calibration if "LNO_COP_SCIENCE_2" in value][0]
            
            uvisCopRow = [int(value.replace("UVIS_COP_ROW = ","")) for value in calibration if "UVIS_COP_ROW" in value][0]
            
            
            if soCopRow1 == soCopRow2:
                if soCopRow1 > 0:
                    soCopRows = [soCopRow1]
                else:
                    soCopRows = []
            else:
                soCopRows = [soCopRow1, soCopRow2]
    
            if lnoCopRow1 == lnoCopRow2:
                if lnoCopRow1 > 0:
                    lnoCopRows = [lnoCopRow1]
                else:
                    lnoCopRows = []
            else:
                lnoCopRows = [lnoCopRow1, lnoCopRow2]
                
            if uvisCopRow > 0:
                uvisCopRows = [uvisCopRow]
            else:
                uvisCopRows = []
    
    
            title = ""
            for soCopRow in soCopRows:
                channel = "so"
                description = getObservationDescription(channel, copTableDict, soFixedRow, soCopRow, silent=True)
                title += "<br>%s: %s" %(channel.upper(), description)
    
            for lnoCopRow in lnoCopRows:
                channel = "lno"
                description = getObservationDescription(channel, copTableDict, lnoFixedRow, lnoCopRow, silent=True)
                title += "<br>%s: %s" %(channel.upper(), description)
            
            for uvisCopRow in uvisCopRows:
                channel = "uvis"
                description = getObservationDescription(channel, copTableDict, 0, uvisCopRow, silent=True)
                title += "<br>%s: %s" %(channel.upper(), description)
    
    
            h += r"<h3>"+title+r"</h3>"+"\n"
            if len(calibration) > 0:
                h += r"<p>"+"\n"
                for textLine in calibration:
                    h += textLine + "<br>"
                h += r"</p>"
    
    
    h += r"<br>"+"\n"
    h += r"<br>"+"\n"
    h += r"<p>Page last modified: %s</p>" %(datetime.now().strftime('%a, %d %b %Y %H:%M:%S')) +"\n"
    
    #write html page
    with open(os.path.join(paths["CALIBRATION_PATH"], "science_calibrations.html"), 'w') as f:
        f.write(h)
            
    
