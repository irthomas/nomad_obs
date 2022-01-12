# -*- coding: utf-8 -*-
"""
Created on Wed Dec  8 10:46:39 2021

@author: iant

SCRIPT TO READ IN THE EXISTING SCIENCE TABLES AND GENERATE A FEW SUBDOMAIN ROWS FOR A MINOR PATCH

"""
import os
import re
from datetime import datetime
import numpy as np

# from cop_patching.generate_cop_tables_v05 import readScienceComments, writeTable
# from cop_patching.generate_cop_tables_v05 import read_in_cop_table, getWindowHeight, exec_time, checkExecTime

from nomad_obs.config.paths import BASE_DIRECTORY



# TODO: check number of steps in fast fullscans
# TODO: check fullscans
# TODO: add int time variations?



old_dir_name = "20210320_120000"
temp_dir_name = datetime.now().strftime("%Y%m%d_%H%M%S") + "_new"
new_dir_name = "mtp051_proposed"




lno_centre_rows = [148, 149, 150, 151, 152, 153, 154, 155, 156]


"""new observations"""

#name:[[orders], int time, rhythm, lines, so=0/lno=1]
new_so_obs_dict = {

"6SUBD CO2 H2O #11":[[121, 132, 148, 156, 160, 165], 4, 1, 16, 0], #Proposed by Loic, priority High
"6SUBD CO2 #12":[[156, 132, 118, 140, 154, 158], 4, 1, 16, 0], #Proposed by Loic, priority Middle
"6SUBD CO2 #13":[[156, 132, 118, 169, 154, 140], 4, 1, 16, 0], #Proposed by Loic, priority Middle
"6SUBD CO2 H2O #14":[[121, 134, 148, 132, 165, 169], 4, 1, 16, 0], #Proposed by Loic, priority High
"6SUBD CO2 H2O CO #15":[[121, 132, 148, 165, 186, 190], 4, 1, 16, 0], #Proposed by Loic, priority High
"6SUBD CO2 #16":[[121, 148, 149, 155, 164, 165], 4, 1, 16, 0], #Proposed by Miguel, priority Middle
"6SUBD CO2 #17":[[123, 142, 148, 155, 156, 165], 4, 1, 16, 0], #CO2 full range, priority Middle
"6SUBD CO2 #18":[[154, 155, 156, 157, 158, 159], 4, 1, 16, 0], #Full homopause, priority Low: test
"6SUBD CO2 #19":[[123, 132, 142, 148, 156, 165], 4, 1, 16, 0], #Lower alt, priority Middle
"6SUBD CO2 #20":[[123, 148, 155, 156, 160, 165], 4, 1, 16, 0], #Full range, priority Middle
"6SUBD CO2 #21":[[171, 122, 142, 155, 156, 165], 4, 1, 16, 0], #Full range try 171, priority Low: test
"6SUBD CO2 #22":[[142, 148, 155, 156, 160, 165], 4, 1, 16, 0], #Mid-high, priority Middle
"6SUBD CO2 #23":[[186, 190, 132, 148, 156, 165], 4, 1, 16, 0], #CO2+CO, priority Middle
"6SUBD CO2 #24":[[186, 190, 132, 148, 155, 165], 4, 1, 16, 0], #CO2+CO, priority Middle
"6SUBD CO2 CO #25":[[156, 123, 118, 148, 186, 132], 4, 1, 16, 0], #iso higher alt, priority Middle
"6SUBD CO2 CO #26":[[197, 200, 177, 145, 186, 132], 4, 1, 16, 0], #iso lower alt, priority Low: test
"6SUBD CO2 CO #27":[[156, 123, 118, 148, 186, 132], 4, 1, 16, 0], #iso higher alt, priority Middle
"6SUBD CO2 H2O #12":[[121, 132, 148, 156, 189, 165], 4, 1, 16, 0], #Proposed by Loic, priority High
"6SUBD CO2 H2O #13":[[121, 132, 148, 156, 186, 165], 4, 1, 16, 0], #Proposed by Loic, priority High

"6SUBD CO #1":[[132, 183, 184, 185, 186, 187], 4, 1, 16, 0], #Proposed by Shohei, priority Middle
"6SUBD CO #2":[[123, 132, 183, 184, 185, 186], 4, 1, 16, 0], #Proposed by Shohei, priority Middle
"6SUBD CO #3":[[132, 132, 185, 185, 186, 186], 4, 1, 16, 0], #Proposed by Shohei, priority Middle
"6SUBD CO #4":[[132, 185, 185, 185, 185, 185], 4, 1, 16, 0], #Proposed by Shohei, priority Middle
"6SUBD CO #5":[[132, 186, 186, 186, 186, 186], 4, 1, 16, 0], #Proposed by Shohei, priority Middle
}




#name:[[orders], int time, rhythm, lines, so=0/lno=1]
"""made with make_lno_obs_dict_2022-01.py"""

