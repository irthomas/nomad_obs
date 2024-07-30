# -*- coding: utf-8 -*-
"""
Created on Fri Oct  6 14:34:59 2023

@author: iant

MAKE THE ORBIT PLAN FROM THE INPUT COP ROWS TO GET EARLY MTPS THROUGH THE PLANNING PIPELINE

1. SELECT THE mtpNumber
2. WHEN THE FILE IS GENERATED, RENAME TO nomad_mtpXXX_plan_generic.xlsx 
3. PLACE IN THE CORRECT ORBIT PLAN DIRECTORY
4. ADD THE START/END TIMES TO mtp_inputs.py
5. RUN run_planning.py ON THAT MTP
"""

import os


# add the correct MTP info in obs_inputs
from nomad_obs.mtp_inputs import getMtpConstants

# change observation types and their priorities in observation_weights
from nomad_obs.observation_weights import observationCycles

# change list of possible observation types and their paramters in observation_names
from nomad_obs.observation_names import occultationObservationDict, nadirObservationDict

# define new or modify existing regions of interest in regions_of_interest
from nomad_obs.regions_of_interest import nadirRegionsOfInterest, occultationRegionsOfInterest

# change directory paths and SPICE kernels here
# always select OFFLINE=True if running on home computer
from nomad_obs.config.paths import setupPaths, devWebsitePaths
# now run the script

# if the number of COP rows is incorrect in the occultation files, add an override here
from nomad_obs.update_orbit_list import updateWrongOrbitTypes

from nomad_obs.config.constants import LNO_CENTRE_DETECTOR_LINE
from nomad_obs.cop_rows.cop_table_functions import makeCopTableDict


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
from nomad_obs.cop_rows.cop_table_functions import getCopRows
# from nomad_obs.cop_rows.add_cop_rows import addIrCopRows, addUvisCopRows

# from nomad_obs.html.make_calibration_webpage import writeCalibrationWebpage
# from nomad_obs.html.make_nadir_webpage import writeNadirWebpage
# from nomad_obs.html.make_occultation_webpage import writeOccultationWebpage
# from nomad_obs.html.make_overview_webpage import makeOverviewPage
# from nomad_obs.html.make_website import writeIndexWebpage, writeMtpMasterPage


mtpNumber = 7


mtpConstants = getMtpConstants(mtpNumber)
paths = setupPaths(mtpConstants)

if "orbitList" not in globals():
    print("### Planning observations for MTP %i ###" % mtpNumber)
    orbitList = []
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
    printStatement("Adding generic orbit plan to orbit list (no nightsides or limbs, to be added manually)")

    # orbitList = makeGenericOrbitPlan(orbitList, mtpConstants, paths)
    # printStatement("Writing generic observation plan to file")
    # writeOrbitPlanXlsx(orbitList, mtpConstants, paths, "plan_generic")

    printStatement("Finding COP rows to orbit list")
    copTableDict = getCopTables(mtpConstants)

    # manually update orbitList with special observations e.g. SO during ACS occultations
    if mtpNumber == 2:
        orbitList[27]["allowedObservationTypes"].extend(["egress", "ingress"])
        orbitList[30]["allowedObservationTypes"].extend(["egress", "ingress"])
        orbitList[91]["allowedObservationTypes"].extend(["egress", "ingress"])
    if mtpNumber == 3:
        orbitList[5]["allowedObservationTypes"].extend(["egress"])
        orbitList[8]["allowedObservationTypes"].extend(["ingress"])
        orbitList[10]["allowedObservationTypes"].extend(["ingress"])
    if mtpNumber == 7:
        orbitList[195]["allowedObservationTypes"].remove("merged")
        orbitList[195]["allowedObservationTypes"].append("grazing")


# loop through orbitList, printing orbits where the chosen obs type is found
# obs_name = "egress"
# i = 0
# for orbit in orbitList:
#     if obs_name in orbit["allowedObservationTypes"]:
#         i += 1
#         print(i, orbit["orbitNumber"], orbit["utcOrbitStart"])

