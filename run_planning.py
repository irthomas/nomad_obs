# -*- coding: utf-8 -*-
"""
Created on Mon Mar  4 08:22:23 2019

@author: iant



TODO:
    REWORK GENERIC PLAN ORBIT TYPE SELECTOR FOR ORBITS WITH OCCULTATIONS + LIMB AND OCCULTATIONS + OCM
    ADD RANDOM NUMBER GENERATOR FOR NADIR ROI FLYOVERS, REDUCE ROIS AND NADIRS ON ORBITS OF TYPE 1
    READ IN OCM EXTRACTED EVENTS FILE
    READ IN MERGED/GRAZING OCCULTATION TYPES FROM KICKOFF SUMMARY FILES
    
    
"""

__project__   = "NOMAD Observation Planning"
__author__    = "Ian Thomas"
__contact__   = "ian . thomas AT aeronomie . be"


#select the MTP number to be run
mtpNumber = 54


r"""
*Remember to update spice kernels first!
*Get event file, MRO overlaps and SOLAR_LOS limb files from Ops zip:

event_files\LEVF_M0xx_SOC_PLANNING.EVF

summary_files\mtp0xx\2deg_latlon_15min_LST
summary_files\mtp0xx\2deg_latlon_30min_LST
summary_files\mtp0xx\5deg_latlon_15min_LST
summary_files\mtp0xx\5deg_latlon_30min_LST

summary_files\mtp0xx\kickoff\nadir_dayside_nightside_thermal_orbits_orbit_type_summary.txt
summary_files\mtp0xx\kickoff\NOMAD_egress_solar_occulations_summary.txt
summary_files\mtp0xx\kickoff\NOMAD_ingress_and_merged_solar_occulations_summary.txt
summary_files\mtp0xx\kickoff\NOMAD_grazing_solar_occulations_summary.txt (if present)

summary_files\mtp0xx\MARS_IN_LNO_OCC_FOV.txt
summary_files\mtp0xx\MARS_IN_UVIS_OCC_FOV.txt

*Add start/end times to mtp_inputs.py
*Then run run_planning.py

*Check draft orbit plan - remove lots of LNO nadirs, trying to keep as many of the following:
    
Region                    Priority  reduce box size; not run each time.
------                    --------
Olympus Mons	          Run preferentially but not always
Curiosity	              Run preferentially but not always
Perseverance              Run preferentially but not always
MRO overlaps              Normal priority
Acidalia Planitia	      Normal priority
Nili Fossae	              Normal priority
Mawrth Vallis/Aram Chaos  Normal priority
Meridiani Sulfates	      Normal priority
Mawrth Vallis	          Normal priority
Other targets	          Normal priority

*note that many daysides directly before/after solar calibrations and Phobos/Deimos pointings are not allowed - can remove many of these


*check OCM start/end times, particularly those orbits with occultations near OCMs
*compare column L (dayside start time) to start/end times in extracted_events/OCM_events.txt in the zip
*if any clash with nadir observations, change to orbit type 14 and remove observations from irDayside column

*check true limbs are correctly registered:
    type 28 = solar occ and day limb
    type 28 = day limb only
    type 47 = night limb only

*Check number of grazings matches the extracted event file nomad_grazing_events.txt:
    if not, compare start/end times to determine which are incorrect, then modify update_orbit_list.py accordingly


*Add a few LNO nightsides (type 7) if space is available -> less critical if nightside limbs already present

*Add a few LNO-only limbs (type 8) when FOV in range if space is available (we have lots of LNO+UVIS limbs now)
    run check_when_mars_in_occ_fovs.py with correct MTP and then copy output into orbit plan -> choose some with LNO and UVIS

*If there are occultation-free periods, change IR daysides to mainly Surface Ice observations e.g. Surface Ice 4SUBD 01


*Use excel formula to check for incorrect orbit types 3 when no LNO obs:
    copy formula into draft orbit plan cell N2 and then drag down the column
    =IF(OR(AND(A2=3,H2=""),AND(A2=14,NOT(H2=""))), 1, 0)
    
*Then delete everything from column N onwards
    
*Ignore all UVIS inputs for now

*Move nomad_mtp0xx_plan_generic.xlsx to orbit_plans\mtp0xx\

*Then run run_planning.py again to finish planning
    Possible errors: occultation just before OCM slot - check timings in nomad_ingress_events.txt (or grazing)
    Change orbit type 1 (or 5) and add ingress observation name manually
    
    
*Send nomad_mtp0xx_plan_generic.xlsx, nomad_mtp0xx_plan.csv and nomad_mtp0xx_lno_orbits.txt to nomad.iops



"""
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
# from nomad_obs.io.write_outputs import dump_json

