# -*- coding: utf-8 -*-
"""
Created on Mon Apr 27 12:36:42 2020

@author: iant
"""

import os
import json
import sys

from nomad_obs.config.constants import SO_CHANNEL_CODE, LNO_CHANNEL_CODE, OFF_CHANNEL_CODE, PRECOOLING_COP_ROW, OFF_COP_ROW
from nomad_obs.config.constants import LIMB_ORBIT_TYPES, OBJECTIVE_ORDERS
from nomad_obs.acs_so_joint_occultations import SOC_JOINT_OBSERVATION_NAMES, SOC_JOINT_OBSERVATION_TYPES

# from nomad_obs.observation_names import nadirObservationDict


def writeOutputTxt(filepath, lines_to_write):
    """function to write output to a log file"""
    with open(filepath+".txt", 'w') as txtFile:
        for line_to_write in lines_to_write:
            txtFile.write(line_to_write+'\n')


def writeOutputCsv(filepath, lines_to_write):
    """function to write output to a log file"""
    with open(filepath+".csv", 'w') as txtFile:
        for line_to_write in lines_to_write:
            txtFile.write(line_to_write+'\n')


def dump_json(orbit_list):

    print("Error: Dumping orbit list to json")

    orbit_dict = {(i+1): v for i, v in enumerate(orbit_list)}

    json_string = json.dumps(orbit_dict, indent=4)
    with open('orbit_list.json', 'w') as f:
        f.write(json_string)

    sys.exit()


