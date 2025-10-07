# -*- coding: utf-8 -*-
"""
Created on Mon Mar  4 08:22:23 2019

@author: iant


DONE:
    REWORK GENERIC PLAN ORBIT TYPE SELECTOR FOR ORBITS WITH OCCULTATIONS + LIMB AND OCCULTATIONS + OCM
    READ IN MERGED/GRAZING OCCULTATION TYPES FROM KICKOFF SUMMARY FILES (NO LONGER NEEDED)
    IMPROVE DISTRIBUTION OF OBSERVATION TYPES BASED ON PRIORITY

TODO:
    RUN CO2 ORDERS WHEN JOINT OCCULTATION WITH MAVEN

    NEED TO REDO MTP085 WITH THE 24H OF OBS REMOVED
    
    REWRITE LNO NADIR SELECTOR TO ASSIGN OBS AS A FUNCTION OF SZA WITH EQUAL SHORT/LONG DAYSIDES WITH MRO OR ROI

"""

from nomad_obs.config.paths import setupPaths  # , devWebsitePaths
from nomad_obs.html.make_website import writeIndexWebpage, writeMtpMasterPage
from nomad_obs.html.make_overview_webpage import makeOverviewPage
from nomad_obs.html.make_occultation_webpage import writeOccultationWebpage
from nomad_obs.html.make_nadir_webpage import writeNadirWebpage
from nomad_obs.cop_rows.add_cop_rows import addIrCopRows, addUvisCopRows
from nomad_obs.cop_rows.cop_table_functions import getCopTables
from nomad_obs.event_file.event_file_functions import addMappsEvents
from nomad_obs.io.write_outputs import writeAcsJointObsNumbers, writeIrCopRowsTxt, writeLnoUvisJointObsNumbers, writeOrbitPlanCsv, \
    writeLnoGroundAssetJointObsInfo, writeObjectiveOrbitNumbers
from nomad_obs.io.orbit_plan_xlsx import getMtpPlanXlsx, writeOrbitPlanXlsx
from nomad_obs.planning.thermal_rule_fit import fitNadirToThermalRule
from nomad_obs.planning.merge_input_orbit_plan import mergeMtpPlan
from nomad_obs.planning.make_orbit_plan import makeGenericOrbitPlan, makeCompleteOrbitPlan, addCorrectNadirObservations
from nomad_obs.planning.plot_regions_of_interest import plotRegionsOfInterest
from nomad_obs.planning.find_regions_of_interest import regionsOfInterestNadir, regionsOfInterestOccultation, findMatchingRegions
from nomad_obs.planning.occultations import getOccultationData, findGrazingOccultations
from nomad_obs.planning.nadirs import getNadirData
from nomad_obs.other.check_observation_names import checkKeys
from nomad_obs.other.generic_functions import printStatement
from nomad_obs.update_orbit_list import updateWrongOrbitTypes
from nomad_obs.regions_of_interest import nadirRegionsOfInterest, occultationRegionsOfInterest
from nomad_obs.observation_names import occultationObservationDict, nadirObservationDict
from nomad_obs.observation_weights import observationCycles
from nomad_obs.mtp_inputs import getMtpConstants


__project__ = "NOMAD Observation Planning"
__author__ = "Ian Thomas"
__contact__ = "ian . thomas AT aeronomie . be"


# select the MTP number to be run
mtpNumber = 95


