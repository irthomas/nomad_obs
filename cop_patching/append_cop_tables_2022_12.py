# -*- coding: utf-8 -*-
"""
Created on Wed Dec  8 10:46:39 2021

@author: iant

SCRIPT TO READ IN THE EXISTING SCIENCE TABLES AND GENERATE A FEW SUBDOMAIN ROWS FOR A MINOR PATCH

"""
import os
import re
import sys
from datetime import datetime
import numpy as np

# from cop_patching.generate_cop_tables_v05 import readScienceComments, writeTable
# from cop_patching.generate_cop_tables_v05 import read_in_cop_table, getWindowHeight, exec_time, checkExecTime

from nomad_obs.config.paths import BASE_DIRECTORY



# TODO: check number of steps in fast fullscans
# TODO: check fullscans
# TODO: add int time variations?



old_dir_name = "20220219_061000"
temp_dir_name = datetime.now().strftime("%Y%m%d_%H%M%S") + "_new"
new_dir_name = "mtp063_proposed"


    

lno_centre_rows = [150, 151, 152, 153, 154]
so_centre_rows = [122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132, 133, 134]

#readout wait time, i.e. buffer in milliseconds to add before next integration
readout_wait_time = {"so":150., "lno":450.}


#index of rows available for overwriting - indices are from notepad row numbers
#add 1 to end of each range
available_cop_rows = {
    "lno":{
        "fixed":[*range(32, 47), *range(230, 258)],
        "science":[*range(3679, 4098)],
        "sub_domain":[*range(3899, 4098)] #overwrite fast miniscans and nadir with only 1 diffraction order
    },

    "so":{
        "fixed":[*range(111, 258)],
        "science":[*range(3600, 4098)],
        "sub_domain":[*range(3229, 4098)]
    }

}



MAKE_TABLES = True
# MAKE_TABLES = False

"""new observations"""

#name:[[orders], int time, rhythm, lines, so=0/lno=1]
new_so_obs_dict = {

"6SUBD CO2 CO #28":[[186, 185, 148, 132, 190, 155], 4, 1, 16, 0], #co isotopes and temperature, priority high
"6SUBD CO2 CO #29":[[186, 185, 148, 132, 140, 142], 4, 1, 16, 0], #co isotopes and temperature, priority high
"6SUBD CO2 CO #30":[[186, 185, 148, 132, 140, 165], 4, 1, 16, 0], #co isotopes and temperature, priority low (backup)
"6SUBD CO2 CO #31":[[186, 185, 148, 132, 142, 165], 4, 1, 16, 0], #co isotopes and temperature, priority low (backup)
"6SUBD CO2 CO #32":[[186, 185, 148, 132, 140, 155], 4, 1, 16, 0], #co isotopes and temperature, priority low (backup)
"6SUBD CO2 CO #33":[[186, 185, 148, 132, 142, 155], 4, 1, 16, 0], #co isotopes and temperature, priority low (backup)


"6SUBD Nominal #52":[[121, 134, 169, 129, 148, 165], 4, 1, 16, 0], #148 instead of 149, priority high
"6SUBD Nominal #53":[[121, 136, 169, 129, 148, 165], 4, 1, 16, 0], #148 instead of 149, priority high



"6SUBD Nominal 4 line #1":[[121, 134, 169, 129, 148, 165], 4, 1, 4, 0], #148 instead of 149, priority test with 4 lines
"6SUBD Nominal 4 line #2":[[121, 136, 169, 129, 148, 165], 4, 1, 4, 0], #148 instead of 149, priority test with 4 lines
  
    
}




#name:[[orders], int time, rhythm, lines, so=0/lno=1]
"""made with make_lno_obs_dict_2022-01.py"""