def writeIrCopRowsTxt(orbit_list, mtpConstants, paths):
    """write cop rows to output files. remember: only the allowed ingresses and egresses allocated to NOMAD are written to file.
                  for nadir, every orbit must be written to file, with -1s written in orbits without observations"""
    mtpNumber = mtpConstants["mtpNumber"]

    outputHeader = "TC20 FIXED,TC20 PRECOOLING,TC20 SCI1,TC20 SCI2,LNO_OBSERVING (1=YES;0=NO),OBSERVATION NUMBER,OBSERVATION TYPE,APPROX TC START TIME,COMMENTS"
    opsOutputDict = {"ir_dayside_nadir": [outputHeader],
                     "ir_egress_occultations": [outputHeader], "ir_grazing_occultations": [outputHeader],
                     "ir_ingress_occultations": [outputHeader], "ir_nightside_nadir": [outputHeader]}
    # which file to write cop rows to
    opsOutputNames = {"dayside": "ir_dayside_nadir",
                      "dayside2": "ir_dayside_nadir", "dayside3": "ir_dayside_nadir",
                      "egress": "ir_egress_occultations", "grazing": "ir_grazing_occultations",
                      "ingress": "ir_ingress_occultations", "merged": "ir_ingress_occultations",
                      "nightside": "ir_nightside_nadir"}

    for orbit in orbit_list:
        finalOrbitPlan = orbit["finalOrbitPlan"]  # final version with cop rows and measurements specified
        irMeasuredObsTypes = orbit["irMeasuredObsTypes"][:]
        uvisMeasuredObsTypes = orbit["uvisMeasuredObsTypes"][:]

        # which variable contains cop row info
        lnoObsTypeNames = {"dayside": "irDayside", "nightside": "irNightside"}  # matching ir daysides have been made for when UVIS has 3 x TCs per orbit
        for measuredObsType in lnoObsTypeNames.keys():  # loop through potential IR nadir types
            obsType = lnoObsTypeNames[measuredObsType]
            if measuredObsType in irMeasuredObsTypes:  # if dayside or nightside is found, write COP rows. LNO cannot run multiple TCs
                #                print(orbit["orbitNumber"])
                copRow1 = finalOrbitPlan[obsType+"CopRows"]["scienceCopRow"]
                copRow2 = copRow1  # lno nadir has only 1 science
                precoolingRow = PRECOOLING_COP_ROW
                fixedRow = finalOrbitPlan[obsType+"CopRows"]["fixedCopRow"]
                channelCode = finalOrbitPlan[obsType+"ChannelCode"]
                obsComment = "LNO ON"
                # special case for limb
                if "limb" in finalOrbitPlan["irDayside"].lower():
                    obsTypeOut = "limb"
                else:
                    obsTypeOut = measuredObsType

                outputLineToWrite = "%i,%i,%i,%i,%i,%i,%s,%s,%s" % (fixedRow, precoolingRow, copRow1, copRow2,
                                                                    channelCode, orbit["orbitNumber"], obsTypeOut,
                                                                    orbit[measuredObsType]["utcStart"], obsComment)
                opsOutputDict[opsOutputNames[measuredObsType]].append(outputLineToWrite)

        # special bit - we need to write a line of -1s for each orbit when LNO is not operating, and 3xlines if UVIS in 3xTCs mode
        uvisObsTypeNames = {"dayside": "uvisDayside", "dayside2": "uvisDayside2", "dayside3": "uvisDayside3",
                            "nightside": "uvisNightside"}  # matching ir daysides have been made for when UVIS has 3 x TCs per orbit
        for measuredObsType in uvisObsTypeNames.keys():  # loop through potential UVIS nadir types
            obsType = uvisObsTypeNames[measuredObsType]
            # if dayside, dayside2 or dayside3, or nightside is found in uvis list, but not in LNO list, write a line to corresponding LNO COP row file anyway
            if measuredObsType in uvisMeasuredObsTypes and measuredObsType not in irMeasuredObsTypes:
                copRow1 = OFF_COP_ROW
                copRow2 = OFF_COP_ROW
                precoolingRow = OFF_COP_ROW
                fixedRow = OFF_COP_ROW
                channelCode = OFF_COP_ROW
                obsComment = "LNO OFF"
                if "limb" in finalOrbitPlan["irDayside"].lower():
                    obsTypeOut = "limb"
                else:
                    obsTypeOut = measuredObsType

                if measuredObsType in ["dayside2", "dayside3"]:  # UVIS 3x TC20s not implemented. Using timings from dayside instead
                    measuredObsTypeOut = "dayside"
                else:
                    measuredObsTypeOut = measuredObsType  # otherwise just use the normal dayside/nightside

                outputLineToWrite = "%i,%i,%i,%i,%i,%i,%s,%s,%s" % (
                    fixedRow, precoolingRow, copRow1, copRow2, channelCode, orbit["orbitNumber"], obsTypeOut, orbit[measuredObsTypeOut]["utcStart"], obsComment)
                opsOutputDict[opsOutputNames[measuredObsType]].append(outputLineToWrite)

        # if both LNO and UVIS off, write a single line anyway (only for dayside)
        measuredObsType = "dayside"
        if measuredObsType not in irMeasuredObsTypes and measuredObsType not in uvisMeasuredObsTypes:
            copRow1 = OFF_COP_ROW
            copRow2 = OFF_COP_ROW
            precoolingRow = OFF_COP_ROW
            fixedRow = OFF_COP_ROW
            channelCode = OFF_COP_ROW
            obsComment = "ALL OFF"
            if "limb" in finalOrbitPlan["irDayside"].lower():
                obsTypeOut = "Dayside Limb"
            else:
                obsTypeOut = measuredObsType

            outputLineToWrite = "%i,%i,%i,%i,%i,%i,%s,%s,%s" % (fixedRow, precoolingRow, copRow1, copRow2,
                                                                channelCode, orbit["orbitNumber"], obsTypeOut, orbit[measuredObsType]["utcStart"], obsComment)
            opsOutputDict[opsOutputNames[measuredObsType]].append(outputLineToWrite)

        # find which variable name contains cop row info
        # remember order is reversed for egress
        obsTypeNames = {"ingress": ["irIngressHigh", "irIngressLow"], "merged": ["irIngressHigh", "irIngressLow"],
                        "grazing": ["irIngressHigh", "irIngressLow"], "egress": ["irEgressLow", "irEgressHigh"]}
        for measuredObsType in obsTypeNames.keys():
            obsType1, obsType2 = obsTypeNames[measuredObsType]
            if measuredObsType in irMeasuredObsTypes:
                copRow1 = finalOrbitPlan[obsType1+"CopRows"]["scienceCopRow"]
                copRow2 = finalOrbitPlan[obsType2+"CopRows"]["scienceCopRow"]
                precoolingRow = PRECOOLING_COP_ROW
                fixedRow = finalOrbitPlan[obsType1+"CopRows"]["fixedCopRow"]
                channelCode = finalOrbitPlan[obsType1+"ChannelCode"]
                if channelCode == SO_CHANNEL_CODE:
                    obsComment = "SO ON"
                elif channelCode == LNO_CHANNEL_CODE:
                    obsComment = "LNO ON"
                elif channelCode == OFF_CHANNEL_CODE:
                    obsComment = "IR OFF"
                    precoolingRow = OFF_COP_ROW  # set precooling to -1
                obsTypeOut = measuredObsType

                outputLineToWrite = "%i,%i,%i,%i,%i,%i,%s,%s,%s" % (fixedRow, precoolingRow, copRow1, copRow2,
                                                                    channelCode, orbit["orbitNumber"], obsTypeOut,
                                                                    orbit[measuredObsType]["utcStart"], obsComment)
                opsOutputDict[opsOutputNames[measuredObsType]].append(outputLineToWrite)

    for opsOutputName in opsOutputDict.keys():
        writeOutputTxt(os.path.join(paths["COP_ROW_PATH"], "mtp%03d_%s" % (mtpNumber, opsOutputName)), opsOutputDict[opsOutputName])