new_lno_obs_dict = {

"Carbonates #1":[[174, 175, 176, 189, 190, 191], 240, 8, 4, 1],
"Carbonates #2":[[174, 175, 176, 189, 190, 191], 240, 8, 8, 1],
"Carbonates #3":[[174, 175, 176, 189, 190, 191], 240, 8, 12, 1],
"Carbonates #4":[[174, 175, 176, 189, 190, 191], 215, 15, 4, 1],
"Carbonates #5":[[174, 175, 176, 189, 190, 191], 215, 15, 8, 1],
"Carbonates #6":[[174, 175, 176, 189, 190, 191], 215, 15, 12, 1],
"Carbonates #7":[[174, 175, 176], 225, 8, 8, 1],
"Carbonates #8":[[174, 175, 176], 220, 8, 16, 1],
"Carbonates #9":[[174, 175, 176], 190, 15, 8, 1],
"Carbonates #10":[[174, 175, 176], 185, 15, 16, 1],
"Carbonates #11":[[189, 190, 191], 225, 8, 8, 1],
"Carbonates #12":[[189, 190, 191], 220, 8, 16, 1],
"Carbonates #13":[[189, 190, 191], 190, 15, 8, 1],
"Carbonates #14":[[189, 190, 191], 185, 15, 16, 1],
"Phyllosilicates #1":[[189, 190, 191, 192, 193, 201], 240, 8, 4, 1],
"Phyllosilicates #2":[[189, 190, 191, 192, 193, 201], 240, 8, 8, 1],
"Phyllosilicates #3":[[189, 190, 191, 192, 193, 201], 240, 8, 12, 1],
"Phyllosilicates #4":[[189, 190, 191, 192, 193, 201], 215, 15, 4, 1],
"Phyllosilicates #5":[[189, 190, 191, 192, 193, 201], 215, 15, 8, 1],
"Phyllosilicates #6":[[189, 190, 191, 192, 193, 201], 215, 15, 12, 1],
"Phyllosilicates #7":[[190, 191, 192], 225, 8, 8, 1],
"Phyllosilicates #8":[[190, 191, 192], 220, 8, 16, 1],
"Phyllosilicates #9":[[190, 191, 192], 190, 15, 8, 1],
"Phyllosilicates #10":[[190, 191, 192], 185, 15, 16, 1],
"Carb Phyl #1":[[174, 175, 176, 190, 191, 192], 240, 8, 4, 1],
"Carb Phyl #2":[[174, 175, 176, 190, 191, 192], 240, 8, 8, 1],
"Carb Phyl #3":[[174, 175, 176, 190, 191, 192], 240, 8, 12, 1],
"Carb Phyl #4":[[174, 175, 176, 190, 191, 192], 215, 15, 4, 1],
"Carb Phyl #5":[[174, 175, 176, 190, 191, 192], 215, 15, 8, 1],
"Carb Phyl #6":[[174, 175, 176, 190, 191, 192], 215, 15, 12, 1],
"Water Band #1":[[160, 162, 164, 166, 168, 170], 240, 8, 4, 1],
"Water Band #2":[[160, 162, 164, 166, 168, 170], 240, 8, 8, 1],
"Water Band #3":[[160, 162, 164, 166, 168, 170], 240, 8, 12, 1],
"Water Band #4":[[160, 162, 164, 166, 168, 170], 215, 15, 4, 1],
"Water Band #5":[[160, 162, 164, 166, 168, 170], 215, 15, 8, 1],
"Water Band #6":[[160, 162, 164, 166, 168, 170], 215, 15, 12, 1],
"Water Band #7":[[160, 163, 166, 169, 172, 175], 240, 8, 4, 1],
"Water Band #8":[[160, 163, 166, 169, 172, 175], 240, 8, 8, 1],
"Water Band #9":[[160, 163, 166, 169, 172, 175], 240, 8, 12, 1],
"Water Band #10":[[160, 163, 166, 169, 172, 175], 215, 15, 4, 1],
"Water Band #11":[[160, 163, 166, 169, 172, 175], 215, 15, 8, 1],
"Water Band #12":[[160, 163, 166, 169, 172, 175], 215, 15, 12, 1],
"Water Band #13":[[157, 160, 163, 166, 169, 172], 240, 8, 4, 1],
"Water Band #14":[[157, 160, 163, 166, 169, 172], 240, 8, 8, 1],
"Water Band #15":[[157, 160, 163, 166, 169, 172], 240, 8, 12, 1],
"Water Band #16":[[157, 160, 163, 166, 169, 172], 215, 15, 4, 1],
"Water Band #17":[[157, 160, 163, 166, 169, 172], 215, 15, 8, 1],
"Water Band #18":[[157, 160, 163, 166, 169, 172], 215, 15, 12, 1],
"Water Band #19":[[163, 165, 167, 169], 205, 8, 6, 1],
"Water Band #20":[[163, 165, 167, 169], 200, 8, 12, 1],
"Water Band #21":[[163, 165, 167, 169], 210, 15, 6, 1],
"Water Band #22":[[163, 165, 167, 169], 185, 15, 12, 1],
"Water Band #23":[[160, 165, 170], 225, 8, 8, 1],
"Water Band #24":[[160, 165, 170], 220, 8, 16, 1],
"Water Band #25":[[160, 165, 170], 190, 15, 8, 1],
"Water Band #26":[[160, 165, 170], 185, 15, 16, 1],
"Water Band #27":[[163, 168, 173], 225, 8, 8, 1],
"Water Band #28":[[163, 168, 173], 220, 8, 16, 1],
"Water Band #29":[[163, 168, 173], 190, 15, 8, 1],
"Water Band #30":[[163, 168, 173], 185, 15, 16, 1],
"Water Band #31":[[154, 157, 160, 163, 166, 169], 240, 8, 4, 1],
"Water Band #32":[[154, 157, 160, 163, 166, 169], 240, 8, 8, 1],
"Water Band #33":[[154, 157, 160, 163, 166, 169], 240, 8, 12, 1],
"Water Band #34":[[154, 157, 160, 163, 166, 169], 215, 15, 4, 1],
"Water Band #35":[[154, 157, 160, 163, 166, 169], 215, 15, 8, 1],
"Water Band #36":[[154, 157, 160, 163, 166, 169], 215, 15, 12, 1],
"Water pyroxene #1":[[160, 163, 164, 172, 185, 191], 240, 8, 4, 1],
"Water pyroxene #2":[[160, 163, 164, 172, 185, 191], 240, 8, 8, 1],
"Water pyroxene #3":[[160, 163, 164, 172, 185, 191], 240, 8, 12, 1],
"Water pyroxene #4":[[160, 163, 164, 172, 185, 191], 215, 15, 4, 1],
"Water pyroxene #5":[[160, 163, 164, 172, 185, 191], 215, 15, 8, 1],
"Water pyroxene #6":[[160, 163, 164, 172, 185, 191], 215, 15, 12, 1],
"Water pyroxene #7":[[160, 163, 164, 172, 191, 192], 240, 8, 4, 1],
"Water pyroxene #8":[[160, 163, 164, 172, 191, 192], 240, 8, 8, 1],
"Water pyroxene #9":[[160, 163, 164, 172, 191, 192], 240, 8, 12, 1],
"Water pyroxene #10":[[160, 163, 164, 172, 191, 192], 215, 15, 4, 1],
"Water pyroxene #11":[[160, 163, 164, 172, 191, 192], 215, 15, 8, 1],
"Water pyroxene #12":[[160, 163, 164, 172, 191, 192], 215, 15, 12, 1],
"Hydration band #1":[[130, 147, 160], 225, 8, 8, 1],
"Hydration band #2":[[130, 147, 160], 220, 8, 16, 1],
"Hydration band #3":[[130, 147, 160], 190, 15, 8, 1],
"Hydration band #4":[[130, 147, 160], 185, 15, 16, 1],
"Hydration band #5":[[130, 147, 165], 225, 8, 8, 1],
"Hydration band #6":[[130, 147, 165], 220, 8, 16, 1],
"Hydration band #7":[[130, 147, 165], 190, 15, 8, 1],
"Hydration band #8":[[130, 147, 165], 185, 15, 16, 1],
"Hydration band #9":[[130, 148, 160], 225, 8, 8, 1],
"Hydration band #10":[[130, 148, 160], 220, 8, 16, 1],
"Hydration band #11":[[130, 148, 160], 190, 15, 8, 1],
"Hydration band #12":[[130, 148, 160], 185, 15, 16, 1],
"Hydration band #13":[[130, 148, 165], 225, 8, 8, 1],
"Hydration band #14":[[130, 148, 165], 220, 8, 16, 1],
"Hydration band #15":[[130, 148, 165], 190, 15, 8, 1],
"Hydration band #16":[[130, 148, 165], 185, 15, 16, 1],
"Hydrated minerals #1":[[148, 153, 158, 164, 170, 177], 240, 8, 4, 1],
"Hydrated minerals #2":[[148, 153, 158, 164, 170, 177], 240, 8, 8, 1],
"Hydrated minerals #3":[[148, 153, 158, 164, 170, 177], 240, 8, 12, 1],
"Hydrated minerals #4":[[148, 153, 158, 164, 170, 177], 215, 15, 4, 1],
"Hydrated minerals #5":[[148, 153, 158, 164, 170, 177], 215, 15, 8, 1],
"Hydrated minerals #6":[[148, 153, 158, 164, 170, 177], 215, 15, 12, 1],

"169 #1":[[169, 169, 169], 190, 15, 8, 1],
"169 #2":[[169, 169, 169], 185, 15, 16, 1],

}



