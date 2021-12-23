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


# previous_patch_date = "20210320_120000"
previous_patch_date = "mtp051_proposed"

new_dir_name = datetime.now().strftime("%Y%m%d_%H%M%S") + "_new"





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

}



#name:[[orders], int time, rhythm, lines, so=0/lno=1]
"""made with make_lno_obs_dict_2022-01.py"""

new_lno_obs_dict = {

"Carbonates #1":[[174, 175, 176, 189, 190, 191], 240, 8, 4],
"Carbonates #2":[[174, 175, 176, 189, 190, 191], 240, 8, 8],
"Carbonates #3":[[174, 175, 176, 189, 190, 191], 240, 8, 12],
"Carbonates #4":[[174, 175, 176, 189, 190, 191], 215, 15, 4],
"Carbonates #5":[[174, 175, 176, 189, 190, 191], 215, 15, 8],
"Carbonates #6":[[174, 175, 176, 189, 190, 191], 215, 15, 12],
"Carbonates #7":[[174, 175, 176], 225, 8, 8],
"Carbonates #8":[[174, 175, 176], 220, 8, 16],
"Carbonates #9":[[174, 175, 176], 190, 15, 8],
"Carbonates #10":[[174, 175, 176], 185, 15, 16],
"Carbonates #11":[[189, 190, 191], 225, 8, 8],
"Carbonates #12":[[189, 190, 191], 220, 8, 16],
"Carbonates #13":[[189, 190, 191], 190, 15, 8],
"Carbonates #14":[[189, 190, 191], 185, 15, 16],
"Phyllosilicates #1":[[189, 190, 191, 192, 193, 201], 240, 8, 4],
"Phyllosilicates #2":[[189, 190, 191, 192, 193, 201], 240, 8, 8],
"Phyllosilicates #3":[[189, 190, 191, 192, 193, 201], 240, 8, 12],
"Phyllosilicates #4":[[189, 190, 191, 192, 193, 201], 215, 15, 4],
"Phyllosilicates #5":[[189, 190, 191, 192, 193, 201], 215, 15, 8],
"Phyllosilicates #6":[[189, 190, 191, 192, 193, 201], 215, 15, 12],
"Phyllosilicates #7":[[190, 191, 192], 225, 8, 8],
"Phyllosilicates #8":[[190, 191, 192], 220, 8, 16],
"Phyllosilicates #9":[[190, 191, 192], 190, 15, 8],
"Phyllosilicates #10":[[190, 191, 192], 185, 15, 16],
"Carb Phyl #1":[[174, 175, 176, 190, 191, 192], 240, 8, 4],
"Carb Phyl #2":[[174, 175, 176, 190, 191, 192], 240, 8, 8],
"Carb Phyl #3":[[174, 175, 176, 190, 191, 192], 240, 8, 12],
"Carb Phyl #4":[[174, 175, 176, 190, 191, 192], 215, 15, 4],
"Carb Phyl #5":[[174, 175, 176, 190, 191, 192], 215, 15, 8],
"Carb Phyl #6":[[174, 175, 176, 190, 191, 192], 215, 15, 12],
"Water Band #1":[[160, 162, 164, 166, 168, 170], 240, 8, 4],
"Water Band #2":[[160, 162, 164, 166, 168, 170], 240, 8, 8],
"Water Band #3":[[160, 162, 164, 166, 168, 170], 240, 8, 12],
"Water Band #4":[[160, 162, 164, 166, 168, 170], 215, 15, 4],
"Water Band #5":[[160, 162, 164, 166, 168, 170], 215, 15, 8],
"Water Band #6":[[160, 162, 164, 166, 168, 170], 215, 15, 12],
"Water Band #7":[[160, 163, 166, 169, 172, 175], 240, 8, 4],
"Water Band #8":[[160, 163, 166, 169, 172, 175], 240, 8, 8],
"Water Band #9":[[160, 163, 166, 169, 172, 175], 240, 8, 12],
"Water Band #10":[[160, 163, 166, 169, 172, 175], 215, 15, 4],
"Water Band #11":[[160, 163, 166, 169, 172, 175], 215, 15, 8],
"Water Band #12":[[160, 163, 166, 169, 172, 175], 215, 15, 12],
"Water Band #13":[[157, 160, 163, 166, 169, 172], 240, 8, 4],
"Water Band #14":[[157, 160, 163, 166, 169, 172], 240, 8, 8],
"Water Band #15":[[157, 160, 163, 166, 169, 172], 240, 8, 12],
"Water Band #16":[[157, 160, 163, 166, 169, 172], 215, 15, 4],
"Water Band #17":[[157, 160, 163, 166, 169, 172], 215, 15, 8],
"Water Band #18":[[157, 160, 163, 166, 169, 172], 215, 15, 12],
"Water Band #19":[[163, 165, 167, 169], 205, 8, 6],
"Water Band #20":[[163, 165, 167, 169], 200, 8, 12],
"Water Band #21":[[163, 165, 167, 169], 210, 15, 6],
"Water Band #22":[[163, 165, 167, 169], 185, 15, 12],
"Water Band #23":[[160, 165, 170], 225, 8, 8],
"Water Band #24":[[160, 165, 170], 220, 8, 16],
"Water Band #25":[[160, 165, 170], 190, 15, 8],
"Water Band #26":[[160, 165, 170], 185, 15, 16],
"Water Band #27":[[163, 168, 173], 225, 8, 8],
"Water Band #28":[[163, 168, 173], 220, 8, 16],
"Water Band #29":[[163, 168, 173], 190, 15, 8],
"Water Band #30":[[163, 168, 173], 185, 15, 16],
"Water Band #31":[[154, 157, 160, 163, 166, 169], 240, 8, 4],
"Water Band #32":[[154, 157, 160, 163, 166, 169], 240, 8, 8],
"Water Band #33":[[154, 157, 160, 163, 166, 169], 240, 8, 12],
"Water Band #34":[[154, 157, 160, 163, 166, 169], 215, 15, 4],
"Water Band #35":[[154, 157, 160, 163, 166, 169], 215, 15, 8],
"Water Band #36":[[154, 157, 160, 163, 166, 169], 215, 15, 12],
"Water pyroxene #1":[[160, 163, 164, 172, 185, 191], 240, 8, 4],
"Water pyroxene #2":[[160, 163, 164, 172, 185, 191], 240, 8, 8],
"Water pyroxene #3":[[160, 163, 164, 172, 185, 191], 240, 8, 12],
"Water pyroxene #4":[[160, 163, 164, 172, 185, 191], 215, 15, 4],
"Water pyroxene #5":[[160, 163, 164, 172, 185, 191], 215, 15, 8],
"Water pyroxene #6":[[160, 163, 164, 172, 185, 191], 215, 15, 12],
"Water pyroxene #7":[[160, 163, 164, 172, 191, 192], 240, 8, 4],
"Water pyroxene #8":[[160, 163, 164, 172, 191, 192], 240, 8, 8],
"Water pyroxene #9":[[160, 163, 164, 172, 191, 192], 240, 8, 12],
"Water pyroxene #10":[[160, 163, 164, 172, 191, 192], 215, 15, 4],
"Water pyroxene #11":[[160, 163, 164, 172, 191, 192], 215, 15, 8],
"Water pyroxene #12":[[160, 163, 164, 172, 191, 192], 215, 15, 12],
"Hydration band #1":[[130, 147, 160], 225, 8, 8],
"Hydration band #2":[[130, 147, 160], 220, 8, 16],
"Hydration band #3":[[130, 147, 160], 190, 15, 8],
"Hydration band #4":[[130, 147, 160], 185, 15, 16],
"Hydration band #5":[[130, 147, 165], 225, 8, 8],
"Hydration band #6":[[130, 147, 165], 220, 8, 16],
"Hydration band #7":[[130, 147, 165], 190, 15, 8],
"Hydration band #8":[[130, 147, 165], 185, 15, 16],
"Hydration band #9":[[130, 148, 160], 225, 8, 8],
"Hydration band #10":[[130, 148, 160], 220, 8, 16],
"Hydration band #11":[[130, 148, 160], 190, 15, 8],
"Hydration band #12":[[130, 148, 160], 185, 15, 16],
"Hydration band #13":[[130, 148, 165], 225, 8, 8],
"Hydration band #14":[[130, 148, 165], 220, 8, 16],
"Hydration band #15":[[130, 148, 165], 190, 15, 8],
"Hydration band #16":[[130, 148, 165], 185, 15, 16],
"Hydrated minerals #1":[[148, 153, 158, 164, 170, 177], 240, 8, 4],
"Hydrated minerals #2":[[148, 153, 158, 164, 170, 177], 240, 8, 8],
"Hydrated minerals #3":[[148, 153, 158, 164, 170, 177], 240, 8, 12],
"Hydrated minerals #4":[[148, 153, 158, 164, 170, 177], 215, 15, 4],
"Hydrated minerals #5":[[148, 153, 158, 164, 170, 177], 215, 15, 8],
"Hydrated minerals #6":[[148, 153, 158, 164, 170, 177], 215, 15, 12],

}

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
                        