def writeUvisCopRowsTxt(orbit_list, mtpConstants, paths):
    """write cop rows to output files. remember: only the allowed ingresses and egresses allocated to NOMAD are written to file.
                  for nadir, every orbit must be written to file, with -1s written in orbits without observations"""
    mtpNumber = mtpConstants["mtpNumber"]

    outputHeader = "TC20 UVIS COP ROW,CHANNEL,OBSERVATION NUMBER,OBSERVATION TYPE,APPROX TC START TIME,COMMENTS"
    opsOutputDict = {"uvis_dayside_nadir": [outputHeader],
                     "uvis_egress_occultations": [outputHeader], "uvis_grazing_occultations": [outputHeader],
                     "uvis_ingress_occultations": [outputHeader], "uvis_nightside_nadir": [outputHeader]}
    # which file to write cop rows to
    opsOutputNames = {"dayside": "uvis_dayside_nadir",
                      "dayside2": "uvis_dayside_nadir2", "dayside3": "uvis_dayside_nadir3",
                      "egress": "uvis_egress_occultations", "grazing": "uvis_grazing_occultations",
                      "ingress": "uvis_ingress_occultations", "merged": "uvis_ingress_occultations",
                      "nightside": "uvis_nightside_nadir"}

    for orbit in orbit_list:
        finalOrbitPlan = orbit["finalOrbitPlan"]  # final version with cop rows and measurements specified
        # irMeasuredObsTypes = orbit["irMeasuredObsTypes"][:]
        uvisMeasuredObsTypes = orbit["uvisMeasuredObsTypes"][:]

        # UVIS nadir
        # at least one line per dayside/day limb orbit, 3 lines if 3x TC20s on the same dayside
        # ingress/egress and nightsides - one line per planned observation

        uvisObsTypeNames = {"dayside": "uvisDayside", "dayside2": "uvisDayside2", "dayside3": "uvisDayside3",
                            "nightside": "uvisNightside"}  # matching ir daysides have been made for when UVIS has 3 x TCs per orbit
        for measuredObsType in uvisObsTypeNames.keys():  # loop through potential UVIS nadir types
            obsType = uvisObsTypeNames[measuredObsType]
            # if dayside, dayside2 or dayside3, or nightside is found in uvis list, write a line to UVIS COP row file
            if measuredObsType in uvisMeasuredObsTypes:
                copRow = finalOrbitPlan[obsType+"CopRows"]["scienceCopRow"]
                channelCode = "UVIS Nadir"
                obsComment = "UVIS ON"
                obsTypeOut = measuredObsType

                if measuredObsType in ["dayside2", "dayside3"]:  # UVIS 3x TC20s not implemented. Using timings from dayside instead
                    measuredObsTypeOut = "dayside"
                else:
                    measuredObsTypeOut = measuredObsType  # otherwise just use the normal dayside/nightside

                outputLineToWrite = "%i,%s,%i,%s,%s,%s" % (
                    copRow, channelCode, orbit["orbitNumber"], obsTypeOut, orbit[measuredObsTypeOut]["utcStart"], obsComment)
                opsOutputDict[opsOutputNames[measuredObsType]].append(outputLineToWrite)

        # if both UVIS off, write a single line anyway (only for dayside)
        measuredObsType = "dayside"
        if measuredObsType not in uvisMeasuredObsTypes:
            copRow = OFF_COP_ROW
            channelCode = OFF_COP_ROW
            obsComment = "UVIS OFF"
            obsTypeOut = measuredObsType

            measuredObsTypeOut = measuredObsType

            outputLineToWrite = "%i,%s,%i,%s,%s,%s" % (
                copRow, channelCode, orbit["orbitNumber"], obsTypeOut, orbit[measuredObsTypeOut]["utcStart"], obsComment)
            opsOutputDict[opsOutputNames[measuredObsType]].append(outputLineToWrite)

        # find which variable name contains cop row info
        obsTypeNames = {"ingress": "uvisIngress", "merged": "uvisIngress",
                        "grazing": "uvisIngress", "egress": "uvisEgress"}
        for measuredObsType in obsTypeNames.keys():
            obsType = obsTypeNames[measuredObsType]
            if measuredObsType in uvisMeasuredObsTypes:
                copRow = finalOrbitPlan[obsType+"CopRows"]["scienceCopRow"]
                channelCode = finalOrbitPlan[obsType+"ChannelCode"]
                obsComment = "UVIS ON"
                obsTypeOut = measuredObsType

                outputLineToWrite = "%i,%s,%i,%s,%s,%s" % (
                    copRow, channelCode, orbit["orbitNumber"], obsTypeOut, orbit[measuredObsTypeOut]["utcStart"], obsComment)
                opsOutputDict[opsOutputNames[measuredObsType]].append(outputLineToWrite)

            # if occultation not measured but assigned to NOMAD
            elif measuredObsType in orbit["allowedObservationTypes"]:
                copRow = OFF_COP_ROW
                channelCode = OFF_COP_ROW
                obsComment = "UVIS OFF"
                obsTypeOut = measuredObsType

                outputLineToWrite = "%i,%s,%i,%s,%s,%s" % (
                    copRow, channelCode, orbit["orbitNumber"], obsTypeOut, orbit[measuredObsTypeOut]["utcStart"], obsComment)
                opsOutputDict[opsOutputNames[measuredObsType]].append(outputLineToWrite)

    for opsOutputName in opsOutputDict.keys():
        writeOutputTxt(os.path.join(paths["COP_ROW_PATH"], "mtp%03d_%s" % (mtpNumber, opsOutputName)), opsOutputDict[opsOutputName])