r"""
*Remember to update spice kernels first!
run spice_kernel_downloader.py ensuring that it is in planning mode

*Get event file, MRO overlaps and SOLAR_LOS limb files from Ops FTP:
event_files\LEVF_M0xx_SOC_PLANNING.EVF

summary_files\mtp0xx\2deg_latlon_15min_LST
summary_files\mtp0xx\2deg_latlon_30min_LST
summary_files\mtp0xx\5deg_latlon_15min_LST
summary_files\mtp0xx\5deg_latlon_30min_LST


summary_files\mtp0xx\kickoff\nadir_dayside_nightside_thermal_orbits_orbit_type_summary.txt (optional)
summary_files\mtp0xx\kickoff\NOMAD_egress_solar_occulations_summary.txt (optional)
summary_files\mtp0xx\kickoff\NOMAD_ingress_and_merged_solar_occulations_summary.txt (optional)
summary_files\mtp0xx\kickoff\NOMAD_grazing_solar_occulations_summary.txt (optional, if present)

summary_files\mtp0xx\roi_flyovers_nightside-filtered.txt

If CaSSIS joint limbs:
summary_files\mtp0xx\NOMAD_TRUE_LIMB_ORBITS_OT28_WITH_UVIS_NADIR_LOS_TOWARDS_LIMB.txt (if exists)


If CaSSIS joint nadir obs, check the google doc table
* Find NOMAD thermal orbit numbers (compare CaSSIS UTCs to rows in nadir_dayside_nightside_thermal_orbits_orbit_type_summary.txt)
* Sort orbit numbers in ascending order, add to required_dayside_orbits in nomad_obs/mtp_inputs.py


* Add start/end times, COP table version, and list of forbidden dayside nadir orbits (from ops email), to nomad_obs/mtp_inputs.py
* Then run run_planning.py



* When finished, update the mtpNumber in remove_ir_nadirs.py and run it
* This will automatically remove lots of LNO nadirs, whilst keeping all the CaSSIS nadirs and trying to keep as many of the following:


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

* The new generic orbit plan nomad_mtp0xx_plan_generic.xlsx will be automatically copied to orbit_plans\mtp0xx\
* The generic orbit plan in the root directory can be deleted

* Check that any joint CaSSIS nadirs have been kept and orbit type accepts a dayside nadir i.e. 1, 3, 5 etc.
* Forbidden daysides will be removed, but this should also be checked


*if an OCM covers two daysides, check for ingress occultations on the nightside of the first OCM orbit
*compare timings with nomad_ingress_events.txt
*if found, add "1 irIngress irIngress uvisIngress" to the orbit

*check NOMAD Phobos linescans are correctly registered. Change comment column to &nomadPhobos if not already there;

*if CaSSIS joint limbs:
*change orbit to type 28 (dayside) or 47 (nightside as appropriate) for UVIS ridealong

*If requested by Liege team: add 2 UVIS nightsides (type 7 "uvisNightside") from list of orbits in roi_flyovers_nightside-filtered.txt
    These must not clash with other observations e.g. solar occultations or high priority LNO nadirs
    (UVIS can run night and day on same orbit).

*For other joint observations, plan manually in the orbit_plans\mtp0xx\nomad_mtp0xx_plan_generic.xlsx
    e.g. check occultations matching EUVM joint list (4-7 March, 6-9 May, 5-30 June, 22 Sep - 4 October 2025). Run high altitude CO2 e.g. 6SUBD CO2 H2O #14
    Replace irIngress/Egress etc by the desired observation name
    For finding orbit numbers from a list of times, use the code nomad_obs\search_matching_observation_times.py



*highlight rows in xlsx based on type: yellow = CaSSIS surface ice; blue = CaSSIS limbs; green = UVIS nightside nadir; light blue = EUVM joint occs; light red = IRTF joint obs

*NEW: if grazing occultations, check latitude/min tangent altitude SO constraints are correct



*check true limbs are correctly registered:
    type 28 = solar occ and day limb
    type 28 = day limb only
    type 47 = night limb only

*Check number of grazings matches the extracted event file nomad_grazing_events.txt:
    if not, compare start/end times to determine which are incorrect, then modify update_orbit_list.py accordingly
    Typically one merged event should be changed to a grazing occultation





*Optional: Add a few LNO-only limbs (type 8) when FOV in range if space is available (we have lots of LNO+UVIS limbs now)
    run check_when_mars_in_occ_fovs.py with correct MTP and then copy output into orbit plan -> choose some with LNO and UVIS

*If there are occultation-free periods with low LSTs, change IR daysides to mainly Surface Ice observations e.g. Surface Ice 4SUBD 01


*CaSSIS joint obs: set the dayside observation type, replacing irDayside manually, to the correct one as decided by the LNO science team


*Use excel formula to check for incorrect orbit types 3 when no LNO obs:
    copy formula into draft orbit plan cell N2 and then drag down the column
    =IF(OR(AND(A2=3,H2=""),AND(A2=14,NOT(H2=""))), 1, 0)
    Highlight the column and turn on conditional formatting to help find incorrect orbit types (all values=0 when correct)

*Add 141-150 fullscans (CO2 Fullscan Fast #5), a few at the highest latitudes north or south.
*Code to print ingress/egress latitudes:
* [(d["orbitNumber"], d["ingress"]["latMidpoint"],d["egress"]["latMidpoint"]) for d in orbitList if "ingress" in d.keys() and "egress" in d.keys()]
* Best region: south <-60 degrees Ls 40 to 120 (MTPs 89-96)


*Then delete everything from column N onwards

*Ignore all UVIS inputs for now


*Then run run_planning.py again to finish planning
    Possible errors: occultation just before (in same orbit as) OCM slot or special pointing - check timings in nomad_ingress_events.txt (or grazing)
    Change to orbit type 1 (or 5 if merged/grazing) and add ingress observation name manually e.g. irIngress, irIngress, uvisIngress


*Place nomad_mtp0xx_plan_generic.xlsx, nomad_mtp0xx_plan.csv, nomad_mtp0xx_lno_orbits.txt, nomad_mtp0xx_lno_irdayside_h2o_orbits.txt on the ftp in
/Operations/nomad_ops/orbit_plans/mtpxxx

###
Wait until Ops team sends summary files

###
*When summary files are available:

*Add Phobos Deimos COP rows manually (copy file from a previous MTP and update from spreadsheet)
*Add solar calibration COP rows manually (copy file from a previous MTP and update from spreadsheet)

*Place summary files xlsx files in summary files directory and run check_cop_rows_in_summary_files.py once selecting the correct MTP number
*Check the output in the console:
    * For every file, the number of rows must match
    * The times in the two columns must be approximately correct i.e. nadirs within 15 minutes and occultations within 1 minute
    * If there are no grazing occultations you can ignore the error that the file does not exist
*Open NOMAD_dayside_nadir_summary.xlsx and check coloured rows are filled with -1s

*Copy the updated planning.db to the website directory \components\com_nomad\data

"""


