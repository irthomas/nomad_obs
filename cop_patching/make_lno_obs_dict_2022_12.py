# -*- coding: utf-8 -*-
"""
Created on Wed Dec 22 17:07:07 2021

@author: iant

MAKE NEW LNO OBS DICT



"""

import numpy as np

from cop_patching.append_cop_tables_2022_01 import new_lno_obs_dict  as old_lno_obs_dict


IT_RANGES = {200:np.arange(180., 241., 5.), 500:np.arange(480., 620., 5.)}

#normal
lno_normal_orders = {
    "Carbonates":[
        {"orders":[174, 175, 176, 189, 190, 191], "rhythms":[30, 60], "binning":[1, 2], "it_ranges":[200, 500]},
        {"orders":[174, 175, 176], "rhythms":[30, 60], "binning":[1], "it_ranges":[200]},
        {"orders":[189, 190, 191], "rhythms":[30, 60], "binning":[1], "it_ranges":[200]},
    ],
    "Phyllosilicates":[
        {"orders":[189, 190, 191, 192, 193, 201], "rhythms":[30, 60], "binning":[1, 2], "it_ranges":[200, 500]},
        {"orders":[190, 191, 192], "rhythms":[30, 60], "binning":[1], "it_ranges":[200]},
    ],
    "Carb Phyl":[
        {"orders":[174, 175, 176, 190, 191, 192], "rhythms":[30, 60], "binning":[1, 2], "it_ranges":[200, 500]},
    ],
    "Water Band":[
        {"orders":[160, 162, 164, 166, 168, 170], "rhythms":[30, 60], "binning":[1, 2], "it_ranges":[200, 500]},
        { "orders":[160, 163, 166, 169, 172, 175], "rhythms":[30, 60], "binning":[1, 2], "it_ranges":[200, 500]},
        {"orders":[157, 160, 163, 166, 169, 172], "rhythms":[30, 60], "binning":[1, 2], "it_ranges":[200, 500]},
        {"orders":[163, 165, 167, 169], "rhythms":[30, 60], "binning":[1], "it_ranges":[200, 500]},
        {"orders":[160, 165, 170], "rhythms":[30, 60], "binning":[1], "it_ranges":[200]},
        {"orders":[163, 168, 173], "rhythms":[30, 60], "binning":[1], "it_ranges":[200]},
        {"orders":[154, 157, 160, 163, 166, 169], "rhythms":[30, 60], "binning":[1, 2], "it_ranges":[200, 500]},
    ],
    "Water pyroxene":[
        {"orders":[160, 163, 164, 172, 185, 191], "rhythms":[30, 60], "binning":[1, 2], "it_ranges":[200, 500]},
        {"orders":[160, 163, 164, 172, 191, 192], "rhythms":[30, 60], "binning":[1, 2], "it_ranges":[200, 500]},
    ],
    "Hydration band":[
        {"orders":[130, 147, 160],"rhythms":[30, 60], "binning":[1], "it_ranges":[200]},
        {"orders":[130, 147, 165],"rhythms":[30, 60], "binning":[1], "it_ranges":[200]},
        {"orders":[130, 148, 160],"rhythms":[30, 60], "binning":[1], "it_ranges":[200]},
        {"orders":[130, 148, 165],"rhythms":[30, 60], "binning":[1], "it_ranges":[200]},
    ],
    "Hydrated minerals":[
        {"orders":[148, 153, 158, 164, 170, 177], "rhythms":[30, 60], "binning":[1, 2], "it_ranges":[200, 500]},
    ],
    "Hydrated single orders":[
        {"orders":[148, 153, 164], "rhythms":[30, 60], "binning":[1], "it_ranges":[200, 500]},
        {"orders":[158, 170, 164], "rhythms":[30, 60], "binning":[1], "it_ranges":[200, 500]},
        {"orders":[148, 164, 177], "rhythms":[30, 60], "binning":[1], "it_ranges":[200, 500]},
        {"orders":[148, 153, 164], "rhythms":[15], "binning":[1], "it_ranges":[500]},
        {"orders":[158, 170, 164], "rhythms":[15], "binning":[1], "it_ranges":[500]},
        {"orders":[148, 164, 177], "rhythms":[15], "binning":[1], "it_ranges":[500]},
    ],
}




def exec_time1(n_acc, window_height, int_time):
    """input COP table values, return microseconds"""
    return int(((n_acc+1.0) * (int_time + 71.0 + 320.0 * (window_height + 1.0) + 1000.0) + 337.0) )

def exec_time2(accumulation_count, n_rows, n_subd, integration_time):
    """use real number of rows"""
    window_height = np.float32(n_rows - 1.0)
    return int(np.ceil(exec_time1(accumulation_count, window_height, integration_time) * np.float32(n_subd)))

def exec_time(accumulation_count, n_rows, n_subd, integration_time):
    """use real number of rows, time in milliseconds"""
    window_height = np.float32(n_rows - 1.0)
    return (exec_time1(accumulation_count, window_height, integration_time*1000.0) * np.float32(n_subd)) / 1000.0


def n_acc1(max_exec_time, window_height, int_time):
    n_accs_float = (max_exec_time - 337.0) / (int_time + 71.0 + 320.0 * (window_height + 1.0) + 1000.0) - 1.0
    n_accs = int(np.floor(n_accs_float/2.0) * 2.0) #make even for all observations, sbsf 0 or 1
    return n_accs

def n_acc2(max_exec_time, n_rows, int_time):
    """use real number of rows"""
    window_height = np.float32(n_rows - 1.0)
    return n_acc1(max_exec_time, window_height, int_time)

def n_acc(max_exec_time, n_rows, n_orders, int_time):
    """use real number of rows, times in milliseconds"""
    window_height = np.float32(n_rows - 1.0)
    exec_time_per_order = (max_exec_time * 1000.0) / np.float32(n_orders)
    return n_acc1(exec_time_per_order, window_height, int_time*1000.0)


def find_best_it(n_rows, n_orders, rhythm, it_range):
    """calculate best LNO combination of number of accumulations and integration times"""
    max_t = rhythm * 1000. - 450. #milliseconds in total for all orders
    
    total_exec_times = np.zeros_like(it_range)
    # print("####")
    for i, it in enumerate(it_range):
        
        n_accs = n_acc(max_t, n_rows, n_orders, it)
        time = exec_time(n_accs, n_rows, n_orders, it)
        total_exec_times[i] = time
        
        # print(n_accs, time, it)
    
    best_index = np.argmax(total_exec_times)
    best_it = it_range[best_index]
    
    return best_it




new_lno_obs_dict = {}
for name, orders_list in lno_normal_orders.items():
    loop = 0
    for orders_dict in orders_list:
        orders = orders_dict["orders"]
        for rhythm in orders_dict["rhythms"]:
            for binning in orders_dict["binning"]:
                for it in orders_dict["it_ranges"]:
                    it_range = IT_RANGES[it]
                    loop += 1
                    
                    n_rows = int((binning+1)*24./len(orders))
                    n_orders = len(orders)
                    
                    it = int(find_best_it(n_rows, n_orders, rhythm, it_range))
                    
                    #make obs name, check if already existing
                    obs_name = "%s #%i" %(name, loop)
                    while obs_name in old_lno_obs_dict.keys():
                        obs_name = "%s #%i" %(name, loop)
                        loop += 1
                    
                    new_lno_obs_dict[obs_name] = [orders, it, rhythm, n_rows]

for name, data in new_lno_obs_dict.items():
    print('"%s":%s,' %(name, data))

