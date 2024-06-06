# -*- coding: utf-8 -*-
"""
Created on Mon Apr 27 15:17:06 2020

@author: iant
"""


def mergeMtpPlan(orbit_list, mtp_plan, new_dict_name, old_dict_name):
    """merge iterated orbit plan into orbit list, check that they match each other"""
    if len(mtp_plan) != len(orbit_list):
        print("Error: length of plan read in from file does not match number of orbits calculated")

    for orbit, orbit_plan in zip(orbit_list, mtp_plan):
        orbit[new_dict_name] = {}

        if orbit_plan["orbitType"] == 1 and orbit[old_dict_name]["orbitType"] != 1:
            print("Error: occultation mismatch between orbit plan written and orbit plan read in for orbit number %i" % orbit["orbitNumber"])

        # do checks to ensure that ingress/egresses match in orbit list and mtp plan
        occultationFound = [True for value in orbit["allowedObservationTypes"] if value in ["ingress", "egress", "merged", "grazing"]]
        if orbit_plan["orbitType"] in [1, 5, 6] and not occultationFound:
            print("Error: occultation detected in orbit that shouldn't have occultations")

        for key, value in orbit_plan.items():
            if key in ["orbitType", "irIngressHigh", "irIngressLow", "uvisIngress", "irEgressHigh", "irEgressLow", "uvisEgress", "irDayside",
                       "uvisDayside", "irNightside", "uvisNightside", "comment"]:
                orbit[new_dict_name][key] = value
            if value != "":
                orbit[key] = value

    return orbit_list