MAKE_COP_ROWS = True
# MAKE_COP_ROWS = False

MAKE_FIGURES = True
# MAKE_FIGURES = False


# def run_planning(mtpNumber):
if True:
    # START PROGRAM HERE
    print("### Planning observations for MTP %i ###" % mtpNumber)
    orbitList = []
    mtpConstants = getMtpConstants(mtpNumber)
    paths = setupPaths(mtpConstants)
    # devPaths = devWebsitePaths(mtpConstants)

    printStatement("Starting program")
    printStatement("Reading in initialisation data and inputs from mapps event file")
    printStatement("Getting nadir data")
    orbitList = getNadirData(orbitList, mtpConstants)
    printStatement("Getting occultation data")
    orbitList = getOccultationData(orbitList, mtpConstants)
    printStatement("Finding grazing occultations")
    orbitList = findGrazingOccultations(orbitList, mtpConstants)
    orbitList = updateWrongOrbitTypes(orbitList, mtpConstants)
    printStatement("Checking for corresponding MAPPS events")
    orbitList = addMappsEvents(orbitList, mtpConstants, paths)
    printStatement("Finding dayside nadir observations in regions of interest")
    orbitList = regionsOfInterestNadir(orbitList, mtpConstants, nadirRegionsOfInterest, observationCycles)
    printStatement("Finding occultation observations in regions of interest")
    orbitList = regionsOfInterestOccultation(orbitList, mtpConstants, occultationRegionsOfInterest, observationCycles)
    printStatement("Adding flags to file where obsevations match a region of interest")
    orbitList = findMatchingRegions(orbitList)
    printStatement("Plotting occultation and nadir regions of interest")
    plotRegionsOfInterest(paths, occultationRegionsOfInterest, nadirRegionsOfInterest)
    printStatement("Adding generic orbit plan to orbit list")
    orbitList = makeGenericOrbitPlan(orbitList, mtpConstants, paths)
    printStatement("Writing generic observation plan to file")
    writeOrbitPlanXlsx(orbitList, mtpConstants, paths, "plan_generic")

    printStatement("Getting iterated mtp plan from file and merging with orbit list")
    mtpPlan = getMtpPlanXlsx(mtpConstants, paths, "plan_generic")
    orbitList = mergeMtpPlan(orbitList, mtpPlan, "genericOrbitPlanIn", "genericOrbitPlanOut")
    printStatement("Writing joint observation number files for UVIS")
    writeLnoUvisJointObsNumbers(orbitList, mtpConstants, paths)
    printStatement("Writing final orbit plan to csv file")
    writeOrbitPlanCsv(orbitList, mtpConstants, paths)

    printStatement("Checking that all observation keys are in the dictionary")
    checkKeys(occultationObservationDict, nadirObservationDict, observationCycles)
    printStatement("Generating complete orbit plan (with real observation names) and adding to orbit list")
    orbitList2 = orbitList.copy()
    orbitList = makeCompleteOrbitPlan(orbitList, observationCycles)
    printStatement("Writing complete observation plan to file")
    writeOrbitPlanXlsx(orbitList, mtpConstants, paths, "plan", place_in_base_dir=False)

    printStatement("Getting final mtp plan from file and merging with orbit list")
    finalMtpPlan = getMtpPlanXlsx(mtpConstants, paths, "plan")
    # read in final plan, make finalOrbitPlan, checking it matches the previous completeOrbitPlan
    orbitList = mergeMtpPlan(orbitList, finalMtpPlan, "finalOrbitPlan", "completeOrbitPlan")
    orbitList = addCorrectNadirObservations(orbitList)
    printStatement("Reducing LNO dayside nadir observations to fit thermal rule")
    orbitList = fitNadirToThermalRule(orbitList, mtpConstants)
    printStatement("Finding and adding COP rows to orbit list")
    copTableDict = getCopTables(mtpConstants)
    orbitList = addIrCopRows(orbitList, copTableDict, mtpConstants, occultationObservationDict, nadirObservationDict)
    orbitList = addUvisCopRows(orbitList, copTableDict, mtpConstants, occultationObservationDict, nadirObservationDict, paths, from_file=True)

    if MAKE_COP_ROWS:
        printStatement("Writing COP rows to text files")
        writeIrCopRowsTxt(orbitList, mtpConstants, paths)
        # writeUvisCopRowsTxt(orbitList, mtpConstants, paths)

        printStatement("Writing LNO and Curosity + InSight joint observation files")
        writeLnoGroundAssetJointObsInfo(orbitList, mtpConstants, paths, "Curiosity")
        writeLnoGroundAssetJointObsInfo(orbitList, mtpConstants, paths, "Insight")

        printStatement("Writing joint observation number files for ACS")
        writeAcsJointObsNumbers(orbitList, mtpConstants, paths)

        printStatement("Writing joint observation number files for specific objectives")
        writeObjectiveOrbitNumbers(orbitList, mtpConstants, paths, "LNO", "irDayside", "H2O")

    printStatement("Writing mtp occultation webpage")
    writeOccultationWebpage(orbitList, mtpConstants, paths, make_figures=MAKE_FIGURES)  # also updates sql
    printStatement("Writing mtp nadir webpage")
    writeNadirWebpage(orbitList, mtpConstants, paths, make_figures=MAKE_FIGURES)  # also updates sql

    if MAKE_FIGURES:
        printStatement("Making order plots and writing mtp overview page")
        makeOverviewPage(orbitList, mtpConstants, paths, occultationObservationDict, nadirObservationDict)
        printStatement("Writing master page for this MTP and updating main index webpage")
        writeMtpMasterPage(mtpConstants, paths)
        writeIndexWebpage(mtpConstants, paths)
        # printStatement("Updating science calibrations webpage")
        # writeCalibrationWebpage(paths)

