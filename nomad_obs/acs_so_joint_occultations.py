# -*- coding: utf-8 -*-
"""
Created on Mon Apr 27 10:04:17 2020

@author: iant
"""

SOC_JOINT_OBSERVATION_NAMES = {
    "NOM_02":["6SUBD Nominal #1", "6SUBD Nominal #2"],
    "NOM_03":["6SUBD Nominal #3", "6SUBD Nominal #42", "6SUBD Nominal #45", "6SUBD Nominal #48", "6SUBD Nominal #51", "6SUBD Nominal #11", \
              "6SUBD Nominal #12", "6SUBD CO2 H2O #11", "6SUBD CO2 H2O #14", "6SUBD CO2 H2O CO #15", "6SUBD CO2 CO #25", "6SUBD CO2 CO #26", \
              "6SUBD CO2 CO #27", "6SUBD CO2 H2O #12", "6SUBD CO2 H2O #13", "6SUBD Nominal #53", "6SUBD Nominal #52"],


    "CO_001":["6SUBD Nom CO #1", "6SUBD Nom CO #2", "6SUBD Nom CO #3", "6SUBD Nom CO #4", "6SUBD Nom CO #5"],
    "CO_002":["6SUBD Nom CO #6", "6SUBD Nom CO #7", "6SUBD CO #1", "6SUBD CO #2", "6SUBD CO #3", "6SUBD CO #4", "6SUBD CO #5"],
    "CO2_01":["6SUBD Nom CO2 #1", "6SUBD Nom CO2 #2", "CO2 100km #1", "6SUBD CO2 #1", "6SUBD CO2 #10"],
    "CO2_02":["132 only #2", "133 only #2", "134 only #2", "6SUBD CO2 Dipole #1", "CO2 Fullscan Fast #3", "6SUBD CO2 #12", "6SUBD CO2 #13", \
              "6SUBD CO2 #16", "6SUBD CO2 #17", "6SUBD CO2 #18", "6SUBD CO2 #19", "6SUBD CO2 #20", "6SUBD CO2 #21", "6SUBD CO2 #22", \
              "6SUBD CO2 #23", "6SUBD CO2 #24"],

    "HCL_01":["126 only #2", "127 only #2", "129 only #2", "Dust H2O 01", "HDO 01", \
              "HCL #4", "HCL #5", "HCL #8", "HCL #9", "HCL #10", "HCL #11"],

    
    "AER_01":["AER 01"],
#    "DUST01":["Dust H2O 01"],
#    "HDO_01":["HDO 01"],
    "ICE_01":["Water Ice 01"],
    
    "NOM_01":["Nominal Science 1xCO2 LA01"],
    "FUL_01":["All Fullscan Fast #2", "All Fullscan Slow #2", "CO2 Fullscan Fast #2", "CO Fullscan Fast #2", "LNO Occultation Fullscan Fast #2"]
    }


SOC_JOINT_OBSERVATION_TYPES = [
        "OCCEG",
        "OCCIN",
        "OCCME",
#        "OCCGR" #ACS doesn't run grazings
        ]
        


