# -*- coding: utf-8 -*-
"""
Created on Mon Apr 27 12:30:22 2020

@author: iant
"""

import numpy as np
import os
import matplotlib.pyplot as plt


from nomad_obs.config.constants import ACCEPTABLE_MTP_NADIR_TIME_ERROR
from nomad_obs.config.constants import FIG_X, FIG_Y
from nomad_obs.config.paths import SQLITE_PATH, OFFLINE

from nomad_obs.html.make_webpage_table import writeHtmlTable
from nomad_obs.io.write_outputs import writeOutputTxt
from nomad_obs.planning.spice_functions import et2utc
from nomad_obs.sql.obs_database import obsDB
from nomad_obs.sql.obs_database_sqlite import connect_db, convert_table_datetimes, insert_rows, close_db
from nomad_obs.sql.db_fields import nadir_table_fields




def writeNadirWebpage(orbit_list, mtpConstants, paths, make_figures=True):
    """write nadir website page"""
    mtpNumber = mtpConstants["mtpNumber"]
    mappsEventFilename = mtpConstants["mappsEventFilename"]

    htmlHeader = ["Orbit Index", "Nadir Type", "UTC Start Time", "UTC Centre Time", "UTC End Time", "Duration (s)", \
                "Start Longitude", "Centre Longitude", "End Longitude", \
                "Start Latitude", "Centre Latitude", "End Latitude", \
                "Centre Incidence Angle", "Centre Local Time (hrs)", \
                "Orbit Type", "IR Observation Name", "IR Description", "UVIS Description", "Orbit Comment"]
    linesToWrite = ["".join(column+"\t" for column in htmlHeader)]
    sql_table_rows = []
    
    htmlRows = []
    plotData = {"incidence":[], "et":[]}
    for orbit in orbit_list:
        orbitType = orbit["finalOrbitPlan"]["orbitType"]
        
        #nightside nadir
        nightside = orbit["nightside"]
        #get obs description from file (if it exists)
        if "irNightsideCopRows" in orbit["finalOrbitPlan"].keys():
            irDescription = orbit["finalOrbitPlan"]["irNightsideCopRows"]["copRowDescription"]
        else:
            irDescription = "-"
        if "uvisNightsideCopRows" in orbit["finalOrbitPlan"].keys():
            uvisDescription = "COP row %i: %s" %(orbit["finalOrbitPlan"]["uvisNightsideCopRows"]["scienceCopRow"], orbit["finalOrbitPlan"]["uvisNightsideCopRows"]["copRowDescription"])
        else:
            uvisDescription = "-"
            
        if "irNightsideObservationName" in orbit["finalOrbitPlan"].keys():
            irObservationName = orbit["finalOrbitPlan"]["irNightsideObservationName"]
        else:
            irObservationName = "-"
        comment = "" #no nightside nadir comment
    
        lineToWrite = [orbit["orbitNumber"], mtpNumber, "Nightside", nightside["utcStart"], nightside["utcMidpoint"], nightside["utcEnd"], "%0.2f" %nightside["duration"], \
                       "%0.2f" %nightside["lonStart"], "%0.2f" %nightside["lonMidpoint"], "%0.2f" %nightside["lonEnd"], \
                       "%0.2f" %nightside["latStart"], "%0.2f" %nightside["latMidpoint"], "%0.2f" %nightside["latEnd"], \
                       "%0.2f" %nightside["incidenceMidpoint"], "%0.2f" %nightside["lstMidpoint"], \
                       
                       orbitType, irObservationName, irDescription, uvisDescription, comment
                       ]
        linesToWrite.append("".join(str(element)+"\t" for element in lineToWrite))
        sql_table_rows.append(lineToWrite)
    
        rowColour = "b2b2b2"
        htmlRow = lineToWrite+[rowColour]
        htmlRows.append(htmlRow)
        



        #dayside nadir
        dayside = orbit["dayside"]
        
        #get obs description from file (if it exists)
        if "irDaysideCopRows" in orbit["finalOrbitPlan"].keys():
            irDescription = orbit["finalOrbitPlan"]["irDaysideCopRows"]["copRowDescription"]
        else:
            irDescription = "-"
        if "uvisDaysideCopRows" in orbit["finalOrbitPlan"].keys():
            
            #special case when UVIS has 3x TC20s in one nadir:
            if isinstance(orbit["finalOrbitPlan"]["uvisDaysideCopRows"]["scienceCopRow"], list):
                #first, check if all COP rows are the same (if so, just write info once)
                if len(set(orbit["finalOrbitPlan"]["uvisDaysideCopRows"]["scienceCopRow"])):
                    uvisDescription = "3x COP rows %i: %s" %(orbit["finalOrbitPlan"]["uvisDaysideCopRows"]["scienceCopRow"][0], orbit["finalOrbitPlan"]["uvisDaysideCopRows"]["copRowDescription"][0])
                else: #loop through COP rows
                    uvisDescription = ""
                    for copRow, copRowDescription in zip(orbit["finalOrbitPlan"]["uvisDaysideCopRows"]["scienceCopRow"], orbit["finalOrbitPlan"]["uvisDaysideCopRows"]["copRowDescription"]):
                        uvisDescription += "COP row %i: %s; " %(copRow, copRowDescription)
            else:
                uvisDescription = "COP row %i: %s" %(orbit["finalOrbitPlan"]["uvisDaysideCopRows"]["scienceCopRow"], orbit["finalOrbitPlan"]["uvisDaysideCopRows"]["copRowDescription"])
        else:
            uvisDescription = "-"
            
        if "irDaysideObservationName" in orbit["finalOrbitPlan"].keys():
            irObservationName = orbit["finalOrbitPlan"]["irDaysideObservationName"]
        else:
            irObservationName = "-"
        comment = orbit["finalOrbitPlan"]["comment"]
        if "&LST=" in comment:
            comment = ""
    
        lineToWrite = [orbit["orbitNumber"], mtpNumber, "Dayside", dayside["utcStart"], dayside["utcMidpoint"], dayside["utcEnd"], "%0.2f" %dayside["duration"], \
                       "%0.2f" %dayside["lonStart"], "%0.2f" %dayside["lonMidpoint"], "%0.2f" %dayside["lonEnd"], \
                       "%0.2f" %dayside["latStart"], "%0.2f" %dayside["latMidpoint"], "%0.2f" %dayside["latEnd"], \
                       "%0.2f" %dayside["incidenceMidpoint"], "%0.2f" %dayside["lstMidpoint"], \
                       
                       orbitType, irObservationName, irDescription, uvisDescription, comment
                       ]
        linesToWrite.append("".join(str(element)+"\t" for element in lineToWrite))
        sql_table_rows.append(lineToWrite)
    
        rowColour = "98fab4"
        htmlRow = lineToWrite+[rowColour]
        htmlRows.append(htmlRow)
        
        plotData["incidence"].append(dayside["incidenceMidpoint"])
        plotData["et"].append(dayside["etMidpoint"])
    





    if make_figures:
        linkName = "nomad_mtp%03d_nadir.txt" %mtpNumber
        linkDescription = "Table data in text format"
        extraComments = ["UTC Start Time = Terminator crossing time", \
                         "UTC End Time = Terminator crossing time", \
        #                 "Duration time includes extra time before and after terminator crossing", \
                         "Dayside nadir timings do not include 10 second initialisation time", \
                         "LTP file used for this analysis: %s" %mappsEventFilename, \
                         "Timings may vary from SOC by up to %i seconds, due to orbit differences" %ACCEPTABLE_MTP_NADIR_TIME_ERROR, \
                         "Colour code: Grey = nightside nadir; Green = dayside nadir"]
        #                "Note that observation start/end times here have not yet been checked for clashes with other NOMAD observations"]
        writeHtmlTable("nomad_mtp%03d_nadir" %mtpNumber, "NOMAD MTP%03d Nadir Observations" %mtpNumber, htmlHeader, htmlRows, paths, linkNameDesc=[linkName, linkDescription], extraComments=extraComments)
        writeOutputTxt(os.path.join(paths["HTML_MTP_PATH"], "nomad_mtp%03d_nadir" %mtpNumber), linesToWrite)
        
        
        plt.figure(figsize=(FIG_X, FIG_Y-2))
        plt.plot(plotData["et"], plotData["incidence"])
        xTickIndices = list(range(0, len(plotData["et"]), (np.int(len(plotData["et"])/4) -1)))
        xTickLabels = [et2utc(plotData["et"][x])[0:11] for x in xTickIndices]
        xTicks = [plotData["et"][x] for x in xTickIndices]
        plt.xticks(xTicks, xTickLabels)
        plt.xlabel("Observation Time")
        plt.ylabel("Dayside nadir Minimum Solar Incidence Angle (deg)")
        plt.title("MTP%03d Dayside Nadir Minimum Solar Incidence Angle" %mtpNumber)
        plt.savefig(os.path.join(paths["HTML_MTP_PATH"], "mtp%03d_nadir_minimum_incidence_angle.png" %mtpNumber))
        plt.close()



    """write nadir data to sql database"""
    if OFFLINE:
        from nomad_obs.sql.db_fields import nadir_table_fields_sqlite
        #save to local sqlite db
        con = connect_db(SQLITE_PATH)
        
        sql_table_rows_datetime = convert_table_datetimes(nadir_table_fields_sqlite, sql_table_rows)
        insert_rows(con, "nadirs", nadir_table_fields_sqlite, sql_table_rows_datetime, check_duplicates=True, duplicate_columns=[3, 4, 5])
        close_db(con)
     
    else:
        db_obj = obsDB(paths)
#       db_obj.drop_table("nomad_nadirs")
#       db_obj.new_table("nomad_nadirs", table_fields)
        sql_table_rows_datetime = db_obj.convert_table_datetimes(nadir_table_fields, sql_table_rows)
        db_obj.insert_rows("nomad_nadirs", nadir_table_fields, sql_table_rows_datetime, check_duplicates=True, duplicate_columns=[2, 3, 4])
#       table = db_obj.read_table("nomad_nadirs")
        db_obj.close()