# #loop through orbitList, printing all obs types for each orbit
for orbit in orbitList:
    print(orbit["orbitNumber"], orbit["utcOrbitStart"], orbit["allowedObservationTypes"])


# get list of egress / ingress / merged / grazing orbits
egress_orbits = []
ingress_merged_orbits = []
grazing_orbits = []
for orbit in orbitList:
    if "egress" in orbit["allowedObservationTypes"]:
        egress_orbits.append({"orbitNumber": orbit["orbitNumber"], "orbitType": 1})
    if "ingress" in orbit["allowedObservationTypes"]:
        ingress_merged_orbits.append({"orbitNumber": orbit["orbitNumber"], "orbitType": 1})
    if "merged" in orbit["allowedObservationTypes"]:
        ingress_merged_orbits.append({"orbitNumber": orbit["orbitNumber"], "orbitType": 5})
    if "grazing" in orbit["allowedObservationTypes"]:
        grazing_orbits.append({"orbitNumber": orbit["orbitNumber"], "orbitType": 5})


printStatement("Reading in COP rows")

n_orbits = len(orbitList)


obs_type_names = [
    "ir_dayside_nadir",
    "ir_egress_occultations",
    "ir_grazing_occultations",
    "ir_ingress_occultations",
    "ir_nightside_nadir"
]


# get raw data from cop row files
cop_file_lines = {}
# loop through observation types
for obs_type_name in obs_type_names:
    if mtpNumber < 8:
        cop_path = os.path.join(paths["COP_ROW_PATH"], "sent", "nomad_mtp%03d_%s.txt" % (mtpNumber, obs_type_name[3:]))
    else:
        cop_path = os.path.join(paths["COP_ROW_PATH"], "sent", "mtp%03d_%s" % (mtpNumber, obs_type_name))

    if not os.path.exists(cop_path):
        print("File not found %s" % cop_path)

    with open(cop_path, "r") as f:
        lines = f.readlines()

    split_lines = []
    for line in lines[1:]:
        split = line.split(",")
        split_lines.append(split)

    cop_file_lines[obs_type_name] = split_lines


# make list of dictionaries, one for each orbit containing channel and cop row(s) for each observation type
cop_orbits = [{"orbitNumber": i+1} for i in range(n_orbits)]

# do dayside nadir first
obs_type_name = "ir_dayside_nadir"
orbit_times = []
orbit = 0

# extract COP rows, orbit numbers from file, make a dictionary from them
for split in cop_file_lines[obs_type_name]:
    orbit_time = split[-2]

    # some are orbit type 14 where there can be 3 rows for the same nadir orbit
    # only add if unique orbit time, otherwise skip repeats
    if orbit_time not in orbit_times:
        orbit += 1
        orbit_times.append(orbit_time)
    else:
        continue

    cop = [int(split[2])]
    if mtpNumber < 4:
        # assume channel is LNO
        channel = 1
    else:
        channel = int(split[4])

    # sometimes to last lines have extra orbits without full times
    if orbit > len(cop_orbits):
        print("Error", split)
    else:
        cop_orbits[orbit-1]["utc"] = orbit_time
        cop_orbits[orbit-1][obs_type_name] = {"channel": channel, "cop": cop}


# save list of times to to use for the nightside
dayside_orbit_times = orbit_times[:]

# nightside nadir
obs_type_name = "ir_nightside_nadir"

for split in cop_file_lines[obs_type_name]:
    orbit_time = split[-2]

    if len(orbit_time) > 19:  # avoid - or NONE

        cop = [int(split[2])]
        if mtpNumber < 4:
            # assume channel is LNO
            channel = 1
        else:
            channel = int(split[4])
        # get orbit number from orbit time
        # list is generated from dayside nadirs
        ix = dayside_orbit_times.index(orbit_time)
        cop_orbits[ix][obs_type_name] = {"channel": channel, "cop": cop}
        cop_orbits[ix]["orbitType"] = 17