new_lno_obs_dict = {

"Carbonates #15":[[174, 175, 176, 189, 190, 191], 540, 30, 8],
"Carbonates #17":[[174, 175, 176, 189, 190, 191], 540, 30, 12],
"Carbonates #18":[[174, 175, 176, 189, 190, 191], 580, 60, 8],
"Carbonates #19":[[174, 175, 176, 189, 190, 191], 515, 60, 12],
"Carbonates #20":[[174, 175, 176, 189, 190, 191], 190, 30, 12],
"Carbonates #21":[[174, 175, 176, 189, 190, 191], 215, 60, 12],
"Carbonates #22":[[174, 175, 176], 215, 30, 8],
"Carbonates #23":[[174, 175, 176], 185, 30, 16],
"Carbonates #24":[[174, 175, 176], 205, 60, 8],
"Carbonates #25":[[174, 175, 176], 190, 60, 16],
"Carbonates #26":[[189, 190, 191], 215, 30, 8],
"Carbonates #27":[[189, 190, 191], 185, 30, 16],
"Carbonates #28":[[189, 190, 191], 205, 60, 8],
"Carbonates #29":[[189, 190, 191], 190, 60, 16],
"Phyllosilicates #11":[[189, 190, 191, 192, 193, 201], 540, 30, 8],
"Phyllosilicates #13":[[189, 190, 191, 192, 193, 201], 540, 30, 12],
"Phyllosilicates #14":[[189, 190, 191, 192, 193, 201], 580, 60, 8],
"Phyllosilicates #15":[[189, 190, 191, 192, 193, 201], 515, 60, 12],
"Phyllosilicates #16":[[189, 190, 191, 192, 193, 201], 190, 30, 12],
"Phyllosilicates #17":[[189, 190, 191, 192, 193, 201], 215, 60, 12],
"Phyllosilicates #18":[[190, 191, 192], 185, 30, 16],
"Phyllosilicates #19":[[190, 191, 192], 190, 60, 16],
"Carb Phyl #7":[[174, 175, 176, 190, 191, 192], 540, 30, 8],
"Carb Phyl #9":[[174, 175, 176, 190, 191, 192], 540, 30, 12],
"Carb Phyl #10":[[174, 175, 176, 190, 191, 192], 580, 60, 8],
"Carb Phyl #11":[[174, 175, 176, 190, 191, 192], 515, 60, 12],
"Carb Phyl #12":[[174, 175, 176, 190, 191, 192], 190, 30, 12],
"Carb Phyl #13":[[174, 175, 176, 190, 191, 192], 215, 60, 12],
"Water Band #37":[[160, 162, 164, 166, 168, 170], 540, 30, 8],
"Water Band #39":[[160, 162, 164, 166, 168, 170], 540, 30, 12],
"Water Band #40":[[160, 162, 164, 166, 168, 170], 580, 60, 8],
"Water Band #41":[[160, 162, 164, 166, 168, 170], 515, 60, 12],
"Water Band #42":[[160, 163, 166, 169, 172, 175], 540, 30, 8],
"Water Band #43":[[160, 163, 166, 169, 172, 175], 540, 30, 12],
"Water Band #44":[[160, 163, 166, 169, 172, 175], 580, 60, 8],
"Water Band #45":[[160, 163, 166, 169, 172, 175], 515, 60, 12],
"Water Band #46":[[157, 160, 163, 166, 169, 172], 540, 30, 8],
"Water Band #47":[[157, 160, 163, 166, 169, 172], 540, 30, 12],
"Water Band #48":[[157, 160, 163, 166, 169, 172], 580, 60, 8],
"Water Band #49":[[157, 160, 163, 166, 169, 172], 515, 60, 12],
"Water Band #50":[[154, 157, 160, 163, 166, 169], 540, 30, 8],
"Water Band #51":[[154, 157, 160, 163, 166, 169], 540, 30, 12],
"Water Band #52":[[154, 157, 160, 163, 166, 169], 580, 60, 8],
"Water Band #53":[[154, 157, 160, 163, 166, 169], 515, 60, 12],
"Water Band #54":[[160, 162, 164, 166, 168, 170], 190, 30, 12],
"Water Band #55":[[160, 162, 164, 166, 168, 170], 215, 60, 12],
"Water Band #56":[[160, 163, 166, 169, 172, 175], 190, 30, 12],
"Water Band #57":[[160, 163, 166, 169, 172, 175], 215, 60, 12],
"Water Band #58":[[157, 160, 163, 166, 169, 172], 190, 30, 12],
"Water Band #59":[[157, 160, 163, 166, 169, 172], 215, 60, 12],
"Water Band #60":[[154, 157, 160, 163, 166, 169], 190, 30, 12],
"Water Band #61":[[154, 157, 160, 163, 166, 169], 215, 60, 12],
"Water Band #62":[[163, 165, 167, 169], 205, 30, 12],
"Water Band #63":[[163, 165, 167, 169], 485, 30, 12],
"Water Band #64":[[163, 165, 167, 169], 210, 60, 12],
"Water Band #65":[[163, 165, 167, 169], 590, 60, 12],
"Water Band #66":[[160, 165, 170], 215, 30, 8],
"Water Band #67":[[160, 165, 170], 185, 30, 16],
"Water Band #68":[[160, 165, 170], 205, 60, 8],
"Water Band #69":[[160, 165, 170], 190, 60, 16],
"Water Band #70":[[163, 168, 173], 215, 30, 8],
"Water Band #71":[[163, 168, 173], 185, 30, 16],
"Water Band #72":[[163, 168, 173], 205, 60, 8],
"Water Band #73":[[163, 168, 173], 190, 60, 16],
"Water pyroxene #13":[[160, 163, 164, 172, 185, 191], 540, 30, 8],
"Water pyroxene #15":[[160, 163, 164, 172, 185, 191], 540, 30, 12],
"Water pyroxene #16":[[160, 163, 164, 172, 185, 191], 580, 60, 8],
"Water pyroxene #17":[[160, 163, 164, 172, 185, 191], 515, 60, 12],
"Water pyroxene #18":[[160, 163, 164, 172, 191, 192], 540, 30, 8],
"Water pyroxene #19":[[160, 163, 164, 172, 191, 192], 540, 30, 12],
"Water pyroxene #20":[[160, 163, 164, 172, 191, 192], 580, 60, 8],
"Water pyroxene #21":[[160, 163, 164, 172, 191, 192], 515, 60, 12],
"Water pyroxene #22":[[160, 163, 164, 172, 185, 191], 190, 30, 12],
"Water pyroxene #23":[[160, 163, 164, 172, 185, 191], 215, 60, 12],
"Water pyroxene #24":[[160, 163, 164, 172, 191, 192], 190, 30, 12],
"Water pyroxene #25":[[160, 163, 164, 172, 191, 192], 215, 60, 12],
"Hydration band #17":[[130, 147, 160], 215, 30, 8],
"Hydration band #19":[[130, 147, 160], 185, 30, 16],
"Hydration band #20":[[130, 147, 160], 205, 60, 8],
"Hydration band #21":[[130, 147, 160], 190, 60, 16],
"Hydration band #22":[[130, 147, 165], 215, 30, 8],
"Hydration band #23":[[130, 147, 165], 185, 30, 16],
"Hydration band #24":[[130, 147, 165], 205, 60, 8],
"Hydration band #25":[[130, 147, 165], 190, 60, 16],
"Hydration band #26":[[130, 148, 160], 215, 30, 8],
"Hydration band #27":[[130, 148, 160], 185, 30, 16],
"Hydration band #28":[[130, 148, 160], 205, 60, 8],
"Hydration band #29":[[130, 148, 160], 190, 60, 16],
"Hydration band #30":[[130, 148, 165], 215, 30, 8],
"Hydration band #31":[[130, 148, 165], 185, 30, 16],
"Hydration band #32":[[130, 148, 165], 205, 60, 8],
"Hydration band #33":[[130, 148, 165], 190, 60, 16],
"Hydrated minerals #7":[[148, 153, 158, 164, 170, 177], 540, 30, 8],
"Hydrated minerals #9":[[148, 153, 158, 164, 170, 177], 540, 30, 12],
"Hydrated minerals #10":[[148, 153, 158, 164, 170, 177], 580, 60, 8],
"Hydrated minerals #11":[[148, 153, 158, 164, 170, 177], 515, 60, 12],
"Hydrated minerals #12":[[148, 153, 158, 164, 170, 177], 190, 30, 12],
"Hydrated minerals #13":[[148, 153, 158, 164, 170, 177], 215, 60, 12],
"Hydrated single orders #1":[[148, 153, 164], 215, 30, 8],
"Hydrated single orders #2":[[148, 153, 164], 575, 30, 8],
"Hydrated single orders #3":[[148, 153, 164], 185, 30, 16],
"Hydrated single orders #4":[[148, 153, 164], 510, 30, 16],
"Hydrated single orders #5":[[148, 153, 164], 205, 60, 8],
"Hydrated single orders #6":[[148, 153, 164], 505, 60, 8],
"Hydrated single orders #7":[[148, 153, 164], 190, 60, 16],
"Hydrated single orders #8":[[148, 153, 164], 595, 60, 16],
"Hydrated single orders #9":[[158, 170, 164], 215, 30, 8],
"Hydrated single orders #10":[[158, 170, 164], 575, 30, 8],
"Hydrated single orders #11":[[158, 170, 164], 185, 30, 16],
"Hydrated single orders #12":[[158, 170, 164], 510, 30, 16],
"Hydrated single orders #13":[[158, 170, 164], 205, 60, 8],
"Hydrated single orders #14":[[158, 170, 164], 505, 60, 8],
"Hydrated single orders #15":[[158, 170, 164], 190, 60, 16],
"Hydrated single orders #16":[[158, 170, 164], 595, 60, 16],
"Hydrated single orders #17":[[148, 164, 177], 215, 30, 8],
"Hydrated single orders #18":[[148, 164, 177], 575, 30, 8],
"Hydrated single orders #19":[[148, 164, 177], 185, 30, 16],
"Hydrated single orders #20":[[148, 164, 177], 510, 30, 16],
"Hydrated single orders #21":[[148, 164, 177], 205, 60, 8],
"Hydrated single orders #22":[[148, 164, 177], 505, 60, 8],
"Hydrated single orders #23":[[148, 164, 177], 190, 60, 16],
"Hydrated single orders #24":[[148, 164, 177], 595, 60, 16],
"Hydrated single orders #25":[[148, 153, 164], 535, 15, 8],
"Hydrated single orders #26":[[148, 153, 164], 530, 15, 16],
"Hydrated single orders #27":[[158, 170, 164], 535, 15, 8],
"Hydrated single orders #28":[[158, 170, 164], 530, 15, 16],
"Hydrated single orders #29":[[148, 164, 177], 535, 15, 8],
"Hydrated single orders #30":[[148, 164, 177], 530, 15, 16],




"Surface Ice 3SUBD #2":[[189, 132, 133], 205, 15, 144],
"Surface Ice 3SUBD #3":[[193, 132, 133], 205, 15, 144],
"Surface Ice 2SUBD #1":[[132, 133], 200, 15, 144],

}



