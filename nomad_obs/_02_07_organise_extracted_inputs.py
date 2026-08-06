# -*- coding: utf-8 -*-
"""
Created on Tue Oct  7 10:42:03 2025

@author: iant

EXTRACT FILES FROM KICKOFF/SUMMARY FILE ZIPS

ASSUME FILES ARE PLACED IN TMP DIR IN NOMAD_OBS
"""


import glob
import os
import re
import shutil

from nomad_obs.mtp_inputs import getMtpConstants
from nomad_obs.config.paths import setupPaths, BASE_DIRECTORY

EXTRACTED_DIRS_PATH = os.path.join(BASE_DIRECTORY, "tmp")


overview_dirs_path = sorted(glob.glob(EXTRACTED_DIRS_PATH + os.sep + "*overview*"))
summary_dirs_path = sorted(glob.glob(EXTRACTED_DIRS_PATH + os.sep + "*summary_files*"))

overview_dirs_mtime = [os.path.getmtime(path) for path in overview_dirs_path]
summary_dirs_mtime = [os.path.getmtime(path) for path in summary_dirs_path]


type = ""
if len(overview_dirs_path) > 0 and len(summary_dirs_path) > 0:
    if overview_dirs_mtime[-1] > summary_dirs_mtime[-1]:
        # if highest numbered mtp was modified last
        latest_dir_path = overview_dirs_path[-1]
        latest_dir = os.path.basename(latest_dir_path)
        type_ = "overview"
    if summary_dirs_mtime[-1] > overview_dirs_mtime[-1]:
        # if highest numbered mtp was modified last
        latest_dir_path = summary_dirs_path[-1]
        latest_dir = os.path.basename(latest_dir_path)
        type_ = "summary"

elif len(overview_dirs_path) > 0:
    # if no summary files
    latest_dir_path = overview_dirs_path[-1]
    latest_dir = os.path.basename(latest_dir_path)
    type_ = "overview"
elif len(summary_dirs_path) > 0:
    # if no overview files
    latest_dir_path = summary_dirs_path[-1]
    latest_dir = os.path.basename(latest_dir_path)
    type_ = "summary"
else:
    print("Error: no directories")

# get paths, make summary file dir
# get MTP number from latest filename
mtpNumber = int(re.findall("MTP([0-9][0-9][0-9])_.*", latest_dir)[0])
mtpConstants = getMtpConstants(mtpNumber)

print("Setting up %s files for MTP%i" % (type_, mtpNumber))
errors = []

# first call makes the paths
paths = setupPaths(mtpConstants)


