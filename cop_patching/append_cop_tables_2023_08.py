# -*- coding: utf-8 -*-
"""
Created on Wed Dec  8 10:46:39 2021

@author: iant

SCRIPT TO READ IN THE EXISTING SCIENCE TABLES AND GENERATE A FEW SUBDOMAIN ROWS FOR A MINOR PATCH


HOW TO PATCH:
    1) SET old_dir_name = THE CURRENT COP TABLE DIRECTORY
    2) GIVE A NEW DIRECTORY NAME BASED ON THE MTP E.G. new_dir_name = mtpXXX_proposed

    IF WANTING NEW WINDOW TOP, WINDOW HEIGHT, OR NEW RHYTHM:
        INCLUDE AT MINIMUM X_fixed AND X_science AND/OR X_fullscan_science IN OBS_TO_UPDATE WHERE X= so OR lno
        ADD NEW WINDOW TOPS TO X_centre_rows WHERE 152 = CENTRE OF 

"""
import os
import re
import sys
from datetime import datetime
# import numpy as np
import logging

# from cop_patching.generate_cop_tables_v05 import readScienceComments, writeTable
# from cop_patching.generate_cop_tables_v05 import read_in_cop_table, getWindowHeight, exec_time, checkExecTime

from nomad_obs.config.paths import BASE_DIRECTORY
from cop_patching.exec_time_nacc_functions import n_acc, exec_time





old_dir_name = "20230218_120000"
temp_dir_name = datetime.now().strftime("%Y%m%d_%H%M%S") + "_new"
new_dir_name = "mtp073_proposed"

logger_level = "DEBUG"
logger_name = os.path.join("cop_patching", "log.txt")
    

lno_centre_rows = [150, 151, 152, 153, 154]
so_centre_rows = [122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132, 133, 134]

#readout wait time, i.e. buffer in milliseconds to add before next integration
readout_wait_time = {"so":150., "lno":400.}


#index of rows available for overwriting - indices are from notepad row numbers
#add 1 to end of each range
available_cop_rows = {
    "lno":{
        "fixed":[*range(245, 258)],
        "stepping":[*range(73, 258)],
        "science":[*range(4015, 4098)],
        # "sub_domain":[*range(4084, 4098)]
        "sub_domain":[*range(510, 631)]
    },

    "so":{
        # "fixed":[*range(111, 258)],
        "stepping":[*range(27, 258)],
        "science":[*range(4076, 4098)],
        "sub_domain":[*range(3239, 4098)]
    }

}




MAKE_TABLES = True
# MAKE_TABLES = False


OBS_TO_UPDATE = [
# "so_fixed",
"so_science", #includes subdomain
# "so_fullscan_fixed",
"so_fullscan_stepping",
"so_fullscan_science", #includes subdomain

"lno_fixed",
"lno_science", #includes subdomain
# "lno_fullscan_fixed",
# "lno_fullscan_stepping",
# "lno_fullscan_science", #includes subdomain
]



"""new observations"""

#name:[[orders], int time, rhythm, lines, so=0/lno=1]
new_so_obs_dict = {

"6SUBD Nominal #54":[[121, 134, 148, 169, 186, 190], 4, 1, 16, 0], # nominal with 148
"6SUBD Nominal #55":[[121, 140, 146, 148, 169, 186], 4, 1, 16, 0], # CO/CO2 isotopes with temperature
"6SUBD Nominal #56":[[148, 132, 183, 184, 185, 186], 4, 1, 16, 0], # CO isotopes with temperature
    
}



#name:[[orders], int time, rhythm, lines, so=0/lno=1]
new_lno_obs_dict = {
        
"Surface Ice 3SUBD #4":[[168, 189, 193], 205, 15, 144],
"Surface Ice 3SUBD #4M":[[168, 189, 193], 530, 30, 144],
"Surface Ice 3SUBD #4L":[[168, 189, 193], 520, 60, 144],

"Surface Ice 3SUBD #5":[[168, 190, 193], 205, 15, 144],
"Surface Ice 3SUBD #5M":[[168, 190, 193], 530, 30, 144],
"Surface Ice 3SUBD #5L":[[168, 190, 193], 520, 60, 144],

"Surface Ice 3SUBD #6":[[193, 167, 189], 205, 15, 144],
"Surface Ice 3SUBD #7":[[193, 167, 190], 205, 15, 144],

"Surface Ice 3SUBD #8":[[193, 169, 189], 205, 15, 144],
"Surface Ice 3SUBD #9":[[193, 169, 190], 205, 15, 144],


"Surface Ice 3SUBD #10":[[168, 132, 133], 205, 15, 144],
"Surface Ice 3SUBD #10M":[[168, 132, 133], 530, 30, 144],
"Surface Ice 3SUBD #10L":[[168, 132, 133], 520, 60, 144],

"Surface Ice 2SUBD #1M":[[132, 133], 500, 30, 144],
"Surface Ice 2SUBD #1L":[[132, 133], 515, 60, 144],

"Ice CO 2SUBD #2M":[[189, 193], 500, 30, 144],
"Ice CO 2SUBD #2L":[[189, 193], 515, 60, 144],


"Surface Ice 3SUBD #2M":[[168, 189, 190], 530, 30, 144],
"Surface Ice 3SUBD #2L":[[168, 189, 190], 520, 60, 144],


"Ice H2O 2SUBD #1M":[[193, 168], 500, 30, 144],
"Ice H2O 2SUBD #1L":[[193, 168], 515, 60, 144],

"Ice CO 2SUBD #1M":[[193,190], 500, 30, 144],
"Ice CO 2SUBD #1L":[[193,190], 515, 60, 144],

"Ice CO 2SUBD #3M":[[193,193], 500, 30, 144],
"Ice CO 2SUBD #3L":[[193,193], 515, 60, 144],

}