#fullscans
lno_fullscans = [
    # {"name":"Water Band Fullscan #1A", "start":159, "steps":12, "step":1, "rhythms":[30, 60], "steps_binning":{6:[1, 2], 4:[1], 3:[0, 1]}, "approx_it":[200, 500]},
    {"name":"Water Band Fullscan #2A", "start":158, "steps":7, "step":2, "rhythms":[30, 60], "steps_binning":{6:[1, 2], 3:[0, 1]}, "approx_it":[500]},
    {"name":"Water Band Fullscan #3A", "start":154, "steps":12, "step":2, "rhythms":[30, 60], "steps_binning":{6:[1, 2], 3:[0, 1]}, "approx_it":[500]},

    # {"name":"Carbonates #1A", "start":172, "steps":22, "step":1, "rhythms":[30, 60], "steps_binning":{6:[1, 2], 4:[1], 3:[0, 1]}, "approx_it":[200, 500]},
    {"name":"Carbonates #2A", "start":171, "steps":12, "step":2, "rhythms":[30, 60], "steps_binning":{6:[1, 2], 3:[0, 1]}, "approx_it":[500]},

    # {"name":"Phyllosilicates #1A", "start":187, "steps":16, "step":1, "rhythms":[30, 60], "steps_binning":{6:[1, 2], 4:[1], 3:[0, 1]}, "approx_it":[200, 500]},
    {"name":"Phyllosilicates #2A", "start":185, "steps":10, "step":2, "rhythms":[30, 60], "steps_binning":{6:[1, 2], 3:[0, 1]}, "approx_it":[500]},

    # {"name":"Carb Phyl #1A", "start":173, "steps":30, "step":1, "rhythms":[30, 60], "steps_binning":{6:[1, 2], 4:[1], 3:[0, 1]}, "approx_it":[200, 500]},
    {"name":"Carb Phyl #2A", "start":171, "steps":17, "step":2, "rhythms":[30, 60], "steps_binning":{6:[1, 2], 3:[0, 1]}, "approx_it":[500]},

    {"name":"Hydrated minerals #1A", "start":142, "steps":7, "step":6, "rhythms":[30, 60], "steps_binning":{6:[1, 2], 3:[0, 1]}, "approx_it":[200, 500]},

#     {"name":"Phobos All #1A", "start":159, "steps":44, "step":1, "rhythms":[30, 60], "steps_binning":{6:[0, 1, 2], 4:[0, 1], 3:[0, 1]}},
#     {"name":"Phobos All #2A", "start":157, "steps":24, "step":2, "rhythms":[30, 60], "steps_binning":{6:[0, 1, 2], 4:[0, 1], 3:[0, 1]}},
#     {"name":"Phobos All #3A", "start":156, "steps":17, "step":3, "rhythms":[30, 60], "steps_binning":{6:[0, 1, 2], 4:[0, 1], 3:[0, 1]}},

#     {"name":"Phobos All #4A", "start":118, "steps":90, "step":1, "rhythms":[30, 60], "steps_binning":{6:[0, 1, 2], 4:[0, 1], 3:[0, 1]}},
#     {"name":"Phobos All #5A", "start":117, "steps":45, "step":2, "rhythms":[30, 60], "steps_binning":{6:[0, 1, 2], 4:[0, 1], 3:[0, 1]}},
#     {"name":"Phobos All #6A", "start":116, "steps":30, "step":3, "rhythms":[30, 60], "steps_binning":{6:[0, 1, 2], 4:[0, 1], 3:[0, 1]}},


]



