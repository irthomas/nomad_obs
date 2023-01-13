# -*- coding: utf-8 -*-
"""
Created on Tue Jan 10 12:04:00 2023

@author: iant

CHECK PREVIOUS MTPS TO SEE WHICH COP ROWS HAVE BEEN USED
"""


import os

# from cop_patching.append_cop_tables_2022_12 import read_cop_csv


mtp_range = range(58, 64)


cop_row_root_path = os.path.normcase(r"C:\Users\iant\Documents\PROGRAMS\nomad_obs\observations\cop_rows")

cop_rows_made = {
    "calibrations":{},
    "dayside_nadir":{},
    "egress_occultations":{},
    "grazing_occultations":{},
    "ingress_occultations":{},
    "nightside_nadir":{},
    "phobos_deimos":{},
    }

for cop_row_name in cop_rows_made.keys():
    cop_rows_made[cop_row_name] = {
        "so":{"fixed":[], "sub_domain":[]},
        "lno":{"fixed":[], "sub_domain":[]},
    }
        


for mtp_number in mtp_range:

    cop_row_dir = os.path.join(cop_row_root_path, "mtp%03i" %mtp_number)



    if os.path.exists(os.path.join(cop_row_dir, "sent")):
        cop_row_dir = os.path.join(cop_row_dir, "sent")
        
        
    
    
    #load obs cop rows
    for cop_row_name in cop_rows_made.keys():
        
        cop_row_path = os.path.join(cop_row_dir, "mtp%03i_ir_%s.txt" %(mtp_number, cop_row_name))
        if os.path.exists(cop_row_path):
            with open(cop_row_path, "r") as f:
                lines = f.readlines()
                
                if len(lines) > 1:
                    for i in range(1, len(lines)):
                        line_split = lines[i].split(",")
                        
                        fixed_row = int(line_split[0])
                        sub1 = int(line_split[2])
                        sub2 = int(line_split[3])
                        
                        channel = int(line_split[4])
                        
                        if fixed_row > -1:
                            cop_rows_made[cop_row_name][{0:"so", 1:"lno"}[channel]]["fixed"].append(fixed_row)
                        if sub1 > -1:
                            cop_rows_made[cop_row_name][{0:"so", 1:"lno"}[channel]]["sub_domain"].append(sub1)
                        if sub2 > -1:
                            cop_rows_made[cop_row_name][{0:"so", 1:"lno"}[channel]]["sub_domain"].append(sub2)
                        
                        # stop()
                
                
        else:
            print("Warning: %s does not exist" %cop_row_path)
                
all_fixed_rows = []
all_sub_domain_rows = []

for channel in ["so", "lno"]:
    for cop_row_name in cop_rows_made.keys():
        all_fixed_rows.extend(cop_rows_made[cop_row_name][channel]["fixed"])
        all_sub_domain_rows.extend(cop_rows_made[cop_row_name][channel]["sub_domain"])
                          
    all_fixed_rows = sorted(list(set(all_fixed_rows)))
    all_sub_domain_rows = sorted(list(set(all_sub_domain_rows)))
    
    print("##### %s FIXED" %channel)
    print(all_fixed_rows)
    
    print("##### %s SUBDOMAIN" %channel)
    print(all_sub_domain_rows)