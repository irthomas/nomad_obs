# -*- coding: utf-8 -*-
"""
Created on Mon Apr 27 12:30:22 2020

@author: iant
"""

import numpy as np
import os
import matplotlib.pyplot as plt
import h5py
from datetime import datetime

from nomad_obs.config.constants import ACCEPTABLE_MTP_NADIR_TIME_ERROR
from nomad_obs.config.constants import FIG_X, FIG_Y
from nomad_obs.config.paths import SQLITE_PATH

from nomad_obs.html.make_webpage_table import writeHtmlTable
from nomad_obs.io.write_outputs import writeOutputTxt
from nomad_obs.planning.spice_functions import et2utc
from nomad_obs.sql.obs_database_sqlite import connect_db, convert_table_datetimes, insert_rows, close_db
from nomad_obs.sql.obs_database_sqlite import read_table


def get_dtype(name):
    """get h5 dtype for a dataset name"""
    dtypes = {
        float: ["Duration", "Start Longitude", "50km Longitude", "Centre Longitude", "End Longitude", "Start Latitude", "50km Latitude", "Centre Latitude",
                "End Latitude", "Centre Incidence Angle", "Centre Local Time", "50km Local Time",],
        int: ["Index", "MTP Orbit Number", "MTP Number", ],
        "S500": ["IR Observation Name", "IR Description", "UVIS Description", "Orbit Comment"],
        "S50": ["Instrument", "Occultation Type", "Nadir Type", "UTC Start Time", "UTC Transition Time", "UTC Centre Time", "UTC End Time", "Orbit Type"]
    }
    for key, types in dtypes.items():
        if name in types:
            return key


