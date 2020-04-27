# -*- coding: utf-8 -*-
"""
Created on Mon Apr 27 12:16:58 2020

@author: iant
"""
import sys
from datetime import datetime, timedelta
import spiceypy as sp


from nomad_obs.config.constants import SPICE_DATETIME_FORMAT, SPICE_ABCORR



def stop():
    print("**********Fatal Error********")
#    halt
    sys.exit() #breaks program
    return 0


def printStatement(string_in):
    """write statement with current utc time"""
    print("%s (%s)" %(string_in, datetime.strftime(datetime.now(), SPICE_DATETIME_FORMAT)))



def findIndex(valueIn,listIn):
    if valueIn in listIn:
        indexOut = [index for index,value in enumerate(listIn) if value == valueIn]
        if len(indexOut) > 1:
            print("Error: Multiple values found")
        else:
            return indexOut[0]
    else:
        print("Error: Not found")
    






def getMtpTimes(mtpNumber):
    """find mtp start/end times and ls for an mtp"""
    
    def lsubs(et):
        return sp.lspcn("MARS",et,SPICE_ABCORR) * sp.dpr()

    mtp0Start = datetime(2018, 3, 24)
    mtpTimeDelta = timedelta(days=28)
    
    mtpStart = mtp0Start + mtpTimeDelta * mtpNumber
    mtpEnd = mtpStart + mtpTimeDelta
    
    mtpStartString = datetime.strftime(mtpStart, SPICE_DATETIME_FORMAT[:8])
    mtpEndString = datetime.strftime(mtpEnd, SPICE_DATETIME_FORMAT[:8])
    
    mtpStartEt = sp.utc2et(mtpStartString)
    mtpEndEt = sp.utc2et(mtpEndString)
    
    mtpStartLs = lsubs(mtpStartEt)
    mtpEndLs = lsubs(mtpEndEt)
    
    return mtpStartString, mtpEndString, mtpStartLs, mtpEndLs


"""code to print MTP start/end times as a table"""
#print("MTP Number,Start Date,End Date,Start Ls,End Ls")
#for mtpNumber in range(41):
#    mtpStartString, mtpEndString, mtpStartLs, mtpEndLs = getMtpTimes(mtpNumber)
#    print("MTP%03i,%s,%s,%0.1f,%0.1f" %(mtpNumber, mtpStartString, mtpEndString, mtpStartLs, mtpEndLs))



