# -*- coding: utf-8 -*-
"""
Created on Mon Apr 27 12:36:04 2020

@author: iant
"""
import os

from nomad_obs.config.constants import LNO_CENTRE_DETECTOR_LINE, IR_OFF_CODE, UVIS_OFF_CODE, OFF_CHANNEL_CODE
from nomad_obs.cop_rows.cop_table_functions import makeCopTableDict, getObservationDescription, getCopRows

from nomad_obs.other.generic_functions import stop


def addIrCopRows(orbit_list, copTableDict, mtpConstants, occultationObservationDict, nadirObservationDict):
    """find cop rows that match observation names in final plan, add to orbit list"""
    centreDetectorLines = {
        0: mtpConstants["soCentreDetectorLine"],
        1: LNO_CENTRE_DETECTOR_LINE  # for lno occultations only
    }

    copTableCombinationDict = {
        0: makeCopTableDict(0, copTableDict),
        1: makeCopTableDict(1, copTableDict)
    }

    for orbit in orbit_list:
        #        print(orbit["orbitNumber"])
        finalOrbitPlan = orbit["finalOrbitPlan"]
        irMeasuredObsTypes = orbit["irMeasuredObsTypes"]
        uvisMeasuredObsTypes = orbit["uvisMeasuredObsTypes"]

        # now check each allowed type and add cop rows
        if "ingress" in irMeasuredObsTypes or "merged" in irMeasuredObsTypes or "grazing" in irMeasuredObsTypes:
            for obsType in ["irIngressHigh", "irIngressLow"]:

                observationName = finalOrbitPlan[obsType]
                observationDict = occultationObservationDict

                if observationName == IR_OFF_CODE:
                    finalOrbitPlan[obsType+"ObservationName"] = "-"
                    finalOrbitPlan[obsType+"ChannelCode"] = OFF_CHANNEL_CODE
                    finalOrbitPlan[obsType+"CopRows"] = {"scienceCopRow": -1, "fixedCopRow": -1, "copRowDescription": ""}

                else:
                    outputDict, diffractionOrders, integrationTime, rhythm, windowHeight, channelCode = getCopRows(
                        observationName, observationDict, copTableDict, copTableCombinationDict, centreDetectorLines, silent=True)
                    if len(outputDict) == 0:  # if error
                        print("Error in orbit %i obs type %s" % (orbit["orbitNumber"], obsType))
                        stop()

                    finalOrbitPlan[obsType+"ObservationName"] = observationName
                    finalOrbitPlan[obsType+"Orders"] = diffractionOrders
                    finalOrbitPlan[obsType+"IntegrationTime"] = integrationTime
                    finalOrbitPlan[obsType+"Rhythm"] = rhythm
                    finalOrbitPlan[obsType+"DetectorRows"] = windowHeight
                    finalOrbitPlan[obsType+"ChannelCode"] = channelCode
                    finalOrbitPlan[obsType+"CopRows"] = outputDict

        if "egress" in irMeasuredObsTypes:
            for obsType in ["irEgressHigh", "irEgressLow"]:

                observationName = finalOrbitPlan[obsType]
                observationDict = occultationObservationDict

                if observationName == IR_OFF_CODE:
                    finalOrbitPlan[obsType+"ObservationName"] = "-"
                    finalOrbitPlan[obsType+"ChannelCode"] = OFF_CHANNEL_CODE
                    finalOrbitPlan[obsType+"CopRows"] = {"scienceCopRow": -1, "fixedCopRow": -1, "copRowDescription": ""}

                else:
                    outputDict, diffractionOrders, integrationTime, rhythm, windowHeight, channelCode = getCopRows(
                        observationName, observationDict, copTableDict, copTableCombinationDict, centreDetectorLines, silent=True)
                    if len(outputDict) == 0:  # if error
                        print("Error in orbit %i obs type %s" % (orbit["orbitNumber"], obsType))
                        stop()

                    finalOrbitPlan[obsType+"ObservationName"] = observationName
                    finalOrbitPlan[obsType+"Orders"] = diffractionOrders
                    finalOrbitPlan[obsType+"IntegrationTime"] = integrationTime
                    finalOrbitPlan[obsType+"Rhythm"] = rhythm
                    finalOrbitPlan[obsType+"DetectorRows"] = windowHeight
                    finalOrbitPlan[obsType+"ChannelCode"] = channelCode
                    finalOrbitPlan[obsType+"CopRows"] = outputDict

        if "dayside" in irMeasuredObsTypes:
            obsType = "irDayside"

            observationName = finalOrbitPlan[obsType]
            observationDict = nadirObservationDict

            outputDict, diffractionOrders, integrationTime, rhythm, windowHeight, channelCode = getCopRows(
                observationName, observationDict, copTableDict, copTableCombinationDict, centreDetectorLines, silent=True)
            if len(outputDict) == 0:  # if error
                print("Error in orbit %i obs type %s" % (orbit["orbitNumber"], obsType))
                stop()

            finalOrbitPlan[obsType+"ObservationName"] = observationName
            finalOrbitPlan[obsType+"Orders"] = diffractionOrders
            finalOrbitPlan[obsType+"IntegrationTime"] = integrationTime
            finalOrbitPlan[obsType+"Rhythm"] = rhythm
            finalOrbitPlan[obsType+"DetectorRows"] = windowHeight
            finalOrbitPlan[obsType+"ChannelCode"] = channelCode
            finalOrbitPlan[obsType+"CopRows"] = outputDict

        else:  # if uvis operating, still write COP rows for nadirs
            if "dayside" in uvisMeasuredObsTypes:  # if uvis operating, still write COP rows for nadirs
                obsType = "irDayside"
                finalOrbitPlan[obsType+"CopRows"] = {"scienceCopRow": -1, "fixedCopRow": -1, "copRowDescription": ""}
            if "dayside2" in uvisMeasuredObsTypes:  # if uvis operating, still write COP rows for nadirs
                obsType = "irDayside2"
                finalOrbitPlan[obsType+"CopRows"] = {"scienceCopRow": -1, "fixedCopRow": -1, "copRowDescription": ""}
            if "dayside3" in uvisMeasuredObsTypes:  # if uvis operating, still write COP rows for nadirs
                obsType = "irDayside3"
                finalOrbitPlan[obsType+"CopRows"] = {"scienceCopRow": -1, "fixedCopRow": -1, "copRowDescription": ""}

        # if orbit type not 12 (NOMAD OFF) then there should always be nadir COP rows specified
        if orbit["orbitType"] != 12 and "dayside" not in uvisMeasuredObsTypes:
            obsType = "irDayside"
            finalOrbitPlan[obsType+"CopRows"] = {"scienceCopRow": -1, "fixedCopRow": -1, "copRowDescription": ""}

        if "nightside" in irMeasuredObsTypes:
            obsType = "irNightside"

            observationName = finalOrbitPlan[obsType]
            observationDict = nadirObservationDict

            outputDict, diffractionOrders, integrationTime, rhythm, windowHeight, channelCode = getCopRows(
                observationName, observationDict, copTableDict, copTableCombinationDict, centreDetectorLines, silent=True)
            if len(outputDict) == 0:  # if error
                print("Error in orbit %i obs type %s" % (orbit["orbitNumber"], obsType))
                stop()

            finalOrbitPlan[obsType+"ObservationName"] = observationName
            finalOrbitPlan[obsType+"Orders"] = diffractionOrders
            finalOrbitPlan[obsType+"IntegrationTime"] = integrationTime
            finalOrbitPlan[obsType+"Rhythm"] = rhythm
            finalOrbitPlan[obsType+"DetectorRows"] = windowHeight
            finalOrbitPlan[obsType+"ChannelCode"] = channelCode
            finalOrbitPlan[obsType+"CopRows"] = outputDict
        else:  # if uvis operating, still write COP rows for nadirs
            if "nightside" in uvisMeasuredObsTypes:  # if uvis operating, still write COP rows for nadirs
                obsType = "uvisNightside"
                finalOrbitPlan[obsType+"CopRows"] = {"scienceCopRow": -1, "copRowDescription": ""}

        # for UVIS, add -1s to be replaced with real values later
        if "ingress" in uvisMeasuredObsTypes or "merged" in uvisMeasuredObsTypes or "grazing" in uvisMeasuredObsTypes:
            obsType = "uvisIngress"
            observationName = finalOrbitPlan[obsType]
            finalOrbitPlan[obsType+"ObservationName"] = observationName
            finalOrbitPlan[obsType+"CopRows"] = {"scienceCopRow": -1, "copRowDescription": ""}

        if "egress" in uvisMeasuredObsTypes:
            obsType = "uvisEgress"
            observationName = finalOrbitPlan[obsType]
            finalOrbitPlan[obsType+"ObservationName"] = observationName
            finalOrbitPlan[obsType+"CopRows"] = {"scienceCopRow": -1, "copRowDescription": ""}

        if "dayside" in uvisMeasuredObsTypes:
            obsType = "uvisDayside"
            observationName = finalOrbitPlan[obsType]
            finalOrbitPlan[obsType+"ObservationName"] = observationName
            finalOrbitPlan[obsType+"CopRows"] = {"scienceCopRow": -1, "copRowDescription": ""}

        if "dayside2" in uvisMeasuredObsTypes:
            obsType = "uvisDayside2"
            observationName = finalOrbitPlan["uvisDayside"]  # use same uvis dayside obs name for 3 x TC20s
            finalOrbitPlan[obsType+"ObservationName"] = observationName
            finalOrbitPlan[obsType+"CopRows"] = {"scienceCopRow": -1, "copRowDescription": ""}

        if "dayside3" in uvisMeasuredObsTypes:
            obsType = "uvisDayside3"
            observationName = finalOrbitPlan["uvisDayside"]  # use same uvis dayside obs name for 3 x TC20s
            finalOrbitPlan[obsType+"ObservationName"] = observationName
            finalOrbitPlan[obsType+"CopRows"] = {"scienceCopRow": -1, "copRowDescription": ""}

        if "nightside" in uvisMeasuredObsTypes:
            obsType = "uvisNightside"
            observationName = finalOrbitPlan["uvisDayside"]  # use same uvis dayside obs name for 3 x TC20s
            finalOrbitPlan[obsType+"ObservationName"] = observationName
            finalOrbitPlan[obsType+"CopRows"] = {"scienceCopRow": -1, "copRowDescription": ""}

        # if orbit type not 12 (NOMAD OFF) then there should always be nadir COP rows specified
        if orbit["orbitType"] != 12 and "dayside" not in uvisMeasuredObsTypes:
            obsType = "uvisDayside"
            finalOrbitPlan[obsType+"CopRows"] = {"scienceCopRow": -1, "copRowDescription": ""}

    return orbit_list