"""new fullscans"""
# if start order = 165 and n steps=10, then main orders measured are 166-175. 165 is measured occasionally
# 124
so_fullscans = [
    {"name":"Fullscan 4 steps #1", "start":124, "steps":10, "step":4, "rhythms":[1], "steps_binning":{6:[3]}, "approx_it":[4]},
    {"name":"Fullscan 4 steps #1", "start":124, "steps":11, "step":4, "rhythms":[1], "steps_binning":{6:[3]}, "approx_it":[4]},
    {"name":"Fullscan 4 steps #1", "start":124, "steps":12, "step":4, "rhythms":[1], "steps_binning":{6:[3]}, "approx_it":[4]},

    {"name":"Fullscan 4 steps #1", "start":114, "steps":14, "step":5, "rhythms":[1], "steps_binning":{6:[3]}, "approx_it":[4]},
    {"name":"Fullscan 4 steps #1", "start":114, "steps":15, "step":5, "rhythms":[1], "steps_binning":{6:[3]}, "approx_it":[4]},
    {"name":"Fullscan 4 steps #1", "start":114, "steps":16, "step":5, "rhythms":[1], "steps_binning":{6:[3]}, "approx_it":[4]},
]

lno_fullscans = []





#logger stuff
if os.path.exists(logger_name):
    os.remove(logger_name)


logging.basicConfig(filename=logger_name,
    filemode='a',
    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
    datefmt='%H:%M:%S',
    level=logging.DEBUG)

logger = logging.getLogger()



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



    #new for MTP063 and 073
    elif rhythm == 30:
        if n_orders == 2:
            it = {(11, 500):500}[(binning, approx_it)] #fix
        elif n_orders == 3:
            it = {(0,200):215, (0,500):575, (1, 200):185, (1, 500):510, (17, 500):530}[(binning, approx_it)]
        elif n_orders == 4:
            it = {(1, 200):205, (1, 500):485}[(binning, approx_it)]
        elif n_orders == 6:
            it = {(1, 200):210, (1, 500):540, (2, 200):190, (2, 500):540}[(binning, approx_it)]

        

    elif rhythm == 60:
        if n_orders == 2:
            it = {(11, 500):515}[(binning, approx_it)] #fix
        elif n_orders == 3:
            it = {(0,200):205, (0,500):505, (1, 200):190, (1, 500):595, (17, 500):520}[(binning, approx_it)]
        elif n_orders == 4:
            it = {(1, 200):210, (1, 500):590}[(binning, approx_it)]
        elif n_orders == 6:
            it = {(1, 200):190, (1, 500):580, (2, 200):215, (2, 500):515}[(binning, approx_it)]
        
    #for occultations
    elif rhythm == 1:
        if n_orders == 6:
            it = {(3, 4):4}[(binning, approx_it)]


    if it > 0:
        return it
    else:
        print("Error: combination not found")
        logger.error("Combination not found: %s", [rhythm, n_orders, binning, approx_it])
                






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
        logger.error("Error parsing comment %s", comment)
        
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
        logger.error("Error parsing comment %s", comment)
        
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
        logger.error("Error parsing comment %s", comment)
        return {}
        
    return parsed_dict




    
def make_cop_path(cop_date, channel, cop_name):
    """make path"""

    return os.path.join(BASE_DIRECTORY, "cop_tables", cop_date, "%s_%s_table.csv" %(channel, cop_name))    
    




def read_cop_csv(csv_filepath):
    """read in table into list of dictionaries"""

    logger.debug("read_cop_csv %s", csv_filepath)


    dict_list = []
    with open(csv_filepath) as f:
        lines = f.readlines()
        
        for i, line in enumerate(lines):
            if i == 0:
                header = ["index", "npp_index"]
                header.extend([s.strip() for s in line.split(",")])
                header.append("comment")
                # print(header)
            else:
                npp_index = i + 1 #notepad++ header is row 1, therefore first row is row 2
                index = i - 1
                split = line.split(",")
                if "#" in split[-1]: #if comment
                    row = [index, npp_index]
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
    
    if not os.path.exists(dir_out):
        logger.info("Making directory %s", dir_out)

    os.makedirs(dir_out, exist_ok=True)

    with open(csv_filepath, "w") as f:
        for line in lines:
            f.write(line + ending)





def replace_lines(channel, cop_name, available_rows, existing_dir, new_lines_dir, merged_dir):
    """merge existing file with new file, writing new lines to new proposed file filling in the available rows"""

    logger.debug("replace_lines %s", [channel, cop_name, existing_dir, new_lines_dir, merged_dir])
    
    
    csv_filepath_new = make_cop_path(new_lines_dir, channel, cop_name)
    with open(csv_filepath_new) as f:
        lines_new = f.readlines()
        
        logger.info("Reading %i new lines from file %s", len(lines_new), csv_filepath_new)

    
    csv_filepath = make_cop_path(existing_dir, channel, cop_name)
    with open(csv_filepath) as f:
        lines = f.readlines()

    logger.info("Reading %i existing lines from file %s", len(lines), csv_filepath)
    
   
    i = 0
    for line_new in lines_new:
        if len(available_rows) <= i:
            print("Error: %i lines in file %s, insufficient lines to write index %i (%i required)" %(len(lines), csv_filepath, i, len(lines_new)))
            logger.error("Error: %i lines in file %s, insufficient lines to write index %i (%i required)", len(lines), csv_filepath, i, len(lines_new))
        else:
            logger.info("Adding line %s to line %i", line_new, available_rows[i] - 1)

        lines[available_rows[i] - 1] = line_new
        i += 1
        
    if len(lines_new) == 0:
        logger.info("No new lines to add, skipping replacement")
    
    csv_filepath = make_cop_path(merged_dir, channel, cop_name)
    write_cop_csv(csv_filepath, lines, ending="")

    rows_used = available_rows[:i]
    rows_unused = available_rows[i:]
    
    logger.info("%i new rows added to file %s", len(rows_used), csv_filepath)
    logger.info("%i rows still available in file %s", len(rows_unused), csv_filepath)

    return rows_used, rows_unused





