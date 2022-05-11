# -*- coding: utf-8 -*-
"""
Created on Mon Apr 27 12:19:31 2020

@author: iant
"""

import numpy as np
import os
import matplotlib.pyplot as plt
import spiceypy as sp



from nomad_obs.config.constants import FIG_X, FIG_Y


def plotRegionsOfInterest(paths, occultationRegionsOfInterest, nadirRegionsOfInterest):
    """Plot all regions of interest and observation types on empty map"""

    def plotRectangle(axis, lon_corner0, lon_corner1, lat_corner0, lat_corner1, colour):
        
        corners = np.asfarray([[lon_corner0, lat_corner0], \
                   [lon_corner0, lat_corner1], \
                   [lon_corner1, lat_corner1], \
                   [lon_corner1, lat_corner0], \
                   [lon_corner0, lat_corner0]])
        axis.plot(corners[:, 0], corners[:, 1], color=colour)
    
    
    fig = plt.figure(figsize=(FIG_X+4, FIG_Y+4))
    ax = fig.add_subplot(111, projection="mollweide")
    ax.grid(True)
    plt.title("Nadir (red) and occultation (blue) regions of interest")
    
    horizontal_offset = 0.05
    for regionOfInterest in occultationRegionsOfInterest:
        
        plotRectangle(ax, regionOfInterest[6]/sp.dpr(), regionOfInterest[7]/sp.dpr(), regionOfInterest[4]/sp.dpr(), regionOfInterest[5]/sp.dpr(), "b")
        ax.annotate(regionOfInterest[0], [np.mean((regionOfInterest[6], regionOfInterest[7]))/sp.dpr()+horizontal_offset, np.mean((regionOfInterest[4], regionOfInterest[4], regionOfInterest[5]))/sp.dpr()], color="b")
    
    for regionOfInterest in nadirRegionsOfInterest:
        verticalOffset = 0.05
        plotRectangle(ax, regionOfInterest[6]/sp.dpr(), regionOfInterest[7]/sp.dpr(), regionOfInterest[4]/sp.dpr(), regionOfInterest[5]/sp.dpr(), "r")
        ax.annotate(regionOfInterest[0], [np.mean((regionOfInterest[6], regionOfInterest[7]))/sp.dpr()+horizontal_offset, np.mean((regionOfInterest[4], regionOfInterest[4], regionOfInterest[5]))/sp.dpr()+verticalOffset], color="r")
    
    plt.savefig(os.path.join(paths["OBS_DIRECTORY"], "regions_of_interest.png"))
    plt.close()
    