#fullscans
lno_fullscans = [
    {"name":"Water Band Fullscan #1", "start":160, "steps":11, "step":1, "rhythms":[8, 15], "steps_binning":{6:[0, 1, 2], 4:[0, 1], 3:[0, 1]}},
    {"name":"Water Band Fullscan #1A", "start":160, "steps":12, "step":1, "rhythms":[8, 15], "steps_binning":{6:[0, 1, 2], 4:[0, 1], 3:[0, 1]}},
    {"name":"Water Band Fullscan #2", "start":160, "steps":6, "step":2, "rhythms":[8, 15], "steps_binning":{6:[0, 1, 2], 4:[0, 1], 3:[0, 1]}},
    {"name":"Water Band Fullscan #2A", "start":160, "steps":7, "step":2, "rhythms":[8, 15], "steps_binning":{6:[0, 1, 2], 4:[0, 1], 3:[0, 1]}},
    {"name":"Water Band Fullscan #3", "start":156, "steps":11, "step":2, "rhythms":[8, 15], "steps_binning":{6:[0, 1, 2], 4:[0, 1], 3:[0, 1]}},
    {"name":"Water Band Fullscan #3A", "start":156, "steps":12, "step":2, "rhythms":[8, 15], "steps_binning":{6:[0, 1, 2], 4:[0, 1], 3:[0, 1]}},

    {"name":"Carbonates #1", "start":173, "steps":21, "step":1, "rhythms":[8, 15], "steps_binning":{6:[0, 1, 2], 4:[0, 1], 3:[0, 1]}},
    {"name":"Carbonates #1A", "start":173, "steps":22, "step":1, "rhythms":[8, 15], "steps_binning":{6:[0, 1, 2], 4:[0, 1], 3:[0, 1]}},
    {"name":"Carbonates #2", "start":173, "steps":11, "step":2, "rhythms":[8, 15], "steps_binning":{6:[0, 1, 2], 4:[0, 1], 3:[0, 1]}},
    {"name":"Carbonates #2A", "start":173, "steps":12, "step":2, "rhythms":[8, 15], "steps_binning":{6:[0, 1, 2], 4:[0, 1], 3:[0, 1]}},

    {"name":"Phyllosilicates #1", "start":188, "steps":15, "step":1, "rhythms":[8, 15], "steps_binning":{6:[0, 1, 2], 4:[0, 1], 3:[0, 1]}},
    {"name":"Phyllosilicates #1A", "start":188, "steps":16, "step":1, "rhythms":[8, 15], "steps_binning":{6:[0, 1, 2], 4:[0, 1], 3:[0, 1]}},
    {"name":"Phyllosilicates #2", "start":187, "steps":9, "step":2, "rhythms":[8, 15], "steps_binning":{6:[0, 1, 2], 4:[0, 1], 3:[0, 1]}},
    {"name":"Phyllosilicates #2A", "start":187, "steps":10, "step":2, "rhythms":[8, 15], "steps_binning":{6:[0, 1, 2], 4:[0, 1], 3:[0, 1]}},

    {"name":"Carb Phyl #1", "start":174, "steps":29, "step":1, "rhythms":[8, 15], "steps_binning":{6:[0, 1, 2], 4:[0, 1], 3:[0, 1]}},
    {"name":"Carb Phyl #1A", "start":174, "steps":30, "step":1, "rhythms":[8, 15], "steps_binning":{6:[0, 1, 2], 4:[0, 1], 3:[0, 1]}},
    {"name":"Carb Phyl #2", "start":173, "steps":16, "step":2, "rhythms":[8, 15], "steps_binning":{6:[0, 1, 2], 4:[0, 1], 3:[0, 1]}},
    {"name":"Carb Phyl #2A", "start":173, "steps":17, "step":2, "rhythms":[8, 15], "steps_binning":{6:[0, 1, 2], 4:[0, 1], 3:[0, 1]}},

    {"name":"Hydrated minerals #1", "start":148, "steps":6, "step":6, "rhythms":[8, 15], "steps_binning":{6:[0, 1, 2], 4:[0, 1], 3:[0, 1]}},
    {"name":"Hydrated minerals #1A", "start":148, "steps":7, "step":6, "rhythms":[8, 15], "steps_binning":{6:[0, 1, 2], 4:[0, 1], 3:[0, 1]}},

    {"name":"Phobos All #1", "start":160, "steps":43, "step":1, "rhythms":[8, 15], "steps_binning":{6:[0, 1, 2], 4:[0, 1], 3:[0, 1]}},
    {"name":"Phobos All #1A", "start":160, "steps":44, "step":1, "rhythms":[8, 15], "steps_binning":{6:[0, 1, 2], 4:[0, 1], 3:[0, 1]}},
    {"name":"Phobos All #2", "start":159, "steps":23, "step":2, "rhythms":[8, 15], "steps_binning":{6:[0, 1, 2], 4:[0, 1], 3:[0, 1]}},
    {"name":"Phobos All #2A", "start":159, "steps":24, "step":2, "rhythms":[8, 15], "steps_binning":{6:[0, 1, 2], 4:[0, 1], 3:[0, 1]}},
    {"name":"Phobos All #3", "start":159, "steps":16, "step":3, "rhythms":[8, 15], "steps_binning":{6:[0, 1, 2], 4:[0, 1], 3:[0, 1]}},
    {"name":"Phobos All #3A", "start":159, "steps":17, "step":3, "rhythms":[8, 15], "steps_binning":{6:[0, 1, 2], 4:[0, 1], 3:[0, 1]}},

    {"name":"Phobos All #4", "start":119, "steps":90, "step":1, "rhythms":[8, 15], "steps_binning":{6:[0, 1, 2], 4:[0, 1], 3:[0, 1]}},
    {"name":"Phobos All #4A", "start":119, "steps":90, "step":1, "rhythms":[8, 15], "steps_binning":{6:[0, 1, 2], 4:[0, 1], 3:[0, 1]}},
    {"name":"Phobos All #5", "start":119, "steps":45, "step":2, "rhythms":[8, 15], "steps_binning":{6:[0, 1, 2], 4:[0, 1], 3:[0, 1]}},
    {"name":"Phobos All #5A", "start":119, "steps":45, "step":2, "rhythms":[8, 15], "steps_binning":{6:[0, 1, 2], 4:[0, 1], 3:[0, 1]}},
    {"name":"Phobos All #6", "start":119, "steps":30, "step":3, "rhythms":[8, 15], "steps_binning":{6:[0, 1, 2], 4:[0, 1], 3:[0, 1]}},
    {"name":"Phobos All #6A", "start":119, "steps":30, "step":3, "rhythms":[8, 15], "steps_binning":{6:[0, 1, 2], 4:[0, 1], 3:[0, 1]}},


]