def new_subdomain_rows(channel, new_obs_dict, sci_dir_in, subd_dir_out):

    logger.debug("new_subdomain_rows %s", [channel, new_obs_dict, sci_dir_in, subd_dir_out])

    cop_name = "science"
    path = make_cop_path(sci_dir_in, channel, cop_name)
    dict_list = read_cop_csv(path)
    
    
    
    #for science table - split into cals and science. Cals are added manually
    dict_list_sci = []
    for line_dict in dict_list:
        if line_dict["steppingPointer"] == 0 and line_dict["accumulationCount"] > 0: #science
            dict_list_sci.append(line_dict)
        
    logger.info("Read in %i non-empty and non-calibration lines from %s", len(dict_list_sci), path)
            
    
    lines = []
    
    #match new observations to existing rows
    for name, params in new_obs_dict.items():
        
        logger.info("Checking for observation %s %s in existing subdomain rows", name, params)
        
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
                logger.error("Error: observation not found in science table %s %s", matches, match_dict)
    
    
        line = ",".join([str(i) for i in science_rows]) + " # ORDERS " + " ".join([str(i) for i in orders]) + " -- " + science_comment
        
        lines.append(line)
        
        logger.info("Appending new subdomain row %s", line)

    
    #write new rows to file
    cop_name = "sub_domain"
    path = make_cop_path(subd_dir_out, channel, cop_name)
    write_cop_csv(path, lines)
    print("%i %s %s lines written to file %s" %(len(lines), channel, cop_name, path))
    logger.info("%i %s %s lines written to file %s" %(len(lines), channel, cop_name, path))

    


def new_science_rows(channel, new_obs_dict, old_sci_dir, sci_dir_out):
    """make science rows normal obs"""

    logger.debug("new_science_rows %s", [channel, new_obs_dict, old_sci_dir, sci_dir_out])


    #read in old science table
    cop_name = "science"
    path = make_cop_path(old_sci_dir, channel, cop_name)
    existing_dict_list = read_cop_csv(path)

    logger.info("Read in %i lines from %s", len(existing_dict_list), path)
    
    #remove index and comment dict entry from existing dict list for comparison with new rows
    for existing_dict in existing_dict_list:
        existing_dict.pop("index")
        existing_dict.pop("npp_index")
        existing_dict.pop("comment")



    sci_dict_list = []
    
    buffer_time = readout_wait_time[channel]
    
    for name, params in new_obs_dict.items():

        logger.info("Checking for observation %s %s in existing science rows", name, params)

        orders = params[0]
        it = params[1] #milliseconds
        rhythm = params[2]
        d_rows = params[3]
        n_orders = len(orders)
        
        binning = int(d_rows / (24 / n_orders) - 1)
        max_t = rhythm * 1000. - buffer_time #milliseconds in total for all orders
        n_accs = n_acc(max_t, d_rows, n_orders, it)
        # print("NAccs = %i from parameters %s" %(n_accs, [max_t, d_rows, n_orders, it]))
        logger.debug("NAccs = %i from parameters %s", n_accs, [max_t, d_rows, n_orders, it])
        
        
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
                    
                    logger.info("Adding new line to science dictionary %s", sci_dict)

                else:
                    logger.info("Line already in existing science cop table %s", sci_dict)

            else:
                logger.info("Line already in science dictionary %s", sci_dict)
                
    
    #sort by order
    sci_dict_list = sorted(sci_dict_list, key=lambda d: d["aotfPointer"]) 
    
    
    #now convert dicts to lines
    
    if len(sci_dict_list) == 0:
        logger.info("All lines already in table, none added")
    else:
        logger.info("Adding %i lines to the science table", len(sci_dict_list))
    
    lines = []
    
    for d in sci_dict_list:
        #0,1,1,122,0,18,17,205000 # NADIR_144ROWS_15SECS_3SUBDS -- EXECTIME=14373MS
        
        execution_time = exec_time(d["accumulationCount"], d["other"]["d_rows"], d["other"]["n_orders"], d["integrationTime"]/1000.0)


        if d["integrationTime"] < 5000: #if less than 5ms
            comment_type = "OCCULTATION"
        elif d["integrationTime"] > 100000: #if more than 100ms
            comment_type = "NADIR"
        else:
            print("Error: observation type comment unknown")

        
        comment = "%s_%iROWS_%iSECS_%iSUBDS -- EXECTIME=%iMS" \
            %(comment_type, d["other"]["d_rows"], d["other"]["rhythm"], d["other"]["n_orders"], execution_time)
        line = "%i,%i,%i,%i,%i,%i,%i,%i # %s" %(d["degf"], d["dvaf"], d["sbsf"], d["aotfPointer"], d["steppingPointer"], d["accumulationCount"], d["binningFactor"], d["integrationTime"], comment)
        
        lines.append(line)


        logger.info("Appending new science row %s", line)

    
    #write new rows to file
    cop_name = "science"
    path = make_cop_path(sci_dir_out, channel, cop_name)
    write_cop_csv(path, lines)
    print("%i %s %s lines written to file %s" %(len(lines), channel, cop_name, path))
    logger.info("%i %s %s lines written to file %s" %(len(lines), channel, cop_name, path))