def addUvisCopRows(orbit_list, copTableDict, mtpConstants, occultationObservationDict, nadirObservationDict, paths, from_file=True):

    if not from_file:
        """find cop rows that match observation names in final plan, add to orbit list"""
        centreDetectorLines = {}

        # read COP tables from csvs
        copTableCombinationDict = {
            2: makeCopTableDict(2, copTableDict),
        }

        for orbit in orbit_list:
            #        print(orbit["orbitNumber"])
            finalOrbitPlan = orbit["finalOrbitPlan"]
            uvisMeasuredObsTypes = orbit["uvisMeasuredObsTypes"]

            # now check each allowed type and add cop rows
            if "ingress" in uvisMeasuredObsTypes or "merged" in uvisMeasuredObsTypes or "grazing" in uvisMeasuredObsTypes:
                obsType = "uvisIngress"

                observationName = finalOrbitPlan[obsType]
                observationDict = occultationObservationDict

                if observationName == UVIS_OFF_CODE:
                    finalOrbitPlan[obsType+"ObservationName"] = "-"
                    finalOrbitPlan[obsType+"ChannelCode"] = OFF_CHANNEL_CODE
                    finalOrbitPlan[obsType+"CopRows"] = {"scienceCopRow": -1, "copRowDescription": ""}

                else:
                    outputDict, diffractionOrders, integrationTime, rhythm, windowHeight, channelCode = getCopRows(
                        observationName, observationDict, copTableDict, copTableCombinationDict, centreDetectorLines, silent=True)
                    if len(outputDict) == 0:  # if error
                        print("Error in orbit %i obs type %s" % (orbit["orbitNumber"], obsType))
                        stop()

                    finalOrbitPlan[obsType+"ObservationName"] = observationName
                    finalOrbitPlan[obsType+"Orders"] = diffractionOrders
                    finalOrbitPlan[obsType+"IntegrationTime"] = integrationTime
                    finalOrbitPlan[obsType+"Rhythm"] = rhythm
                    finalOrbitPlan[obsType+"DetectorRows"] = windowHeight
                    finalOrbitPlan[obsType+"ChannelCode"] = channelCode
                    finalOrbitPlan[obsType+"CopRows"] = outputDict

            if "egress" in uvisMeasuredObsTypes:
                obsType = "uvisEgress"

                observationName = finalOrbitPlan[obsType]
                observationDict = occultationObservationDict

                if observationName == UVIS_OFF_CODE:
                    finalOrbitPlan[obsType+"ObservationName"] = "-"
                    finalOrbitPlan[obsType+"ChannelCode"] = OFF_CHANNEL_CODE
                    finalOrbitPlan[obsType+"CopRows"] = {"scienceCopRow": -1, "copRowDescription": ""}

                else:
                    outputDict, diffractionOrders, integrationTime, rhythm, windowHeight, channelCode = getCopRows(
                        observationName, observationDict, copTableDict, copTableCombinationDict, centreDetectorLines, silent=True)
                    if len(outputDict) == 0:  # if error
                        print("Error in orbit %i obs type %s" % (orbit["orbitNumber"], obsType))
                        stop()

                    finalOrbitPlan[obsType+"ObservationName"] = observationName
                    finalOrbitPlan[obsType+"Orders"] = diffractionOrders
                    finalOrbitPlan[obsType+"IntegrationTime"] = integrationTime
                    finalOrbitPlan[obsType+"Rhythm"] = rhythm
                    finalOrbitPlan[obsType+"DetectorRows"] = windowHeight
                    finalOrbitPlan[obsType+"ChannelCode"] = channelCode
                    finalOrbitPlan[obsType+"CopRows"] = outputDict

            if "dayside" in uvisMeasuredObsTypes:
                obsType = "uvisDayside"

                observationName = finalOrbitPlan[obsType]
                observationDict = nadirObservationDict

                outputDict, diffractionOrders, integrationTime, rhythm, windowHeight, channelCode = getCopRows(
                    observationName, observationDict, copTableDict, copTableCombinationDict, centreDetectorLines, silent=True)
                if len(outputDict) == 0:  # if error
                    print("Error in orbit %i obs type %s" % (orbit["orbitNumber"], obsType))
                    stop()

                finalOrbitPlan[obsType+"ObservationName"] = observationName
                finalOrbitPlan[obsType+"Orders"] = diffractionOrders
                finalOrbitPlan[obsType+"IntegrationTime"] = integrationTime
                finalOrbitPlan[obsType+"Rhythm"] = rhythm
                finalOrbitPlan[obsType+"DetectorRows"] = windowHeight
                finalOrbitPlan[obsType+"ChannelCode"] = channelCode
                finalOrbitPlan[obsType+"CopRows"] = outputDict

            if "nightside" in uvisMeasuredObsTypes:
                obsType = "uvisNightside"

                observationName = finalOrbitPlan[obsType]
                observationDict = nadirObservationDict

                outputDict, diffractionOrders, integrationTime, rhythm, windowHeight, channelCode = getCopRows(
                    observationName, observationDict, copTableDict, copTableCombinationDict, centreDetectorLines, silent=True)
                if len(outputDict) == 0:  # if error
                    print("Error in orbit %i obs type %s" % (orbit["orbitNumber"], obsType))
                    stop()

                finalOrbitPlan[obsType+"ObservationName"] = observationName
                finalOrbitPlan[obsType+"Orders"] = diffractionOrders
                finalOrbitPlan[obsType+"IntegrationTime"] = integrationTime
                finalOrbitPlan[obsType+"Rhythm"] = rhythm
                finalOrbitPlan[obsType+"DetectorRows"] = windowHeight
                finalOrbitPlan[obsType+"ChannelCode"] = channelCode
                finalOrbitPlan[obsType+"CopRows"] = outputDict

    else:
        """get UVIS COP rows from file (if they already exist)"""
        mtpNumber = mtpConstants["mtpNumber"]

        uvisFilesAvailable = os.path.isfile(os.path.join(paths["COP_ROW_PATH"], "mtp%03d_uvis_dayside_nadir.txt" % mtpNumber))
        # grazing file only present if there are grazing occultations
        uvisGrazingAvailable = os.path.isfile(os.path.join(paths["COP_ROW_PATH"], "mtp%03d_uvis_grazing_occultations.txt" % mtpNumber))

        if uvisFilesAvailable:
            if uvisGrazingAvailable:
                uvisInputDict = {"uvis_dayside_nadir": [],
                                 "uvis_egress_occultations": [], "uvis_grazing_occultations": [],
                                 "uvis_ingress_occultations": [], "uvis_nightside_nadir": []}
            else:
                uvisInputDict = {"uvis_dayside_nadir": [],
                                 "uvis_egress_occultations": [],
                                 "uvis_ingress_occultations": [], "uvis_nightside_nadir": []}
            for uvisInputName in uvisInputDict.keys():
                with open(os.path.join(paths["COP_ROW_PATH"], "mtp%03d_%s.txt" % (mtpNumber, uvisInputName))) as f:
                    for index, line in enumerate(f):
                        content = line.strip('\n')
                        if index > 0:  # if first line, skip

                            # if more info in file, just take first number
                            if "," in content:
                                content = content.split(",")[0]

                            uvisInputDict[uvisInputName].append(int(content))

            if not uvisGrazingAvailable:  # create empty grazing dictionary
                uvisInputDict["uvis_grazing_occultations"] = []

            daysideCounter = -1
            egressCounter = -1
            grazingCounter = -1
            ingressCounter = -1
            nightsideCounter = -1

            for orbit in orbit_list:
                finalOrbitPlan = orbit["finalOrbitPlan"]
                print(orbit["orbitNumber"], end=", ")
                if "ingress" in orbit["allowedObservationTypes"]:
                    ingressCounter += 1
                    if ingressCounter == len(uvisInputDict["uvis_ingress_occultations"]):
                        print("Error: insufficient ingress COP rows, index %i" % ingressCounter)
                    copRow = uvisInputDict["uvis_ingress_occultations"][ingressCounter]

                    # if uvis ingresses removed from orbit plans, make an entry for them
                    if "uvisIngressCopRows" not in finalOrbitPlan.keys():
                        finalOrbitPlan["uvisIngressCopRows"] = {"scienceCopRow": -1, "copRowDescription": ""}

                    finalOrbitPlan["uvisIngressCopRows"]["scienceCopRow"] = copRow
                    finalOrbitPlan["uvisIngressCopRows"]["copRowDescription"] = getObservationDescription("uvis", copTableDict, 0, copRow, silent=True)

                if "merged" in orbit["allowedObservationTypes"]:  # merged is same as ingress
                    ingressCounter += 1
                    if ingressCounter == len(uvisInputDict["uvis_ingress_occultations"]):
                        print("Error: insufficient merged COP rows, index %i" % ingressCounter)
                    copRow = uvisInputDict["uvis_ingress_occultations"][ingressCounter]

                    # if uvis ingresses removed from orbit plans, make an entry for them
                    if "uvisIngressCopRows" not in finalOrbitPlan.keys():
                        finalOrbitPlan["uvisIngressCopRows"] = {"scienceCopRow": -1, "copRowDescription": ""}

                    finalOrbitPlan["uvisIngressCopRows"]["scienceCopRow"] = copRow
                    finalOrbitPlan["uvisIngressCopRows"]["copRowDescription"] = getObservationDescription("uvis", copTableDict, 0, copRow, silent=True)

                if "grazing" in orbit["allowedObservationTypes"]:  # grazing is taken from a different file but added to ingress orbit plan
                    grazingCounter += 1
                    if grazingCounter == len(uvisInputDict["uvis_grazing_occultations"]):
                        print("Error: insufficient grazing COP rows, index %i" % grazingCounter)
                    copRow = uvisInputDict["uvis_grazing_occultations"][grazingCounter]

                    # if uvis ingresses removed from orbit plans, make an entry for them
                    if "uvisIngressCopRows" not in finalOrbitPlan.keys():
                        finalOrbitPlan["uvisIngressCopRows"] = {"scienceCopRow": -1, "copRowDescription": ""}

                    finalOrbitPlan["uvisIngressCopRows"]["scienceCopRow"] = copRow
                    finalOrbitPlan["uvisIngressCopRows"]["copRowDescription"] = getObservationDescription("uvis", copTableDict, 0, copRow, silent=True)

                if "egress" in orbit["allowedObservationTypes"]:
                    egressCounter += 1
                    if egressCounter == len(uvisInputDict["uvis_egress_occultations"]):
                        print("Error: insufficient egress COP rows, index %i" % egressCounter)
                    copRow = uvisInputDict["uvis_egress_occultations"][egressCounter]

                    # if uvis ingresses removed from orbit plans, make an entry for them
                    if "uvisEgressCopRows" not in finalOrbitPlan.keys():
                        finalOrbitPlan["uvisEgressCopRows"] = {"scienceCopRow": -1, "copRowDescription": ""}

                    finalOrbitPlan["uvisEgressCopRows"]["scienceCopRow"] = copRow
                    finalOrbitPlan["uvisEgressCopRows"]["copRowDescription"] = getObservationDescription("uvis", copTableDict, 0, copRow, silent=True)

                if "dayside" in orbit["allowedObservationTypes"]:
                    daysideCounter += 1
                    copRow = uvisInputDict["uvis_dayside_nadir"][daysideCounter]
                    finalOrbitPlan["uvisDaysideCopRows"]["scienceCopRow"] = copRow
                    copRowDescription = getObservationDescription("uvis", copTableDict, 0, copRow, silent=True)
                    finalOrbitPlan["uvisDaysideCopRows"]["copRowDescription"] = copRowDescription

                    # special case: UVIS can have 3 x TC20s in one dayside nadir
                    if "dayside2" in orbit["allowedObservationTypes"]:
                        copRows = [copRow]
                        copRowDescriptions = [copRowDescription]

                        daysideCounter += 1
                        copRow = uvisInputDict["uvis_dayside_nadir"][daysideCounter]
                        copRowDescription = getObservationDescription("uvis", copTableDict, 0, copRow, silent=True)
                        copRows.append(copRow)
                        copRowDescriptions.append(copRowDescription)

                        daysideCounter += 1
                        copRow = uvisInputDict["uvis_dayside_nadir"][daysideCounter]
                        copRowDescription = getObservationDescription("uvis", copTableDict, 0, copRow, silent=True)
                        copRows.append(copRow)
                        copRowDescriptions.append(copRowDescription)

                        finalOrbitPlan["uvisDaysideCopRows"]["scienceCopRow"] = copRows
                        finalOrbitPlan["uvisDaysideCopRows"]["copRowDescription"] = copRowDescriptions

                if "nightside" in orbit["allowedObservationTypes"]:
                    nightsideCounter += 1
                    # print("nightsideCounter=", nightsideCounter)
                    copRow = uvisInputDict["uvis_nightside_nadir"][nightsideCounter]
                    finalOrbitPlan["uvisNightsideCopRows"]["scienceCopRow"] = copRow
                    finalOrbitPlan["uvisNightsideCopRows"]["copRowDescription"] = getObservationDescription("uvis", copTableDict, 0, copRow, silent=True)

            # print stats
            for name, counter, dictionary in zip(["dayside", "egress", "grazing", "ingress", "nightside"],
                                                 [daysideCounter, egressCounter, grazingCounter, ingressCounter, nightsideCounter],
                                                 [uvisInputDict["uvis_dayside_nadir"], uvisInputDict["uvis_egress_occultations"],
                                                  uvisInputDict["uvis_grazing_occultations"], uvisInputDict["uvis_ingress_occultations"],
                                                  uvisInputDict["uvis_nightside_nadir"]]):
                nRowsAdded = counter+1
                nRowsAvailable = len(dictionary)
                nRowsMissing = nRowsAvailable - nRowsAdded
                print("%i %s COP rows added to orbit list, %i were in file. %i have not been accounted for" % (nRowsAdded, name, nRowsAvailable, nRowsMissing))

    return orbit_list
