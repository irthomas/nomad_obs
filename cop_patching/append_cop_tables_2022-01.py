# -*- coding: utf-8 -*-
"""
Created on Wed Dec  8 10:46:39 2021

@author: iant

SCRIPT TO READ IN THE EXISTING SCIENCE TABLES AND GENERATE A FEW SUBDOMAIN ROWS FOR A MINOR PATCH

"""
import os
import re

from cop_patching.generate_cop_tables_v05 import readScienceComments, writeTable
from cop_patching.generate_cop_tables_v05 import read_in_cop_table, getWindowHeight, exec_time, checkExecTime

from nomad_obs.config.paths import BASE_DIRECTORY


PREVIOUS_COP_TABLE_DIRECTORY_NAME = "20210320_120000"
COP_TABLE_PATH = os.path.join(BASE_DIRECTORY, "cop_tables", PREVIOUS_COP_TABLE_DIRECTORY_NAME)


channels = ["so", "lno"]

#normal
lno_normal_orders = {
    "Carbonates":[
        {"orders":[174, 175, 176, 189, 190, 191], "rhythms":[8, 15], "binning":[0, 1, 2]},
        {"orders":[174, 175, 176], "rhythms":[8, 15], "binning":[0, 1]},
        {"orders":[189, 190, 191], "rhythms":[8, 15], "binning":[0, 1]},
    ],
    "Phyllosilicates":[
        {"orders":[189, 190, 191, 192, 193, 201], "rhythms":[8, 15], "binning":[0, 1, 2]},
        {"orders":[190, 191, 192], "rhythms":[8, 15], "binning":[0, 1]},
    ],
    "Carb Phyl":[
        {"orders":[174, 175, 176, 190, 191, 192], "rhythms":[8, 15], "binning":[0, 1, 2]},
    ],
    "Water Band":[
        {"orders":[160, 162, 164, 166, 168, 170], "rhythms":[8, 15], "binning":[0, 1, 2]},
        { "orders":[160, 163, 166, 169, 172, 175], "rhythms":[8, 15], "binning":[0, 1, 2]},
        {"orders":[157, 160, 163, 166, 169, 172], "rhythms":[8, 15], "binning":[0, 1, 2]},
        {"orders":[163, 165, 167, 169], "rhythms":[8, 15], "binning":[0, 1]},
        {"orders":[160, 165, 170], "rhythms":[8, 15], "binning":[0, 1]},
        {"orders":[163, 168, 173], "rhythms":[8, 15], "binning":[0, 1]},
    ],
}
#fullscans
lno_fullscans = [
    {"name":"Water Band Fullscan #1", "start":160, "steps":11, "step":1, "rhythms":[8, 15], "steps_rhythm":{6:[0, 1, 2], 4:[1], 3:[0, 1]}},
    {"name":"Water Band Fullscan #2", "start":160, "steps":6, "step":2, "rhythms":[8, 15], "steps_rhythm":{6:[0, 1, 2], 4:[1], 3:[0, 1]}},
    {"name":"Water Band Fullscan #3", "start":156, "steps":11, "step":2, "rhythms":[8, 15], "steps_rhythm":{6:[0, 1, 2], 4:[1], 3:[0, 1]}},
    {"name":"Carbonates #1", "start":173, "steps":21, "step":1, "rhythms":[8, 15], "steps_rhythm":{6:[0, 1, 2], 4:[1], 3:[0, 1]}},
    {"name":"Carbonates #2", "start":173, "steps":11, "step":2, "rhythms":[8, 15], "steps_rhythm":{6:[0, 1, 2], 4:[1], 3:[0, 1]}},
    {"name":"Phyllosilicates #1", "start":188, "steps":15, "step":1, "rhythms":[8, 15], "steps_rhythm":{6:[0, 1, 2], 4:[1], 3:[0, 1]}},
    {"name":"Phyllosilicates #2", "start":187, "steps":9, "step":2, "rhythms":[8, 15], "steps_rhythm":{6:[0, 1, 2], 4:[1], 3:[0, 1]}},
    {"name":"Carb Phyl #1", "start":174, "steps":29, "step":1, "rhythms":[8, 15], "steps_rhythm":{6:[0, 1, 2], 4:[1], 3:[0, 1]}},
    {"name":"Carb Phyl #2", "start":173, "steps":16, "step":2, "rhythms":[8, 15], "steps_rhythm":{6:[0, 1, 2], 4:[1], 3:[0, 1]}},
    {"name":"Phobos All #1", "start":160, "steps":43, "step":1, "rhythms":[8, 15], "steps_rhythm":{6:[0, 1, 2], 4:[1], 3:[0, 1]}},
    {"name":"Phobos All #2", "start":159, "steps":23, "step":2, "rhythms":[8, 15], "steps_rhythm":{6:[0, 1, 2], 4:[1], 3:[0, 1]}},
    {"name":"Phobos All #3", "start":159, "steps":16, "step":3, "rhythms":[8, 15], "steps_rhythm":{6:[0, 1, 2], 4:[1], 3:[0, 1]}},
]



new_so_obs_dict = {
"CO2 #1":[[122, 132, 148, 156, 160, 165], 4, 1, 16, 0], #Loic
"CO2 #2":[[156, 132, 118, 140, 154, 158], 4, 1, 16, 0], #Loic - run fewer, at higher latitudes
"CO2 #3":[[156, 116, 118, 169, 154, 140], 4, 1, 16, 0], #Loic
"CO2 #4":[[121, 134, 149, 132, 165, 169], 4, 1, 16, 0], #Loic
"CO2 #5":[[121, 149, 132, 165, 186, 190], 4, 1, 16, 0], #Loic
"CO2 #6":[[121, 148, 149, 155, 164, 165], 4, 1, 16, 0], #Miguel



}
#replace lots of nominal 149s with 148



new_lno_obs_dict = {}
for name, orders_list in lno_normal_orders.items():
    loop = 0
    for orders_dict in orders_list:
        orders = orders_dict["orders"]
        for rhythm in orders_dict["rhythms"]:
            for binning in orders_dict["binning"]:
                loop += 1
                new_lno_obs_dict["%s #%i" %(name, loop)] = [orders, 200, rhythm, int((binning+1)*24./len(orders))]



# """check for repeated orders in lines"""
# for searchIndex, (searchObsName, searchObsData) in enumerate(new_so_obs_dict.items()):
#     searchOrders, _, _, _, _ = searchObsData
#     for eachIndex, (eachObsName, eachObsData) in enumerate(new_so_obs_dict.items()):
#         eachOrders, _, _, _, _ = eachObsData
#         if sorted(searchOrders) == sorted(eachOrders):
#             if searchIndex != eachIndex:
#                 print("######SO Repeats#####")
#                 print("Match found:", searchObsName, "matches", eachObsName, searchObsData, eachObsData)

# for searchIndex, (searchObsName, searchObsData) in enumerate(newLnoObservationDict.items()):
#     searchOrders, _, _, _, _ = searchObsData
#     for eachIndex, (eachObsName, eachObsData) in enumerate(newLnoObservationDict.items()):
#         eachOrders, _, _, _, _ = eachObsData
#         if sorted(searchOrders) == sorted(eachOrders):
#             if searchIndex != eachIndex:
#                 print("######LNO Repeats#####")
#                 print("Match found:", searchObsName, "matches", eachObsName, searchObsData, eachObsData)