def get_int_time(rhythm, n_orders, binning, approx_it):
    # get best integration time, only for making the fullscans
    
    it = 0
    if rhythm == 8:
        if n_orders == 3:
            it = {(0, 200):225, (1, 200):220}[(binning, approx_it)]
        elif n_orders == 4:
            it = {(0, 200):205, (1, 200):200}[(binning, approx_it)]
        elif n_orders == 6:
            it = {(0, 200):240, (1, 200):240, (2, 200):240}[(binning, approx_it)]
    elif rhythm == 15:
        if n_orders == 3:
            it = {(0, 200):190, (1, 200):185}[(binning, approx_it)]
        elif n_orders == 4:
            it = {(0, 200):210, (1, 200):185}[(binning, approx_it)]
        elif n_orders == 6:
            it = {(0, 200):215, (1, 200):215, (2, 200):215}[(binning, approx_it)]


    #new for MTP063
    elif rhythm == 30:
        if n_orders == 3:
            it = {(0,200):215, (0,500):575, (1, 200):185, (1, 500):510}[(binning, approx_it)]
        elif n_orders == 4:
            it = {(1, 200):205, (1, 500):485}[(binning, approx_it)]
        elif n_orders == 6:
            it = {(1, 200):210, (1, 500):540, (2, 200):190, (2, 500):540}[(binning, approx_it)]
    elif rhythm == 60:
        if n_orders == 3:
            it = {(0,200):205, (0,500):505, (1, 200):190, (1, 500):595}[(binning, approx_it)]
        elif n_orders == 4:
            it = {(1, 200):210, (1, 500):590}[(binning, approx_it)]
        elif n_orders == 6:
            it = {(1, 200):190, (1, 500):580, (2, 200):215, (2, 500):515}[(binning, approx_it)]
        
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





