# -*- coding: utf-8 -*-
"""
Created on Mon Mar  4 08:22:23 2019

@author: iant
"""

__project__   = "NOMAD Observation Planning"
__author__    = "Ian Thomas"
__contact__   = "ian . thomas AT aeronomie . be"


### THESE CAN BE MODIFIED ####
#select the MTP number to be run
mtpNumber = 35
"""excel =IF(OR(AND(A2=3,H2=""),AND(A2=14,NOT(H2=""))), 1, 0)"""
"""remember to update spice kernels first..."""

#add the correct MTP info in obs_inputs
from nomad_obs.mtp_inputs import getMtpConstants

#change observation types and their priorities in observation_weights
from nomad_obs.observation_weights import observationCycles

#change list of possible observation types and their paramters in observation_names
from nomad_obs.observation_names import occultationObservationDict, nadirObservationDict

#define new or modify existing regions of interest in regions_of_interest
from nomad_obs.regions_of_interest import nadirRegionsOfInterest, occultationRegionsOfInterest

#change directory paths and SPICE kernels here
#always select OFFLINE=True if running on home computer
from nomad_obs.config.paths import setupPaths, devWebsitePaths, OFFLINE
#now run the script

#if the number of COP rows is incorrect in the occultation files, add an override here
from nomad_obs.update_orbit_list import updateWrongOrbitTypes




### THESE SHOULD NOT BE MODIFIED UNLESS UPDATING ####
from nomad_obs.other.generic_functions import printStatement
from nomad_obs.other.check_observation_names import checkKeys

from nomad_obs.planning.nadirs import getNadirData
from nomad_obs.planning.occultations import getOccultationData, findGrazingOccultations
from nomad_obs.planning.find_regions_of_interest import regionsOfInterestNadir, regionsOfInterestOccultation, findMatchingRegions
from nomad_obs.planning.plot_regions_of_interest import plotRegionsOfInterest
from nomad_obs.planning.make_orbit_plan import makeGenericOrbitPlan, makeCompleteOrbitPlan, addCorrectNadirObservations
from nomad_obs.planning.merge_input_orbit_plan import mergeMtpPlan
from nomad_obs.planning.thermal_rule_fit import fitNadirToThermalRule

from nomad_obs.io.orbit_plan_xlsx import getMtpPlanXlsx, writeOrbitPlanXlsx
from nomad_obs.io.write_outputs import writeAcsJointObsNumbers, writeIrCopRowsTxt, writeLnoUvisJointObsNumbers, writeOrbitPlanCsv, writeLnoGroundAssetJointObsInfo

from nomad_obs.event_file.event_file_functions import addMappsEvents

from nomad_obs.cop_rows.cop_table_functions import getCopTables
from nomad_obs.cop_rows.add_cop_rows import addIrCopRows, addUvisCopRows

from nomad_obs.html.make_calibration_webpage import writeCalibrationWebpage
from nomad_obs.html.make_nadir_webpage import writeNadirWebpage
from nomad_obs.html.make_occultation_webpage import writeOccultationWebpage
from nomad_obs.html.make_overview_webpage import makeOverviewPage
from nomad_obs.html.make_website import writeIndexWebpage, writeMtpMasterPage
from nomad_obs.html.copy_webpages_to_dev_site import copyWebpagesToDevSite






#START PROGRAM HERE
orbitList = []
mtpConstants = getMtpConstants(mtpNumber)
paths = setupPaths(mtpConstants)
devPaths = devWebsitePaths(mtpConstants)

