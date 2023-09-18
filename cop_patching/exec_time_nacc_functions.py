# -*- coding: utf-8 -*-
"""
Created on Mon Sep 18 09:43:34 2023

@author: iant
"""

import numpy as np

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
    n_accs = n_acc1(exec_time_per_order, window_height, int_time*1000.0)
    
    return n_accs


def getBinningFactor(n_rows, n_subdomains, rows=24):
    """use real number of rows, return COP table style binning factor (-1)"""
    n_bins = np.float(n_rows) / (np.float(rows)/np.float(n_subdomains))
    if np.round(n_bins) == n_bins:
        return int(n_bins)-1
    else:
        print("Error: n_bins is not an integer: %0.2f, %i" %(n_bins,int(n_bins)))
        print(n_rows, n_subdomains, rows)
        