def replace_lines(channel, cop_name, available_rows, existing_dir, new_lines_dir, merged_dir):
    """merge existing file with new file, writing new lines to new proposed file filling in the available rows"""
    
    
    csv_filepath_new = make_cop_path(new_lines_dir, channel, cop_name)
    with open(csv_filepath_new) as f:
        lines_new = f.readlines()
    
    csv_filepath = make_cop_path(existing_dir, channel, cop_name)
    with open(csv_filepath) as f:
        lines = f.readlines()
        
       
        i = 0
        for line_new in lines_new:
            if len(available_rows) <= i:
                print("Error: %i lines in file %s, insufficient lines to write index %i (%i required)" %(len(lines), csv_filepath, i, len(lines_new)))
            lines[available_rows[i] - 1] = line_new
            i += 1
    
    csv_filepath = make_cop_path(merged_dir, channel, cop_name)
    write_cop_csv(csv_filepath, lines, ending="")

    rows_used = available_rows[:i]
    rows_unused = available_rows[i:]

    return rows_used, rows_unused


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
                print("Error: observation not found in science table", matches, match_dict)
    
    
        line = ",".join([str(i) for i in science_rows]) + " # ORDERS " + " ".join([str(i) for i in orders]) + " -- " + science_comment
        
        lines.append(line)
    
    #write new rows to file
    cop_name = "sub_domain"
    path = make_cop_path(subd_dir_out, channel, cop_name)
    write_cop_csv(path, lines)
    print("%i %s %s lines written to file %s" %(len(lines), channel, cop_name, path))

    


