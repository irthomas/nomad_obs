# -*- coding: utf-8 -*-
"""
Created on Mon Apr 27 12:33:07 2020

@author: iant
"""

import numpy as np
import os
import matplotlib.pyplot as plt
import spiceypy as sp
from datetime import datetime

from nomad_obs.config.constants import FIG_X, FIG_Y
from nomad_obs.config.constants import NADIR_SEARCH_STEP_SIZE, OCCULTATION_SEARCH_STEP_SIZE
from nomad_obs.config.constants import INITIALISATION_TIME, PRECOOLING_TIME
from nomad_obs.planning.spice_functions import getLonLatLst, getLonLatIncidenceLst, getTangentAltitude
from nomad_obs.cop_rows.cop_table_functions import getObsParameters



def makeOverviewPage(orbit_list, mtpConstants, paths, occultationObservationDict, nadirObservationDict):
    """plot occultation orders for mtp overview page"""
    mtpNumber = mtpConstants["mtpNumber"]
    obsTypeNames = {"ingress":"irIngressLow", "egress":"irEgressLow"}

    
    #loop through once to find list of all orders measured
    ordersAll = []
    for orbit in orbit_list:
        occultationObsTypes = [occultationType for occultationType in orbit["allowedObservationTypes"][:] if occultationType in ["ingress", "egress"]]    
        for occultationObsType in occultationObsTypes:
            if occultationObsType in orbit.keys():
                obsTypeName = obsTypeNames[occultationObsType]
    
                orders = orbit["finalOrbitPlan"][obsTypeName+"Orders"]
                if 0 in orders: #remove darks
                    orders.remove(0)
                if "COP#" in "%s" %orders[0]: #remove manual COP selection
                    orders = []
                ordersAll.extend(orders)
    uniqueOccultationOrders = sorted(list(set(ordersAll)))
    
    #loop through again to plot each order on a single graph
    for chosenOrder in uniqueOccultationOrders:
        title = "Solar occultations for diffraction order %s" %(chosenOrder)
        fig = plt.figure(figsize=(FIG_X, FIG_Y))
        ax = fig.add_subplot(111, projection="mollweide")
        ax.grid(True)
        plt.title(title)
    
        lonsAll = [] #pre-make list of all observing points of this order, otherwise colourbar scale will be incorrect
        latsAll = []
        altsAll = []
        for orbit in orbit_list:
            occultationObsTypes = [occultationType for occultationType in orbit["allowedObservationTypes"][:] if occultationType in ["ingress", "egress"]]    
            for occultationObsType in occultationObsTypes:
                if occultationObsType in orbit.keys():
                    obsTypeName = obsTypeNames[occultationObsType]
        
                    orders = orbit["finalOrbitPlan"][obsTypeName+"Orders"]
                    if chosenOrder in orders:
                        occultation = orbit[occultationObsType]
                        
                        #if lats/lons/alts not yet in orbitList, find and write to list
                        if "alts" not in occultation.keys():
                            #just plot the half of the occultation closest to the surface, not the high altitude bits
                            #ignore merged or grazing occs at this point
                            if occultationObsType == "ingress":
                                ets = np.arange(occultation["etMidpoint"], occultation["etEnd"], OCCULTATION_SEARCH_STEP_SIZE)
                            elif occultationObsType == "egress":
                                ets = np.arange(occultation["etStart"], occultation["etMidpoint"], OCCULTATION_SEARCH_STEP_SIZE)
                            lonsLatsLsts = np.asfarray([getLonLatLst(et) for et in ets])
                            occultation["lons"] = lonsLatsLsts[:, 0]
                            occultation["lats"] = lonsLatsLsts[:, 1]
                            occultation["alts"] = np.asfarray([getTangentAltitude(et) for et in ets])
                            
                        #else take lats/lons/alts from orbitList if already exists
                        lonsAll.extend(occultation["lons"])
                        latsAll.extend(occultation["lats"])
                        altsAll.extend(occultation["alts"])
                        
        plot1 = ax.scatter(np.asfarray(lonsAll)/sp.dpr(), np.asfarray(latsAll)/sp.dpr(), \
                           c=np.asfarray(altsAll), cmap=plt.cm.jet, marker='o', linewidth=0)
    
        cbar = fig.colorbar(plot1, fraction=0.046, pad=0.04)
        cbar.set_label("Tangent Point Altitude (km)", rotation=270, labelpad=20)
        fig.tight_layout()
        plt.savefig(os.path.join(paths["IMG_MTP_PATH"], "occultations_mtp%03d_order%i_altitude.png" %(mtpNumber, chosenOrder)))
        plt.close()
    
    
    
    """plot nadir orders"""
    #find all orders measured
    ordersAll = []
    for orbit in orbit_list:
        if "dayside" in orbit["irMeasuredObsTypes"]:
            orders = orbit["finalOrbitPlan"]["irDaysideOrders"]
            if 0 in orders: #remove darks
                orders.remove(0)
            if "COP#" in "%s" %orders[0]: #remove manual COP selection
                orders = []
            ordersAll.extend(orders)
    uniqueNadirOrders = sorted(list(set(ordersAll)))
    
    #plot each order
    for chosenOrder in uniqueNadirOrders:
        title = "Dayside nadirs for diffraction order %s" %(chosenOrder)
        fig = plt.figure(figsize=(FIG_X, FIG_Y))
        ax = fig.add_subplot(111, projection="mollweide")
        ax.grid(True)
        plt.title(title)
    
        lonsAll = [] #pre-make list of all observing points of this order, otherwise colourbar scale will be incorrect
        latsAll = []
        anglesAll = []
        for orbit in orbit_list:
            if "dayside" in orbit["irMeasuredObsTypes"]:
                orders = orbit["finalOrbitPlan"]["irDaysideOrders"]
                if chosenOrder in orders:
                    nadir = orbit["dayside"]
                    
                    #if lats/lons/incidence angles not yet in orbitList, find and write to list
                    if "incidences" not in nadir.keys():