def writeLnoUvisJointObsNumbers(orbit_list, mtpConstants, paths):
    """write LNO obs numbers for UVIS-LNO joint obs"""
    """irDayside field must contain text and must not be a limb measurement"""
    """note that a check is NOT made to see if this file arlready exists. It should be identical each time it is made and should never be edited by hand"""
    mtpNumber = mtpConstants["mtpNumber"]

    ORBIT_PLAN_NAME = "genericOrbitPlanIn"

    lnoOperatingOrbits = ["THERMAL ORBIT NUMBER WITH LNO NADIR"]
    for orbit in orbit_list:
        if "irDayside" in orbit[ORBIT_PLAN_NAME].keys():
            if orbit[ORBIT_PLAN_NAME]["orbitType"] not in LIMB_ORBIT_TYPES:
                if orbit[ORBIT_PLAN_NAME]["irDayside"] != "":
                    lnoOperatingOrbits.append("%s" % orbit["orbitNumber"])

    writeOutputTxt(os.path.join(paths["ORBIT_PLAN_PATH"], "nomad_mtp%03d_lno_orbits" % mtpNumber), lnoOperatingOrbits)


def writeLnoGroundAssetJointObsInfo(orbit_list, mtpConstants, paths, ground_asset_name):
    """ write NOMAD + SAM-TLS joint obs info - start/end time, incidence angle, COP rows used"""
    mtpNumber = mtpConstants["mtpNumber"]

    ORBIT_PLAN_NAME = "finalOrbitPlan"

    lnoGroundAssetJointObs = [
        "UTC TIME WHEN LNO OBSERVING CLOSE TO %s, INCIDENCE ANGLE, LOCAL SOLAR TIME, LNO DIFFRACTION ORDERS MEASURED" % ground_asset_name.upper()]
    for orbit in orbit_list:
        if "irDayside" in orbit[ORBIT_PLAN_NAME].keys():  # check if dayside
            if orbit[ORBIT_PLAN_NAME]["irDayside"] != "":  # check if LNO observing
                if "daysideRegions" in orbit.keys():  # check if any regions of interest observed
                    for daysideRegion in orbit["daysideRegions"]:
                        if ground_asset_name.upper() in daysideRegion["name"]:  # check if curiosity
                            #                            print(orbit["orbitNumber"])
                            ordersMeasured = orbit[ORBIT_PLAN_NAME]["irDaysideOrders"]
                            orders = "#"+" #".join(str(order) for order in ordersMeasured)
                            utcTimeMeasured = daysideRegion["utc"]
                            incidenceAngleMeasured = daysideRegion["incidenceAngle"]
                            lstMeasured = daysideRegion["lst"]

                            outputText = "%s, %0.1f, %0.1f, %s" % (utcTimeMeasured, incidenceAngleMeasured, lstMeasured, orders)
                            lnoGroundAssetJointObs.append(outputText)
