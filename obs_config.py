# -*- coding: utf-8 -*-
"""
Created on Wed Nov 14 09:58:57 2018

@author: iant
"""

import os
import sys


__project__   = "NOMAD Observation Planning"
__author__    = "Ian Thomas"
__contact__   = "ian.thomas@aeronomie.be"


OFFLINE = True #if working remotely, don't write obs to sql db
#OFFLINE = False #write obs to sql db

###############################set up directory paths##############################################################

"""where to find scripts?"""
if sys.platform == "win32":
#    BASE_DIRECTORY = os.path.normcase(os.getcwd())
    BASE_DIRECTORY = os.path.join("C:", os.sep, "Users", "iant", "Dropbox", "NOMAD", "Python", "nomad_obs")
elif sys.platform == "linux":
    BASE_DIRECTORY = os.path.join(os.sep, "bira-iasb", "projects", "NOMAD", "Science", "Planning", "nomad_obs")



"""where to put input and output files and build master copy of website?"""
if sys.platform == "win32":
    OBS_DIRECTORY = os.path.join("C:", os.sep, "Users", "iant", "Dropbox", "NOMAD", "Python", "nomad_obs", "observations")
elif sys.platform == "linux":
    OBS_DIRECTORY = os.path.join(os.sep, "bira-iasb", "projects", "NOMAD", "Science", "Planning", "nomad_obs", "observations")


"""dev website directory, for placing a copy of all the files generated, to be put online"""
#not yet implemented
if sys.platform == "win32":
    if OFFLINE:
        DEV_DIRECTORY = BASE_DIRECTORY
    else:
        DEV_DIRECTORY = os.path.join("W:", os.sep, "websites", "dev", "mars", "en", "exomars", "observations")
elif sys.platform == "linux":
    DEV_DIRECTORY = os.path.join(os.sep, "bira-iasb", "websites", "dev", "mars", "en", "exomars", "observations")


"""where to find cop tables? Note that COP patches are done at the end of an MTP, and so planning the MTP after must be done with the new tables!"""
if sys.platform == "win32":
    COP_TABLE_DIRECTORY = os.path.join("C:", os.sep, "Users", "iant", "Dropbox", "NOMAD", "Python", "data", "cop_tables")
#    COP_TABLE_DIRECTORY = os.path.join("W:", os.sep, "data", "SATELLITE", "TRACE-GAS-ORBITER", "NOMAD", "cop_tables")
elif sys.platform == "linux":
    COP_TABLE_DIRECTORY = os.path.join(os.sep, "bira-iasb", "data", "SATELLITE", "TRACE-GAS-ORBITER", "NOMAD", "cop_tables")


"""where to find the SPICE metakernel?"""
if sys.platform == "win32":
    KERNEL_DIRECTORY = os.path.join("C:", os.sep, "Users", "iant", "Documents", "DATA", "local_spice_kernels", "kernels", "mk")
#    KERNEL_DIRECTORY = os.path.join("C", "Users", "ithom", "Documents", "Work", "kernels", "mk")
#    KERNEL_DIRECTORY = os.path.join("W:", os.sep, "data", "SATELLITE", "TRACE-GAS-ORBITER", "NOMAD", "kernels", "mk")
elif sys.platform == "linux":
    KERNEL_DIRECTORY = os.path.join(os.sep, "bira-iasb", "data", "SATELLITE", "TRACE-GAS-ORBITER", "NOMAD", "kernels", "mk")



"""which SPICE metakernel to use?"""
if sys.platform == "win32":
    METAKERNEL_NAME = "em16_plan.tm"
#    METAKERNEL_NAME = "em16_ops.tm" #don't use for planning!!
elif sys.platform == "linux":
    #find planning kernel in directory
    for fileName in os.listdir(KERNEL_DIRECTORY):
        if "em16_plan_" in fileName:
            METAKERNEL_NAME = fileName




def setupPaths(mtpConstants):
    """set up paths to output files"""
    mtpNumber = mtpConstants["mtpNumber"]
    
    paths = {
            "OBS_DIRECTORY":os.path.join(OBS_DIRECTORY), \
            "COP_ROW_BASE_PATH":os.path.join(OBS_DIRECTORY, "cop_rows"), \
            "ORBIT_PLAN_BASE_PATH":os.path.join(OBS_DIRECTORY, "orbit_plans"), \
            "SUMMARY_FILE_BASE_PATH":os.path.join(OBS_DIRECTORY, "summary_files"), \
            "MTP_BASE_PATH":os.path.join(OBS_DIRECTORY, "mtp_pages"), \
            "HTML_BASE_PATH":os.path.join(OBS_DIRECTORY, "pages"), \

            "EVENT_FILE_PATH":os.path.join(OBS_DIRECTORY, "event_files"), \
            "ITL_FILE_PATH":os.path.join(OBS_DIRECTORY, "itls"), \
            "CALIBRATION_PATH":os.path.join(OBS_DIRECTORY, "calibrations"), \
            
            "COP_ROW_PATH":os.path.join(OBS_DIRECTORY, "cop_rows", "mtp%03d" %mtpNumber), \
            "ORBIT_PLAN_PATH":os.path.join(OBS_DIRECTORY, "orbit_plans", "mtp%03d" %mtpNumber), \
            "SUMMARY_FILE_PATH":os.path.join(OBS_DIRECTORY, "summary_files", "mtp%03d" %mtpNumber), \
            "HTML_MTP_PATH":os.path.join(OBS_DIRECTORY, "mtp_pages", "mtp%03d" %mtpNumber), \
            "IMG_MTP_PATH":os.path.join(OBS_DIRECTORY, "mtp_pages", "mtp%03d" %mtpNumber, "img"), \
            }    
    
    #make directories if not already existing
    for pathName, path in paths.items():
        if not os.path.exists(path):
            print("Making %s path" %pathName)
            os.mkdir(path)

    return paths





def devWebsitePaths(mtpConstants):
    """set up paths to output files"""
    mtpNumber = mtpConstants["mtpNumber"]
    
    paths = {
            "OBS_DIRECTORY":os.path.join(DEV_DIRECTORY), \
            "CALIBRATION_PATH":os.path.join(DEV_DIRECTORY, "calibrations"), \
            "COP_ROW_PATH":os.path.join(DEV_DIRECTORY, "cop_rows", "mtp%03d" %mtpNumber), \
            "EVENT_FILE_PATH":os.path.join(DEV_DIRECTORY, "event_files"), \
            "ITL_FILE_PATH":os.path.join(DEV_DIRECTORY, "itls"), \
            "HTML_MTP_PATH":os.path.join(DEV_DIRECTORY, "mtp_pages", "mtp%03d" %mtpNumber), \
            "ORBIT_PLAN_PATH":os.path.join(DEV_DIRECTORY, "orbit_plans", "mtp%03d" %mtpNumber), \
            "SUMMARY_FILE_PATH":os.path.join(DEV_DIRECTORY, "summary_files", "mtp%03d" %mtpNumber), \
            }    
    return paths




#load spiceypy kernels
import spiceypy as sp
print("KERNEL_DIRECTORY=%s, METAKERNEL_NAME=%s" %(KERNEL_DIRECTORY, METAKERNEL_NAME))
os.chdir(KERNEL_DIRECTORY)
sp.furnsh(METAKERNEL_NAME)
print(sp.tkvrsn("toolkit"))
os.chdir(BASE_DIRECTORY)



