# -*- coding: utf-8 -*-
"""
Created on Fri Sep  4 11:35:04 2026

@author: iant
"""
import os
import numpy as np
from datetime import datetime

from nomad_obs.mtp_inputs import getMtpConstants
from nomad_obs.config.paths import setupPaths
from nomad_obs.io.orbit_plan_xlsx import getMtpPlanXlsx

DT_STR = "%Y %b %d %H:%M:%S"


mtpNumber = 112
mtpConstants = getMtpConstants(mtpNumber)
paths = setupPaths(mtpConstants)


filename = "roi_flyovers_nightside-filtered.txt"


filepath = os.path.join(paths["SUMMARY_FILE_PATH"], filename)

with open(filepath, "r") as f:
    lines = f.readlines()

orbit_numbers = []
utcs = []
for line in lines:
    if line[0:6] == "Target":
        continue

    line_sp = line.split(",")
    orbit_number = line_sp[3]
    utc = line_sp[4]

    orbit_numbers.append(int(orbit_number))
    utcs.append(utc)

    # print(orbit_number, utc)


mtpPlan = getMtpPlanXlsx(mtpConstants, paths, "plan_generic")

# uvisDaysides = [d["uvisDayside"] for d in mtpPlan]
# uvisNightsides = [d["uvisNightside"] for d in mtpPlan]
# ingresses = [d["irIngressHigh"] for d in mtpPlan]
# egresses = [d["irEgressHigh"] for d in mtpPlan]
# ots = [d["orbitType"] for d in mtpPlan]
# # comments = [d["comment"] for d in mtpPlan]
# n2d_utcs = [d["night2dayTerminator"] for d in mtpPlan]

for orbit_number, obs_utc in zip(orbit_numbers, utcs):

    orbit_plan = mtpPlan[orbit_number - 1]

    if orbit_plan["orbitType"] in [3, 14]:

        n2d_utc = orbit_plan["night2dayTerminator"]

        n2d_dt = datetime.strptime(n2d_utc, DT_STR)
        obs_dt = datetime.strptime(obs_utc, DT_STR)
        diff = np.abs((n2d_dt - obs_dt).total_seconds())

        if diff / 60 < 60.0 and diff > 0:
            ok = True
        else:
            ok = False

        print("## Orbit number: %i (excel row %i)" % (orbit_number, orbit_number + 1))
        print("Day nadir start time: %s; obs start time: %s; %0.2f minutes before." % (n2d_utc, obs_utc, diff / 60.0), ok)

    else:
        print("Orbit %i cannot be run (orbit type=%i)" % (orbit_number, orbit_plan["orbitType"]))