#                            print(outputText)

    writeOutputTxt(os.path.join(paths["ORBIT_PLAN_PATH"], "nomad_mtp%03d_lno_%s_joint_obs" % (mtpNumber, ground_asset_name.lower())), lnoGroundAssetJointObs)


def writeAcsJointObsNumbers(orbit_list, mtpConstants, paths):
    """write ACS joint obs"""
    """note that a check is NOT made to see if this file arlready exists. It should be identical each time it is made and should never be edited by hand"""
    mtpNumber = mtpConstants["mtpNumber"]

    obsTypeNames = {"ingress": "irIngressLow", "merged": "irIngressLow", "grazing": "irIngressLow", "egress": "irEgressLow"}
    outputStrings = []

    joint_obs_counter = 0

    for socObsName, obsNames in SOC_JOINT_OBSERVATION_NAMES.items():  # loop through all joint observation names

        for socObsType in SOC_JOINT_OBSERVATION_TYPES:  # loop through egress, ingress, merged
            outputString = "%s, %s" % (socObsName, socObsType)
            found = False

            for orbit in orbit_list:
                # get allowed occultation types for that orbit from orbit list
                occultationObsTypes = [occultationType for occultationType in orbit["allowedObservationTypes"]
                                       [:] if occultationType in ["ingress", "egress", "merged", "grazing"]]
                for occultationObsType in occultationObsTypes:  # loop through allowed occultations
                    if occultationObsType in orbit.keys():
                        obsTypeName = obsTypeNames[occultationObsType]
                        for obsName in obsNames:
                            if obsName == orbit["finalOrbitPlan"][obsTypeName]:  # if the nomad observation name if found in the orbit list
                                if obsName != "":
                                    eventDescription = orbit[occultationObsType]["occultationEventFileCounts"]
                                    if socObsType in eventDescription:
                                        eventOrbitNumber = eventDescription.split("-")[-1]
                                        outputString += ", %s" % eventOrbitNumber
                                        found = True
                                        joint_obs_counter += 1
            if found:
                outputStrings.append(outputString)

    print("%i joint occultations added to the ACS list" % (joint_obs_counter))
    writeOutputCsv(os.path.join(paths["COP_ROW_PATH"], "joint_occ_mtp%03d" % mtpNumber), outputStrings)