# CALIBRATION FILE MUST BE FILLED IN MANUALLY. USE VALUES FROM SOLAR_CALIBRATIONS.XLSX FILE FOR MINISCANS/FULLSCANS. SEE PREVIOUS MTPS FOR EXAMPLES.
# THIS AND THE OTHER IR COP ROWS SHOULD BE CHECKED (COMPARE TO SUMMARY FILES FROM BOJAN/CLAUDIO), PARTICULARLY TIMINGS AND NUMBER OF ROWS IN FILES
# LNO ORBIT NUMBER FILE, FOR UVIS OPS TEAM
# WHEN THE OU SENDS THE COP ROWS TO THE OPS TEAM, PLACE A COPY IN THE COP_ROW/MTPXXX FOLDER AND RERUN THE PLANNING
# THE SQL DATABASE WILL BE UPDATED WITH THE UVIS COP ROWS


# all MTPs should run successfully (tested up to MTP084)
# for adding UVIS COP rows to planning (change to function)
# for very old MTPs (e.g. those without MRO overlap files, may need to set IGNORE_MISSING=True)
# for mtpNumber in range(83, 85):
#     run_planning(mtpNumber)


# windows only
# run planning script in pop-out window so user can continue working
# import os
# import sys
# if sys.platform == "win32":
#    if __name__ == "__main__":
#        os.system("python -i run_planning.py")
