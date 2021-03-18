# -*- coding: utf-8 -*-
"""
Created on Thu Nov 19 11:41:43 2020

@author: iant

READ IN LNO AND UVIS OCCULTATION-IN-SOLAR-FOV FILES AND MAKE A LIST TO COPY TO EXCEL FILE
"""

import os

mtpNumber = 40

from nomad_obs.mtp_inputs import getMtpConstants

from nomad_obs.config.paths import setupPaths


mtpConstants = getMtpConstants(mtpNumber)
paths = setupPaths(mtpConstants)

filepaths = [
    os.path.join(paths["SUMMARY_FILE_PATH"], "MARS_IN_LNO_OCC_FOV.txt"), 
    os.path.join(paths["SUMMARY_FILE_PATH"], "MARS_IN_UVIS_OCC_FOV.txt"),
    ]


with open(filepaths[0], "r") as f:
    lines = f.readlines()
lno_orbit_numbers = [int(line.split(",")[-1].replace("\n", "")) for i, line in enumerate(lines) if i>0]

with open(filepaths[1], "r") as f:
    lines = f.readlines()
uvis_orbit_numbers = [int(line.split(",")[-1].replace("\n", "")) for i, line in enumerate(lines) if i>0]

last_orbit_number = max(lno_orbit_numbers)

orbit_numbers = range(last_orbit_number+1)

print("Mars in LNO/UVIS occultation FOVs")
for orbit_number in orbit_numbers[1:]:
    if orbit_number in uvis_orbit_numbers:
        print("UVIS")
    elif orbit_number in lno_orbit_numbers:
        print("LNO")
    else:
        print("")
print("End")