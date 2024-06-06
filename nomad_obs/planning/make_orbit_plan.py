# -*- coding: utf-8 -*-
"""
Created on Mon Apr 27 12:22:31 2020

@author: iant
"""


from datetime import datetime
import random


from nomad_obs.io.read_mro_overlap_file import getMroOverlaps
from nomad_obs.config.constants import SPICE_DATETIME_FORMAT
from nomad_obs.options import USE_TWO_SCIENCES
from nomad_obs.config.constants import UVIS_MULTIPLE_TC_NADIR_ORBIT_TYPES, UVIS_DEFAULT_ORBIT_TYPE
from nomad_obs.other.generic_functions import stop


def makeGenericOrbitPlan(orbit_list, mtp_constants, paths, silent=True):
    """save generic plan to orbit list. This doesn't have nightsides or limbs, just occs and dayside nadirs"""
    """baseline orbit plan orbit types: 1 or 5 if occultations, 14 if not, 3 if nadir region of interest detected"""
    # Potential improvment: automatically add some limbs and nightsides to fill in the times when occultations cannot be performed

    # inputs for defining generic orbit plan
    LNO_CYCLE = ["ON", "OFF", "OFF"] * 200  # i.e. 33% duty cycle for orbits without occultations.
    # This should begin with a 3 so that first observation after OCM is an LNO
    # The script automatically starts with an LNO OFF orbit if the preceding orbit has a measurement to avoid scheduling too many consecutive observations.

    lno_cycle = -1

    mroOverlapOrbits = getMroOverlaps(paths)

    for orbit in orbit_list:

        lstMidpoint = orbit["dayside"]["lstMidpoint"]
        incidenceMidpoint = orbit["dayside"]["incidenceMidpoint"]

        generic_orbit = {}
        generic_orbit_type = UVIS_DEFAULT_ORBIT_TYPE
        generic_orbit_comment = ""

        """check for possible OCMs (Saturday afternoons, 11 - 4pm)"""
        timeStringOut = orbit["dayside"]["utcStart"]
        orbitNumber = orbit["orbitNumber"]

        generic_orbit["irNightside"] = ""  # default irNightside to always off unless nightside limb added below
        generic_orbit["uvisNightside"] = ""  # default irNightside to always off unless nightside limb added below
        generic_orbit["irDayside"] = ""  # default

        # first check for OCMs
        all_off = False
        if datetime.strptime(timeStringOut, SPICE_DATETIME_FORMAT).isoweekday() == 6:
            if orbitNumber != 1:  # if not first orbit
                if orbitNumber != len(orbit_list):  # if not last orbit
                    if 12 < datetime.strptime(timeStringOut, SPICE_DATETIME_FORMAT).hour < 16:
                        generic_orbit_comment += "&possibleOCM; "
                        all_off = True

        # special section for true dayside limbs. Set dayside limb to type 28 first to avoid routine dayside nadirs being added
        # type 18s (occultations with limbs) are added later
        if "trueLimb" in orbit["allowedObservationTypes"]:
            generic_orbit_type = 28
            generic_orbit["irIngressHigh"] = ""  # no occultations ever on true limb orbits
            generic_orbit["irIngressLow"] = ""
            generic_orbit["uvisIngress"] = ""
            generic_orbit["irEgressHigh"] = ""
            generic_orbit["irEgressLow"] = ""
            generic_orbit["uvisEgress"] = ""
            generic_orbit["irDayside"] = "irLimb"
            generic_orbit["uvisDayside"] = "uvisLimb"
            generic_orbit_comment = "&trueDayLimb; "

        # night limbs must be done here so that region of interests on the dayside can be added after
        if "trueNightLimb" in orbit["allowedObservationTypes"]:
            print("Adding trueNightLimb")
            generic_orbit_type = 47
            generic_orbit["irIngressHigh"] = ""  # no occultations ever on true limb orbits
            generic_orbit["irIngressLow"] = ""
            generic_orbit["uvisIngress"] = ""
            generic_orbit["irEgressHigh"] = ""
            generic_orbit["irEgressLow"] = ""
            generic_orbit["uvisEgress"] = ""
            generic_orbit["irDayside"] = ""
            generic_orbit["uvisDayside"] = "uvisDayside"
            generic_orbit["irNightside"] = "irNightLimb"
            generic_orbit["uvisNightside"] = "uvisNightLimb"
            generic_orbit_comment += "&trueNightLimb; "

        # solar calibrations prevent all observations from occuring
        if "nomadSolarCalibration" in orbit["allowedObservationTypes"]:
            print("Adding NOMAD Solar Calibration")
            all_off = True
            generic_orbit_comment += "&nomadSolarCalibration; "
        if "acsSolarCalibration" in orbit["allowedObservationTypes"]:
            print("Adding ACS Solar Calibration")
            all_off = True
            generic_orbit_comment += "&acsSolarCalibration; "
        if "cassisSolarCalibration" in orbit["allowedObservationTypes"]:
            print("Adding CaSSIS Solar Calibration")
            all_off = True
            generic_orbit_comment += "&cassisSolarCalibration; "

        if "nomadPhobos" in orbit["allowedObservationTypes"]:
            print("Adding Phobos Solar Calibration")
            all_off = True
            generic_orbit_comment += "&nomadPhobos; "
        if "nomadDeimos" in orbit["allowedObservationTypes"]:
            print("Adding Deimos Solar Calibration")
            all_off = True
            generic_orbit_comment += "&nomadDeimos; "

        for occultation_type in orbit["allowedObservationTypes"]:

            if occultation_type == "ingress":
                if "trueLimb" in orbit["allowedObservationTypes"]:
                    generic_orbit_type = 28
                else:
                    generic_orbit_type = 1

                generic_orbit["irIngressHigh"] = "irIngress"
                generic_orbit["irIngressLow"] = "irIngress"
                generic_orbit["uvisIngress"] = "uvisIngress"

                if "egress" in orbit["allowedObservationTypes"]:  # if 2 occultations in same orbit
                    generic_orbit["irDayside"] = "irShortDayside"
                else:
                    generic_orbit["irDayside"] = "irDayside"
                    generic_orbit["irEgressHigh"] = ""
                    generic_orbit["irEgressLow"] = ""
                    generic_orbit["uvisEgress"] = ""

                generic_orbit["uvisDayside"] = "uvisDayside"

            elif occultation_type == "egress":
                if "trueLimb" in orbit["allowedObservationTypes"]:
                    generic_orbit_type = 28
                else:
                    generic_orbit_type = 1

                generic_orbit["irEgressHigh"] = "irEgress"
                generic_orbit["irEgressLow"] = "irEgress"
                generic_orbit["uvisEgress"] = "uvisEgress"

                if "ingress" in orbit["allowedObservationTypes"]:  # if 2 occultations in same orbit
                    generic_orbit["irDayside"] = "irShortDayside"
                else:
                    generic_orbit["irDayside"] = "irDayside"
                    generic_orbit["irIngressHigh"] = ""
                    generic_orbit["irIngressLow"] = ""
                    generic_orbit["uvisIngress"] = ""

                generic_orbit["uvisDayside"] = "uvisDayside"

            elif occultation_type == "merged":
                generic_orbit["irIngressHigh"] = "irMerged"
                generic_orbit["irIngressLow"] = "irMerged"
                generic_orbit["uvisIngress"] = "uvisMerged"

                generic_orbit["irEgressHigh"] = ""
                generic_orbit["irEgressLow"] = ""
                generic_orbit["uvisEgress"] = ""

                generic_orbit_type = 5
                generic_orbit["irDayside"] = "irShortDayside"
                generic_orbit["uvisDayside"] = "uvisDayside"

            elif occultation_type == "grazing":
                generic_orbit["irIngressHigh"] = "irGrazing"
                generic_orbit["irIngressLow"] = "irGrazing"
                generic_orbit["uvisIngress"] = "uvisGrazing"

                generic_orbit["irEgressHigh"] = ""
                generic_orbit["irEgressLow"] = ""
                generic_orbit["uvisEgress"] = ""

                generic_orbit_type = 5
                generic_orbit["irDayside"] = "irDayside"
                generic_orbit["uvisDayside"] = "uvisDayside"

            lno_cycle = 0  # reset lno to off

            # check for occultation regions of interest
            if "occultationRegions" in orbit.keys():  # if occ obs matches region of interest, set SO on and override generic comment with specific obs
                for region in orbit["occultationRegions"]:
                    if region["occultationType"] == occultation_type:
                        generic_orbit_comment += "&%sMatch:%s; " % (region["occultationType"], region["name"])
                        matchingOccultationType = region["occultationType"]
                        if "observationName" in orbit[matchingOccultationType].keys():  # if dedicated obs type found, overwrite generic obs
                            if matchingOccultationType == "ingress":
                                generic_orbit["irIngressHigh"] = orbit[matchingOccultationType]["observationName"]
                                generic_orbit["irIngressLow"] = orbit[matchingOccultationType]["observationName"]
                            if matchingOccultationType == "egress":
                                generic_orbit["irEgressHigh"] = orbit[matchingOccultationType]["observationName"]
                                generic_orbit["irEgressLow"] = orbit[matchingOccultationType]["observationName"]
                            if matchingOccultationType == "merged":
                                generic_orbit["irIngressHigh"] = orbit[matchingOccultationType]["observationName"]
                                generic_orbit["irIngressLow"] = orbit[matchingOccultationType]["observationName"]
                            if matchingOccultationType == "grazing":
                                generic_orbit["irIngressHigh"] = orbit[matchingOccultationType]["observationName"]
                                generic_orbit["irIngressLow"] = orbit[matchingOccultationType]["observationName"]

                        else:
                            print("Warning: region of interest found but no dedicated observation type has been specified")

            if "trueLimb" in orbit["allowedObservationTypes"]:
                generic_orbit["irDayside"] = "irLimb"
                generic_orbit["uvisDayside"] = "uvisLimb"

        if generic_orbit_type in [4, 14]:  # if no occultations - nadir only

            generic_orbit["irIngressHigh"] = ""
            generic_orbit["irIngressLow"] = ""
            generic_orbit["uvisIngress"] = ""
            generic_orbit["irEgressHigh"] = ""
            generic_orbit["irEgressLow"] = ""
            generic_orbit["uvisEgress"] = ""

            # check nadir regions of interest
            if "daysideRegions" in orbit.keys():  # if nadir obs matches region of interest, set LNO on
                lno_on_off = "ON"
                lno_cycle = 0  # reset lno to off

                for region in orbit["daysideRegions"]:
                    generic_orbit_comment += "&daysideMatch:%s; " % (region["name"])

            else:
                lno_cycle += 1
                lno_on_off = LNO_CYCLE[lno_cycle]

            if lno_on_off == "ON":
                generic_orbit_type = 3
                generic_orbit["irDayside"] = "irLongDayside"
                generic_orbit["uvisDayside"] = "uvisDayside"

                # check nadir regions of interest in orbit list
                if "observationName" in orbit["dayside"].keys():  # if dedicated obs type found, overwrite generic obs
                    generic_orbit["irDayside"] = orbit["dayside"]["observationName"]

            else:  # if lno off and no occultations
                generic_orbit["irDayside"] = ""
                if generic_orbit_type == 4:  # if 3x UVIS TCs
                    generic_orbit["uvisDayside"] = "uvisDayside"

                elif generic_orbit_type == 14:  # if 1x UVIS TCs
                    generic_orbit["uvisDayside"] = "uvisDayside"

        else:  # if not orbit types 4 or 14, still check for nadir regions

            if generic_orbit_type not in [18, 28]:  # if dayside limb, don't check for regions of interest

                # check nadir regions of interest
                if "daysideRegions" in orbit.keys():  # if nadir obs matches region of interest, set LNO on
                    for region in orbit["daysideRegions"]:
                        generic_orbit_comment += "&daysideMatch:%s; " % (region["name"])

                # check nadir regions of interest in orbit list
                if "observationName" in orbit["dayside"].keys():  # if dedicated obs type found, overwrite generic obs
                    generic_orbit["irDayside"] = orbit["dayside"]["observationName"]

        # now add MRO overlaps to comments
        if orbitNumber in mroOverlapOrbits:
            generic_orbit_comment += "&mroOverlap; "

            # if LNO is off, switch on and change orbit type to 3. If LNO already on, leave alone
            if generic_orbit["irDayside"] == "":
                generic_orbit["irDayside"] = "irDayside"
            if generic_orbit_type in [4, 14]:
                generic_orbit_type = 3

        if all_off:
            generic_orbit_type = 14
            generic_orbit["irIngressHigh"] = ""  # no occultations ever on solar cal orbits
            generic_orbit["irIngressLow"] = ""
            generic_orbit["uvisIngress"] = ""
            generic_orbit["irEgressHigh"] = ""
            generic_orbit["irEgressLow"] = ""
            generic_orbit["uvisEgress"] = ""
            generic_orbit["irDayside"] = ""
            generic_orbit["uvisDayside"] = ""
            generic_orbit["irNightside"] = ""
            generic_orbit["uvisNightside"] = ""
            lno_cycle = -1  # reset lno to on for next orbit

        # if after all that, the comment is still empty, add lst and solar incidence angle
        if generic_orbit_comment == "":
            generic_orbit_comment = "&LST=%0.1fhrs; &Angle=%i; " % (lstMidpoint, incidenceMidpoint)

        orbit["genericOrbitPlanOut"] = {"orbitType": generic_orbit_type, "orbitTypes": generic_orbit, "comment": generic_orbit_comment}
    return orbit_list