def new_fullscan_stepping_rows(channel, fullscan_dict_list, stepping_dir_out):

    # stepValue,steppingParameter,stepCount,stepSpeed
    # 0,INTEGRATION_TIME,0,0 # EMPTY ROW
    # 1,AOTF_IX,10,0 # FULLSCAN_10ORDERS_1SUBDS
    # 1,AOTF_IX,10,2 # FULLSCAN_10ORDERS_3SUBDS
    # 1,AOTF_IX,10,5 # FULLSCAN_10ORDERS_6SUBDS

    logger.debug("new_fullscan_stepping_rows %s", [channel, fullscan_dict_list, stepping_dir_out])

    
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
                
                logger.info("Adding to stepping dictionary %s", step_dict)
    
    
    lines = []
    
    for d in step_dict_list:
        #1,AOTF_IX,30,0 # FULLSCAN_30ORDERS_1SUBDS
        
        
        comment = "FULLSCAN_%iORDERS_%iSTEPPING_%iSUBDS" \
            %(d["stepCount"], d["stepValue"], d["stepSpeed"]+1)
        line = "%i,%s,%i,%i # %s" %(d["stepValue"], d["steppingParameter"], d["stepCount"], d["stepSpeed"], comment)
        
        lines.append(line)

        logger.info("Appending new stepping row %s", line)
    
        #write new rows to file
        cop_name = "stepping"
        path = make_cop_path(stepping_dir_out, channel, cop_name)
        write_cop_csv(path, lines)
    print("%i %s %s lines written to file %s" %(len(lines), channel, cop_name, path))
    logger.info("%i %s %s lines written to file %s", len(lines), channel, cop_name, path)




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
            d_found = dict(d)
            
    if found:
        logger.debug("Stepping line found: %s", d_found)
        return index
    else:
        print("Error %s line not found in %s with parameters" %(channel, stepping_dir), stepValue, stepCount, stepSpeed)
        logger.error("%s line not found in %s with parameters %s", channel, stepping_dir, [stepValue, stepCount, stepSpeed])
    



def new_fullscan_science_rows(channel, fullscan_dict_list, stepping_dir_in, sci_dir_out):
    """make science rows fullscans"""

    # make new science rows
    # 0,1,1,165,5,60,5,190000 # NADIR_FULLSCAN_SLOW_10ORDERS_144ROWS_15SECS_1SUBDS -- EXECTIME=14466MS
    # degf,dvaf,sbsf,aotfPointer,steppingPointer,accumulationCount,binningFactor,integrationTime

    logger.debug("new_fullscan_science_rows %s", [channel, fullscan_dict_list, stepping_dir_in, sci_dir_out])

    
    sci_dict_list = []
    
    for fullscan in fullscan_dict_list:
        start_order = fullscan["start"]
        stepCount = fullscan["steps"]
        stepValue = fullscan["step"]
    
        for rhythm in fullscan["rhythms"]:
            for stepSpeed, binnings in fullscan["steps_binning"].items():
        
                for binning in binnings:
                    
                    for approx_it in fullscan["approx_it"]:
        
                    
                        it = get_int_time(rhythm, stepSpeed, binning, approx_it)
        
                        d_rows = int((24 / stepSpeed) * (binning+1))
            
                        max_t = rhythm * 1000. - readout_wait_time[channel] #milliseconds in total for all orders
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
        
                            logger.info("Adding to science dictionary %s", sci_dict)

    #sort by order
    # sci_dict_list = sorted(sci_dict_list, key=lambda d: d["aotfPointer"]) 
    
    
    #now convert dicts to lines
    
    lines = []
    
    for d in sci_dict_list:
        # 0,1,1,165,6,18,17,205000 # NADIR_FULLSCAN_FAST_10ORDERS_144ROWS_15SECS_3SUBDS -- EXECTIME=14373MS
        
        execution_time = exec_time(d["accumulationCount"], d["other"]["d_rows"], d["other"]["stepSpeed"], d["integrationTime"]/1000.0)

        if d["integrationTime"] < 5000: #if less than 5ms
            comment_type = "OCCULTATION"
        elif d["integrationTime"] > 100000: #if more than 100ms
            comment_type = "NADIR"
        else:
            print("Error: observation type comment unknown")



        comment = "%s_FULLSCAN_FAST_%iORDERS_%iROWS_%iSECS_%iSUBDS -- EXECTIME=%iMS" \
            %(comment_type, d["other"]["stepCount"], d["other"]["d_rows"], d["other"]["rhythm"], d["other"]["stepSpeed"], execution_time)
        line = "%i,%i,%i,%i,%i,%i,%i,%i # %s" %(d["degf"], d["dvaf"], d["sbsf"], d["aotfPointer"], d["steppingPointer"], d["accumulationCount"], d["binningFactor"], d["integrationTime"], comment)
        
        lines.append(line)

        logger.info("Appending new science row %s", line)
    
    #write new rows to file
    cop_name = "science"
    path = make_cop_path(sci_dir_out, channel, cop_name)
    write_cop_csv(path, lines)
    print("%i %s %s lines written to file %s" %(len(lines), channel, cop_name, path))
    logger.info("%i %s %s lines written to file %s" %(len(lines), channel, cop_name, path))



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
        existing_dict.pop("npp_index")
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
        
        if channel == "so" and d["rythm"]==1:
            comment = "OCCULTATION"
        elif channel == "lno" and d["rythm"] > 1:
            comment = "NADIR"
        else:
            print("Error: observation type comment unknown")
            
        line = "%i,%i,%i,%i,%i,%i,%i # %s" %(d["windowLineCount"], d["windowLeftTop"], d["detectorSupply"], d["aotfDelay"], \
                                             d["dataSource"], d["dataValidSource"], d["rythm"], comment)
        
        logger.info("Adding new line to fixed file: %s", line)
        lines.append(line)
    
    #write new rows to file
    cop_name = "fixed"
    path = make_cop_path(fixed_dir_out, channel, cop_name)
    write_cop_csv(path, lines)
    print("%i %s %s lines written to file %s" %(len(lines), channel, cop_name, path))
    logger.info("%i %s %s lines written to file %s", len(lines), channel, cop_name, path)



