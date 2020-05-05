# -*- coding: utf-8 -*-
"""
Created on Mon Apr 27 10:04:17 2020

@author: iant
"""

SOC_JOINT_OBSERVATION_NAMES = {
    "NOM_02":["6SUBD Nominal #1", "6SUBD Nominal #2"],
    "NOM_03":["6SUBD Nominal #3"],
    "CO_001":["6SUBD Nom CO #1", "6SUBD Nom CO #2", "6SUBD Nom CO #3", "6SUBD Nom CO #4", "6SUBD Nom CO #5"],
    "CO2_01":["6SUBD Nom CO2 #1", "6SUBD Nom CO2 #2", "CO2 100km #1", "6SUBD CO2 #1", "6SUBD CO2 #10"],

    "HCL_01":["126 only #2", "127 only #2", "129 only #2", "CO2 Fullscan Fast #3", "Dust H2O 01", "HDO 01"],

    
    "AER_01":["AER 01"],
#    "DUST01":["Dust H2O 01"],
#    "HDO_01":["HDO 01"],
    "ICE_01":["Water Ice 01"],
    
    "NOM_01":["Nominal Science 1xCO2 LA01"],
    }


SOC_JOINT_OBSERVATION_TYPES = [
        "OCCEG",
        "OCCIN",
        "OCCME",
#        "OCCGR" #ACS doesn't run grazings
        ]
        