def new_science_rows(channel, new_obs_dict, old_sci_dir, sci_dir_out):
    """make science rows normal obs"""


    #read in old science table
    cop_name = "science"
    path = make_cop_path(old_sci_dir, channel, cop_name)
    existing_dict_list = read_cop_csv(path)
    
    #remove index and comment dict entry from existing dict list for comparison with new rows
    for existing_dict in existing_dict_list:
        existing_dict.pop("index")
        existing_dict.pop("comment")


    sci_dict_list = []
    
    buffer_time = readout_wait_time[channel]
    
    for name, params in new_obs_dict.items():
        orders = params[0]
        it = params[1] #milliseconds
        rhythm = params[2]
        d_rows = params[3]
        n_orders = len(orders)
        
        binning = int(d_rows / (24 / n_orders) - 1)
        max_t = rhythm * 1000. - buffer_time #milliseconds in total for all orders
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
                
                #check if entry already in existing science table
                #remove 'other' key
                sci_dict_to_compare = {k:sci_dict[k] for k in sci_dict if k != "other"}
                
                if sci_dict_to_compare not in existing_dict_list:
                    sci_dict_list.append(sci_dict)

                # else:
                #     print("Warning line already in science table", sci_dict)
                
    
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
    print("%i %s %s lines written to file %s" %(len(lines), channel, cop_name, path))







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
    print("%i %s %s lines written to file %s" %(len(lines), channel, cop_name, path))




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
                    
                    for approx_it in lno_fullscan["approx_it"]:
        
                    
                        it = get_int_time(rhythm, stepSpeed, binning, approx_it)
        
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
    print("%i %s %s lines written to file %s" %(len(lines), channel, cop_name, path))



def new_fixed_rows(channel, new_obs_dict, centre_rows, old_fixed_dir, fixed_dir_out):
    """make fixed rows for new normal obs"""

    # windowLineCount,windowLeftTop,detectorSupply,aotfDelay,dataSource,dataValidSource,rythm
    # 143,80,1,1,0,0,15 # DEFAULT_NADIR
    # 15,144,1,1,0,0,1 # DEFAULT_OCCULTATION
    # 143,76,1,1,0,0,4 # NADIR
    # 143,77,1,1,0,0,4 # NADIR


    #read in old fixed table
    cop_name = "fixed"
    path = make_cop_path(old_fixed_dir, channel, cop_name)
    existing_dict_list = read_cop_csv(path)
    
    #remove index and comment dict entry from existing dict list for comparison with new rows
    for existing_dict in existing_dict_list:
        existing_dict.pop("index")
        existing_dict.pop("comment")
   
    
    
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
                
                #check if entry already in existing fixed table
                if fixed_dict not in existing_dict_list:
                
                    fixed_dict_list.append(fixed_dict)
                # else:
                #     print("Warning line already in fixed table", fixed_dict)

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
    print("%i %s %s lines written to file %s" %(len(lines), channel, cop_name, path))



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
    print("%i %s %s lines written to file %s" %(len(lines), channel, cop_name, path))



def new_subdomain_fullscan_rows(channel, stepping_dir_in, sci_dir_in, subd_dir_out, science_rows_to_add=[]):

    
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
    for row, line_dict in enumerate(dict_list):
        
        if len(science_rows_to_add) > 0:
            if row not in science_rows_to_add:
                continue
        
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
    print("%i %s %s lines written to file %s" %(len(lines), channel, cop_name, path))



