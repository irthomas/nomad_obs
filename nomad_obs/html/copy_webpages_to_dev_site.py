# -*- coding: utf-8 -*-
"""
Created on Mon Apr 27 12:34:29 2020

@author: iant
"""

import os
import shutil
from distutils.dir_util import copy_tree


def copyWebpagesToDevSite(paths, devPaths, silent=False):
    """make of copy of all the new files on the aeronomie dev website"""
    
    if not silent: print("Copying html index page")
    #copy index.html
    local_filepath = os.path.join(paths["OBS_DIRECTORY"], "index.html")
    website_filepath = os.path.join(devPaths["OBS_DIRECTORY"], "index.html")
    shutil.copy(local_filepath, website_filepath, follow_symlinks=False)
    
    if not silent: print("Copying science calibration page")
    #copy science_calibrations.html
    local_filepath = os.path.join(paths["CALIBRATION_PATH"], "science_calibrations.html")
    website_filepath = os.path.join(devPaths["CALIBRATION_PATH"], "science_calibrations.html")
    shutil.copy(local_filepath, website_filepath, follow_symlinks=False)

    if not silent: print("Copying cop rows")
    #copy mtp cop rows
    local_directory_path = paths["COP_ROW_PATH"]
    website_directory_path = devPaths["COP_ROW_PATH"]
    copy_tree(local_directory_path, website_directory_path)

    if not silent: print("Copying event files")
    #copy all event files
    local_directory_path = paths["EVENT_FILE_PATH"]
    website_directory_path = devPaths["EVENT_FILE_PATH"]
    copy_tree(local_directory_path, website_directory_path)
    
    if not silent: print("Copying HTML pages")
    #copy mtp html pages
    local_directory_path = paths["HTML_MTP_PATH"]
    website_directory_path = devPaths["HTML_MTP_PATH"]
    copy_tree(local_directory_path, website_directory_path)

    if not silent: print("Copying ITL files")
    #copy all available itl files
    local_directory_path = paths["ITL_FILE_PATH"]
    website_directory_path = devPaths["ITL_FILE_PATH"]
    copy_tree(local_directory_path, website_directory_path)

    if not silent: print("Copying orbit plans")
    #copy mtp orbit plans
    local_directory_path = paths["ORBIT_PLAN_PATH"]
    website_directory_path = devPaths["ORBIT_PLAN_PATH"]
    copy_tree(local_directory_path, website_directory_path)

    if not silent: print("Copying summary files")
    #copy mtp summary files
    local_directory_path = paths["SUMMARY_FILE_PATH"]
    website_directory_path = devPaths["SUMMARY_FILE_PATH"]
    copy_tree(local_directory_path, website_directory_path)