printStatement("Starting program")
printStatement("Reading in initialisation data and inputs from mapps event file")    
printStatement("Getting nadir data")
orbitList = getNadirData(orbitList, mtpConstants)
printStatement("Getting occultation data")
orbitList = getOccultationData(orbitList, mtpConstants)
printStatement("Finding grazing occultations")
orbitList = findGrazingOccultations(orbitList)
orbitList = updateWrongOrbitTypes(orbitList, mtpConstants)
printStatement("Checking for corresponding MAPPS events")
orbitList = addMappsEvents(orbitList, mtpConstants, paths)
printStatement("Finding dayside nadir observations in regions of interest")
orbitList = regionsOfInterestNadir(orbitList, nadirRegionsOfInterest, observationCycles)
printStatement("Finding occultation observations in regions of interest")
orbitList = regionsOfInterestOccultation(orbitList, occultationRegionsOfInterest, observationCycles)
printStatement("Adding flags to file where obsevations match a region of interest")
orbitList = findMatchingRegions(orbitList)
printStatement("Plotting occultation and nadir regions of interest")
plotRegionsOfInterest(paths, occultationRegionsOfInterest, nadirRegionsOfInterest)
printStatement("Adding generic orbit plan to orbit list (no nightsides or limbs, to be added manually)")
orbitList = makeGenericOrbitPlan(orbitList, mtpConstants, paths)
printStatement("Writing generic observation plan to file")
writeOrbitPlanXlsx(orbitList, mtpConstants, paths, "plan_generic")
#GENERIC ORBIT PLAN WILL BE PLACED IN BASE DIRECTORY. REMOVE NADIRS AND SEND THIS TO NOMAD.IOPS
#WHEN MODIFIED VERSION IS SENT BACK, UPDATE NIGHTSIDES, ADD LNO ONLY LIMBS, AND CHECK FOR ERRORS
#IF ALL IS OK THEN PLACE IT IN THE ORBIT_PLANS/MTPXXX FOLDER AND RUN ENTIRE SCRIPT AGAIN


printStatement("Getting iterated mtp plan from file and merging with orbit list")
mtpPlan = getMtpPlanXlsx(mtpConstants, paths, "plan_generic")
orbitList = mergeMtpPlan(orbitList, mtpPlan, "genericOrbitPlanIn", "genericOrbitPlanOut")
printStatement("Writing joint observation number files for UVIS")
writeLnoUvisJointObsNumbers(orbitList, mtpConstants, paths)
printStatement("Writing final orbit plan to csv file")
writeOrbitPlanCsv(orbitList, mtpConstants, paths)
#LNO-UVIS JOINT OBSERVATION FILE WILL BE CREATED IN BASE DIRECTORY.
#SEND THIS AND THE UPDATED GENERIC ORBIT PLAN TO NOMAD.IOPS


printStatement("Checking that all observation keys are in dictionary")
checkKeys(occultationObservationDict, nadirObservationDict, observationCycles)
printStatement("Generating complete orbit plan (with real observation names) and adding to orbit list")
orbitList = makeCompleteOrbitPlan(orbitList, observationCycles)
printStatement("Writing complete observation plan to file")
writeOrbitPlanXlsx(orbitList, mtpConstants, paths, "plan")
#FINAL ORBIT PLAN WILL BE PLACED IN BASE DIRECTORY. CHECK FOR ISSUES
#IF ALL OK THEN PLACE IT IN THE ORBIT_PLANS/MTPXXX FOLDER AND RUN ENTIRE SCRIPT AGAIN