def parse_comment(comment):
    """parse COP row comments"""
    
    regex = re.compile(r"\S_(\d*)ROWS_(\d*)SECS_(\d*)SUBDS.*EXECTIME=(\d*)MS")
    
    match = regex.findall(comment)[0]
    if len(match) == 4:
        match = try_int(match)
        parsed_dict = {"rows":match[0], "rhythm":match[1], "n_orders":match[2], "exec_time":match[3]}
    
    else:
        print("Error parsing comments")
        
    return parsed_dict



    
def make_cop_path(cop_date, channel, cop_name):

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
                print(header)
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



def write_cop_csv(csv_filepath, lines):
    """write COP csv file"""
    
    dir_out = os.path.dirname(csv_filepath)
    os.makedirs(dir_out, exist_ok=True)

    with open(csv_filepath, "w") as f:
        for line in lines:
            f.write(line+"\n")



def new_subdomain_rows(channel, new_obs_dict):
    cop_name = "science"
    
    path = make_cop_path(previous_patch_date, channel, cop_name)
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
                    
                    #finally check rhythm matches
                    comment = dict_sci["comment"]
                    d = parse_comment(comment)
                    if d["rhythm"] == rhythm:
                        # print("match_found", match_dict, dict_sci)
                        
                        found = True
                        science_rows[i_ord] = dict_sci["index"]
                        science_comment = comment
    
            if not found:
                print("Error: observation not found in science table")
    
    
        line = ",".join([str(i) for i in science_rows]) + " # ORDERS " + " ".join([str(i) for i in orders]) + " -- " + science_comment
        
        lines.append(line)
    
    #write new rows to file
    cop_name = "sub_domain"
    path = make_cop_path(new_dir_name, channel, cop_name)
    write_cop_csv(path, lines)

    


