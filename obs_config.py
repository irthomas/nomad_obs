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



###############################set up directory paths##############################################################

"""where to find scripts?"""
if sys.platform == "win32":
#    BASE_DIRECTORY = os.path.normcase(os.getcwd())
    BASE_DIRECTORY = os.path.join("C:", os.sep, "Users", "iant", "Dropbox", "NOMAD", "Python", "nomad_obs")
elif sys.platform == "linux":
    BASE_DIRECTORY = os.path.join(os.sep, "bira-iasb", "projects", "NOMAD", "Science", "Planning", "Observation_planning")



"""change if neccessary. You will need to create a subdirectories called "mtps", "input" and "output" within this directory"""
if sys.platform == "win32":
    OBS_DIRECTORY = os.path.join("C:", os.sep, "Users", "iant", "Dropbox", "NOMAD", "Python", "nomad_obs", "observations")
elif sys.platform == "linux":
    BASE_DIRECTORY = os.path.join(os.sep, "bira-iasb", "projects", "NOMAD", "Science", "Planning", "Observation_planning", "observations")



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
#    KERNEL_DIRECTORY = os.path.join("W", "data", "SATELLITE", "TRACE-GAS-ORBITER", "NOMAD", "kernels", "mk")
elif sys.platform == "linux":
    KERNEL_DIRECTORY = os.path.join(os.sep, "bira-iasb", "data", "SATELLITE", "TRACE-GAS-ORBITER", "NOMAD", "kernels", "mk")



"""which SPICE metakernel to use?"""
if sys.platform == "win32":
    METAKERNEL_NAME = "em16_plan_win.tm"
#    METAKERNEL_NAME = "em16_ops.tm" #don't use for planning!!
elif sys.platform == "linux":
    METAKERNEL_NAME = "em16_plan_v320_20181206_002.tm"