def int_time(rhythm, n_orders, binning):
    # get best integration time
    
    it = 0
    if rhythm == 8:
        if n_orders == 3:
            it = {0:225, 1:220}[binning]
        elif n_orders == 4:
            it = {0:205, 1:200}[binning]
        elif n_orders == 6:
            it = {0:240, 1:240, 2:240}[binning]
    elif rhythm == 15:
        if n_orders == 3:
            it = {0:190, 1:185}[binning]
        elif n_orders == 4:
            it = {0:210, 1:185}[binning]
        elif n_orders == 6:
            it = {0:215, 1:215, 2:215}[binning]
        
    if it > 0:
        return it
    else:
        print("Error: combination not found")
                



def exec_time1(n_acc, window_height, int_time):
    """input COP table values, return microseconds"""
    return int(((n_acc+1.0) * (int_time + 71.0 + 320.0 * (window_height + 1.0) + 1000.0) + 337.0) )

def exec_time(accumulation_count, n_rows, n_subd, integration_time):
    """use real number of rows, time in milliseconds"""
    window_height = np.float32(n_rows - 1.0)
    return (exec_time1(accumulation_count, window_height, integration_time*1000.0) * np.float32(n_subd)) / 1000.0


def n_acc1(max_exec_time, window_height, int_time):
    n_accs_float = (max_exec_time - 337.0) / (int_time + 71.0 + 320.0 * (window_height + 1.0) + 1000.0) - 1.0
    n_accs = int(np.floor(n_accs_float/2.0) * 2.0) #make even for all observations, sbsf 0 or 1
    return n_accs


def n_acc(max_exec_time, n_rows, n_orders, int_time):
    """use real number of rows, times in milliseconds"""
    window_height = np.float32(n_rows - 1.0)
    exec_time_per_order = (max_exec_time * 1000.0) / np.float32(n_orders)
    return n_acc1(exec_time_per_order, window_height, int_time*1000.0)

def try_int(l):
    """try to strip spaces/line feeds and convert all values to ints"""
    
    l2 = []
    for element in l:
        
        # print(element)
        try: 
            element.strip()
        except AttributeError:
            pass

        try:
            element = int(element)
        except ValueError:
            pass
        
        l2.append(element)
    return l2
                        


def parse_science_comment(comment):
    """parse normal obs COP row comments"""
    
    regex = re.compile(r"\S_(\d*)ROWS_(\d*)SECS_(\d*)SUBDS.*EXECTIME=(\d*)MS")
    
    match = regex.findall(comment)[0]
    if len(match) == 4:
        match = try_int(match)
        parsed_dict = {"rows":match[0], "rhythm":match[1], "n_orders":match[2], "exec_time":match[3]}
    
    else:
        print("Error parsing comments")
        
    return parsed_dict


def parse_fullscan_science_comment(comment):
    """parse fullscan COP row comments"""
    
    regex = re.compile(r"\S_(\d*)ORDERS_(\d*)ROWS_(\d*)SECS_(\d*)SUBDS.*EXECTIME=(\d*)MS")
    
    match = regex.findall(comment)[0]
    if len(match) == 5:
        match = try_int(match)
        parsed_dict = {"orders":match[0], "rows":match[1], "rhythm":match[2], "n_orders":match[3], "exec_time":match[4]}
    
    else:
        print("Error parsing comments")
        
    return parsed_dict



def parse_subd_comment(comment):
    """parse subdomain COP row comments"""
    
    regex = re.compile(r"(?:ORDERS (.*) -- (\S*)_(\d*)ROWS_(\d*)SECS_(\d*)SUBDS.*EXECTIME=(\d*)MS|(\S*)_(\d*)-(\d*)-(\d*)ORDERS_(\d*)ROWS_(\d*)SECS_(\d*)SUBDS.*EXECTIME=(\d*)MS|EMPTY ROW)")
    
    match = regex.findall(comment)[0]
    match = [s for s in match if s]
    
    if len(match) == 6:
        #normal obs
        orders = try_int(match[0].split())
        match = try_int(match[1:])
        parsed_dict = {"orders":orders, "name":match[0], "rows":match[1], "rhythm":match[2], "n_orders":match[3], "exec_time":match[4]}
        
    
    elif len(match) == 8:
        match = try_int(match)
        parsed_dict = {"name":match[0], "start":match[1], "step":match[2], "stop":match[3], "rows":match[4], "rhythm":match[5], "n_orders":match[6], "exec_time":match[7]}
    
    elif comment == "EMPTY ROW":
        return {}
        
    else:
        print("Error parsing comments")
        return {}
        
    return parsed_dict




    
def make_cop_path(cop_date, channel, cop_name):
    """make path"""

    return os.path.join(BASE_DIRECTORY, "cop_tables", cop_date, "%s_%s_table.csv" %(channel, cop_name))    
    