def makeCompleteOrbitPlan(orbit_list, observationCycles):
    """fill in generic plan with real observation names"""
#    occultationCounter = -1
#    occultationMergedCounter = -1
#    occultationGrazingCounter = -1
#    occultationRidealongCounter = -1
#    nadirCounter = -1
#    nadirLimbCounter = -1
#    nadirNightsideCounter = -1

    for orbit in orbit_list:

        genericObsTypes = orbit["genericOrbitPlanIn"]
        orbitType = genericObsTypes["orbitType"]

        irIngressHigh = "******ERROR******"  # to be replaced in loop
        irIngressLow = "******ERROR******"  # to be replaced in loop
        irEgressHigh = "******ERROR******"  # to be replaced in loop
        irEgressLow = "******ERROR******"  # to be replaced in loop
        irDayside = "******ERROR******"  # to be replaced in loop
        irNightside = "******ERROR******"  # to be replaced in loop

    #    uvisIngress = genericObsTypes["uvisIngress"]
    #    uvisEgress = genericObsTypes["uvisEgress"]
    #    uvisDayside = genericObsTypes["uvisDayside"]

        if orbitType in [1, 28]:
            # SO/LNO
            if genericObsTypes["irIngressHigh"] == "":  # no observation
                irIngressHigh = ""
                irIngressLow = ""
            elif genericObsTypes["irIngressHigh"] == "irIngress":  # generic observation

                irIngressHigh = random.choice(observationCycles["OccultationCycleNominal"][1])
                # special obs where high and low altitude obs are different
                if USE_TWO_SCIENCES:
                    if irIngressHigh == "Nominal Science 1xCO2 LA01" or irIngressHigh == "Nominal Science 1xCO2 HA01":
                        irIngressHigh = "Nominal Science 1xCO2 HA01"
                        irIngressLow = "Nominal Science 1xCO2 LA01"
                    elif irIngressHigh == "Nominal Science 1xCO2 LA02" or irIngressHigh == "Nominal Science 1xCO2 HA02":
                        irIngressHigh = "Nominal Science 1xCO2 HA02"
                        irIngressLow = "Nominal Science 1xCO2 LA02"
                    elif irIngressHigh == "Nominal Science 1xCO2 LA03" or irIngressHigh == "Nominal Science 1xCO2 HA03":
                        irIngressHigh = "Nominal Science 1xCO2 HA03"
                        irIngressLow = "Nominal Science 1xCO2 LA03"
                    elif irIngressHigh == "Nominal Science 1xCO2 LA04" or irIngressHigh == "Nominal Science 1xCO2 HA04":
                        irIngressHigh = "Nominal Science 1xCO2 HA04"
                        irIngressLow = "Nominal Science 1xCO2 LA04"
                else:
                    irIngressLow = irIngressHigh

            else:
                irIngressHigh = genericObsTypes["irIngressHigh"]  # use preselected targeted obs
                irIngressLow = genericObsTypes["irIngressLow"]  # use preselected targeted obs
                # uvisIngress = "uvisIngress"

            # UVIS
            if genericObsTypes["uvisIngress"] == "":  # no observation
                uvisIngress = ""

            elif genericObsTypes["uvisIngress"] == "uvisIngress":  # generic observation
                uvisIngress = "uvisIngress"

            else:
                uvisIngress = genericObsTypes["uvisIngress"]  # use preselected targeted obs

            # SO/LNO
            if genericObsTypes["irEgressHigh"] == "":  # no observation
                irEgressHigh = ""
                irEgressLow = ""
            elif genericObsTypes["irEgressHigh"] == "irEgress":  # generic observation

                irEgressHigh = random.choice(observationCycles["OccultationCycleNominal"][1])
                # special obs where high and low altitude obs are different
                if USE_TWO_SCIENCES:
                    if irEgressHigh == "Nominal Science 1xCO2 LA01" or irEgressHigh == "Nominal Science 1xCO2 HA01":
                        irEgressHigh = "Nominal Science 1xCO2 HA01"
                        irEgressLow = "Nominal Science 1xCO2 LA01"
                    elif irEgressHigh == "Nominal Science 1xCO2 LA02" or irEgressHigh == "Nominal Science 1xCO2 HA02":
                        irEgressHigh = "Nominal Science 1xCO2 HA02"
                        irEgressLow = "Nominal Science 1xCO2 LA02"
                    elif irEgressHigh == "Nominal Science 1xCO2 LA03" or irEgressHigh == "Nominal Science 1xCO2 HA03":
                        irEgressHigh = "Nominal Science 1xCO2 HA03"
                        irEgressLow = "Nominal Science 1xCO2 LA03"
                    elif irEgressHigh == "Nominal Science 1xCO2 LA04" or irEgressHigh == "Nominal Science 1xCO2 HA04":
                        irEgressHigh = "Nominal Science 1xCO2 HA04"
                        irEgressLow = "Nominal Science 1xCO2 LA04"
                else:
                    irEgressLow = irEgressHigh

            else:
                irEgressHigh = genericObsTypes["irEgressHigh"]  # use preselected targeted obs
                irEgressLow = genericObsTypes["irEgressLow"]  # use preselected targeted obs

            # UVIS
            if genericObsTypes["uvisEgress"] == "":  # no observation
                uvisEgress = ""

            elif genericObsTypes["uvisEgress"] == "uvisEgress":  # generic observation
                uvisEgress = "uvisEgress"

            else:
                uvisEgress = genericObsTypes["uvisEgress"]  # use preselected targeted obs

            # SO/LNO dayside with occultations
            if genericObsTypes["irDayside"] == "":  # if LNO off
                irDayside = ""
            elif genericObsTypes["irDayside"] in ["irDayside", "irShortDayside", "irLongDayside"]:  # generic observation
                irDayside = random.choice(observationCycles["NadirCycleNominal"][1])
            else:  # use preselected targeted obs
                irDayside = genericObsTypes["irDayside"]

            # UVIS dayside with occultations
            if genericObsTypes["uvisDayside"] == "":  # if UVIS off
                uvisDayside = ""
            elif genericObsTypes["uvisDayside"] == "uvisDayside":  # generic observation
                uvisDayside = "uvisDayside"
            else:  # use preselected targeted obs
                uvisDayside = genericObsTypes["uvisDayside"]

            orbit["allowedObservationTypes"].append("dayside")  # dayside allowed with occultations

            irNightside = ""  # never nightside with occultations
            uvisNightside = ""  # never nightside with occultations

        if orbitType in [5, 6]:  # merged/grazing with UVIS and/or LNO nadir
            if "merged" not in orbit["allowedObservationTypes"] and "grazing" not in orbit["allowedObservationTypes"]:
                print("Error: orbit type %i must have a merged or grazing occulatation" % orbitType)

            # SO/LNO
            if genericObsTypes["irIngressHigh"] == "irMerged":  # generic observation
                irIngressHigh = random.choice(observationCycles["OccultationCycleMerged"][1])
                irIngressLow = irIngressHigh
            elif genericObsTypes["irIngressHigh"] == "irGrazing":  # generic observation
                irIngressHigh = random.choice(observationCycles["OccultationCycleGrazing"][1])
                irIngressLow = irIngressHigh
            else:
                irIngressHigh = genericObsTypes["irIngressHigh"]  # use preselected targeted obs
                irIngressLow = genericObsTypes["irIngressLow"]  # use preselected targeted obs

            # UVIS
            if genericObsTypes["uvisIngress"] == "uvisMerged":  # generic observation
                uvisIngress = "uvisMerged"
            elif genericObsTypes["uvisIngress"] == "uvisGrazing":  # generic observation
                uvisIngress = "uvisGrazing"
            else:
                uvisIngress = genericObsTypes["uvisIngress"]  # use preselected targeted obs

            # egress always blank if merged or grazing
            irEgressHigh = ""
            irEgressLow = ""
            uvisEgress = ""

            # SO/LNO dayside with occultations
            if genericObsTypes["irDayside"] == "":  # if LNO off
                irDayside = ""
            elif genericObsTypes["irDayside"] in ["irDayside", "irShortDayside", "irLongDayside"]:  # generic observation
                irDayside = random.choice(observationCycles["NadirCycleNominal"][1])
            else:  # use preselected targeted obs
                irDayside = genericObsTypes["irDayside"]

            # UVIS dayside with occultations
            if genericObsTypes["uvisDayside"] == "":  # if UVIS off
                uvisDayside = ""
            elif genericObsTypes["uvisDayside"] == "uvisDayside":  # generic observation
                uvisDayside = "uvisDayside"
            else:  # use preselected targeted obs
                uvisDayside = genericObsTypes["uvisDayside"]

            orbit["allowedObservationTypes"].append("dayside")  # dayside allowed with occultations

            irNightside = ""  # never nightside with occultations
            uvisNightside = ""  # never nightside with occultations

        if orbitType in [3, 4, 14]:  # no occultations, dayside nadir only. Possible OCM here
            irIngressHigh = ""
            irIngressLow = ""
            uvisIngress = ""
            irEgressHigh = ""
            irEgressLow = ""
            uvisEgress = ""

            irNightside = ""
            uvisNightside = ""

            if orbitType in [3, 14]:
                orbit["allowedObservationTypes"].append("dayside")
            elif orbitType == 4:
                orbit["allowedObservationTypes"].append("dayside")
                orbit["allowedObservationTypes"].append("dayside2")
                orbit["allowedObservationTypes"].append("dayside3")

            # UVIS dayside
            if genericObsTypes["uvisDayside"] == "":  # if UVIS off
                uvisDayside = ""
            elif genericObsTypes["uvisDayside"] == "uvisDayside":  # generic observation
                uvisDayside = "uvisDayside"
            else:  # use preselected targeted obs
                uvisDayside = genericObsTypes["uvisDayside"]

            if genericObsTypes["irDayside"] in ["irDayside", "irShortDayside", "irLongDayside"]:  # LNO generic dayside nadir
                if orbitType == 3:
                    irDayside = random.choice(observationCycles["NadirCycleNominal"][1])
                elif orbitType == 4:
                    print("Error: orbit type 4 cannot have LNO dayside")
                    irDayside = ""
                elif orbitType == 14:
                    print("Error: orbit type 14 cannot have LNO dayside")
                    irDayside = ""

            elif genericObsTypes["irDayside"] == "":  # LNO off
                if orbitType == 3:
                    irDayside = ""
                elif orbitType == 4:
                    irDayside = ""
                elif orbitType == 14:
                    irDayside = ""

            else:  # use preselected targeted obs
                if orbitType == 3:
                    irDayside = genericObsTypes["irDayside"]
                elif orbitType == 4:
                    print("Error: orbit type 4 cannot have LNO dayside")
                    irDayside = ""
                elif orbitType == 14:
                    print("Error: orbit type 14 cannot have LNO dayside")
                    irDayside = ""

        if orbitType in [7, 17]:  # UVIS+LNO nightside or UVIS alone

            irIngressHigh = ""
            irIngressLow = ""
            uvisIngress = ""
            irEgressHigh = ""
            irEgressLow = ""
            uvisEgress = ""

            orbit["allowedObservationTypes"].append("dayside")  # nightsides also have daysides
            orbit["allowedObservationTypes"].append("nightside")

            if genericObsTypes["irDayside"] in ["irDayside", "irShortDayside", "irLongDayside"]:  # dayside nadir
                irDayside = random.choice(observationCycles["NadirCycleNominal"][1])
            elif genericObsTypes["irDayside"] == "":  # LNO off
                irDayside = ""
            else:
                irDayside = genericObsTypes["irDayside"]  # use preselected targeted obs

            # UVIS dayside
            if genericObsTypes["uvisDayside"] == "":  # if UVIS off
                uvisDayside = ""
            elif genericObsTypes["uvisDayside"] == "uvisDayside":  # generic observation
                uvisDayside = "uvisDayside"
            else:  # use preselected targeted obs
                uvisDayside = genericObsTypes["uvisDayside"]

            if genericObsTypes["irNightside"] == "":  # LNO off
                irNightside = ""
                uvisNightside = "uvisOnlyNightside"
                if orbitType == 7:
                    print("Warning: orbit type 7 found with blank nightside nadir")

            else:  # if LNO nightside or preselected targeted obs
                # UVIS always on for nightsides/nightlimbs
                if orbitType == 7:
                    if genericObsTypes["irNightside"] == "irNightside":  # if generic obs
                        irNightside = random.choice(observationCycles["NadirCycleNightside"][1])
                        uvisNightside = "uvisNightside"
                    else:
                        irNightside = genericObsTypes["irNightside"]  # use preselected targeted obs
                        uvisNightside = "uvisNightside"

                else:  # if LNO should be off
                    print("Error: orbit type 17 cannot have LNO nightside (orbit %i)" % orbit["orbitNumber"])
                    print(genericObsTypes["irNightside"])
                    irNightside = ""
                    uvisNightside = "uvisOnlyNightside"

        if orbitType in [8, 18, 28]:  # LNO and/or UVIS dayside limb with or without occultations

            if orbitType in [8]:
                irIngressHigh = ""
                irIngressLow = ""
                uvisIngress = ""
                irEgressHigh = ""
                irEgressLow = ""
                uvisEgress = ""

            orbit["allowedObservationTypes"].append("dayside")  # TODO: comment out?

            if genericObsTypes["irDayside"] == "":  # LNO off
                irDayside = ""
                print("Warning: orbit type 8 found with blank limb observation")

                if orbitType == 8:
                    uvisDayside = "uvisDayside"
                else:
                    uvisDayside = "uvisOnlyLimb"

            elif genericObsTypes["irDayside"] == "irLimb":  # LNO on
                #                nadirLimbCounter += 1
                irDayside = random.choice(observationCycles["NadirCycleLimb"][1])

                if orbitType == 8:
                    uvisDayside = "uvisDayside"
                else:
                    uvisDayside = "uvisLimb"

            else:  # use LNO limb preselected targeted obs
                irDayside = genericObsTypes["irDayside"]
                print("Warning: check that observation %s is suitable for an LNO limb measurement" % irDayside)

                if orbitType == 8:
                    uvisDayside = "uvisDayside"
                else:
                    uvisDayside = "uvisLimb"

            irNightside = ""
            uvisNightside = ""

        if orbitType in [47]:  # LNO and/or UVIS nightside limb

            irIngressHigh = ""
            irIngressLow = ""
            uvisIngress = ""
            irEgressHigh = ""
            irEgressLow = ""
            uvisEgress = ""
            uvisNightside = "uvisNightLimb"  # always run night limbs

            orbit["allowedObservationTypes"].append("dayside")  # TODO: comment out?
            orbit["allowedObservationTypes"].append("nightside")  # TODO: comment out?

            if genericObsTypes["irNightside"] == "":  # LNO off
                irNightside = ""
                print("Warning: orbit type 47 found with blank night limb observation")

            elif genericObsTypes["irNightside"] == "irNightLimb":  # LNO on
                irNightside = random.choice(observationCycles["NadirCycleNightLimb"][1])

            else:  # use LNO night limb preselected targeted obs
                irNightside = genericObsTypes["irNightside"]
                print("Warning: check that observation %s is suitable for an LNO night limb measurement" % irNightside)

            # set LNO dayside to ON only for targeted observations
            if genericObsTypes["irDayside"] == "":  # LNO off
                irDayside = ""

            elif irDayside in ["irDayside", "irShortDayside", "irLongDayside"]:  # this should not happen - no generic daysides on night limbs
                print("Error: LNO generic dayside observation %s on same orbit at nightside limb" % irDayside)
                stop()

            else:  # use LNO dayside preselected targeted obs
                irDayside = genericObsTypes["irDayside"]
                print("LNO targeted dayside observation %s on same orbit at nightside limb" % irDayside)

            # UVIS dayside
            if genericObsTypes["uvisDayside"] == "":  # if UVIS off
                uvisDayside = ""
            elif genericObsTypes["uvisDayside"] == "uvisDayside":  # generic observation
                uvisDayside = "uvisDayside"
            else:  # use preselected targeted obs
                uvisDayside = genericObsTypes["uvisDayside"]

        orbit["completeOrbitPlan"] = \
            {
            "orbitType": orbitType,
            "irIngressHigh": irIngressHigh,
            "irIngressLow": irIngressLow,
            "irEgressHigh": irEgressHigh,
            "irEgressLow": irEgressLow,
            "irDayside": irDayside,
            "irNightside": irNightside,

            "uvisIngress": uvisIngress,
            "uvisEgress": uvisEgress,
            "uvisDayside": uvisDayside,
            "uvisNightside": uvisNightside,

            "comment": genericObsTypes["comment"],
        }
    return orbit_list


