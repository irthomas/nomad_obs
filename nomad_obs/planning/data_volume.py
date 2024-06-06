# -*- coding: utf-8 -*-
"""
Created on Tue May 28 14:26:53 2024

@author: iant

DATA VOLUME CALCULATIONS
"""


import numpy as np

obsLength = 2000

rhythm = 25858
vStart = 57
vEnd = 245
hStart = 0
hEnd = 1047
bits = 16

n_frames = obsLength / (rhythm/1000.0)
n_pixels = (vEnd - vStart) * (hEnd - hStart)
n_bits_per_frame = n_pixels * bits

hsk_bits = obsLength * 800

mbit_total = (n_frames * n_bits_per_frame + hsk_bits) / 1.0e6


# count the theoretical number of each event type in each STP
obsEvents = {
    "nomadPhobos": {1: [], 2: [], 3: [], 4: {}},  # run all
    "nomadDeimos": {1: [], 2: [], 3: [], 4: {}},  # run all
    "nomadSolarCalibration": {1: [], 2: [], 3: [], 4: {}},  # run all
    "trueLimb": {1: [], 2: [], 3: [], 4: {}},  # run all
    "trueNightLimb": {1: [], 2: [], 3: [], 4: {}},  # run all
    "nightside": {1: [], 2: [], 3: [], 4: {}},  # run all

    "merged": {1: [], 2: [], 3: [], 4: {}},  # run half
    "grazing": {1: [], 2: [], 3: [], 4: {}},  # run all
    "ingress": {1: [], 2: [], 3: [], 4: {}},  # run half
    "egress": {1: [], 2: [], 3: [], 4: {}},  # run half
    "dayside": {1: [], 2: [], 3: [], 4: {}},  # run some
}

etStartMtp = orbitList[0]["etOrbitStart"]
stpStarts = np.asarray([etStartMtp, etStartMtp+(3600*24*7), etStartMtp+2*(3600*24*7), etStartMtp+3*(3600*24*7)])
for orbit in orbitList:
    # find STP number 1,2,3 or 4

    etOrbitStart = orbit["etOrbitStart"]
    stpNumber = np.max(np.where(etOrbitStart >= stpStarts)[0])
    print(etOrbitStart, stpNumber)

    # if "nomadPhobos" in orbit["allowedObservationTypes"]:
    #     obsEvents

# first define solar calibrations


# then define limbs

# then define Phobos observations

# then define solar occultations

# then define nightside nadirs

# the remaining is to be spread between dayside nadirs