def read_cop_csv(csv_filepath):
    """read in table into list of dictionaries"""


    dict_list = []
    with open(csv_filepath) as f:
        lines = f.readlines()
        
        for i, line in enumerate(lines):
            if i == 0:
                header = ["index"]
                header.extend([s.strip() for s in line.split(",")])
                header.append("comment")
                # print(header)
            else:
                index = i - 1
                split = line.split(",")
                if "#" in split[-1]: #if comment
                    row = [index]
                    row.extend([s.strip() for s in split[:-1:]])
                    row.append(split[-1].split("#")[0].strip())
                    row.append(split[-1].split("#")[1].strip())
                    
                else:
                    row = [index]
                    row.extend([s.strip() for s in split])
                    row.append("")

                row = try_int(row)
                    
                line_dict = {h:e for h,e in zip(header, row)}
                dict_list.append(line_dict)
    return dict_list    



def write_cop_csv(csv_filepath, lines, ending="\n"):
    """write COP csv file"""
    
    dir_out = os.path.dirname(csv_filepath)
    os.makedirs(dir_out, exist_ok=True)

    with open(csv_filepath, "w") as f:
        for line in lines:
            f.write(line + ending)





def replace_lines(channel, cop_name, start_row_index, existing_dir, new_lines_dir, merged_dir):
    """write new lines to new proposed directory starting from given index"""
    
    
    csv_filepath_new = make_cop_path(new_lines_dir, channel, cop_name)
    with open(csv_filepath_new) as f:
        lines_new = f.readlines()
    
    csv_filepath = make_cop_path(existing_dir, channel, cop_name)
    with open(csv_filepath) as f:
        lines = f.readlines()
        
        i = start_row_index - 1
        
        for line_new in lines_new:
            lines[i] = line_new
            i += 1
    
    csv_filepath = make_cop_path(merged_dir, channel, cop_name)
    write_cop_csv(csv_filepath, lines, ending="")





def new_subdomain_rows(channel, new_obs_dict, sci_dir_in, subd_dir_out):

    cop_name = "science"
    path = make_cop_path(sci_dir_in, channel, cop_name)
    dict_list = read_cop_csv(path)
    
    
    
    #for science table - split into cals and science
    
    # dict_list_cal = []
    dict_list_sci = []
    for line_dict in dict_list:
        if line_dict["steppingPointer"] == 0 and line_dict["accumulationCount"] > 0: #science
            dict_list_sci.append(line_dict)
        
        # elif line_dict["steppingPointer"] > 0 and line_dict["accumulationCount"] > 0: #cal
        #     dict_list_cal.append(line_dict)
            
    
    lines = []
    
    #match new observations to existing rows
    for name, params in new_obs_dict.items():
        orders = params[0]
        it = params[1] * 1000
        rhythm = params[2]
        d_rows = params[3]
        n_orders = len(orders)
        
        binning = int(d_rows / (24 / n_orders) - 1)
        
        if orders[-1] == 0: #if last order is a dark
            sbsf = 0
        else:
            sbsf = 1
            
            
        science_rows = [0] * 6
        
        #loop through orders, checking if each one exists in the science table. 
        for i_ord, order in enumerate(orders):
            found = False
            
            match_dict = {
                "sbsf":sbsf,
                "aotfPointer":order,
                "steppingPointer":0,
                "binningFactor":binning,
                "integrationTime":it,
            }
            
            for dict_sci in dict_list_sci:
                matches = 0
                for k, v in match_dict.items():
                    if dict_sci[k] == v:
                        # print("true", dict_sci[k], v)
                        matches += 1
                
                if matches == len(match_dict.keys()): #if all match
                    
                    #finally check rhythm and nrows matches
                    comment = dict_sci["comment"]
                    parsed = parse_science_comment(comment)
                    if parsed["rhythm"] == rhythm:
                        
                        if parsed["n_orders"] == n_orders:
                            
                            if parsed["rows"] == d_rows:
                                # print("match_found", match_dict, dict_sci)
                        
                                found = True
                                science_rows[i_ord] = dict_sci["index"]
                                science_comment = comment
    
            if not found:
                print("Error: observation not found in science table", matches, len(match_dict.keys()))
    
    
        line = ",".join([str(i) for i in science_rows]) + " # ORDERS " + " ".join([str(i) for i in orders]) + " -- " + science_comment
        
        lines.append(line)
    
    #write new rows to file
    cop_name = "sub_domain"
    path = make_cop_path(subd_dir_out, channel, cop_name)
    write_cop_csv(path, lines)

    


def new_science_rows(channel, new_obs_dict, sci_dir_out):
    """make science rows normal obs"""
    sci_dict_list = []
    
    for name, params in new_obs_dict.items():
        orders = params[0]
        it = params[1] #milliseconds
        rhythm = params[2]
        d_rows = params[3]
        n_orders = len(orders)
        
        binning = int(d_rows / (24 / n_orders) - 1)
        max_t = rhythm * 1000. - 450. #milliseconds in total for all orders
        n_accs = n_acc(max_t, d_rows, n_orders, it)
        
        if orders[-1] == 0: #if last order is a dark
            sbsf = 0
        else:
            sbsf = 1
            
       
        for i_ord, order in enumerate(orders):
            sci_dict = {
                "degf":0,
                "dvaf":1,
                "sbsf":sbsf,
                "aotfPointer":order,
                "steppingPointer":0,
                "accumulationCount":n_accs,
                "binningFactor":binning,
                "integrationTime":int(it * 1000),
                "other":{"d_rows":d_rows, "rhythm":rhythm, "n_orders":n_orders}
            }
    
            #store if the entry is not yet in the list        
            if sci_dict not in sci_dict_list:
                sci_dict_list.append(sci_dict)
    
    #sort by order
    sci_dict_list = sorted(sci_dict_list, key=lambda d: d["aotfPointer"]) 
    
    
    #now convert dicts to lines
    
    lines = []
    
    for d in sci_dict_list:
        #0,1,1,122,0,18,17,205000 # NADIR_144ROWS_15SECS_3SUBDS -- EXECTIME=14373MS
        
        execution_time = exec_time(d["accumulationCount"], d["other"]["d_rows"], d["other"]["n_orders"], d["integrationTime"]/1000.0)
        comment = "NADIR_%iROWS_%iSECS_%iSUBDS -- EXECTIME=%iMS" \
            %(d["other"]["d_rows"], d["other"]["rhythm"], d["other"]["n_orders"], execution_time)
        line = "%i,%i,%i,%i,%i,%i,%i,%i # %s" %(d["degf"], d["dvaf"], d["sbsf"], d["aotfPointer"], d["steppingPointer"], d["accumulationCount"], d["binningFactor"], d["integrationTime"], comment)
        
        lines.append(line)
    
    #write new rows to file
    cop_name = "science"
    path = make_cop_path(sci_dir_out, channel, cop_name)
    write_cop_csv(path, lines)