# occultations
obs_type_name = "ir_egress_occultations"
i = 0  # line number

for split in cop_file_lines[obs_type_name]:
    cop = [int(split[2]), int(split[3])]

    if mtpNumber < 4:
        # assume SO channel for early occultations
        channel = 0
    else:
        # channel can be SO or LNO for later occs
        channel = int(split[4])

    # get correct orbit number from orbitList
    orbit_number = egress_orbits[i]["orbitNumber"]
    cop_orbits[orbit_number-1][obs_type_name] = {"channel": channel, "cop": cop}
    cop_orbits[orbit_number-1]["orbitType"] = egress_orbits[i]["orbitType"]
    i += 1


obs_type_name = "ir_ingress_occultations"
i = 0  # line number

for split in cop_file_lines[obs_type_name]:
    cop = [int(split[2]), int(split[3])]

    if mtpNumber < 4:
        # assume SO channel for early occultations
        channel = 0
    else:
        # channel can be SO or LNO for later occs
        channel = int(split[4])

    # get correct orbit number from orbitList
    orbit_number = ingress_merged_orbits[i]["orbitNumber"]
    cop_orbits[orbit_number-1][obs_type_name] = {"channel": channel, "cop": cop}
    cop_orbits[orbit_number-1]["orbitType"] = ingress_merged_orbits[i]["orbitType"]
    i += 1


obs_type_name = "ir_grazing_occultations"
i = 0  # line number

for split in cop_file_lines[obs_type_name]:
    cop = [int(split[2]), int(split[3])]

    if mtpNumber < 4:
        # assume SO channel for early occultations
        channel = 0
    else:
        # channel can be SO or LNO for later occs
        channel = int(split[4])

    # get correct orbit number from orbitList
    orbit_number = grazing_orbits[i]["orbitNumber"]
    cop_orbits[orbit_number-1][obs_type_name] = {"channel": channel, "cop": cop}
    cop_orbits[orbit_number-1]["orbitType"] = grazing_orbits[i]["orbitType"]
    i += 1


# deduce orbit type for the remaining nadir LNO on/off orbits, add to cop orbit list
for cop_orbit in cop_orbits:
    if "orbitType" in cop_orbit.keys():
        continue

    if "ir_dayside_nadir" in cop_orbit.keys():
        # check, sometimes the final orbits aren't correct if the cop row files stop before the end of the MTP

        if cop_orbit["ir_dayside_nadir"]["cop"][0] > -1:
            cop_orbit["orbitType"] = 3
        else:
            cop_orbit["orbitType"] = 4
            # remove dayside if cop row = -1
            del cop_orbit["ir_dayside_nadir"]
    else:
        cop_orbit["orbitType"] = 4


# make dictionary connecting obs names to subdomain cop rows numbers
# NADIR
centreDetectorLines = {
    0: mtpConstants["soCentreDetectorLine"],
    1: LNO_CENTRE_DETECTOR_LINE  # for lno occultations only
}
copTableCombinationDict = {
    0: makeCopTableDict(0, copTableDict),
    1: makeCopTableDict(1, copTableDict)
}

nadir_cop_obs = {}
obs_names = list(nadirObservationDict.keys())
for obs_name in obs_names:
    try:
        outputDict, diffractionOrders, integrationTime, rhythm, windowHeight, channelCode = getCopRows(
            obs_name, nadirObservationDict, copTableDict, copTableCombinationDict, centreDetectorLines, silent=True)
        subd_cop_row = outputDict["scienceCopRow"]
        nadir_cop_obs[subd_cop_row] = obs_name
    except:
        continue


