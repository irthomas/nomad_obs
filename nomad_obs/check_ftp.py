# -*- coding: utf-8 -*-
"""
Created on Mon Jun  3 09:39:59 2024

@author: iant

CHECK FTP FOR NEW DOCUMENTS
IF COP ROWS FOUND, EMAIL A SUMMARY


CHECK EVERY 10 MINUTES


"""

import hashlib
import time
from datetime import datetime
import os

from nomad_obs.ftp.tools import get_ftp_file_dict, copy_file_from_ftp, get_orbit_plan_path, email_summary

from nomad_obs.cop_rows.cop_table_functions import getCopTables
from nomad_obs.cop_rows.cop_table_functions import getObservationDescription

FORMAT_STR_DAYS = "%Y-%m-%d"
FORMAT_STR_SECONDS = "%Y-%m-%d %H:%M:%S"

ORBIT_TYPES = {
    -1: {"description": "Off"},
    1: {"description": "SO and UVIS occultations; LNO and UVIS dayside nadir"},
    2: {"description": "SO and UVIS occultations; UVIS-only split dayside nadir"},
    3: {"description": "LNO and UVIS long dayside nadir"},
    4: {"description": "UVIS-only split dayside nadir"},
    14: {"description": "UVIS-only long dayside nadir"},
    5: {"description": "SO and UVIS merged or grazing occultations; LNO and UVIS dayside nadir"},
    6: {"description": "SO and UVIS merged or grazing occultations; UVIS-only split dayside nadir"},
    7: {"description": "LNO and UVIS dayside nadir; LNO and UVIS nightside nadir"},
    17: {"description": "LNO and UVIS dayside nadir; UVIS-only nightside nadir"},
    27: {"description": "LNO and UVIS dayside nadir; LNO nightside limb; UVIS nightside nadir"},
    47: {"description": "LNO and UVIS dayside nadir; LNO and UVIS nightside limb"},
    8: {"description": "LNO dayside limb; UVIS dayside nadir"},
    18: {"description": "SO and UVIS occultations; LNO dayside limb; UVIS dayside nadir"},
    28: {"description": "LNO and UVIS dayside limb"},
}

DAYSIDE_ORBIT_TYPES = [1, 2, 3, 4, 5, 6, 7, 8, 14, 17, 18, 27, 28, 47]
NIGHTSIDE_ORBIT_TYPES = [7, 17, 27, 47]

COP_TABLE_VERSION = "20231028_120000"


def get_local_md5(local_path):
    """get md5 checksum of file stored locally"""
    with open(local_path, "rb") as f:
        file_hash = hashlib.md5()
        while chunk := f.read(8192):
            file_hash.update(chunk)

    return file_hash.hexdigest()