def new_fullscan_stepping_rows(channel, fullscan_dict_list, stepping_dir_out):

    # stepValue,steppingParameter,stepCount,stepSpeed
    # 0,INTEGRATION_TIME,0,0 # EMPTY ROW
    # 1,AOTF_IX,10,0 # FULLSCAN_10ORDERS_1SUBDS
    # 1,AOTF_IX,10,2 # FULLSCAN_10ORDERS_3SUBDS
    # 1,AOTF_IX,10,5 # FULLSCAN_10ORDERS_6SUBDS
    
    step_dict_list = []
    
    for lno_fullscan in fullscan_dict_list:
        steps = lno_fullscan["steps"]
        step = lno_fullscan["step"]
        
        for speed, binning in lno_fullscan["steps_binning"].items():
    
            step_dict = {
                "stepValue":step,
                "steppingParameter":"AOTF_IX",
                "stepCount":steps,
                "stepSpeed":speed - 1,
                # "other":{"d_rows":d_rows, "rhythm":rhythm, "n_orders":n_orders}
            }
    
            #store if the entry is not yet in the list        
            if step_dict not in step_dict_list:
                step_dict_list.append(step_dict)
    
    
    lines = []
    
    for d in step_dict_list:
        #1,AOTF_IX,30,0 # FULLSCAN_30ORDERS_1SUBDS
        
        
        comment = "FULLSCAN_%iORDERS_%iSTEPPING_%iSUBDS" \
            %(d["stepCount"], d["stepValue"], d["stepSpeed"]+1)
        line = "%i,%s,%i,%i # %s" %(d["stepValue"], d["steppingParameter"], d["stepCount"], d["stepSpeed"], comment)
        
        lines.append(line)
    
        #write new rows to file
        cop_name = "stepping"
        path = make_cop_path(stepping_dir_out, channel, cop_name)
        write_cop_csv(path, lines)




def find_stepping_line(channel, stepping_dir, stepValue, stepCount, stepSpeed):
    """read in stepping table, find corresponding line"""
    steppingParameter = "AOTF_IX" #for fullscans
    
    cop_name = "stepping"
    path = make_cop_path(stepping_dir, channel, cop_name)
    dict_list = read_cop_csv(path)
    
    found = False
    for d in dict_list:
        if d["stepValue"] == stepValue and d["steppingParameter"] == steppingParameter and d["stepCount"] == stepCount and d["stepSpeed"] == stepSpeed:
            found = True
            index = d["index"]
            
    if found:
        return index
    else:
        print("Error line not found")
    


def new_fullscan_science_rows(channel, fullscan_dict_list, stepping_dir_in, sci_dir_out):
    """make science rows fullscans"""

    # make new science rows
    # 0,1,1,165,5,60,5,190000 # NADIR_FULLSCAN_SLOW_10ORDERS_144ROWS_15SECS_1SUBDS -- EXECTIME=14466MS
    # degf,dvaf,sbsf,aotfPointer,steppingPointer,accumulationCount,binningFactor,integrationTime
    
    sci_dict_list = []
    
    for lno_fullscan in fullscan_dict_list:
        start_order = lno_fullscan["start"]
        stepCount = lno_fullscan["steps"]
        stepValue = lno_fullscan["step"]
    
        for rhythm in lno_fullscan["rhythms"]:
            for stepSpeed, binnings in lno_fullscan["steps_binning"].items():
        
                for binning in binnings:
        
                    
                    it = int_time(rhythm, stepSpeed, binning)
    
    
                    d_rows = int((24 / stepSpeed) * (binning+1))
        
                    max_t = rhythm * 1000. - 450. #milliseconds in total for all orders
                    n_accs = n_acc(max_t, d_rows, stepSpeed, it)
                    
                    steppingPointer = find_stepping_line(channel, stepping_dir_in, stepValue, stepCount, stepSpeed-1)
    
    
                    sci_dict = {
                        "degf":0,
                        "dvaf":1,
                        "sbsf":1,
                        "aotfPointer":start_order,
                        "steppingPointer":steppingPointer,
                        "accumulationCount":n_accs,
                        "binningFactor":binning,
                        "integrationTime":int(it * 1000),
                        "other":{"d_rows":d_rows, "rhythm":rhythm, "stepCount":stepCount, "stepSpeed":stepSpeed}
                    }
    
                    #store if the entry is not yet in the list        
                    if sci_dict not in sci_dict_list:
                        sci_dict_list.append(sci_dict)
        
    #sort by order
    # sci_dict_list = sorted(sci_dict_list, key=lambda d: d["aotfPointer"]) 
    
    
    #now convert dicts to lines
    
    lines = []
    
    for d in sci_dict_list:
        # 0,1,1,165,6,18,17,205000 # NADIR_FULLSCAN_FAST_10ORDERS_144ROWS_15SECS_3SUBDS -- EXECTIME=14373MS
        
        execution_time = exec_time(d["accumulationCount"], d["other"]["d_rows"], d["other"]["stepSpeed"], d["integrationTime"]/1000.0)
        comment = "NADIR_FULLSCAN_FAST_%iORDERS_%iROWS_%iSECS_%iSUBDS -- EXECTIME=%iMS" \
            %(d["other"]["stepCount"], d["other"]["d_rows"], d["other"]["rhythm"], d["other"]["stepSpeed"], execution_time)
        line = "%i,%i,%i,%i,%i,%i,%i,%i # %s" %(d["degf"], d["dvaf"], d["sbsf"], d["aotfPointer"], d["steppingPointer"], d["accumulationCount"], d["binningFactor"], d["integrationTime"], comment)
        
        lines.append(line)
    
    #write new rows to file
    cop_name = "science"
    path = make_cop_path(sci_dir_out, channel, cop_name)
    write_cop_csv(path, lines)



