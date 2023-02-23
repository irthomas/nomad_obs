# -*- coding: utf-8 -*-
"""
Created on Mon Apr 27 12:31:24 2020

@author: iant
"""
import numpy as np
import os
import matplotlib.pyplot as plt


from nomad_obs.config.constants import SO_TRANSITION_ALTITUDE, ACCEPTABLE_MTP_OCCULTATION_TIME_ERROR
from nomad_obs.config.constants import FIG_X, FIG_Y
from nomad_obs.config.paths import SQLITE_PATH

from nomad_obs.html.make_webpage_table import writeHtmlTable
from nomad_obs.io.write_outputs import writeOutputTxt
from nomad_obs.planning.spice_functions import et2utc

from nomad_obs.sql.obs_database_sqlite import connect_db, convert_table_datetimes, insert_rows, close_db
from nomad_obs.sql.db_fields import occultation_table_fields_sqlite

from nomad_obs.sql.new_sqlite_db import new_sqlite_db


def writeOccultationWebpage(orbit_list, mtpConstants, paths, make_figures=True):
    """write occultation website page"""
    mtpNumber = mtpConstants["mtpNumber"]
    mappsEventFilename = mtpConstants["mappsEventFilename"]

    def getValue(key):
        if occultation[key] != "-":
            return "%0.2f" %occultation[key]
        else:
            return "-"
    


    alt = "%0.0fkm" %SO_TRANSITION_ALTITUDE
    htmlHeader = ["Instrument", "Orbit Number", "Occultation Type", "UTC Start Time", "UTC Transition Time", "UTC End Time", "Duration (s)", \
                "Start Longitude", alt+" Longitude", "End Longitude", \
                "Start Latitude", alt+" Latitude", "End Latitude", alt+" Local Time (hrs)", \
                "Orbit Type", "IR Observation Name", "IR Description", "UVIS Description", "Orbit Comment"]
    linesToWrite = ["".join(column+"\t" for column in htmlHeader)]
    sql_table_rows = []

    occultationNames = ["ingress","egress","merged","grazing"]
    irObsTypeNames = {"ingress":["irIngressHigh","irIngressLow"], "merged":["irIngressHigh","irIngressLow"], "grazing":["irIngressHigh","irIngressLow"], "egress":["irEgressLow","irEgressHigh"]}
    uvisObsTypeNames = {"ingress":"uvisIngress", "merged":"uvisIngress", "grazing":"uvisIngress", "egress":"uvisEgress"}
    
    
    htmlRows = []
    plotDataIngress = {"lon":[], "lat":[], "duration":[], "et":[]}
    plotDataEgress = {"lon":[], "lat":[], "duration":[], "et":[]}
    for orbit in orbit_list:
        orbitType = orbit["finalOrbitPlan"]["orbitType"]
    
        for occultationName in occultationNames:
            if occultationName in orbit.keys():
                occultation = orbit[occultationName]
    
                obsType1, obsType2 = irObsTypeNames[occultationName]
                
                #get obs description from file (if it exists)
                if obsType1+"CopRows" in orbit["finalOrbitPlan"].keys():
                    description1 = "%s" %(orbit["finalOrbitPlan"][obsType1+"CopRows"]["copRowDescription"])
                    description2 = "%s" %(orbit["finalOrbitPlan"][obsType2+"CopRows"]["copRowDescription"])
                    if description1 == description2: #if SCI1 = SCI2
                        irDescription = description1
                    else:
                        irDescription = description1 + "; " + description2
                    
                    name1 = "%s" %(orbit["finalOrbitPlan"][obsType1+"ObservationName"])
                    name2 = "%s" %(orbit["finalOrbitPlan"][obsType2+"ObservationName"])
                    if name1 == name2:
                        irObservationName = name1
                    else:
                        irObservationName = name1 + "; " + name2
                        
                else:
                    irDescription = "-"
                    irObservationName = "-"
                    
                uvisObsType = uvisObsTypeNames[occultationName]
                if uvisObsType+"CopRows" in orbit["finalOrbitPlan"].keys():
                    uvisDescription = "COP row %i: %s" %(orbit["finalOrbitPlan"][uvisObsType+"CopRows"]["scienceCopRow"], orbit["finalOrbitPlan"][uvisObsType+"CopRows"]["copRowDescription"])
                else:
                    uvisDescription = "-"
                    
                comment = orbit["finalOrbitPlan"]["comment"]
                if "&LST=" in comment:
                    comment = ""
                    
        
                lineToWrite = [occultation["primeInstrument"], orbit["orbitNumber"], mtpNumber, occultationName.capitalize(), \
                               occultation["utcStart"], occultation["utcTransition"], occultation["utcEnd"], "%0.2f" %occultation["duration"], \
                               "%0.2f" %occultation["lonStart"], getValue("lonTransition"), "%0.2f" %occultation["lonEnd"], \
                               "%0.2f" %occultation["latStart"], getValue("latTransition"), "%0.2f" %occultation["latEnd"], \
                               getValue("lstTransition"), 
                               
                               orbitType, irObservationName, irDescription, uvisDescription, comment
                               ]
                linesToWrite.append("".join(str(element)+"\t" for element in lineToWrite))
                sql_table_rows.append(lineToWrite)
        
            
                rowColour = occultation["rowColour"]
                htmlRow = lineToWrite+[rowColour]
                htmlRows.append(htmlRow)
                
                if getValue("lonTransition") != "-": #igore merged or grazing
                    if occultationName == "ingress":
                        plotDataIngress["lon"].append(occultation["lonTransition"])
                        plotDataIngress["lat"].append(occultation["latTransition"])
                        plotDataIngress["duration"].append(occultation["duration"])
                        plotDataIngress["et"].append(occultation["etTransition"])
                    elif occultationName == "egress":
                        plotDataEgress["lon"].append(occultation["lonTransition"])
                        plotDataEgress["lat"].append(occultation["latTransition"])
                        plotDataEgress["duration"].append(occultation["duration"])
                        plotDataEgress["et"].append(occultation["etTransition"])
    
        
        
    if make_figures:
        linkName = "nomad_mtp%03d_occultation.txt" %mtpNumber
        linkDescription = "Table data in text format"
        extraComments = ["UTC Start Time = 0 or 250km tangent altitude", \
                         "UTC End Time = 0 or 250km tangent altitude", \
                         "UTC Transition Time = %i km tangent altitude" %SO_TRANSITION_ALTITUDE, \
                         "LTP file used for this analysis: %s" %mappsEventFilename, \
                         "Timings may vary from SOC by up to %i seconds, due to orbit differences" %ACCEPTABLE_MTP_OCCULTATION_TIME_ERROR, \
                         "Colour code: Green = occultation assigned to NOMAD in LTP; Blue = occultation assigned to ACS in LTP; Red = occultation unassigned in LTP; Yellow = unused observation e.g. tangent altitude too high"]
        #                     "Note that observation start/end times here have not yet been checked for clashes with other NOMAD observations"]
        writeHtmlTable("nomad_mtp%03d_occultation" %mtpNumber, "NOMAD MTP%03d Occultation Observations" %mtpNumber, htmlHeader, htmlRows, paths, linkNameDesc=[linkName, linkDescription], extraComments=extraComments)
        writeOutputTxt(os.path.join(paths["HTML_MTP_PATH"], "nomad_mtp%03d_occultation" %mtpNumber), linesToWrite)
        
    
    
        plt.figure(figsize=(FIG_X, FIG_Y-2))
        plt.scatter(plotDataIngress["et"], plotDataIngress["duration"], c="r", label="Ingress")
        plt.scatter(plotDataEgress["et"], plotDataEgress["duration"], c="b", label="Egress")
        xTickIndices = list(range(0, len(plotDataIngress["et"]), (np.int(len(plotDataIngress["et"])/4) -1)))
        xTickLabels = [et2utc(plotDataIngress["et"][x])[0:11] for x in xTickIndices]
        xTicks = [plotDataIngress["et"][x] for x in xTickIndices]
        plt.xticks(xTicks, xTickLabels)
        plt.xlabel("Observation Time")
        plt.ylabel("Occultation Duration (s)")
        plt.title("MTP%02d Solar Occultation Observation Durations" %mtpNumber)
        plt.legend()
        plt.savefig(os.path.join(paths["HTML_MTP_PATH"], "mtp%03d_occultation_duration.png" %mtpNumber))
        
        plt.close()
        
        plt.figure(figsize=(FIG_X, FIG_Y-2))
        plt.scatter(plotDataIngress["et"], plotDataIngress["lat"], c="r", label="Ingress")
        plt.scatter(plotDataEgress["et"], plotDataEgress["lat"], c="b", label="Egress")
        xTickIndices = list(range(0, len(plotDataIngress["et"]), (np.int(len(plotDataIngress["et"])/4) -1)))
        xTickLabels = [et2utc(plotDataIngress["et"][x])[0:11] for x in xTickIndices]
        xTicks = [plotDataIngress["et"][x] for x in xTickIndices]
        plt.xticks(xTicks, xTickLabels)
        plt.xlabel("Observation Time")
        plt.ylabel("Occultation Latitudes (deg)")
        plt.ylim([-90, 90])
        plt.title("MTP%02d Solar Occultation Observation Latitudes" %mtpNumber)
        plt.legend()
        plt.savefig(os.path.join(paths["HTML_MTP_PATH"], "mtp%03d_occultation_lat.png" %mtpNumber))
        plt.close()
    



    #save to local sqlite db

    if not os.path.exists(SQLITE_PATH):
        print("Sqlite database doesn't exist: creating new file")
        
        new_sqlite_db()
    
    con = connect_db(SQLITE_PATH)
    
    
    table_rows_datetime = convert_table_datetimes(occultation_table_fields_sqlite, sql_table_rows)
    insert_rows(con, "occultations", occultation_table_fields_sqlite, table_rows_datetime, check_duplicates=True, duplicate_columns=[4, 6])
    close_db(con)
        