#                        print(orbit["orbitNumber"])
                        #nadir start/end times have been modified to fit thermal room
                        realStartTime = nadir["obsStart"] + PRECOOLING_TIME + INITIALISATION_TIME
                        realEndTime = nadir["obsEnd"]
                        ets = np.arange(realStartTime, realEndTime, NADIR_SEARCH_STEP_SIZE)
                        lonsLatsIncidencesLsts = np.asfarray([getLonLatIncidenceLst(et) for et in ets])
                        nadir["lons"] = lonsLatsIncidencesLsts[:, 0]
                        nadir["lats"] = lonsLatsIncidencesLsts[:, 1]
                        nadir["incidences"] = lonsLatsIncidencesLsts[:, 2]
                    #else take lats/lons/incidence angles from orbitList if already exists
                    lonsAll.extend(nadir["lons"])
                    latsAll.extend(nadir["lats"])
                    anglesAll.extend(nadir["incidences"])
                    
        plot1 = ax.scatter(np.asfarray(lonsAll)/sp.dpr(), np.asfarray(latsAll)/sp.dpr(), \
                           c=np.asfarray(anglesAll), cmap=plt.cm.jet, marker='o', linewidth=0)
    
        cbar = fig.colorbar(plot1, fraction=0.046, pad=0.04)
        cbar.set_label("Incidence Angle (degrees)", rotation=270, labelpad=20)
        fig.tight_layout()
        plt.savefig(os.path.join(paths["IMG_MTP_PATH"], "dayside_nadirs_mtp%03d_order%i_incidence_angle.png" %(mtpNumber, chosenOrder)))
        plt.close()

    """write mtp overview page"""
    h = r""
    h += r"<h1>MTP%03d Overview</h1>" %(mtpNumber)
    h += r"<h2>Geometry</h2>"+"\n"
    
    imagename = "mtp%03d_occultation_duration.png" %(mtpNumber)
    h += r"<img src='%s'>" %imagename
    imagename = "mtp%03d_occultation_lat.png" %(mtpNumber)
    h += r"<img src='%s'>" %imagename
    imagename = "mtp%03d_nadir_minimum_incidence_angle.png" %(mtpNumber)
    h += r"<img src='%s'>" %imagename
    
    h += r"<p>UVIS typically operates on all dayside nadirs and all occultations</p>"+"\n"
    
    h += r"<h2>Solar Occultations</h2>"+"\n"
    
    h += r"Solar occultation diffraction orders measured this MTP: "+"\n"
    for chosenOrder in sorted(uniqueOccultationOrders):
        h += "%i, " %chosenOrder
    h += r"<br>"+"\n"
    
    for chosenOrder in sorted(uniqueOccultationOrders):
        h += "<h3>Solar occultations for diffraction order %i</h3>" %chosenOrder
        imagename = "img/occultations_mtp%03d_order%i_altitude.png" %(mtpNumber, chosenOrder)
        h += r"<img src='%s'>" %imagename
    
    h += r"<br>"+"\n"
    h += r"<br>"+"\n"
    h += r"<br>"+"\n"
    h += r"<br>"+"\n"
    h += r"<h2>Dayside Nadirs</h2>"+"\n"
    
    h += r"Dayside nadir diffraction orders measured this MTP: "+"\n"
    for chosenOrder in sorted(uniqueNadirOrders):
        h += "%i, " %chosenOrder
    h += r"<br>"+"\n"
    
    for chosenOrder in sorted(uniqueNadirOrders):
        h += "<h3>Dayside nadirs for diffraction order %i</h3>" %chosenOrder
        imagename = "img/dayside_nadirs_mtp%03d_order%i_incidence_angle.png" %(mtpNumber, chosenOrder)
        h += r"<img src='%s'>" %imagename
    
    
    
    h += r"<br>"+"\n"
    h += r"<br>"+"\n"