def new_fixed_rows(channel, new_obs_dict, centre_rows, fixed_dir_out):
    """make fixed rows for new normal obs"""

    # windowLineCount,windowLeftTop,detectorSupply,aotfDelay,dataSource,dataValidSource,rythm
    # 143,80,1,1,0,0,15 # DEFAULT_NADIR
    # 15,144,1,1,0,0,1 # DEFAULT_OCCULTATION
    # 143,76,1,1,0,0,4 # NADIR
    # 143,77,1,1,0,0,4 # NADIR
    
    
    fixed_dict_list = []
    for name, params in new_obs_dict.items():
        rhythm = params[2]
        d_rows = params[3]
        
        
        for centre_row in centre_rows:
            
            window_top = centre_row - int(d_rows / 2)
            
            fixed_dict = {
                "windowLineCount":d_rows - 1,
                "windowLeftTop":window_top,
                "detectorSupply":1,
                "aotfDelay":1,
                "dataSource":0,
                "dataValidSource":0,
                "rythm":rhythm
            }
    
            #store if the entry is not yet in the list        
            if fixed_dict not in fixed_dict_list:
                fixed_dict_list.append(fixed_dict)

        #sort by rhythm
        fixed_dict_list = sorted(fixed_dict_list, key=lambda d: d["rythm"]) 
    
    
        #now convert dicts to lines
        lines = []
        
        for d in fixed_dict_list:
            # 143,76,1,1,0,0,4 # NADIR
            
            comment = "TARGETED_NADIR"
            line = "%i,%i,%i,%i,%i,%i,%i # %s" %(d["windowLineCount"], d["windowLeftTop"], d["detectorSupply"], d["aotfDelay"], \
                                                 d["dataSource"], d["dataValidSource"], d["rythm"], comment)
            
            lines.append(line)
        
        #write new rows to file
        cop_name = "fixed"
        path = make_cop_path(fixed_dir_out, channel, cop_name)
        write_cop_csv(path, lines)



def new_fullscan_fixed_rows(channel, fullscan_dict_list, centre_rows):
    """make fixed rows for new fullscan obs"""

    fixed_dict_list = []
    
    for lno_fullscan in fullscan_dict_list:
        for rhythm in lno_fullscan["rhythms"]:
            for stepSpeed, binnings in lno_fullscan["steps_binning"].items():
        
                for binning in binnings:
        
                    d_rows = int((24 / stepSpeed) * (binning+1))
        
                    for centre_row in centre_rows:
                        
                        window_top = centre_row - int(d_rows / 2)
                        
                        fixed_dict = {
                            "windowLineCount":d_rows - 1,
                            "windowLeftTop":window_top,
                            "detectorSupply":1,
                            "aotfDelay":1,
                            "dataSource":0,
                            "dataValidSource":0,
                            "rythm":rhythm
                        }
                
                        #store if the entry is not yet in the list        
                        if fixed_dict not in fixed_dict_list:
                            fixed_dict_list.append(fixed_dict)
    
        #sort by rhythm
        fixed_dict_list = sorted(fixed_dict_list, key=lambda d: d["rythm"]) 
    
        #now convert dicts to lines
        lines = []
        
        for d in fixed_dict_list:
            # 143,76,1,1,0,0,4 # NADIR
            
            comment = "TARGETED_NADIR"
            line = "%i,%i,%i,%i,%i,%i,%i # %s" %(d["windowLineCount"], d["windowLeftTop"], d["detectorSupply"], d["aotfDelay"], \
                                                 d["dataSource"], d["dataValidSource"], d["rythm"], comment)
            
            lines.append(line)
        
        #write new rows to file
        cop_name = "fixed"
        path = make_cop_path(temp_dir_name, channel, cop_name)
        write_cop_csv(path, lines)



def new_subdomain_fullscan_rows(channel, stepping_dir_in, sci_dir_in, subd_dir_out):

    cop_name = "stepping"
    path = make_cop_path(stepping_dir_in, channel, cop_name)
    stepping_dict_list = read_cop_csv(path)
    #get indices of fullscans from stepping table
    fullscan_indices = [d["index"] for d in stepping_dict_list if d["steppingParameter"] == "AOTF_IX"]
    
    
    cop_name = "science"
    channel = "lno"
    path = make_cop_path(sci_dir_in, channel, cop_name)
    dict_list = read_cop_csv(path)
    
    dict_list_fullscan = []
    for line_dict in dict_list:
        if line_dict["steppingPointer"] > 0 and line_dict["accumulationCount"] > 0: #fullscan cal or science
            if line_dict["steppingPointer"] in fullscan_indices:
                dict_list_fullscan.append(line_dict)
        
    
    matching_fullscans = []
    
    for dict_fullscan in dict_list_fullscan:
        comment = dict_fullscan["comment"]
        parsed = parse_fullscan_science_comment(comment)
    
        #search only for the new lines for Phobos obs
        #those where rows < 25 and rhythm > 7
        if parsed["rows"] < 25 and parsed["rhythm"] > 7:
            matching_fullscans.append(dict_fullscan)
    
    
    
    #now convert dicts to lines
    lines = []
    
    for d in matching_fullscans:
        # 89,0,0,0,0,0 #  NADIR_FULLSCAN_FAST_10ORDERS_144ROWS_15SECS_3SUBDS -- EXECTIME=14373MS
        
        first_order = d["aotfPointer"]
        
        stepping_dicts = [d2 for d2 in stepping_dict_list if d2["index"] == d["steppingPointer"]]
        
        if len(stepping_dicts) == 1:
            stepping_dict = stepping_dicts[0]
            
        stepCount = stepping_dict["stepCount"]
        stepValue = stepping_dict["stepValue"]
        
        last_order = first_order + stepCount * stepValue
        
        parsed = parse_fullscan_science_comment(d["comment"])
    
        comment = "TARGETED_NADIR_FULLSCAN_FAST_%i-%i-%iORDERS_%iROWS_%iSECS_%iSUBDS -- EXECTIME=%iMS" \
            %(first_order, stepValue, last_order, parsed["rows"], parsed["rhythm"], parsed["n_orders"], parsed["exec_time"])
    
        
        line = "%i,0,0,0,0,0 # %s" %(d["index"], comment)
        
        lines.append(line)
        
        #write new rows to file
        cop_name = "sub_domain"
        path = make_cop_path(temp_dir_name, channel, cop_name)
        write_cop_csv(path, lines)






existing_dir = old_dir_name
new_lines_dir = temp_dir_name
merged_dir = new_dir_name


# SO patch: subdomain only

sci_dir_in = old_dir_name
subd_dir_out = temp_dir_name

new_subdomain_rows("so", new_so_obs_dict, sci_dir_in, subd_dir_out) #write new lines to temp dir
# then read in old directory, merge new lines and output to new dir
replace_lines("so", "sub_domain", 3204, existing_dir, new_lines_dir, merged_dir) #first line to start replacing rows (as given in notepad++)


"""LNO patch"""
    
"""normal obs"""

