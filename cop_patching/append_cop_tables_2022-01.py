# -*- coding: utf-8 -*-
"""
Created on Wed Dec  8 10:46:39 2021

@author: iant

SCRIPT TO READ IN THE EXISTING SCIENCE TABLES AND GENERATE A FEW SUBDOMAIN ROWS FOR A MINOR PATCH

"""
import os
import re
from datetime import datetime

from cop_patching.generate_cop_tables_v05 import readScienceComments, writeTable
from cop_patching.generate_cop_tables_v05 import read_in_cop_table, getWindowHeight, exec_time, checkExecTime

from nomad_obs.config.paths import BASE_DIRECTORY


previous_patch_date = "20210320_120000"

new_dir_name = datetime.now().strftime("%Y%m%d_%H%M%S")





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


#name:[[orders], int time, rhythm, lines, so=0/lno=1]

new_so_obs_dict = {

"6SUBD CO2 H2O #11":[[121, 132, 148, 156, 160, 165], 4, 1, 16, 0], #Proposed by Loic, priority High
# "6SUBD CO2 #12":[[156, 132, 118, 140, 154, 158], 4, 1, 16, 0], #Proposed by Loic, priority Middle
# "6SUBD CO2 #13":[[156, 132, 118, 169, 154, 140], 4, 1, 16, 0], #Proposed by Loic, priority Middle
# "6SUBD CO2 H2O #14":[[121, 134, 148, 132, 165, 169], 4, 1, 16, 0], #Proposed by Loic, priority High
# "6SUBD CO2 H2O CO #15":[[121, 132, 148, 165, 186, 190], 4, 1, 16, 0], #Proposed by Loic, priority High
# "6SUBD CO2 #16":[[121, 148, 149, 155, 164, 165], 4, 1, 16, 0], #Proposed by Miguel, priority Middle
# "6SUBD CO2 #17":[[123, 142, 148, 155, 156, 165], 4, 1, 16, 0], #CO2 full range, priority Middle
# "6SUBD CO2 #18":[[154, 155, 156, 157, 158, 159], 4, 1, 16, 0], #Full homopause, priority Low: test
# "6SUBD CO2 #19":[[123, 132, 142, 148, 156, 165], 4, 1, 16, 0], #Lower alt, priority Middle
# "6SUBD CO2 #20":[[123, 148, 155, 156, 160, 165], 4, 1, 16, 0], #Full range, priority Middle
# "6SUBD CO2 #21":[[171, 122, 142, 155, 156, 165], 4, 1, 16, 0], #Full range try 171, priority Low: test
# "6SUBD CO2 #22":[[142, 148, 155, 156, 160, 165], 4, 1, 16, 0], #Mid-high, priority Middle
# "6SUBD CO2 #23":[[186, 190, 132, 148, 156, 165], 4, 1, 16, 0], #CO2+CO, priority Middle
# "6SUBD CO2 #24":[[186, 190, 132, 148, 155, 165], 4, 1, 16, 0], #CO2+CO, priority Middle
# "6SUBD CO2 CO #25":[[156, 123, 118, 148, 186, 132], 4, 1, 16, 0], #iso higher alt, priority Middle
# "6SUBD CO2 CO #26":[[197, 200, 177, 145, 186, 132], 4, 1, 16, 0], #iso lower alt, priority Low: test
# "6SUBD CO2 CO #27":[[156, 123, 118, 148, 186, 132], 4, 1, 16, 0], #iso higher alt, priority Middle
# "6SUBD CO2 H2O #12":[[121, 132, 148, 156, 189, 165], 4, 1, 16, 0], #Proposed by Loic, priority High
# "6SUBD CO2 H2O #13":[[121, 132, 148, 156, 186, 165], 4, 1, 16, 0], #Proposed by Loic, priority High


}


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


channel = "so"
cop_name = "science"

path = make_cop_path(previous_patch_date, channel, cop_name)
dict_list = read_cop_csv(path)




#for science table - split into cals and science

dict_list_cal = []
dict_list_sci = []
for line_dict in dict_list:
    if line_dict["steppingPointer"] == 0 and line_dict["accumulationCount"] > 0: #science
        dict_list_sci.append(line_dict)
    
    elif line_dict["steppingPointer"] > 0 and line_dict["accumulationCount"] > 0: #cal
        dict_list_cal.append(line_dict)
        

lines = []

#match new observations to existing rows
for name, params in new_so_obs_dict.items():
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
    
    for i_ord, order in enumerate(orders):
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
                    
                    science_rows[i_ord] = dict_sci["index"]
                    science_comment = comment



    line = ",".join([str(i) for i in science_rows]) + " # ORDERS " + " ".join([str(i) for i in orders]) + " -- " + science_comment
    
    lines.append(line)

#write new rows to file
cop_name = "sub_domain"
path = make_cop_path(new_dir_name, channel, cop_name)
write_cop_csv(path, lines)

    

# new_lno_obs_dict = {}
# for name, orders_list in lno_normal_orders.items():
#     loop = 0
#     for orders_dict in orders_list:
#         orders = orders_dict["orders"]
#         for rhythm in orders_dict["rhythms"]:
#             for binning in orders_dict["binning"]:
#                 loop += 1
#                 new_lno_obs_dict["%s #%i" %(name, loop)] = [orders, 200, rhythm, int((binning+1)*24./len(orders))]



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