if type_ == "overview":
    # get filenames from extracted dir, copy to correct location

    # CaSSIS limb
    search_dir = os.path.join(latest_dir_path, "Limb", "CaSSIS_limb_UVIS_ride_along")
    search_file = "NOMAD_TRUE_LIMB_ORBITS_OT28_WITH_UVIS_NADIR_LOS_TOWARDS_LIMB.txt"
    dest_dir = paths["SUMMARY_FILE_PATH"]

    if os.path.exists(search_dir):
        search_file_path = os.path.join(search_dir, search_file)
        if os.path.exists(search_file_path):
            dest = os.path.join(dest_dir, search_file)
            shutil.copy(search_file_path, dest)
        else:
            # check if directory is not empty, if so raise error
            nfiles = len(glob.glob(search_dir + os.sep + "*"))
            if nfiles > 0:
                msg = "Error: CaSSIS limb directory is not empty but nothing has been copied"
                print(msg)
                errors.append(msg)

    # UVIS nightside nadir
    search_dir = os.path.join(latest_dir_path, "ROI_Region_Of_Interest_Dayside_Nightside_Flyovers")
    search_file = "roi_flyovers_nightside-filtered.txt"
    dest_dir = paths["SUMMARY_FILE_PATH"]

    if os.path.exists(search_dir):
        search_file_path = os.path.join(search_dir, search_file)
        if os.path.exists(search_file_path):
            dest = os.path.join(dest_dir, search_file)
            shutil.copy(search_file_path, dest)
        else:
            msg = "Error: Nightside file not found"
            print(msg)
            errors.append(msg)

    # Event file
    search_dir = os.path.join(latest_dir_path, "SOC_event_file")
    search_file = "LEVF_M%03i_SOC_PLANNING.EVF" % mtpNumber
    dest_dir = paths["EVENT_FILE_PATH"]

    if os.path.exists(search_dir):
        search_file_path = os.path.join(search_dir, search_file)
        if os.path.exists(search_file_path):
            dest = os.path.join(dest_dir, search_file)
            shutil.copy(search_file_path, dest)
        else:
            msg = "Error: event file not found"
            print(msg)
            errors.append(msg)

    # Summary files
    # make kickoff dir
    kickoff_dir = os.path.join(paths["SUMMARY_FILE_PATH"], "kickoff")
    os.makedirs(kickoff_dir, exist_ok=True)

    search_dir = os.path.join(latest_dir_path, "summary_files")
    search_files = [
        "nadir_dayside_nightside_thermal_orbits_orbit_type_summary.txt",
        "NOMAD_egress_solar_occulations_summary.txt",
        "NOMAD_grazing_solar_occulations_summary.txt",
        "NOMAD_ingress_and_merged_solar_occulations_summary.txt",
    ]
    dest_dir = kickoff_dir

    if os.path.exists(search_dir):
        for search_file in search_files:
            search_file_path = os.path.join(search_dir, search_file)
            if os.path.exists(search_file_path):
                dest = os.path.join(dest_dir, search_file)
                shutil.copy(search_file_path, dest)
            else:
                msg = "Error: %s not found" % search_file
                print(msg)
                errors.append(msg)

    search_dir = os.path.join(latest_dir_path, "TGO-MRO_overlaps")
    search_files = [
        "2deg_latlon_15min_LST",
        "2deg_latlon_30min_LST",
        "5deg_latlon_15min_LST",
        "5deg_latlon_30min_LST",
    ]  # actually directories
    dest_dir = paths["SUMMARY_FILE_PATH"]

    if os.path.exists(search_dir):
        for search_file in search_files:
            search_file_path = os.path.join(search_dir, search_file)
            if os.path.exists(search_file_path):
                dest = os.path.join(dest_dir, search_file)
                shutil.copytree(search_file_path, dest, dirs_exist_ok=True)
            else:
                msg = "Error: %s not found" % search_file
                print(msg)
                errors.append(msg)

    # OCM events
    search_dir = os.path.join(latest_dir_path, "extracted_events")
    search_file = "OCM_events.txt"
    dest_dir = paths["SUMMARY_FILE_PATH"]

    if os.path.exists(search_dir):
        search_file_path = os.path.join(search_dir, search_file)
        if os.path.exists(search_file_path):
            dest = os.path.join(dest_dir, search_file)
            shutil.copy(search_file_path, dest)
        else:
            msg = "Error: OCM events file not found"
            print(msg)
            errors.append(msg)


if type_ == "summary":

    # just get new summary files

    search_dir = os.path.join(latest_dir_path, "summary_files")
    search_files = [
        "NOMAD_dayside_nadir_summary.xlsx",
        "NOMAD_egress_solar_occulations_summary.xlsx",
        "NOMAD_grazing_solar_occulations_summary.xlsx",
        "NOMAD_ingress_and_merged_solar_occulations_summary.xlsx",
        "NOMAD_nightside_nadir_summary.xlsx",
    ]
    dest_dir = paths["SUMMARY_FILE_PATH"]

    if os.path.exists(search_dir):
        for search_file in search_files:
            search_file_path = os.path.join(search_dir, search_file)
            if os.path.exists(search_file_path):
                dest = os.path.join(dest_dir, search_file)

                # don't overwrite existing summary files, they might have been modified by adding cop rows
                if os.path.exists(dest):
                    msg = "Warning: file %s exists, skipping" % search_file
                    print(msg)
                    errors.append(msg)
                else:
                    shutil.copy(search_file_path, dest)
            else:
                msg = "Error: %s not found" % search_file
                print(msg)
                errors.append(msg)


if len(errors) > 0:
    print("##### Errors found #####")
    for error in errors:
        print(error)