printStatement("Getting final mtp plan from file and merging with orbit list")
finalMtpPlan = getMtpPlanXlsx(mtpConstants, paths, "plan")
#read in final plan, make finalOrbitPlan, checking it matches the previous completeOrbitPlan
orbitList = mergeMtpPlan(orbitList, finalMtpPlan, "finalOrbitPlan", "completeOrbitPlan") 
orbitList = addCorrectNadirObservations(orbitList)
printStatement("Reducing LNO dayside nadir observations to fit thermal rule")
orbitList = fitNadirToThermalRule(orbitList)
printStatement("Finding and adding COP rows to orbit list")
copTableDict = getCopTables(mtpConstants)
orbitList = addIrCopRows(orbitList, copTableDict, mtpConstants, occultationObservationDict, nadirObservationDict)
orbitList = addUvisCopRows(orbitList, copTableDict, mtpConstants, paths)
printStatement("Writing COP rows to text files")
writeIrCopRowsTxt(orbitList, mtpConstants, paths)
printStatement("Writing LNO and Curosity + InSight joint observation files")   
writeLnoGroundAssetJointObsInfo(orbitList, mtpConstants, paths, "Curiosity")
writeLnoGroundAssetJointObsInfo(orbitList, mtpConstants, paths, "Insight")
#    writeLnoGroundAssetJointObsInfo(orbitList, mtpConstants, paths, "AEOLIS MENSAE MFF")
printStatement("Writing mtp occultation webpage")
writeOccultationWebpage(orbitList, mtpConstants, paths)
printStatement("Writing mtp nadir webpage")
writeNadirWebpage(orbitList, mtpConstants, paths)
printStatement("Making order plots and writing mtp overview page")
makeOverviewPage(orbitList, mtpConstants, paths, occultationObservationDict, nadirObservationDict)
printStatement("Writing joint observation number files for ACS")
writeAcsJointObsNumbers(orbitList, mtpConstants, paths)
printStatement("Writing master page for this MTP and updating main index webpage")
writeMtpMasterPage(mtpConstants, paths)
writeIndexWebpage(mtpConstants, paths)
printStatement("Updating science calibrations webpage")
writeCalibrationWebpage(paths)
#THE FOLLOWING FILES WILL BE GENERATED IN COP_ROWS/MTPXXX FOLDER:
#CALIBRATION FILE MUST BE FILLED IN MANUALLY. USE VALUES FROM SOLAR_CALIBRATIONS.XLSX FILE FOR MINISCANS/FULLSCANS. SEE PREVIOUS MTPS FOR EXAMPLES.
#THIS AND THE OTHER IR COP ROWS SHOULD BE CHECKED (COMPARE TO SUMMARY FILES FROM BOJAN/CLAUDIO), PARTICULARLY TIMINGS AND NUMBER OF ROWS IN FILES
#LNO ORBIT NUMBER FILE, FOR UVIS OPS TEAM
#JOINT OCCULTATION FILE, FOR ACS TEAM. THIS WILL BE SENT BY BOJAN/CLAUDIO TO THE SOC.
#SEND ALL FILES IN THE COP_ROW/MTPXXX FOLDER TO NOMAD.IOPS@AERONOMIE.BE
#WHEN THE OU SENDS THE COP ROWS TO THE OPS TEAM, PLACE A COPY IN THE COP_ROW/MTPXXX FOLDER AND RERUN THE PLANNING
#THE SQL DATABASE WILL BE UPDATED WITH THE UVIS COP ROWS

#NEW WEBPAGES ARE UPDATED AUTOMATICALLY IN THE LOCAL OBS_DIRECTORY

"""only run step5 when final COP rows are delivered. Must be at BIRA or on linxu system.
Note that chuck/crunch don't have access to website directory so output is written
to a temporary directory. Transfer must be done manually periodically"""
if not OFFLINE:
    printStatement("Copying web pages to aeronomie dev website")
    copyWebpagesToDevSite(paths, devPaths)
    printStatement("Done!")
else:
    printStatement("Warning: working offline, dev website will not be updated")
#COPY FILES TO THE OLD DEV OBS PLANNING WEBSITE
#RUN THE SCRIPT IN THE DEV WEBSITE FOLDER TO COPY THEM TO THE EXTERNAL WEBSITE
#cd /bira-iasb/websites/dev/mars>
#./sync_to_prod.sh 
#CREATE A NEW PAGE ON THE NEW WEBSITE AT NOMAD.AERONOMIE.BE AND COPY THE MTP OVERVIEW PAGE INFO ONTO IT. SET CATEGORY TO MTPS
#THE PAGE WILL BE ADDED TO THE CORRECT PAGE AND THE PLOTS AND DETAILED PLANNING WILL BE UPDATED AUTOMATICALLY FROM THE SQL DATABASE

#PROGRAM FINISHED





        

#windows only
#run planning script in pop-out window so user can continue working
#import os
#import sys
#if sys.platform == "win32":
#    if __name__ == "__main__":
#        os.system("python -i run_planning.py")