#    h += r"<h2>SO/LNO Observation Plan</h2>"+"\n"
    
        
    h += r"<br>"+"\n"
    h += r"<br>"+"\n"
    h += r"<h2>SO/LNO Observation Dictionaries</h2>"+"\n"
    h += r"<h3>Solar Occultation</h3>"+"\n"
    headers = ["Name", "Diffraction Order 1", "Diffraction Order 2", "Diffraction Order 3", "Diffraction Order 4", "Diffraction Order 5", "Diffraction Order 6", "Integration Time", "Rhythm", "Detector Height"]
    h += r"<table border=1>"+"\n"
    h += r"<tr>"+"\n"
    for header in headers:
        h += r"<th>%s</th>" %header
    h += r"</tr>"+"\n"
    for key in sorted(occultationObservationDict.keys()):
        orders, integrationTime, rhythm, detectorRows, channelCode = getObsParameters(key, occultationObservationDict)
    
        h += r"<tr>"+"\n"
        h += r"<td>%s</td>" %(key)
        if "COP" in orders:
            h += r"<td>%s (manual mode)</td>" %(orders)
            for order in range(5):
                h += r"<td>-</td>"+"\n"
        else:    
            for order in orders:
                h += r"<td>%s</td>" %(order)
            for order in range(6-len(orders)):
                h += r"<td>-</td>"+"\n"
                
        h += r"<td>%i</td>" %(integrationTime)
        h += r"<td>%i</td>" %(rhythm)
        h += r"<td>%i</td>" %(detectorRows)
        h += r"</tr>"+"\n"
    h += r"</table>"+"\n"
    
    
    h += r"<h3>Nadir/Limb</h3>"+"\n"
    headers = ["Name", "Diffraction Order 1", "Diffraction Order 2", "Diffraction Order 3", "Diffraction Order 4", "Diffraction Order 5", "Diffraction Order 6", "Integration Time", "Rhythm", "Detector Height"]
    h += r"<table border=1>"+"\n"
    h += r"<tr>"+"\n"
    for header in headers:
        h += r"<th>%s</th>" %header
    h += r"</tr>"
    for key in sorted(nadirObservationDict.keys()):
        orders, integrationTime, rhythm, detectorRows, channelCode = getObsParameters(key, nadirObservationDict)
    
        h += r"<tr>"+"\n"
        h += r"<td>%s</td>" %(key)
        if "COP" in orders:
            h += r"<td>%s (manual mode)</td>" %(orders)
            for order in range(5):
                h += r"<td>-</td>"+"\n"
        else:    
            for order in orders:
                h += r"<td>%s</td>" %(order)
            for order in range(6-len(orders)):
                h += r"<td>-</td>"+"\n"
                
        h += r"<td>%i</td>" %(integrationTime)
        h += r"<td>%i</td>" %(rhythm)
        h += r"<td>%i</td>" %(detectorRows)
        h += r"</tr>"+"\n"
    h += r"</table>"+"\n"
    
    
    
    
    h += r"<br>"+"\n"
    h += r"<br>"+"\n"
    h += r"<p>Page last modified: %s</p>" %(datetime.now().strftime('%a, %d %b %Y %H:%M:%S')) +"\n"
    
    with open(os.path.join(paths["HTML_MTP_PATH"], "nomad_mtp%03d_overview.html" %(mtpNumber)), 'w') as f:
        f.write(h)


#    return uniqueOccultationOrders, uniqueNadirOrders