def writeNadirWebpage(orbit_list, mtpConstants, paths, make_figures=True):
    """write nadir website page"""
    mtpNumber = mtpConstants["mtpNumber"]
    mappsEventFilename = mtpConstants["mappsEventFilename"]

    htmlHeader = ["MTP Orbit Number", "MTP Number", "Nadir Type", "UTC Start Time", "UTC Centre Time", "UTC End Time", "Duration",
                  "Start Longitude", "Centre Longitude", "End Longitude",
                  "Start Latitude", "Centre Latitude", "End Latitude",
                  "Centre Incidence Angle", "Centre Local Time",
                  "Orbit Type", "IR Observation Name", "IR Description", "UVIS Description", "Orbit Comment"]
    linesToWrite = ["".join(column + "\t" for column in htmlHeader)]
    sql_table_rows = []
    values_dict = {s: [] for s in htmlHeader}

    htmlRows = []
    plotData = {"incidence": [], "et": []}
    for orbit in orbit_list:
        orbitType = orbit["finalOrbitPlan"]["orbitType"]

        # nightside nadir
        nightside = orbit["nightside"]
        # get obs description from file (if it exists)
        if "irNightsideCopRows" in orbit["finalOrbitPlan"].keys():
            irDescription = orbit["finalOrbitPlan"]["irNightsideCopRows"]["copRowDescription"]
        else:
            irDescription = "-"
        if "uvisNightsideCopRows" in orbit["finalOrbitPlan"].keys():
            uvisDescription = "COP row %i: %s" % (orbit["finalOrbitPlan"]["uvisNightsideCopRows"]["scienceCopRow"],
                                                  orbit["finalOrbitPlan"]["uvisNightsideCopRows"]["copRowDescription"])
        else:
            uvisDescription = "-"

        if "irNightsideObservationName" in orbit["finalOrbitPlan"].keys():
            irObservationName = orbit["finalOrbitPlan"]["irNightsideObservationName"]
        else:
            irObservationName = "-"
        comment = ""  # no nightside nadir comment

        lineToWrite = [orbit["orbitNumber"], mtpNumber, "Nightside", nightside["utcStart"], nightside["utcMidpoint"], nightside["utcEnd"],
                       "%0.2f" % nightside["duration"],
                       "%0.2f" % nightside["lonStart"], "%0.2f" % nightside["lonMidpoint"], "%0.2f" % nightside["lonEnd"],
                       "%0.2f" % nightside["latStart"], "%0.2f" % nightside["latMidpoint"], "%0.2f" % nightside["latEnd"],
                       "%0.2f" % nightside["incidenceMidpoint"], "%0.2f" % nightside["lstMidpoint"],

                       orbitType, irObservationName, irDescription, uvisDescription, comment
                       ]
        values_dict["MTP Orbit Number"].append(orbit["orbitNumber"])
        values_dict["MTP Number"].append(mtpNumber)
        values_dict["Nadir Type"].append("Nightside")
        values_dict["UTC Start Time"].append(nightside["utcStart"])
        values_dict["UTC Centre Time"].append(nightside["utcMidpoint"])
        values_dict["UTC End Time"].append(nightside["utcEnd"])
        values_dict["Duration"].append(nightside["duration"])
        values_dict["Start Longitude"].append(nightside["lonStart"])
        values_dict["Centre Longitude"].append(nightside["lonMidpoint"])
        values_dict["End Longitude"].append(nightside["lonEnd"])
        values_dict["Start Latitude"].append(nightside["latStart"])
        values_dict["Centre Latitude"].append(nightside["latMidpoint"])
        values_dict["End Latitude"].append(nightside["latEnd"])
        values_dict["Centre Incidence Angle"].append(nightside["incidenceMidpoint"])
        values_dict["Centre Local Time"].append(nightside["lstMidpoint"])
        values_dict["Orbit Type"].append(orbitType)
        values_dict["IR Observation Name"].append(irObservationName)
        values_dict["IR Description"].append(irDescription)
        values_dict["UVIS Description"].append(uvisDescription)
        values_dict["Orbit Comment"].append(comment)

        linesToWrite.append("".join(str(element) + "\t" for element in lineToWrite))
        sql_table_rows.append(lineToWrite)

        rowColour = "b2b2b2"
        htmlRow = lineToWrite + [rowColour]
        htmlRows.append(htmlRow)

        # dayside nadir
        dayside = orbit["dayside"]

        # get obs description from file (if it exists)
        if "irDaysideCopRows" in orbit["finalOrbitPlan"].keys():
            irDescription = orbit["finalOrbitPlan"]["irDaysideCopRows"]["copRowDescription"]
        else:
            irDescription = "-"
        if "uvisDaysideCopRows" in orbit["finalOrbitPlan"].keys():

            # special case when UVIS has 3x TC20s in one nadir:
            if isinstance(orbit["finalOrbitPlan"]["uvisDaysideCopRows"]["scienceCopRow"], list):
                # first, check if all COP rows are the same (if so, just write info once)
                if len(set(orbit["finalOrbitPlan"]["uvisDaysideCopRows"]["scienceCopRow"])):
                    uvisDescription = "3x COP rows %i: %s" % (orbit["finalOrbitPlan"]["uvisDaysideCopRows"]
                                                              ["scienceCopRow"][0], orbit["finalOrbitPlan"]["uvisDaysideCopRows"]["copRowDescription"][0])
                else:  # loop through COP rows
                    uvisDescription = ""
                    for copRow, copRowDescription in zip(orbit["finalOrbitPlan"]["uvisDaysideCopRows"]["scienceCopRow"],
                                                         orbit["finalOrbitPlan"]["uvisDaysideCopRows"]["copRowDescription"]):
                        uvisDescription += "COP row %i: %s; " % (copRow, copRowDescription)
            else:
                uvisDescription = "COP row %i: %s" % (orbit["finalOrbitPlan"]["uvisDaysideCopRows"]["scienceCopRow"],
                                                      orbit["finalOrbitPlan"]["uvisDaysideCopRows"]["copRowDescription"])
        else:
            uvisDescription = "-"

        if "irDaysideObservationName" in orbit["finalOrbitPlan"].keys():
            irObservationName = orbit["finalOrbitPlan"]["irDaysideObservationName"]
        else:
            irObservationName = "-"
        comment = orbit["finalOrbitPlan"]["comment"]
        if "&LST=" in comment:
            comment = ""

        lineToWrite = [orbit["orbitNumber"], mtpNumber, "Dayside", dayside["utcStart"], dayside["utcMidpoint"], dayside["utcEnd"],
                       "%0.2f" % dayside["duration"],
                       "%0.2f" % dayside["lonStart"], "%0.2f" % dayside["lonMidpoint"], "%0.2f" % dayside["lonEnd"],
                       "%0.2f" % dayside["latStart"], "%0.2f" % dayside["latMidpoint"], "%0.2f" % dayside["latEnd"],
                       "%0.2f" % dayside["incidenceMidpoint"], "%0.2f" % dayside["lstMidpoint"],

                       orbitType, irObservationName, irDescription, uvisDescription, comment
                       ]
        values_dict["MTP Orbit Number"].append(orbit["orbitNumber"])
        values_dict["MTP Number"].append(mtpNumber)
        values_dict["Nadir Type"].append("Dayside")
        values_dict["UTC Start Time"].append(dayside["utcStart"])
        values_dict["UTC Centre Time"].append(dayside["utcMidpoint"])
        values_dict["UTC End Time"].append(dayside["utcEnd"])
        values_dict["Duration"].append(dayside["duration"])
        values_dict["Start Longitude"].append(dayside["lonStart"])
        values_dict["Centre Longitude"].append(dayside["lonMidpoint"])
        values_dict["End Longitude"].append(dayside["lonEnd"])
        values_dict["Start Latitude"].append(dayside["latStart"])
        values_dict["Centre Latitude"].append(dayside["latMidpoint"])
        values_dict["End Latitude"].append(dayside["latEnd"])
        values_dict["Centre Incidence Angle"].append(dayside["incidenceMidpoint"])
        values_dict["Centre Local Time"].append(dayside["lstMidpoint"])
        values_dict["Orbit Type"].append(orbitType)
        values_dict["IR Observation Name"].append(irObservationName)
        values_dict["IR Description"].append(irDescription)
        values_dict["UVIS Description"].append(uvisDescription)
        values_dict["Orbit Comment"].append(comment)

        linesToWrite.append("".join(str(element) + "\t" for element in lineToWrite))
        sql_table_rows.append(lineToWrite)

        rowColour = "98fab4"
        htmlRow = lineToWrite + [rowColour]
        htmlRows.append(htmlRow)

        plotData["incidence"].append(dayside["incidenceMidpoint"])
        plotData["et"].append(dayside["etMidpoint"])

    if make_figures:
        linkName = "nomad_mtp%03d_nadir.txt" % mtpNumber
        linkDescription = "Table data in text format"
        extraComments = ["UTC Start Time = Terminator crossing time",
                         "UTC End Time = Terminator crossing time", \
                         #                 "Duration time includes extra time before and after terminator crossing", \
                         "Dayside nadir timings do not include 10 second initialisation time", \
                         "LTP file used for this analysis: %s" % mappsEventFilename, \
                         "Timings may vary from SOC by up to %i seconds, due to orbit differences" % ACCEPTABLE_MTP_NADIR_TIME_ERROR, \
                         "Colour code: Grey = nightside nadir; Green = dayside nadir"]
        #                "Note that observation start/end times here have not yet been checked for clashes with other NOMAD observations"]
        writeHtmlTable("nomad_mtp%03d_nadir" % mtpNumber, "NOMAD MTP%03d Nadir Observations" % mtpNumber, htmlHeader,
                       htmlRows, paths, linkNameDesc=[linkName, linkDescription], extraComments=extraComments)
        writeOutputTxt(os.path.join(paths["HTML_MTP_PATH"], "nomad_mtp%03d_nadir" % mtpNumber), linesToWrite)

        plt.figure(figsize=(FIG_X, FIG_Y - 2))
        plt.plot(plotData["et"], plotData["incidence"])
        xTickIndices = list(range(0, len(plotData["et"]), (int(len(plotData["et"]) / 4) - 1)))
        xTickLabels = [et2utc(plotData["et"][x])[0:11] for x in xTickIndices]
        xTicks = [plotData["et"][x] for x in xTickIndices]
        plt.xticks(xTicks, xTickLabels)
        plt.xlabel("Observation Time")
        plt.ylabel("Dayside nadir Minimum Solar Incidence Angle (deg)")
        plt.title("MTP%03d Dayside Nadir Minimum Solar Incidence Angle" % mtpNumber)
        plt.savefig(os.path.join(paths["HTML_MTP_PATH"], "mtp%03d_nadir_minimum_incidence_angle.png" % mtpNumber))
        plt.close()

    # save to local hdf5
    # with h5py.File("planning.h5", "a") as h5:
    #     if "nadirs" not in h5.keys():
    #         nad_group = h5.create_group("nadirs")
    #     #     exists = False
    #     # else:
    #     #     occ_group = h5["nadirs"]
    #     #     exists = True

    #     for key in values_dict.keys():
    #         if isinstance(values_dict[key][0], str):
    #             # if exists:
    #             #     array = np.asarray(np.concatenate((h5["occultations"][key][...], np.asarray(
    #             #         values_dict[key], dtype=h5py.string_dtype()))), dtype=h5py.string_dtype())
    #             # else:
    #             array = list(values_dict[key])
    #             key_str = key.replace(" ", "_")
    #             if "description" in key.lower() or "name" in key.lower() or "comment" in key.lower():
    #                 nad_group.create_dataset(key_str, (len(array), 1), "S500", data=array)
    #             else:
    #                 nad_group.create_dataset(key_str, (len(array), 1), "S50", data=array)

    #         else:
    #             # if exists:
    #             #     array = np.asarray(np.concatenate((h5["occultations"][key][...], np.asarray(values_dict[key]))))
    #             # else:
    #             array = np.asarray(values_dict[key])
    #         # if exists:
    #         #     del occ_group[key]
    #             key_str = key.replace(" ", "_")
    #             nad_group[key_str] = array

    # """write nadir data to sql database"""
    from nomad_obs.sql.db_fields import nadir_table_fields_sqlite
    # save to local sqlite db
    con = connect_db(SQLITE_PATH)

    sql_table_rows_datetime = convert_table_datetimes(nadir_table_fields_sqlite, sql_table_rows)
    insert_rows(con, "nadirs", nadir_table_fields_sqlite, sql_table_rows_datetime, check_duplicates=True, duplicate_columns=[3, 4, 5])
    close_db(con)

    copy_sql_to_h5()