def get_new_updated_ftp_file_dict():
    """get dictionary of new or updated files"""

    # check ftp for all files
    ftp_file_dict = get_ftp_file_dict()

    new_files = {}

    # for each file on ftp, check if it also exists locally
    print("Checking if file exists locally")
    for ftp_filepath in ftp_file_dict.keys():
        if ftp_file_dict[ftp_filepath]["type"] in ["cop_rows", "orbit_plans"]:
            local_filepath = ftp_file_dict[ftp_filepath]["local_path"]

            # if file exists locally, get md5 checksum for checking later
            if os.path.exists(local_filepath):
                md5 = get_local_md5(local_filepath)
                ftp_file_dict[ftp_filepath]["local_md5"] = md5
                ftp_file_dict[ftp_filepath]["exists"] = True

            else:
                # if it doesn't exist, add to dictionary
                ftp_file_dict[ftp_filepath]["exists"] = False

    # loop through each new or updated file
    print("Copying missing or outdated incoming files to local directory")
    for ftp_filepath in ftp_file_dict.keys():

        if ftp_file_dict[ftp_filepath]["type"] in ["cop_rows", "orbit_plans"]:

            # if file doesn't exist locally, download to local directory
            if not ftp_file_dict[ftp_filepath]["exists"]:
                local_filepath = ftp_file_dict[ftp_filepath]["local_path"]
                local_filename = os.path.basename(local_filepath)
                print("File %s doesn't exist locally - downloading from ftp" % local_filepath)

                dir_path = os.path.split(local_filepath)[0]
                if not os.path.exists(dir_path):
                    print("Making directory %s" % dir_path)
                    os.makedirs(dir_path, exist_ok=True)

                # download
                copy_file_from_ftp(ftp_filepath, local_filepath)
                # add info to new file dictionary
                new_files[local_filename] = {"type": ftp_file_dict[ftp_filepath]["type"], "path": local_filepath, "updated": False}

            else:
                # if file exists but md5 different
                if ftp_file_dict[ftp_filepath]["local_md5"] != ftp_file_dict[ftp_filepath]["remote_md5"]:
                    local_filepath = ftp_file_dict[ftp_filepath]["local_path"]
                    local_filename = os.path.basename(local_filepath)
                    print("File %s exists locally but checksum doesn't match - renaming" % local_filepath)

                    # append file modified time to old file
                    split_text = os.path.splitext(local_filepath)
                    modified_time = os.path.getmtime(local_filepath)
                    modified_time_str = datetime.fromtimestamp(modified_time).strftime('%Y%m%d_%H%M%S')
                    local_filepath_new = "%s_%s%s" % (split_text[0], modified_time_str, split_text[1])
                    os.rename(local_filepath, local_filepath_new)

                    # download new version
                    copy_file_from_ftp(ftp_filepath, local_filepath)

                    # add info to new file dictionary
                    new_files[local_filename] = {"type": ftp_file_dict[ftp_filepath]["type"], "path": local_filepath, "updated": True}

    # return dictionary of new files info
    return new_files