def new_fullscan_fixed_rows(channel, fullscan_dict_list, centre_rows):
    """make fixed rows for new fullscan obs"""

    fixed_dict_list = []
    
    for fullscan in fullscan_dict_list:
        for rhythm in fullscan["rhythms"]:
            for stepSpeed, binnings in fullscan["steps_binning"].items():
        
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
        
        if channel == "so" and d["rythm"]==1:
            comment = "OCCULTATION"
        elif channel == "lno" and d["rythm"] > 1:
            comment = "NADIR"
        else:
            print("Error: observation type comment unknown")

        line = "%i,%i,%i,%i,%i,%i,%i # %s" %(d["windowLineCount"], d["windowLeftTop"], d["detectorSupply"], d["aotfDelay"], \
                                             d["dataSource"], d["dataValidSource"], d["rythm"], comment)

        logger.info("Adding new line to fixed file (fullscan): %s", line)

        lines.append(line)
    
    #write new rows to file
    cop_name = "fixed"
    path = make_cop_path(temp_dir_name, channel, cop_name)
    write_cop_csv(path, lines)
    print("%i %s %s lines written to file %s" %(len(lines), channel, cop_name, path))
    logger.info("%i %s %s lines written to file %s", len(lines), channel, cop_name, path)



def new_subdomain_fullscan_rows(channel, stepping_dir_in, sci_dir_in, subd_dir_out, science_rows_to_add=[]):

    logger.debug("new_subdomain_fullscan_rows %s", [channel, stepping_dir_in, sci_dir_in, subd_dir_out, science_rows_to_add])

    #read in existing lines from stepping table
    cop_name = "stepping"
    path = make_cop_path(stepping_dir_in, channel, cop_name)
    stepping_dict_list = read_cop_csv(path)
    
    #get indices of fullscans from stepping table
    fullscan_indices = [d["index"] for d in stepping_dict_list if d["steppingParameter"] == "AOTF_IX"]
    
    
    
    
    #read in new lines
    cop_name = "science"
    path = make_cop_path(sci_dir_in, channel, cop_name)
    dict_list = read_cop_csv(path)
    
    dict_list_fullscan = []
    for line_dict in dict_list:
        
        
        #if manual selection of the rows to be added
        if len(science_rows_to_add) > 0:

            #if the row is not in one of these, skip
            if line_dict["npp_index"] not in science_rows_to_add: #row starts at 0, science
                continue
        
        if line_dict["steppingPointer"] > 0 and line_dict["accumulationCount"] > 0: #fullscan cal or science
            if line_dict["steppingPointer"] in fullscan_indices:
                
                dict_list_fullscan.append(line_dict)

                logger.info("Adding to fullscan subdomain dictionary %s", line_dict)
        
    
        if len(dict_list_fullscan) == 0:
            print("Error: no matching stepping row found in table")
            logger.error("No matching stepping row found in table with parameters %s", line_dict)
    
    matching_fullscans = []
    
    for dict_fullscan in dict_list_fullscan:
        comment = dict_fullscan["comment"]
        parsed = parse_fullscan_science_comment(comment)
    
        #search only for the new lines for Phobos obs
        #those where rows < 25 and rhythm > 7
        # if parsed["rows"] < 25 and parsed["rhythm"] > 7:
        matching_fullscans.append(dict_fullscan)
    
    
    
    #now convert dicts to lines
    lines = []
    
    for d in matching_fullscans:
        # 89,0,0,0,0,0 #  NADIR_FULLSCAN_FAST_10ORDERS_144ROWS_15SECS_3SUBDS -- EXECTIME=14373MS
        
        first_order = d["aotfPointer"]
        
        stepping_dicts = [d2 for d2 in stepping_dict_list if d2["index"] == d["steppingPointer"]]
        
        if len(stepping_dicts) == 1:
            stepping_dict = stepping_dicts[0]
        else:
            print("Unknown error")
            logger.error("Unknown error")
            
        stepCount = stepping_dict["stepCount"]
        stepValue = stepping_dict["stepValue"]
        
        last_order = first_order + stepCount * stepValue
        
        parsed = parse_fullscan_science_comment(d["comment"])

        if channel == "so" and parsed["exec_time"] < 1000:
            comment_type = "OCCULTATION"
        elif channel == "lno" and parsed["exec_time"] > 1000:
            comment_type = "NADIR"
        else:
            print("Error: observation type comment unknown")

    
        comment = "%s_FULLSCAN_FAST_%i-%i-%iORDERS_%iROWS_%iSECS_%iSUBDS -- EXECTIME=%iMS" \
            %(comment_type, first_order, stepValue, last_order, parsed["rows"], parsed["rhythm"], parsed["n_orders"], parsed["exec_time"])
    
        
        line = "%i,0,0,0,0,0 # %s" %(d["index"], comment)
        
        lines.append(line)

        logger.info("Appending new fullscan subdomain row: %s", line)
        
        #write new rows to file
        cop_name = "sub_domain"
        path = make_cop_path(temp_dir_name, channel, cop_name)
        write_cop_csv(path, lines)
    print("%i %s %s lines written to file %s" %(len(lines), channel, cop_name, path))
    logger.info("%i %s %s lines written to file %s", len(lines), channel, cop_name, path)



