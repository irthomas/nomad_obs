# -*- coding: utf-8 -*-
"""
Created on Mon Mar  4 08:22:23 2019

@author: iant
"""



from obs_inputs import getMtpConstants
from obs_config import setupPaths, devWebsitePaths
from obs_functions import step1, step2, step3, step4, step5

__project__   = "NOMAD Observation Planning"
__author__    = "Ian Thomas"
__contact__   = "ian.thomas@aeronomie.be"





"""change this number, add the correct info to the mtp in obs_inputs, and run this script"""

mtpNumber = 15



#START PROGRAM HERE
orbitList = []
mtpConstants = getMtpConstants(mtpNumber)
paths = setupPaths(mtpConstants)
devPaths = devWebsitePaths(mtpConstants)

orbitList = step1(orbitList, mtpConstants, paths)
#GENERIC ORBIT PLAN WILL BE PLACED IN BASE DIRECTORY. SEND THIS TO NOMAD.IOPS
#WHEN MODIFIED VERSION IS SENT BACK, UPDATE NIGHTSIDES, ADD LNO ONY LIMBS, AND CHECK FOR ERRORS

#IF ALL IS OK THEN PLACE IT IN THE ORBIT_PLANS/MTPXXX FOLDER AND RUN ENTIRE SCRIPT AGAIN


orbitList = step2(orbitList, mtpConstants, paths)

#LNO-UVIS JOINT OBSERVATION FILE WILL BE CREATED IN BASE DIRECTORY.
#SEND THIS AND THE UPDATED GENERIC ORBIT PLAN TO NOMAD.IOPS


orbitList = step3(orbitList, mtpConstants, paths)
#FINAL ORBIT PLAN WILL BE PLACED IN BASE DIRECTORY. CHECK FOR ISSUES
#IF ALL OK THEN PLACE IT IN THE ORBIT_PLANS/MTPXXX FOLDER AND RUN ENTIRE SCRIPT AGAIN


orbitList = step4(orbitList, mtpConstants, paths)
#THE FOLLOWING FILES WILL BE GENERATED IN COP_ROWS/MTPXXX FOLDER:
#CALIBRATION FILE MUST BE FILLED IN MANUALLY. USE VALUES FROM SOLAR_CALIBRATIONS.XLSX FILE FOR MINISCANS/FULLSCANS. SEE PREVIOUS MTPS FOR EXAMPLES.
#THIS AND THE OTHER IR COP ROWS SHOULD BE CHECKED (COMPARE TO SUMMARY FILES FROM BOJAN/CLAUDIO), PARTICULARLY TIMINGS AND NUMBER OF ROWS IN FILES
#LNO ORBIT NUMBER FILE, FOR UVIS OPS TEAM
#JOINT OCCULTATION FILE, FOR ACS TEAM. THIS WILL BE SENT BY BOJAN/CLAUDIO TO THE SOC.
#SEND ALL FILES IN THE COP_ROW/MTPXXX FOLDER TO NOMAD.IOPS@AERONOMIE.BE

#NEW WEBPAGES ARE UPDATED AUTOMATICALLY IN THE LOCAL OBS_DIRECTORY

"""only run step5 when final COP rows are delivered"""
#step5(paths, devPaths)
#COPY FILES TO THE DEV SITE
#RUN THE SCRIPT TO COPY THEM TO THE PROD SITE

#PROGRAM FINISHED