def analyse_cop_rows(new_files):
    """read in info about new files and analyse them"""

    error = False
    h = ""  # generate html for emailing

    obs_info_dict = {}
    for filename in new_files.keys():

        # if any of the new files are cop rows, analyse them
        if new_files[filename]["type"] == "cop_rows":

            mtp, channel_str, obs_type = filename.replace(".txt", "").split("_", 2)

            if obs_type in ["calibration", "calibrations"]:
                obs_type = "calibration"

            # if nadir cop rows delivered, need to get orbit plan to figure out observation types
            if obs_type in ["dayside_nadir", "nightside_nadir"]:
                orbit_plan_path = get_orbit_plan_path(mtp)

                # if orbit plan is not available, stop with error and send error email
                if not os.path.exists(orbit_plan_path):
                    print("Error: %s doesn't exist" % orbit_plan_path)
                    error = True
                    return error, "%s doesn't exist" % orbit_plan_path

                else:
                    # read orbit plan data
                    with open(orbit_plan_path, "rb") as f:
                        orbit_lines = [s.decode().strip() for i, s in enumerate(f.readlines()) if i > 0]

                    # get indices of potential dayside (all) or potential nightside orbit numbers
                    all_orbits_types = [int(i) for i in orbit_lines]
                    nightside_orbits_types = [int(i) for i in orbit_lines if int(i) in NIGHTSIDE_ORBIT_TYPES]

                    # add info to dictionary
                    if obs_type == "dayside_nadir":
                        obs_info_dict[filename] = {"mtp": mtp, "channel_str": channel_str, "obs_type": obs_type, "cop_rows": [],
                                                   "channels": [], "orbit_types": all_orbits_types}
                    elif obs_type == "nightside_nadir":
                        obs_info_dict[filename] = {"mtp": mtp, "channel_str": channel_str, "obs_type": obs_type, "cop_rows": [],
                                                   "channels": [], "orbit_types": nightside_orbits_types}
            else:
                # if not nadir, leave orbit types empty
                obs_info_dict[filename] = {"mtp": mtp, "channel_str": channel_str, "obs_type": obs_type, "cop_rows": [], "channels": [], "orbit_types": []}

            # parse cop row file
            local_filepath = new_files[filename]["path"]
            with open(local_filepath, "rb") as f:
                lines = [s.decode().strip() for i, s in enumerate(f.readlines()) if i > 0]

            for i, line in enumerate(lines):
                # csv file, so split by comma
                split = line.split(",")

                # try to convert cop rows to integers
                if channel_str == "ir":
                    try:
                        sci_cop_row = (int(split[2]), int(split[3]))
                        channel = {0: "so", 1: "lno", -1: "off"}[int(split[4])]
                    except ValueError as e:
                        error = True
                        return error, e
                elif channel_str == "uvis":
                    try:
                        sci_cop_row = int(split[0])
                        channel = "uvis"
                    except ValueError as e:
                        error = True
                        return error, e

                obs_info_dict[filename]["cop_rows"].append(sci_cop_row)
                obs_info_dict[filename]["channels"].append(channel)

                # no orbit type info is available for non-nadir/limbs
                if obs_type not in ["dayside_nadir", "nightside_nadir"]:
                    obs_info_dict[filename]["orbit_types"].append(-1)

            # check that each dayside and nightside has a COP row
            if len(obs_info_dict[filename]["orbit_types"]) != len(obs_info_dict[filename]["cop_rows"]):
                print("Error: %s lengths of orbits and COP rows do not match (%i vs %i)" % (filename, len(obs_info_dict[filename]["orbit_types"]),
                                                                                            len(obs_info_dict[filename]["cop_rows"])))
                error = True
                return error, "Error: %s lengths of orbits and COP rows do not match (%i vs %i)" % (filename, len(obs_info_dict[filename]["orbit_types"]),
                                                                                                    len(obs_info_dict[filename]["cop_rows"]))

            else:
                # merge list of orbit types with COP rows
                channel_str = obs_info_dict[filename]["channel_str"]
                if channel_str == "ir":
                    # off is required to deal with -1s in the cop row files
                    obs_info_dict[filename]["info"] = {"so": {}, "lno": {}, "off": {}}
                else:
                    obs_info_dict[filename]["info"] = {"uvis": {}}

                for orbit_type, cop_row, channel in zip(obs_info_dict[filename]["orbit_types"], obs_info_dict[filename]["cop_rows"],
                                                        obs_info_dict[filename]["channels"]):

                    # add cop rows to dictionary, one item per row in the cop row file for this orbit type and channel
                    # cop row is either X for uvis or (X, X) for so/lno
                    if orbit_type not in obs_info_dict[filename]["info"][channel].keys():
                        obs_info_dict[filename]["info"][channel][orbit_type] = [cop_row]
                    else:
                        obs_info_dict[filename]["info"][channel][orbit_type].append(cop_row)

    # load cop tables from nomad_obs
    copTableDict = getCopTables({"copVersion": COP_TABLE_VERSION})

    # loop again through info for each new cop row file
    for filename in sorted(obs_info_dict.keys()):
        h += "<h3>%s</h3>\n" % filename

        # get observation type from name of file. Note Phobos
        obs_type_str = filename.replace(".txt", "").split("_", 2)[-1].split("_")[0]
        if obs_type_str == "phobos":
            obs_type_str = "Phobos/Deimos"

        # if no cop rows in file
        if len(obs_info_dict[filename]["channels"]) == 0:
            h += "This file is empty<br><br>\n"

        channels = obs_info_dict[filename]["info"].keys()
        # loop through channels with info, including -1 for 'off' for SO/LNO cop row files
        for channel in channels:
            orbit_types = obs_info_dict[filename]["info"][channel].keys()

            # if no orbit types in file then skip file
            if len(orbit_types) > 0:
                if channel == "off":
                    h += "<b>This file contains %i orbit types where the channel was switched off</b><br>\n" % len(orbit_types)
                else:
                    h += "<b>This file contains %i orbit types for the %s channel</b><br>\n" % (len(orbit_types), channel.upper())

                for orbit_type in sorted(orbit_types):

                    if orbit_type != -1:
                        orbit_type_description = ORBIT_TYPES[orbit_type]["description"]

                        h += "<u><br>For orbit type %i (%s):</u><br><ul>\n" % (orbit_type, orbit_type_description)

                    else:
                        h += "<ul>\n"

                    # get list of all cop rows used for each orbit for this orbit type
                    cop_rows = obs_info_dict[filename]["info"][channel][orbit_type]

                    # make a list of number of occurences and cop row for each cop row combination
                    unique_occurences = [[cop_rows.count(x), x] for x in set(cop_rows)]

                    # sort by number of occurences, the most used combination (or off) goes first
                    for occurences, unique_cop_row in sorted(unique_occurences)[::-1]:

                        # -1 = off
                        if str(unique_cop_row) in ["-1", "(-1, -1)"]:
                            h += "<li>The channel was turned off for %i %s observations</li>\n" % (occurences, obs_type_str)
                        else:
                            if channel == "uvis":
                                # get description of cop row from nomad_obs
                                obs_type_description = getObservationDescription(channel, copTableDict, 0, unique_cop_row, silent=True)
                            else:
                                obs_type_description = getObservationDescription(channel, copTableDict, 0, unique_cop_row[0], silent=True)

                            h += "<li>COP row %s was used %i times. Observation type: %s</li>\n" % (
                                str(unique_cop_row), occurences, obs_type_description)

                    h += "</ul><br>\n"

    # clear up the plurals to make it more human readable
    h = h.replace(" 1 times", " once")
    h = h.replace(" 2 times", " twice")
    h = h.replace(" 1 orbit types", " 1 orbit type")

    return error, h, obs_info_dict