def writeOrbitPlanCsv(orbit_List, mtpConstants, paths):
    """write final orbit type numbers to csv file for ops team"""
    """note that a check is NOT made to see if this file arlready exists. It should be identical each time it is made and should never be edited by hand"""
    mtpNumber = mtpConstants["mtpNumber"]

    ORBIT_PLAN_NAME = "genericOrbitPlanIn"

    orbitTypeNumbers = ["#orbitType"]
    for orbit in orbit_List:
        orbitTypeNumbers.append("%i" % orbit[ORBIT_PLAN_NAME]["orbitType"])

    writeOutputCsv(os.path.join(paths["ORBIT_PLAN_PATH"], "nomad_mtp%03d_plan" % mtpNumber), orbitTypeNumbers)


def writeObjectiveOrbitNumbers(orbit_list, mtpConstants, paths, channel, obsType, objective):
    """write LNO obs numbers for UVIS-LNO joint obs for a specific observation type and objective (e.g. irDayside and H2O)"""
    """note that a check is NOT made to see if this file arlready exists. It should be identical each time it is made and should never be edited by hand"""
    """note that fullscans are not checked"""

    mtpNumber = mtpConstants["mtpNumber"]

    if channel in OBJECTIVE_ORDERS.keys():
        if obsType in OBJECTIVE_ORDERS[channel].keys():
            if objective in OBJECTIVE_ORDERS[channel][obsType].keys():
                orders_to_find = OBJECTIVE_ORDERS[channel][obsType][objective]

            else:
                print("Error: Objective not found in objective order dictionary")
        else:
            print("Error: Obs type not found in objective order dictionary")
    else:
        print("Error: Channel not found in objective order dictionary")

    lnoObjectiveOrbits = ["THERMAL ORBIT NUMBER WITH %s MEASURING %s IN %s, OBSERVATION NAME, DIFFRACTION ORDER MEASURED" %
                          (channel.upper(), objective.upper(), obsType.upper())]

    orbitsFound = []

    for orbit in orbit_list:
        ordersFieldName = "%sOrders" % obsType

        if ordersFieldName in orbit["finalOrbitPlan"].keys():  # final version with cop rows and measurements specified

            orders = orbit["finalOrbitPlan"][ordersFieldName]
            obsName = orbit["finalOrbitPlan"]["irDaysideObservationName"]
            orbitNumber = orbit["orbitNumber"]

            for order in orders:
                if order in orders_to_find:
                    if orbitNumber not in orbitsFound:
                        lnoObjectiveOrbits.append("%s, %s, %s" % (orbitNumber, obsName, order))
                        orbitsFound.append(orbitNumber)

    writeOutputTxt(os.path.join(paths["ORBIT_PLAN_PATH"], "nomad_mtp%03d_%s_%s_%s_orbits" %
                   (mtpNumber, channel.lower(), obsType.lower(), objective.lower())), lnoObjectiveOrbits)