if __name__ == "__main__":

    if MAKE_TABLES:
    
        existing_dir = old_dir_name
        new_lines_dir = temp_dir_name
        merged_dir = new_dir_name
        
        
        """ SO patch"""
        
        """normal obs"""


        if "so_fixed" in OBS_TO_UPDATE:
            # new fixed rows
            
            logger.info("### SO fixed ###")
            
            fixed_dir_out = temp_dir_name
            rows_to_replace = available_cop_rows["so"]["fixed"]
            
            new_fixed_rows("so", new_so_obs_dict, so_centre_rows, existing_dir, fixed_dir_out) #write new lines to temp dir
            # then read in old directory, merge new lines and output to new dir
            replace_lines("so", "fixed", rows_to_replace, existing_dir, new_lines_dir, merged_dir) #first line to start replacing rows (as given in notepad++)



        if "so_science" in OBS_TO_UPDATE:
           # new science rows

            logger.info("### SO science ###")

            sci_dir_out = temp_dir_name
            rows_to_replace = available_cop_rows["so"]["science"]
            
            new_science_rows("so", new_so_obs_dict, existing_dir, sci_dir_out) #write new lines to temp dir
            # then read in old directory, merge new lines and output to new dir
            so_science_used_rows, so_science_unused_rows = replace_lines("so", "science", rows_to_replace, existing_dir, new_lines_dir, merged_dir) #first line to start replacing rows (as given in notepad++)
            
            #rename new file to avoid copying over with fullscans - only for checking later
            csv_filepath = make_cop_path(new_lines_dir, "so", "science")
            csv_filepath2 = make_cop_path(new_lines_dir, "so", "science_normal")
            logger.info("Renaming %s -> %s", csv_filepath, csv_filepath2)
            os.rename(csv_filepath, csv_filepath2)
        
        
        
            # add new subdomains
            logger.info("### SO subdomain ###")

            sci_dir_in = merged_dir #need to use updated science table
            subd_dir_out = temp_dir_name
            rows_to_replace = available_cop_rows["so"]["sub_domain"]
            
            new_subdomain_rows("so", new_so_obs_dict, sci_dir_in, subd_dir_out) #write new lines to temp dir
            # then read in old directory, merge new lines and output to new dir
            so_sub_domain_used_rows, so_sub_domain_unused_rows = replace_lines("so", "sub_domain", rows_to_replace, existing_dir, new_lines_dir, merged_dir) #first line to start replacing rows (as given in notepad++)

            #rename new file to avoid copying over with fullscans
            csv_filepath = make_cop_path(new_lines_dir, "so", "sub_domain")
            csv_filepath2 = make_cop_path(new_lines_dir, "so", "sub_domain_normal")
            logger.info("Renaming %s -> %s", csv_filepath, csv_filepath2)
            os.rename(csv_filepath, csv_filepath2)
        

        

        """fullscans"""
        if "so_fullscan_fixed" in OBS_TO_UPDATE:
            # new fixed rows - already covered by previous normal obs
            
            logger.info("### SO fullscan fixed ###")

            new_fullscan_fixed_rows("so", so_fullscans, so_centre_rows)
            replace_lines("so", "fixed", 231, existing_dir, new_lines_dir, merged_dir) #first line to start replacing rows (as given in notepad++)



        if "so_fullscan_stepping" in OBS_TO_UPDATE:
            # new stepping rows

            logger.info("### SO fullscan stepping ###")

            stepping_dir_out = temp_dir_name
            rows_to_replace = available_cop_rows["so"]["stepping"]
            
            new_fullscan_stepping_rows("so", so_fullscans, stepping_dir_out) #write new lines to temp dir
            # then read in old directory, merge new lines and output to new dir
            replace_lines("so", "stepping", rows_to_replace, existing_dir, new_lines_dir, merged_dir) #first line to start replacing rows (as given in notepad++)

            
            
            
        if "so_fullscan_science" in OBS_TO_UPDATE:
            # new science rows for fullscans (requires stepping to be already updated)

            logger.info("### SO fullscan science ###")

            if "so_fullscan_stepping" in OBS_TO_UPDATE:
                stepping_dir_in = merged_dir #need to use updated stepping table
            else:
                stepping_dir_in = old_dir_name #use old stepping table

            sci_dir_out = temp_dir_name #write to new temp dir
            
            existing_dir = merged_dir #use updated so science table
            
            new_fullscan_science_rows("so", so_fullscans, stepping_dir_in, sci_dir_out) #write new lines to temp dir
            # then read in old directory, merge new lines and output to new dir
            so_science_used_rows, so_science_unused_rows = replace_lines("so", "science", so_science_unused_rows, existing_dir, new_lines_dir, merged_dir) #first line to start replacing rows (as given in notepad++)
        
    
            #rename new file to keep a copy for checking later
            csv_filepath = make_cop_path(new_lines_dir, "so", "science")
            csv_filepath2 = make_cop_path(new_lines_dir, "so", "science_fullscan")
            logger.info("Renaming %s -> %s", csv_filepath, csv_filepath2)
            os.rename(csv_filepath, csv_filepath2)
    
        
        
            # subdomains are just single pointers to these rows
            # however they may not be to the same rows in the subdomain and science tables
            logger.info("### SO fullscan subdomain ###")

            if "so_fullscan_stepping" in OBS_TO_UPDATE:
                stepping_dir_in = merged_dir #need to use updated stepping table
            else:
                stepping_dir_in = old_dir_name #use old stepping table

            sci_dir_in = merged_dir #need to use updated science table
            subd_dir_out = temp_dir_name
            
            existing_dir = merged_dir #use updated lno science table
            
            new_subdomain_fullscan_rows("so", stepping_dir_in, sci_dir_in, subd_dir_out, science_rows_to_add=so_science_used_rows) #write new lines to temp dir
            # then read in old directory, merge new lines and output to new dir
            replace_lines("so", "sub_domain", so_sub_domain_unused_rows, existing_dir, new_lines_dir, merged_dir) #first line to start replacing rows (as given in notepad++)
        

            #rename new file to keep a copy for checking later
            csv_filepath = make_cop_path(new_lines_dir, "so", "sub_domain")
            csv_filepath2 = make_cop_path(new_lines_dir, "so", "sub_domain_fullscan")
            logger.info("Renaming %s -> %s", csv_filepath, csv_filepath2)
            os.rename(csv_filepath, csv_filepath2)
    
    







        """LNO patch"""
            
        existing_dir = old_dir_name
        new_lines_dir = temp_dir_name
        merged_dir = new_dir_name

        """normal obs"""
        
        
        if "lno_fixed" in OBS_TO_UPDATE:
            # new fixed rows

            logger.info("### LNO fixed ###")

            fixed_dir_out = temp_dir_name
            rows_to_replace = available_cop_rows["lno"]["fixed"]
            
            new_fixed_rows("lno", new_lno_obs_dict, lno_centre_rows, existing_dir, fixed_dir_out) #write new lines to temp dir
            # then read in old directory, merge new lines and output to new dir
            replace_lines("lno", "fixed", rows_to_replace, existing_dir, new_lines_dir, merged_dir) #first line to start replacing rows (as given in notepad++)
        
        
        if "lno_science" in OBS_TO_UPDATE:
            # new science rows

            logger.info("### LNO science ###")

            sci_dir_out = temp_dir_name
            rows_to_replace = available_cop_rows["lno"]["science"]
            
            new_science_rows("lno", new_lno_obs_dict, existing_dir, sci_dir_out) #write new lines to temp dir
            # then read in old directory, merge new lines and output to new dir
            lno_science_used_rows, lno_science_unused_rows = replace_lines("lno", "science", rows_to_replace, existing_dir, new_lines_dir, merged_dir) #first line to start replacing rows (as given in notepad++)
            
            #rename new file to avoid copying over with fullscans - only for checking later
            csv_filepath = make_cop_path(new_lines_dir, "lno", "science")
            csv_filepath2 = make_cop_path(new_lines_dir, "lno", "science_normal")
            logger.info("Renaming %s -> %s", csv_filepath, csv_filepath2)
            os.rename(csv_filepath, csv_filepath2)
            
            
            # add new subdomains
            logger.info("### LNO subdomain ###")

            sci_dir_in = merged_dir #need to use updated science table
            subd_dir_out = temp_dir_name
            rows_to_replace = available_cop_rows["lno"]["sub_domain"]
            
            new_subdomain_rows("lno", new_lno_obs_dict, sci_dir_in, subd_dir_out) #write new lines to temp dir
            # then read in old directory, merge new lines and output to new dir
            lno_sub_domain_used_rows, lno_sub_domain_unused_rows = replace_lines("lno", "sub_domain", rows_to_replace, existing_dir, new_lines_dir, merged_dir) #first line to start replacing rows (as given in notepad++)
            
            #rename new file to avoid copying over with fullscans
            csv_filepath = make_cop_path(new_lines_dir, "lno", "sub_domain")
            csv_filepath2 = make_cop_path(new_lines_dir, "lno", "sub_domain_normal")
            logger.info("Renaming %s -> %s", csv_filepath, csv_filepath2)
            os.rename(csv_filepath, csv_filepath2)
        
        
        
        
        """fullscans"""
        if "lno_fullscan_fixed" in OBS_TO_UPDATE:
            # new fixed rows - already covered by previous normal obs

            logger.info("### LNO fullscan fixed ###")

            new_fullscan_fixed_rows("lno", lno_fullscans, lno_centre_rows)
            replace_lines("lno", "fixed", 231, existing_dir, new_lines_dir, merged_dir) #first line to start replacing rows (as given in notepad++)



        if "lno_fullscan_stepping" in OBS_TO_UPDATE:
            # new stepping rows

            logger.info("### LNO fullscan stepping ###")

            stepping_dir_out = temp_dir_name
            rows_to_replace = available_cop_rows["lno"]["stepping"]
            
            new_fullscan_stepping_rows("lno", lno_fullscans, stepping_dir_out) #write new lines to temp dir
            # then read in old directory, merge new lines and output to new dir
            replace_lines("lno", "stepping", rows_to_replace, existing_dir, new_lines_dir, merged_dir) #first line to start replacing rows (as given in notepad++)
            
            
            
        if "lno_fullscan_science" in OBS_TO_UPDATE:
            # new science rows for fullscans (requires stepping to be already updated)

            logger.info("### LNO fullscan science ###")


            if "lno_fullscan_stepping" in OBS_TO_UPDATE:
                stepping_dir_in = merged_dir #need to use updated stepping table
            else:
                stepping_dir_in = old_dir_name #use old stepping table

            sci_dir_out = temp_dir_name
            
            existing_dir = merged_dir #use updated lno science table
            
            new_fullscan_science_rows("lno", lno_fullscans, stepping_dir_in, sci_dir_out) #write new lines to temp dir
            # then read in old directory, merge new lines and output to new dir
            lno_science_used_rows, lno_science_unused_rows = replace_lines("lno", "science", lno_science_unused_rows, existing_dir, new_lines_dir, merged_dir) #first line to start replacing rows (as given in notepad++)
        

            #rename new file to keep a copy for checking later
            csv_filepath = make_cop_path(new_lines_dir, "lno", "science")
            csv_filepath2 = make_cop_path(new_lines_dir, "lno", "science_fullscan")
            logger.info("Renaming %s -> %s", csv_filepath, csv_filepath2)
            os.rename(csv_filepath, csv_filepath2)
    
    
        
        
            # subdomains are just single pointers to these rows
            logger.info("### LNO fullscan subdomain ###")

            # however they may not be to the same rows in the subdomain and science tables
            stepping_dir_in = old_dir_name #need to use old stepping table
            sci_dir_in = merged_dir #need to use updated science table
            subd_dir_out = temp_dir_name
            
            existing_dir = merged_dir #use updated lno science table
            
            new_subdomain_fullscan_rows("lno", stepping_dir_in, sci_dir_in, subd_dir_out, science_rows_to_add=lno_science_used_rows) #write new lines to temp dir
            # then read in old directory, merge new lines and output to new dir
            replace_lines("lno", "sub_domain", lno_sub_domain_unused_rows, existing_dir, new_lines_dir, merged_dir) #first line to start replacing rows (as given in notepad++)
        
    
            #rename new file to keep a copy for checking later
            csv_filepath = make_cop_path(new_lines_dir, "lno", "sub_domain")
            csv_filepath2 = make_cop_path(new_lines_dir, "lno", "sub_domain_fullscan")
            logger.info("Renaming %s -> %s", csv_filepath, csv_filepath2)
            os.rename(csv_filepath, csv_filepath2)
    



    """check all new SO and LNO rows"""


    for channel in ["so", "lno"]:

        print("Checking for %s errors" %channel)
        
        cop_name = "stepping"
        #TODO: choose old or new based on whether updated stepping
        if channel == "so":
            if "so_fullscan_stepping" in OBS_TO_UPDATE:
                path = make_cop_path(new_dir_name, channel, cop_name)
            else:
                path = make_cop_path(old_dir_name, channel, cop_name)

        elif channel == "lno":
            if "lno_fullscan_stepping" in OBS_TO_UPDATE:
                path = make_cop_path(new_dir_name, channel, cop_name)
            else:
                path = make_cop_path(old_dir_name, channel, cop_name)


            
        # path = make_cop_path(old_dir_name, channel, cop_name)
        stepping_dict_list = read_cop_csv(path)
        
        cop_name = "science"
        path = make_cop_path(new_dir_name, channel, cop_name)
        sci_dict_list = read_cop_csv(path)
        
        cop_name = "sub_domain"
        path = make_cop_path(new_dir_name, channel, cop_name)
        subd_dict_list_all = read_cop_csv(path)
        
        subd_rows_to_check = available_cop_rows[channel]["sub_domain"]
        
        # subd_rows_to_check = list(range(284, 508)) + list(range(3794, 4095))
        # subd_rows_to_check = list(range(284, 305))
        
        sub_dict_list = [d for d in subd_dict_list_all if d["index"] in subd_rows_to_check and d["science_1"] != 0]
        
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
                        print("Error: timings wrong, total execution time must be <1 second smaller than the rhythm")
                        print(subd_parsed_dict, sci_dict)
                        print(n_rows, dt)
                        sys.exit()
                        
                    elif sci_dict["comment"] not in sub_dict["comment"]:
                        print("Error: comments don't match")
                        sys.exit()
                    
                    #if not exiting
                    print("Line passes tests: %s" %sub_dict["comment"])
                    
                    # print(sci_dict["comment"])
                
            elif "start" in subd_parsed_dict.keys(): #if fullscan
            
                #check science 2 to 6 are all set to 0
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
                
                if et < 1000: #if less than 5ms
                    comment_type = "OCCULTATION"
                elif et > 100: #if more than 100ms
                    comment_type = "NADIR"
                else:
                    print("Error: observation type comment unknown")
                
                
                text = "%s_FULLSCAN_FAST_%i-%i-%iORDERS_%iROWS_%iSECS_%iSUBDS -- EXECTIME=%iMS" %(comment_type, start, step, stop, d_rows, rhythm, n_orders, et)
                
                if text != sub_dict["comment"]:
                    print("Error: comments don't match")
                    print(text)
                    print(sub_dict["comment"])
                    # sys.exit()
                else:
                    print("Line passes tests: %s" %text)
                    
            else:
                print("No science found, skipping line")
                
            # print("################")
    
print("Done: see %s for log" %logger_name)

logging.shutdown()
logger.handlers.clear()