def copy_sql_to_h5():
    """copy everything from sql to hdf5 in date order"""

    con = connect_db(SQLITE_PATH)

    # occultation data
    occ_table = read_table(con, "occultations")
    occ_start_times = [occ_row[5] for occ_row in occ_table]
    occ_sort_indices = np.argsort(occ_start_times)

    htmlHeader = ["Index", "Instrument", "MTP Orbit Number", "MTP Number", "Occultation Type", "UTC Start Time", "UTC Transition Time", "UTC End Time",
                  "Duration", "Start Longitude", "50km Longitude", "End Longitude",
                  "Start Latitude", "50km Latitude", "End Latitude", "50km Local Time",
                  "Orbit Type", "IR Observation Name", "IR Description", "UVIS Description", "Orbit Comment"]

    values_dict = {}
    for col_ix, header in enumerate(htmlHeader):
        values_dict[header] = np.asarray([occ_table[i][col_ix] if occ_table[i][col_ix] else np.nan for i in occ_sort_indices])

    # split by year
    years = np.asarray([d.year for d in values_dict["UTC Start Time"]])
    unique_years = list(set(years))

    with h5py.File("planning.h5", "w") as h5:
        occ_group = h5.create_group("occultations")

        for unique_year in unique_years:
            year_group = occ_group.create_group(str(unique_year))
            year_ixs = np.where(years == unique_year)[0]

            for key in values_dict.keys():
                # print(unique_year, key)
                dtype = get_dtype(key)
                if dtype in ["S500", "S50"]:
                    array = [values_dict[key][i] for i in year_ixs]
                    if isinstance(values_dict[key][0], datetime):
                        array = [datetime.strftime(s, "%Y %b %d %H:%M:%S") for s in array]

                else:
                    array = values_dict[key][year_ixs]
                key_str = key.replace(" ", "_")
                year_group.create_dataset(key_str, (len(array), 1), dtype=dtype, data=array, compression="gzip", shuffle=True)

    # nadir data
    nadir_table = read_table(con, "nadirs")
    nadir_start_times = [nadir_row[5] for nadir_row in nadir_table]
    nadir_sort_indices = np.argsort(nadir_start_times)

    htmlHeader = ["Index", "MTP Orbit Number", "MTP Number", "Nadir Type", "UTC Start Time", "UTC Centre Time", "UTC End Time", "Duration",
                  "Start Longitude", "Centre Longitude", "End Longitude",
                  "Start Latitude", "Centre Latitude", "End Latitude",
                  "Centre Incidence Angle", "Centre Local Time",
                  "Orbit Type", "IR Observation Name", "IR Description", "UVIS Description", "Orbit Comment"]

    values_dict = {}
    for col_ix, header in enumerate(htmlHeader):
        values_dict[header] = np.asarray([nadir_table[i][col_ix] if nadir_table[i][col_ix] else np.nan for i in nadir_sort_indices])

    # split by year
    years = np.asarray([d.year for d in values_dict["UTC Start Time"]])
    unique_years = list(set(years))

    with h5py.File("planning.h5", "a") as h5:
        nadir_group = h5.create_group("nadirs")

        for unique_year in unique_years:
            year_group = nadir_group.create_group(str(unique_year))
            year_ixs = np.where(years == unique_year)[0]

            for key in values_dict.keys():
                # print(unique_year, key)
                dtype = get_dtype(key)
                if dtype in ["S500", "S50"]:
                    array = [values_dict[key][i] for i in year_ixs]
                    if isinstance(values_dict[key][0], datetime):
                        array = [datetime.strftime(s, "%Y %b %d %H:%M:%S") for s in array]
                else:
                    array = values_dict[key][year_ixs]
                key_str = key.replace(" ", "_")
                year_group.create_dataset(key_str, (len(array), 1), dtype=dtype, data=array, compression="gzip", shuffle=True)
