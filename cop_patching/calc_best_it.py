# -*- coding: utf-8 -*-
"""
Created on Mon Sep 18 09:42:24 2023

@author: iant
"""

# from 


import numpy as np


from cop_patching.exec_time_nacc_functions import getBinningFactor, n_acc1, exec_time1


MAX_EXECUTION_TIME = {1:850000, 2:1750000, 4:3600000, 8:7600000, 15:14600000, 30:29600000, 60:59600000} #us
MIN_EXECUTION_TIME = {1:700000, 2:1500000, 4:3200000, 8:7200000, 15:14200000, 30:29200000, 60:59200000} #us




def calculate_best_inttimes(base_inttime, rhythm, nsubdomains, windowheight, order_combinations=[[]], fix_inttime=False):
    if rhythm > 1000000:
        max_exec_time = rhythm - 400000
    else:
        max_exec_time = rhythm - 150000
    
    best_inttime = base_inttime
    best_accumulations = 0
    smallest_lost_time = 10000.0 #ms
    best_execution_time = 0
    
    if fix_inttime:
        possible_inttimes = [base_inttime]
    else:
        if base_inttime > 300000:
            possible_inttimes = np.arange(base_inttime - 40000, base_inttime + 50000, 5000)
        else:
            possible_inttimes = np.arange(base_inttime - 30000, base_inttime + 30000, 5000)

    for inttime in possible_inttimes:
        bins = getBinningFactor(windowheight, nsubdomains, rows=24)
        accumulations = n_acc1(max_exec_time/nsubdomains, windowheight-1, inttime)
        execution_time = exec_time1(accumulations, windowheight-1, inttime)
        lost_time = (max_exec_time - execution_time * nsubdomains)/1000.0 #ms
        if lost_time < smallest_lost_time:
            smallest_lost_time = lost_time
            best_inttime = inttime
            best_accumulations = accumulations
            best_execution_time = int(execution_time / 1000.0)
        if not fix_inttime:
            print("int time %i ms: exec time %i, lost time %0.1f ms (%i accs)" %(inttime/1000, (execution_time*nsubdomains)/1000, lost_time, accumulations))
    print("Printing for NSUBD=%i, RHYTHM=%i" %(nsubdomains, rhythm/1000000))
    
    if fix_inttime:
        print("Fixed inttime: %i us, %i accs, binning = %i. lost time %0.1f ms" %(best_inttime, best_accumulations, bins, smallest_lost_time))
    else:
        print("Best: %i us, %i accs, %i rows per bin. lost time %0.1f ms" %(best_inttime, best_accumulations, bins, smallest_lost_time))
    print("%i # NADIR_SCIENCE_%iSUBD -- EXECTIME=%iMS -- RHYTHM=%iMS -- NROWS=%i" 
          %(best_inttime, nsubdomains, best_execution_time, rhythm/1000, windowheight))
    for order_combination in order_combinations:
        print("0 # NADIR_SCIENCE -- ORDERS "+"%i "*len(order_combination) %tuple(order_combination)+"-- INTTIME=%iMS -- EXECTIME=%iMS -- NROWS=%i"
              %(best_inttime/1000, best_execution_time*nsubdomains, windowheight))



def checkExecTime(exec_time_microsecs, rhythm, silent=False):
    """check if execution time is between min and max values"""    
    min_exec_time = MIN_EXECUTION_TIME[rhythm]
    max_exec_time = MAX_EXECUTION_TIME[rhythm]
    if exec_time_microsecs < min_exec_time:
        if not silent: print(f"Error: execution time too small (exec_time={exec_time_microsecs}, min_exec_time={min_exec_time}, rhythm={rhythm}")
#        stop()
        return 0
    else:
        if exec_time_microsecs > max_exec_time:
            if not silent: print(f"Error: Execution time too large (exec_time={exec_time_microsecs}, max_exec_time={max_exec_time}, rhythm={rhythm}")
#            stop()
            return 0
        else:
            return 1


#cases
# base_inttime = 200000
# rhythm = 15000000
# nsubdomains = 3
# windowheight = 144

cases = [
    # {"it":200000, "rhy":15000000, "nsub":2, "wh":144},
    # {"it":200000, "rhy":15000000, "nsub":3, "wh":144},
    # {"it":200000, "rhy":15000000, "nsub":4, "wh":144},
    # {"it":200000, "rhy":15000000, "nsub":6, "wh":144},

    {"it":500000, "rhy":30000000, "nsub":2, "wh":144},
    # {"it":500000, "rhy":30000000, "nsub":3, "wh":144},

    # {"it":500000, "rhy":60000000, "nsub":2, "wh":144},
    # {"it":500000, "rhy":60000000, "nsub":3, "wh":144},
    ]

for case in cases:
    calculate_best_inttimes(case["it"], case["rhy"], case["nsub"], case["wh"], fix_inttime=False)
