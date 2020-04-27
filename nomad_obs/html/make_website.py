# -*- coding: utf-8 -*-
"""
Created on Mon Apr 27 12:35:00 2020

@author: iant
"""


import os
from datetime import datetime
from nomad_obs.config.paths import OBS_DIRECTORY

from nomad_obs.other.generic_functions import getMtpTimes





def writeMtpMasterPage(mtpConstants, paths):
    """write the master page up to the current mtp"""
    mtpNumber = mtpConstants["mtpNumber"]


    mtpStartString, mtpEndString, mtpStartLs, mtpEndLs = getMtpTimes(mtpNumber)
        
    """write mtp master page"""
    h = r""
    h += r"<h1>MTP%03d Planning (%s - %s, Ls: %0.0f - %0.0f)</h1>" %(mtpNumber, mtpStartString, mtpEndString, mtpStartLs, mtpEndLs)
    pagename = "nomad_mtp%03d_overview.html" %(mtpNumber); desc = "MTP Overview"
    h += r"<p><a href=%s>%s</a></p>" %(pagename, desc)
    pagename = "nomad_mtp%03d_occultation.html" %(mtpNumber); desc = "MTP Occultation Observations"
    h += r"<p><a href=%s>%s</a></p>" %(pagename, desc)
    pagename = "nomad_mtp%03d_nadir.html" %(mtpNumber); desc = "MTP Nadir Observations"
    h += r"<p><a href=%s>%s</a></p>" %(pagename, desc)
    #pagename = "nomad_mtp%03d_merged.html" %(mtpNumber); desc = "MTP Merged Observation Plan"
    #h += r"<p><a href=%s>%s</a></p>" %(pagename, desc)
    
#    pagename = "nomad_mtp%03d_uvis.html" %(mtpNumber); desc = "MTP UVIS Observation Plan"
#    h += r"<p><a href=%s>%s</a></p>" %(pagename, desc)
    h += r"<br>"+"\n"
    
    h += r"<br>"+"\n"
    h += r"<p>Page last modified: %s</p>" %(datetime.now().strftime('%a, %d %b %Y %H:%M:%S')) +"\n"
    pagename = "../../event_files/LEVF_M%03d_SOC_PLANNING.EVF" %(mtpNumber); desc = "."
    h += r"<p><a href=%s>%s</a></p>" %(pagename, desc)
    pagename = "../../itls/MITL_M%03d_NOMAD.ITL" %(mtpNumber); desc = "."
    h += r"<p><a href=%s>%s</a></p>" %(pagename, desc)
    
    with open(os.path.join(paths["HTML_MTP_PATH"], "nomad_mtp%03d.html" %(mtpNumber)), 'w') as f:
        f.write(h)



def writeIndexWebpage(mtpConstants, paths):
    """update website index page with latest mtp"""    
    mtpNumber = mtpConstants["mtpNumber"]



#    MASTER_PAGE_NAMES = ["EXM-NO-SNO-AER-00028-iss0rev4-SO_LNO_COP_Table_Order_Combinations-180528.htm", \
#              "EXM-NO-SNO-AER-00027-iss0rev8-Science_Orbit_Observation_Rules-180306.pdf", \
#              "EXM-NO-PRS-AER-00172-iss0rev0-HDF5_Files_Description_180712.pdf"]
#
#    MASTER_PAGE_DESCRIPTIONS = ["SO and LNO diffraction order combinations", \
#                     "NOMAD Orbit Types and Observation Rules", \
#                     "Description of NOMAD Data and Observations"]


    allMtps = range(1, mtpNumber+1)
    

    
    h = r""
    h += r"<h1>NOMAD Observation Page</h1>"+"\n"
#    h += r"<h2>Miscellaneous Information</h2>"+"\n"
    h += r"<h2>These pages are being merged into the new website at <a href='https://nomad.aeronomie.be'>nomad.aeronomie.be</a></h2>"+"\n"
    h += r"<br>"+"\n"
    h += r"<br>"+"\n"

#    pagename = "nomad_faqs.html"
#    desc = "***Frequently Asked Questions***"
#    h += r"<p><a href=%s>%s</a></p>" %("pages/"+pagename,desc)+"\n"

#    for pageName,pageDescription in zip(MASTER_PAGE_NAMES,MASTER_PAGE_DESCRIPTIONS):
#        h += r"<p><a href=%s>%s</a> - %s</p>" %("pages/"+pageName,pageName,pageDescription)+"\n"

   
    h += r"<h2>NOMAD Past Observations</h2>"+"\n"
    pagename = "nomad_ground_cal_obs.html"; desc="NOMAD Ground Calibration and Recalibration following LNO detector swap"
    h += r"<p><a href=%s>%s</a> - %s</p>" %("pages/"+pagename,pagename,desc)+"\n"
    pagename = "nomad_nec_obs.html"; desc="NOMAD Near Earth Commissioning"
    h += r"<p><a href=%s>%s</a> - %s</p>" %("pages/"+pagename,pagename,desc)+"\n"
    pagename = "nomad_mcc_obs.html"; desc="NOMAD Mid-Cruise Checkout"
    h += r"<p><a href=%s>%s</a> - %s</p>" %("pages/"+pagename,pagename,desc)+"\n"
    pagename = "nomad_mco_obs.html"; desc="NOMAD Mars Capture Orbit"
    h += r"<p><a href=%s>%s</a> - %s</p>" %(("pages/MCO/"+pagename),pagename,desc)+"\n"
    pagename = "nomad_mco2_obs.html"; desc="NOMAD Mars Capture Orbit Part 2"
    h += r"<p><a href=%s>%s</a> - %s</p>" %(("pages/MCO2/"+pagename),pagename,desc)+"\n"
    
    mtpStartString, mtpEndString, mtpStartLs, mtpEndLs = getMtpTimes(0)
    
    pagename = "nomad_commissioning.html"; desc="Post-Aerobraking Commissioning Phase (%s - %s, Ls: %0.0f - %0.0f)" %(mtpStartString, mtpEndString, mtpStartLs, mtpEndLs)
    h += r"<p><a href=%s>%s</a> - %s</p>" %("mtp_pages/mtp000/"+pagename,pagename,desc)+"\n"


    h += r"<h2>NOMAD Nominal Science Observations</h2>"+"\n"

    for mtpIndex in allMtps:
            
        mtpStartString, mtpEndString, mtpStartLs, mtpEndLs = getMtpTimes(mtpIndex)
        
        pagename = "nomad_mtp%03d.html" %(mtpIndex); desc="Medium Term Planning MTP%03d (%s - %s, Ls: %0.0f - %0.0f)" %(mtpIndex, mtpStartString, mtpEndString, mtpStartLs, mtpEndLs)
        h += r"<p><a href=%s>%s</a> - %s</p>" \
            %(("mtp_pages/mtp%03d" %mtpIndex +os.sep+pagename),pagename,desc)+"\n"

    h += r"<br>"+"\n"

    pagename = "science_calibrations.html"; desc="Calibrations During Nominal Science Period"
    h += r"<p><a href=%s>%s</a> - %s</p>" %("calibrations/"+pagename,pagename,desc)+"\n"
    h += r"<br>"+"\n"
    h += r"<br>"+"\n"
    h += r"<p>Page last modified: %s</p>" %(datetime.now().strftime('%a, %d %b %Y %H:%M:%S')) +"\n"

    with open(os.path.join(OBS_DIRECTORY, "index.html"), 'w') as f:
        f.write(h)