def addCorrectNadirObservations(orbit_list):
    """add some final tweaks to ensure dayside/limb/nightside observations are correct e.g. include uvis 3 x TC20s, etc"""

    for orbit in orbit_list:
        finalOrbitPlan = orbit["finalOrbitPlan"]

        # TODO: change this so not all SO grazings are run
        # first, find all allowed occultation measurement types for orbit
        irMeasuredObsTypes = [occultationType for occultationType in orbit["allowedObservationTypes"]
                              [:] if occultationType in ["ingress", "egress", "merged", "grazing"]]

        uvisMeasuredObsTypes = []
        if finalOrbitPlan["uvisIngress"] != "":  # limb is simply a dayside
            uvisMeasuredObsTypes.append("ingress")
        if finalOrbitPlan["uvisEgress"] != "":  # limb is simply a dayside
            uvisMeasuredObsTypes.append("egress")

        # uvis not run on all occultations
        # uvisMeasuredObsTypes = [occultationType for occultationType in orbit["allowedObservationTypes"]
        #                         [:] if occultationType in ["ingress", "egress", "merged", "grazing"]]

        # add nadir types
        if finalOrbitPlan["irDayside"] != "":  # limb is simply a dayside
            irMeasuredObsTypes.append("dayside")
        if finalOrbitPlan["irNightside"] != "":
            irMeasuredObsTypes.append("nightside")
        if finalOrbitPlan["uvisDayside"] != "":
            uvisMeasuredObsTypes.append("dayside")

            # some orbit types have 3 x uvis nadirs
            if finalOrbitPlan["orbitType"] in UVIS_MULTIPLE_TC_NADIR_ORBIT_TYPES:
                uvisMeasuredObsTypes.append("dayside2")
                uvisMeasuredObsTypes.append("dayside3")

        if finalOrbitPlan["uvisNightside"] != "":
            uvisMeasuredObsTypes.append("nightside")

        orbit["irMeasuredObsTypes"] = irMeasuredObsTypes
        orbit["uvisMeasuredObsTypes"] = uvisMeasuredObsTypes

    return orbit_list