def check_ftp():
    """run the main program: check for new files on the ftp, if so send email"""

    new_files = get_new_updated_ftp_file_dict()

    # make html string to email
    h = "<html><head></head><body>\n"

    # loop through new files if present
    if len([s for s in new_files.keys() if not new_files[s]["updated"]]) > 0:
        h += "<h2>The following new files have been uploaded to the ftp:</h2><ul>\n"
        for filename in new_files.keys():
            if not new_files[filename]["updated"]:
                h += "<li>%s</li>\n" % filename

        h += "</ul><br>\n"

    # loop through updated files if present
    if len([s for s in new_files.keys() if new_files[s]["updated"]]) > 0:
        h += "<h2>The following existing files have been updated on the ftp:</h2><ul>\n"
        for filename in new_files.keys():
            if new_files[filename]["updated"]:
                h += "<li>%s</li>\n" % filename

        h += "</ul><br>\n"

    # count number of new cop row and orbit plan files
    n_cop_row_files = len([s for s in new_files.keys() if new_files[s]["type"] == "cop_rows"])
    n_orbit_plan_files = len([s for s in new_files.keys() if new_files[s]["type"] == "orbit_plans"])

    h += "<h3>There are %i new COP row files and %i new orbit plans</h3>\n\n" % (n_cop_row_files, n_orbit_plan_files)

    error = False
    if n_cop_row_files > 0:
        # if new cop row files, make summary
        error, h2, obs_info_dict = analyse_cop_rows(new_files)

        if not error:
            # add cop row summary to email message
            h += h2

    h += "</body></html>"

    # if new/updated files found, write to file and/or email, otherwise end without doing anything
    if n_cop_row_files > 0 or n_orbit_plan_files > 0:

        # with open("test.html", "w") as f:
        #     f.write(h)

        if not error:
            email_summary(h, print_output=False)
        else:
            # send error email just to Ian
            email_summary(h, to=["ian.thomas@aeronomie.be"], print_output=True)


# loop forever
while True:
    print(datetime.now())

    # run main program
    check_ftp()

    # wait 10 minutes
    for i in range(10):
        time.sleep(60)