# new fixed rows
fixed_dir_out = temp_dir_name

new_fixed_rows("lno", new_lno_obs_dict, lno_centre_rows, fixed_dir_out) #write new lines to temp dir
# then read in old directory, merge new lines and output to new dir
replace_lines("lno", "fixed", 140, existing_dir, new_lines_dir, merged_dir) #first line to start replacing rows (as given in notepad++)



# new science rows
sci_dir_out = temp_dir_name

new_science_rows("lno", new_lno_obs_dict, sci_dir_out) #write new lines to temp dir
# then read in old directory, merge new lines and output to new dir
replace_lines("lno", "science", 3223, existing_dir, new_lines_dir, merged_dir) #first line to start replacing rows (as given in notepad++)



# add new subdomains
sci_dir_in = merged_dir #need to use updated science table
subd_dir_out = temp_dir_name

new_subdomain_rows("lno", new_lno_obs_dict, sci_dir_in, subd_dir_out) #write new lines to temp dir
# then read in old directory, merge new lines and output to new dir
replace_lines("lno", "sub_domain", 3796, existing_dir, new_lines_dir, merged_dir) #first line to start replacing rows (as given in notepad++)





"""fullscans"""
    
# new fixed rows - already covered by previous normal obs
# new_fullscan_fixed_rows("lno", lno_fullscans, lno_centre_rows)
# replace_lines("lno", "fixed", 231, existing_dir, new_lines_dir, merged_dir) #first line to start replacing rows (as given in notepad++)

# new stepping rows
stepping_dir_out = temp_dir_name

new_fullscan_stepping_rows("lno", lno_fullscans, stepping_dir_out) #write new lines to temp dir
# then read in old directory, merge new lines and output to new dir
replace_lines("lno", "stepping", 28, existing_dir, new_lines_dir, merged_dir) #first line to start replacing rows (as given in notepad++)





# new science rows for fullscans (requires stepping to be already updated)
stepping_dir_in = merged_dir #need to use updated stepping table
sci_dir_out = temp_dir_name

existing_dir = merged_dir #use updated lno science table

new_fullscan_science_rows("lno", lno_fullscans, stepping_dir_in, sci_dir_out) #write new lines to temp dir
# then read in old directory, merge new lines and output to new dir
replace_lines("lno", "science", 3455, existing_dir, new_lines_dir, merged_dir) #first line to start replacing rows (as given in notepad++)










# fullscans

# subdomains are just single pointers to these rows
# however they may not be to the same rows in the subdomain and science tables
stepping_dir_in = merged_dir #need to use updated stepping table
sci_dir_in = merged_dir #need to use updated science table
subd_dir_out = temp_dir_name

existing_dir = merged_dir #use updated lno science table

new_subdomain_fullscan_rows("lno", stepping_dir_in, sci_dir_in, subd_dir_out) #write new lines to temp dir
# then read in old directory, merge new lines and output to new dir
replace_lines("lno", "sub_domain", 286, existing_dir, new_lines_dir, merged_dir) #first line to start replacing rows (as given in notepad++)







# check all new rows
print("Checking for errors")

cop_name = "stepping"
path = make_cop_path(new_dir_name, "lno", cop_name)
stepping_dict_list = read_cop_csv(path)

cop_name = "science"
channel = "lno"
path = make_cop_path(new_dir_name, "lno", cop_name)
sci_dict_list = read_cop_csv(path)

cop_name = "sub_domain"
channel = "lno"
path = make_cop_path(new_dir_name, "lno", cop_name)
subd_dict_list_all = read_cop_csv(path)

starting_row = 3793

sub_dict_list = [d for d in subd_dict_list_all if d["index"] > starting_row]

for sub_dict in sub_dict_list:#[0:10]:
# sub_dict = sub_dict_list[0]
    subd_parsed_dict = parse_subd_comment(sub_dict["comment"])
    
    if "orders" in subd_parsed_dict.keys(): #if normal obs
        orders = subd_parsed_dict["orders"]
        order_indices = [sub_dict["science_%i" %i] for i in range(1, 7) if sub_dict["science_%i" %i] > 0]

        # print(sub_dict["comment"])
        
        #check length
        if len(orders) != len(order_indices):
            print("Error: wrong length")
            
        n_orders = subd_parsed_dict["n_orders"]
            
        if n_orders != len(orders):
            print("Error: wrong length")
            print(n_orders, orders)
            
            
        for i, order_index in enumerate(order_indices):
            sci_dict = [d for d in sci_dict_list if d["index"] == order_index][0]
            
            order = sci_dict["aotfPointer"]
            
            if order != orders[i]:
                print("Error: wrong order")
    
            if sci_dict["steppingPointer"] != 0:
                print("Error: stepping obs?")
            
            binning = sci_dict["binningFactor"]
            
            n_rows = (24 / n_orders) * (binning + 1)
            
            if not n_rows.is_integer():
                print("Error: not an integer")
                
            if int(n_rows) != subd_parsed_dict["rows"]:
                print("Error: number of rows")
            
            et = exec_time(sci_dict["accumulationCount"], n_rows, n_orders, sci_dict["integrationTime"]/1000.)/1000.
            
            dt = subd_parsed_dict["rhythm"] - et
            
            if dt > 1.0 or dt < 0.0:
                print("Error: timings wrong")
                print(n_rows, dt)
            
            
        
            
        


# """check for repeated orders in lines"""
# for searchIndex, (searchObsName, searchObsData) in enumerate(new_so_obs_dict.items()):
#     searchOrders, _, _, _, _ = searchObsData
#     for eachIndex, (eachObsName, eachObsData) in enumerate(new_so_obs_dict.items()):
#         eachOrders, _, _, _, _ = eachObsData
#         if sorted(searchOrders) == sorted(eachOrders):
#             if searchIndex != eachIndex:
#                 print("######SO Repeats#####")
#                 print("Match found:", searchObsName, "matches", eachObsName, searchObsData, eachObsData)


# #check for repeats in proposed observations
# for search_index, (search_obs_name, search_obs_data) in enumerate(new_lno_obs_dict.items()):
#     search_orders, _, _, _ = search_obs_data
#     for each_index, (each_obs_name, each_obs_data) in enumerate(new_lno_obs_dict.items()):
#         eachOrders, _, _, _ = eachObsData
#         if sorted(searchOrders) == sorted(eachOrders):
#             if searchIndex != eachIndex:
#                 print("######LNO Repeats#####")
#                 print("Match found:", searchObsName, "matches", eachObsName, searchObsData, eachObsData)