if __name__ == "__main__":

    if MAKE_TABLES:
    
        existing_dir = old_dir_name
        new_lines_dir = temp_dir_name
        merged_dir = new_dir_name
        
        
        """ SO patch"""
        
        """normal obs"""

        # new fixed rows
        fixed_dir_out = temp_dir_name
        
        rows_to_replace = available_cop_rows["so"]["fixed"]

        
        new_fixed_rows("so", new_so_obs_dict, so_centre_rows, existing_dir, fixed_dir_out) #write new lines to temp dir
        # then read in old directory, merge new lines and output to new dir
        replace_lines("so", "fixed", rows_to_replace, existing_dir, new_lines_dir, merged_dir) #first line to start replacing rows (as given in notepad++)




        # new science rows
        sci_dir_out = temp_dir_name
        rows_to_replace = available_cop_rows["so"]["science"]
        
        new_science_rows("so", new_so_obs_dict, existing_dir, sci_dir_out) #write new lines to temp dir
        # then read in old directory, merge new lines and output to new dir
        replace_lines("so", "science", rows_to_replace, existing_dir, new_lines_dir, merged_dir) #first line to start replacing rows (as given in notepad++)
        
        #rename new file to avoid copying over
        csv_filepath = make_cop_path(new_lines_dir, "so", "science")
        csv_filepath2 = make_cop_path(new_lines_dir, "so", "science_new")
        os.rename(csv_filepath, csv_filepath2)
        
        
        
        # add new subdomains
        sci_dir_in = merged_dir #need to use updated science table
        subd_dir_out = temp_dir_name
        rows_to_replace = available_cop_rows["so"]["sub_domain"]
        
        new_subdomain_rows("so", new_so_obs_dict, sci_dir_in, subd_dir_out) #write new lines to temp dir
        # then read in old directory, merge new lines and output to new dir
        replace_lines("so", "sub_domain", rows_to_replace, existing_dir, new_lines_dir, merged_dir) #first line to start replacing rows (as given in notepad++)
        
        
        """LNO patch"""
            
        """normal obs"""
        
        # new fixed rows
        fixed_dir_out = temp_dir_name
        rows_to_replace = available_cop_rows["lno"]["fixed"]
        
        new_fixed_rows("lno", new_lno_obs_dict, lno_centre_rows, existing_dir, fixed_dir_out) #write new lines to temp dir
        # then read in old directory, merge new lines and output to new dir
        replace_lines("lno", "fixed", rows_to_replace, existing_dir, new_lines_dir, merged_dir) #first line to start replacing rows (as given in notepad++)
        
        
        
        # new science rows
        sci_dir_out = temp_dir_name
        rows_to_replace = available_cop_rows["lno"]["science"]
        
        new_science_rows("lno", new_lno_obs_dict, existing_dir, sci_dir_out) #write new lines to temp dir
        # then read in old directory, merge new lines and output to new dir
        lno_science_used_rows, lno_science_unused_rows = replace_lines("lno", "science", rows_to_replace, existing_dir, new_lines_dir, merged_dir) #first line to start replacing rows (as given in notepad++)
        
        #rename new file to avoid copying over
        csv_filepath = make_cop_path(new_lines_dir, "lno", "science")
        csv_filepath2 = make_cop_path(new_lines_dir, "lno", "science_new")
        os.rename(csv_filepath, csv_filepath2)
        
        
        # add new subdomains
        sci_dir_in = merged_dir #need to use updated science table
        subd_dir_out = temp_dir_name
        rows_to_replace = available_cop_rows["lno"]["sub_domain"]
        
        new_subdomain_rows("lno", new_lno_obs_dict, sci_dir_in, subd_dir_out) #write new lines to temp dir
        # then read in old directory, merge new lines and output to new dir
        lno_sub_domain_used_rows, lno_sub_domain_unused_rows = replace_lines("lno", "sub_domain", rows_to_replace, existing_dir, new_lines_dir, merged_dir) #first line to start replacing rows (as given in notepad++)
        
        #rename new file to avoid copying over
        csv_filepath = make_cop_path(new_lines_dir, "lno", "sub_domain")
        csv_filepath2 = make_cop_path(new_lines_dir, "lno", "sub_domain_new")
        os.rename(csv_filepath, csv_filepath2)
        
        
        
        
        """fullscans"""
            
        # new fixed rows - already covered by previous normal obs
        # new_fullscan_fixed_rows("lno", lno_fullscans, lno_centre_rows)
        # replace_lines("lno", "fixed", 231, existing_dir, new_lines_dir, merged_dir) #first line to start replacing rows (as given in notepad++)
        
        # new stepping rows
        # stepping_dir_out = temp_dir_name
        # rows_to_replace = available_cop_rows["lno"]["stepping"]
        
        # new_fullscan_stepping_rows("lno", lno_fullscans, stepping_dir_out) #write new lines to temp dir
        # then read in old directory, merge new lines and output to new dir
        # replace_lines("lno", "stepping", rows_to_replace, existing_dir, new_lines_dir, merged_dir) #first line to start replacing rows (as given in notepad++)
        
        
        
        
        
        # new science rows for fullscans (requires stepping to be already updated)
        # stepping_dir_in = merged_dir #need to use updated stepping table
        stepping_dir_in = old_dir_name #use old stepping table
        sci_dir_out = temp_dir_name
        
        existing_dir = merged_dir #use updated lno science table
        
        new_fullscan_science_rows("lno", lno_fullscans, stepping_dir_in, sci_dir_out) #write new lines to temp dir
        # then read in old directory, merge new lines and output to new dir
        lno_science_used_rows, lno_science_unused_rows = replace_lines("lno", "science", lno_science_unused_rows, existing_dir, new_lines_dir, merged_dir) #first line to start replacing rows (as given in notepad++)
        
    
    
        
        
        # subdomains are just single pointers to these rows
        # however they may not be to the same rows in the subdomain and science tables
        stepping_dir_in = old_dir_name #need to use old stepping table
        sci_dir_in = merged_dir #need to use updated science table
        subd_dir_out = temp_dir_name
        
        existing_dir = merged_dir #use updated lno science table
        
        new_subdomain_fullscan_rows("lno", stepping_dir_in, sci_dir_in, subd_dir_out, science_rows_to_add=lno_science_used_rows) #write new lines to temp dir
        # then read in old directory, merge new lines and output to new dir
        replace_lines("lno", "sub_domain", lno_sub_domain_unused_rows, existing_dir, new_lines_dir, merged_dir) #first line to start replacing rows (as given in notepad++)
        
    
    



    """check all new LNO rows"""

    print("Checking for errors")
    
    cop_name = "stepping"
    path = make_cop_path(old_dir_name, "lno", cop_name)
    stepping_dict_list = read_cop_csv(path)
    
    cop_name = "science"
    channel = "lno"
    path = make_cop_path(new_dir_name, "lno", cop_name)
    sci_dict_list = read_cop_csv(path)
    
    cop_name = "sub_domain"
    channel = "lno"
    path = make_cop_path(new_dir_name, "lno", cop_name)
    subd_dict_list_all = read_cop_csv(path)
    
    subd_rows_to_check = list(range(284, 508)) + list(range(3794, 4095))
    # subd_rows_to_check = list(range(284, 305))
    
    sub_dict_list = [d for d in subd_dict_list_all if d["index"] in subd_rows_to_check]
    
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
                sys.exit()
                
            n_orders = subd_parsed_dict["n_orders"]
                
            if n_orders != len(orders):
                print("Error: wrong length")
                print(n_orders, orders)
                sys.exit()
                
                
            for i, order_index in enumerate(order_indices):
                sci_dict = [d for d in sci_dict_list if d["index"] == order_index][0]
                
                order = sci_dict["aotfPointer"]
                
                if order != orders[i]:
                    print("Error: wrong order")
                    sys.exit()
       
                if sci_dict["steppingPointer"] != 0:
                    print("Error: stepping obs?")
                    sys.exit()
                
                binning = sci_dict["binningFactor"]
                
                n_rows = (24 / n_orders) * (binning + 1)
                
                if not n_rows.is_integer():
                    print("Error: not an integer")
                    sys.exit()
                    
                if int(n_rows) != subd_parsed_dict["rows"]:
                    print("Error: number of rows")
                    sys.exit()
                
                et = exec_time(sci_dict["accumulationCount"], n_rows, n_orders, sci_dict["integrationTime"]/1000.)/1000.
                
                dt = subd_parsed_dict["rhythm"] - et
                
                if dt > 1.0 or dt < 0.0:
                    print("Error: timings wrong")
                    print(n_rows, dt)
                    sys.exit()
                    
                if sci_dict["comment"] not in sub_dict["comment"]:
                    print("Error: comments don't match")
                    sys.exit()
                
                # print(sci_dict["comment"])
            
        elif "start" in subd_parsed_dict.keys(): #if fullscan
        
            indices = [sub_dict["science_%i" %i] for i in range(2, 7) if sub_dict["science_%i" %i] != 0]
            
            if len(indices) > 0:
                print("Error: non-zero indices found")
        
            fullscan_index = sub_dict["science_1"]
        
            sci_dict = [d for d in sci_dict_list if d["index"] == fullscan_index][0]
            
            stepping_dict = [d for d in stepping_dict_list if d["index"] == sci_dict["steppingPointer"]][0]
            
            # print(sub_dict["comment"])
            
            start = sci_dict["aotfPointer"]
            step = stepping_dict["stepValue"]
            steps = stepping_dict["stepCount"]
            stop = start + steps * step
    
            n_orders = stepping_dict["stepSpeed"] + 1
            binning = sci_dict["binningFactor"] + 1
            
            d_rows = int((24 / n_orders) * binning)
            
            # print(start, step, stop, d_rows, n_orders)
            
            sci_parsed_dict = parse_fullscan_science_comment(sci_dict["comment"])
            rhythm = sci_parsed_dict["rhythm"]
            et = sci_parsed_dict["exec_time"]
            
            text = "TARGETED_NADIR_FULLSCAN_FAST_%i-%i-%iORDERS_%iROWS_%iSECS_%iSUBDS -- EXECTIME=%iMS" %(start, step, stop, d_rows, rhythm, n_orders, et)
            
            if text != sub_dict["comment"]:
                print("Error: comments don't match")
                sys.exit()
            
        # print("################")
    
    