# OCCULTATION
occ_cop_obs = {}
obs_names = list(occultationObservationDict.keys())
for obs_name in obs_names:
    try:
        outputDict, diffractionOrders, integrationTime, rhythm, windowHeight, channelCode = getCopRows(
            obs_name, occultationObservationDict, copTableDict, copTableCombinationDict, centreDetectorLines, silent=True)
        subd_cop_row = outputDict["scienceCopRow"]
        occ_cop_obs[subd_cop_row] = obs_name
    except:
        pass


# now given the list of orbits and COP rows, work back to find the correct observation name
for cop_orbit in cop_orbits:

    for obs_type_name in obs_type_names:
        if obs_type_name in cop_orbit.keys():
            obs_cop_info = cop_orbit[obs_type_name]
            channel = obs_cop_info["channel"]
            subd_rows = obs_cop_info["cop"]

            if "nadir" in obs_type_name:
                cop_obs = nadir_cop_obs
            else:
                cop_obs = occ_cop_obs

            obs_name = []
            for subd_row in subd_rows:
                if subd_row > -1:
                    obs_name.append(cop_obs[subd_row])
                else:
                    obs_name.append("")
            cop_orbit[obs_type_name]["name"] = obs_name


# make a copy
orbitList2 = orbitList[:]


orbitPlanName = "completeOrbitPlan"

# now merge the cop_orbit list with the orbitList
for i, orbit in enumerate(orbitList2):
    orbit[orbitPlanName] = {}
    orbitPlan = orbit[orbitPlanName]
    orbitPlan["orbitType"] = cop_orbits[i]["orbitType"]

    if "ir_egress_occultations" in cop_orbits[i].keys():
        orbitPlan["irEgressLow"] = cop_orbits[i]["ir_egress_occultations"]["name"][0]
        orbitPlan["irEgressHigh"] = cop_orbits[i]["ir_egress_occultations"]["name"][1]
        orbitPlan["uvisEgress"] = "uvisEgress"
    else:
        orbitPlan["irEgressLow"] = ""
        orbitPlan["irEgressHigh"] = ""
        orbitPlan["uvisEgress"] = ""

    if "ir_ingress_occultations" in cop_orbits[i].keys():
        orbitPlan["irIngressHigh"] = cop_orbits[i]["ir_ingress_occultations"]["name"][0]  # TODO: check order
        orbitPlan["irIngressLow"] = cop_orbits[i]["ir_ingress_occultations"]["name"][1]
        orbitPlan["uvisIngress"] = "uvisIngress"
    elif "ir_grazing_occultations" in cop_orbits[i].keys():
        orbitPlan["irIngressHigh"] = cop_orbits[i]["ir_grazing_occultations"]["name"][0]  # TODO: check order
        orbitPlan["irIngressLow"] = cop_orbits[i]["ir_grazing_occultations"]["name"][1]
        orbitPlan["uvisIngress"] = "uvisIngress"
    else:
        orbitPlan["irIngressHigh"] = ""
        orbitPlan["irIngressLow"] = ""
        orbitPlan["uvisIngress"] = ""

    if "ir_nightside_nadir" in cop_orbits[i].keys():
        orbitPlan["irNightside"] = cop_orbits[i]["ir_nightside_nadir"]["name"][0]
        orbitPlan["uvisNightside"] = "uvisNightside"
    else:
        orbitPlan["irNightside"] = ""
        orbitPlan["uvisNightside"] = ""

    if "ir_dayside_nadir" in cop_orbits[i].keys():
        orbitPlan["irDayside"] = cop_orbits[i]["ir_dayside_nadir"]["name"][0]
        orbitPlan["uvisDayside"] = "uvisDayside"
    else:
        orbitPlan["irDayside"] = ""
        orbitPlan["uvisDayside"] = "uvisDayside"

    orbitPlan["comment"] = "COMMENT"


version = "plan"
writeOrbitPlanXlsx(orbitList2, mtpConstants, paths, version, place_in_base_dir=True)