def new_science_rows(channel, new_obs_dict):
    """make science rows"""
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
    path = make_cop_path(new_dir_name, channel, cop_name)
    write_cop_csv(path, lines)




new_subdomain_rows("so", new_so_obs_dict)
# new_science_rows("lno", new_lno_obs_dict) 

#then add new science lines to csv manually

new_subdomain_rows("lno", new_lno_obs_dict)




#fullscans
lno_fullscans = [
    {"name":"Water Band Fullscan #1", "start":160, "steps":11, "step":1, "rhythms":[8, 15], "steps_binning":{6:[0, 1, 2], 4:[1], 3:[0, 1]}},
    {"name":"Water Band Fullscan #2", "start":160, "steps":6, "step":2, "rhythms":[8, 15], "steps_binning":{6:[0, 1, 2], 4:[1], 3:[0, 1]}},
    {"name":"Water Band Fullscan #3", "start":156, "steps":11, "step":2, "rhythms":[8, 15], "steps_binning":{6:[0, 1, 2], 4:[1], 3:[0, 1]}},
    {"name":"Carbonates #1", "start":173, "steps":21, "step":1, "rhythms":[8, 15], "steps_binning":{6:[0, 1, 2], 4:[1], 3:[0, 1]}},
    {"name":"Carbonates #2", "start":173, "steps":11, "step":2, "rhythms":[8, 15], "steps_binning":{6:[0, 1, 2], 4:[1], 3:[0, 1]}},
    {"name":"Phyllosilicates #1", "start":188, "steps":15, "step":1, "rhythms":[8, 15], "steps_binning":{6:[0, 1, 2], 4:[1], 3:[0, 1]}},
    {"name":"Phyllosilicates #2", "start":187, "steps":9, "step":2, "rhythms":[8, 15], "steps_binning":{6:[0, 1, 2], 4:[1], 3:[0, 1]}},
    {"name":"Carb Phyl #1", "start":174, "steps":29, "step":1, "rhythms":[8, 15], "steps_binning":{6:[0, 1, 2], 4:[1], 3:[0, 1]}},
    {"name":"Carb Phyl #2", "start":173, "steps":16, "step":2, "rhythms":[8, 15], "steps_binning":{6:[0, 1, 2], 4:[1], 3:[0, 1]}},
    {"name":"Phobos All #1", "start":160, "steps":43, "step":1, "rhythms":[8, 15], "steps_binning":{6:[0, 1, 2], 4:[1], 3:[0, 1]}},
    {"name":"Phobos All #2", "start":159, "steps":23, "step":2, "rhythms":[8, 15], "steps_binning":{6:[0, 1, 2], 4:[1], 3:[0, 1]}},
    {"name":"Phobos All #3", "start":159, "steps":16, "step":3, "rhythms":[8, 15], "steps_binning":{6:[0, 1, 2], 4:[1], 3:[0, 1]}},
    {"name":"Hydrated minerals #1", "start":148, "steps":6, "step":6, "rhythms":[8, 15], "steps_binning":{6:[0, 1, 2], 4:[1], 3:[0, 1]}},
]
















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