from nomad_obs.event_file.event_file_functions import addMappsEvents

from nomad_obs.cop_rows.cop_table_functions import getCopTables
from nomad_obs.cop_rows.add_cop_rows import addIrCopRows, addUvisCopRows

# from nomad_obs.html.make_calibration_webpage import writeCalibrationWebpage
from nomad_obs.html.make_nadir_webpage import writeNadirWebpage
from nomad_obs.html.make_occultation_webpage import writeOccultationWebpage
from nomad_obs.html.make_overview_webpage import makeOverviewPage
from nomad_obs.html.make_website import writeIndexWebpage, writeMtpMasterPage
from nomad_obs.html.copy_webpages_to_dev_site import copyWebpagesToDevSite



MAKE_COP_ROWS = True
# MAKE_COP_ROWS = False

MAKE_FIGURES = True
# MAKE_FIGURES = False


# def run_planning(mtpNumber):
if True:
    #START PROGRAM HERE
    print("### Planning observations for MTP %i ###" %mtpNumber)
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
    writeOrbitPlanXlsx(orbitList, mtpConstants, paths, "plan", place_in_base_dir=False)
    #FINAL ORBIT PLAN WILL BE PLACED DIRECTLY IN ORBIT_PLANS/MTPXXX FOLDER AND SCRIPT WILL CONTINUE
    
    
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
    
    if MAKE_COP_ROWS:
        printStatement("Writing COP rows to text files")
        writeIrCopRowsTxt(orbitList, mtpConstants, paths)
        
        printStatement("Writing LNO and Curosity + InSight joint observation files")   
        writeLnoGroundAssetJointObsInfo(orbitList, mtpConstants, paths, "Curiosity")
        writeLnoGroundAssetJointObsInfo(orbitList, mtpConstants, paths, "Insight")
    
        printStatement("Writing joint observation number files for ACS")
        writeAcsJointObsNumbers(orbitList, mtpConstants, paths)
    
    printStatement("Writing mtp occultation webpage")
    writeOccultationWebpage(orbitList, mtpConstants, paths, make_figures=MAKE_FIGURES) #also updates sql
    printStatement("Writing mtp nadir webpage")
    writeNadirWebpage(orbitList, mtpConstants, paths, make_figures=MAKE_FIGURES) #also updates sql
    
    if MAKE_FIGURES:
        printStatement("Making order plots and writing mtp overview page")
        makeOverviewPage(orbitList, mtpConstants, paths, occultationObservationDict, nadirObservationDict)
        printStatement("Writing master page for this MTP and updating main index webpage")
        writeMtpMasterPage(mtpConstants, paths)
        writeIndexWebpage(mtpConstants, paths)
        # printStatement("Updating science calibrations webpage")
        # writeCalibrationWebpage(paths)

    #THE FOLLOWING FILES WILL BE GENERATED IN COP_ROWS/MTPXXX FOLDER:
    #CALIBRATION FILE MUST BE FILLED IN MANUALLY. USE VALUES FROM SOLAR_CALIBRATIONS.XLSX FILE FOR MINISCANS/FULLSCANS. SEE PREVIOUS MTPS FOR EXAMPLES.
    #THIS AND THE OTHER IR COP ROWS SHOULD BE CHECKED (COMPARE TO SUMMARY FILES FROM BOJAN/CLAUDIO), PARTICULARLY TIMINGS AND NUMBER OF ROWS IN FILES
    #LNO ORBIT NUMBER FILE, FOR UVIS OPS TEAM
    #JOINT OCCULTATION FILE, FOR ACS TEAM. THIS WILL BE SENT BY BOJAN/CLAUDIO TO THE SOC.
    #SEND ALL FILES IN THE COP_ROW/MTPXXX FOLDER TO NOMAD.IOPS@AERONOMIE.BE
    #WHEN THE OU SENDS THE COP ROWS TO THE OPS TEAM, PLACE A COPY IN THE COP_ROW/MTPXXX FOLDER AND RERUN THE PLANNING
    #THE SQL DATABASE WILL BE UPDATED WITH THE UVIS COP ROWS
    
    #NEW WEBPAGES ARE UPDATED AUTOMATICALLY IN THE LOCAL OBS_DIRECTORY
    
    """only run step5 when final COP rows are delivered. Must be at BIRA or on linux system.
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
    




# except:
#     dump_json(orbitList)

    

# for mtpNumber in range(14,41):
#     run_planning(mtpNumber)
        

#windows only
#run planning script in pop-out window so user can continue working
#import os
#import sys
#if sys.platform == "win32":
#    if __name__ == "__main__":
#        os.system("python -i run_planning.py")



