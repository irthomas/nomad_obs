# -*- coding: utf-8 -*-
"""
Created on Mon Apr 27 09:55:27 2020

@author: iant

set start times for mtps. Note that program will stop if an observation is allowed at the given start time.
Start time must not be in an occultation and must be on nightside, prior to in ingress.
The first observation must be an Ingress (or merged/grazing if beta angle is high).
End time should be 2 orbits later than real MTP end to avoid discontinuties in planning.
First orbit must match with Bojan/Claudio. Don't generate an MTP plan and then delete/add the first line - change the start time instead!
Define a few extra observations and then delete them from the final observation plan.
CHECK START TIMES IN COSMOGRAPHIA OR SOC EVENT FILE

"""

def getMtpConstants(mtpNumber):

    def convertInputTimeStrings(timeString):
        from datetime import datetime, timedelta
        """convert input time strings to SPICE format and add a delta of a few minutes"""
        time = datetime.strptime(timeString, "%Y-%m-%dT%H:%M:%SZ")
        #start time must be a minute after passing from day to night. Bojan will specify which orbit to start on!
        #end time must be a minute after the end of the event file on the nightside
        delta = timedelta(minutes=1) 
        newTime = time + delta
        utcString = datetime.strftime(newTime, '%Y %b %d %H:%M:%S')   
        return utcString

    if mtpNumber == 0:
        mtpStart = "" #EXMGEO_TD2N start time as specified by Bojan or Claudio
        mtpEnd = "" #EXMGEO_TD2N end time as specified by Bojan or Claudio
        copVersion = "20180313_091700" #desired cop table folder - remember to update if patched
#        ALLOCATED_DATA_VOLUME = #MBits # add if required


        #TODO: find the real start time in the correct datetime format
#        utcstringDaysideNadirStart = "2018MAR24-11:50:00 UTC" #in general, choose a time just after passing from day to night
#        utcstringOccultationStart = utcstringDaysideNadirStart
#        utcstringDaysideNadirEnd = "2018APR21-20:00:00 UTC"
#        utcstringOccultationEnd = utcstringDaysideNadirEnd
#        copVersion = "20180313_091700" #desired cop table folder
#        MAPPS_EVENT_FILE = "ian_mtp000_180307.tgo" #no occultations, using updated LTP post-aerobraking
#        NADIR_ONLY = True
#        SO_CENTRE_DETECTOR_LINE = 128
    
    if mtpNumber == 1:
        mtpStart = "" #EXMGEO_TD2N start time as specified by Bojan or Claudio
        mtpEnd = "" #EXMGEO_TD2N end time as specified by Bojan or Claudio
        copVersion = "20180313_091700" #desired cop table folder - remember to update if patched
#        ALLOCATED_DATA_VOLUME = #MBits # add if required


#        utcstringDaysideNadirStart = "2018APR21-18:40:00 UTC" #in general, choose a time just after passing from day to night
#        utcstringOccultationStart = "2018APR21-17:35:00 UTC"
#        utcstringDaysideNadirEnd = "2018MAY19-16:30:00 UTC"
#        utcstringOccultationEnd = utcstringDaysideNadirEnd
#        copVersion = "20180313_091700" #desired cop table folder
#        MAPPS_EVENT_FILE = "LEVF_M001_SOC_PLANNING.EVF"
#        NADIR_ONLY = False
#        SO_CENTRE_DETECTOR_LINE = 128
    
    elif mtpNumber == 2:
        mtpStart = "" #EXMGEO_TD2N start time as specified by Bojan or Claudio
        mtpEnd = "" #EXMGEO_TD2N end time as specified by Bojan or Claudio
        copVersion = "20180313_091700" #desired cop table folder - remember to update if patched
#        ALLOCATED_DATA_VOLUME = #MBits # add if required


#        utcstringDaysideNadirStart = "2018MAY19-16:20:00 UTC" #in general, choose a time just after passing from day to night
#        utcstringOccultationStart = utcstringDaysideNadirStart
#        utcstringDaysideNadirEnd = "2018JUN16-16:00:00 UTC"
#        utcstringOccultationEnd = utcstringDaysideNadirEnd
#        copVersion = "20180313_091700" #desired cop table folder
#        MAPPS_EVENT_FILE = "LEVF_M002_SOC_PLANNING.EVF"
#        NADIR_ONLY = False
#        SO_CENTRE_DETECTOR_LINE = 130 #boresight misaligned - sun centred on line 130 now

    elif mtpNumber == 3:
        mtpStart = "" #EXMGEO_TD2N start time as specified by Bojan or Claudio
        mtpEnd = "" #EXMGEO_TD2N end time as specified by Bojan or Claudio
        copVersion = "20180616_110400" #desired cop table folder - remember to update if patched
#        ALLOCATED_DATA_VOLUME = #MBits # add if required


#        utcstringDaysideNadirStart = "2018JUN16-14:17:00" #in general, choose a time just after passing from day to night
#        utcstringOccultationStart = utcstringDaysideNadirStart
#        utcstringDaysideNadirEnd = '2018JUN28-17:17:00'
#        utcstringOccultationEnd = utcstringDaysideNadirEnd
#        copVersion = "20180616_110400" #desired cop table folder
#        MAPPS_EVENT_FILE = "LEVF_M003_SOC_PLANNING.EVF"
#        NADIR_ONLY = False
#        SO_CENTRE_DETECTOR_LINE = 131 #boresight misaligned - sun centred on line 131 now
    
    elif mtpNumber == 4:
        mtpStart = "" #EXMGEO_TD2N start time as specified by Bojan or Claudio
        mtpEnd = "" #EXMGEO_TD2N end time as specified by Bojan or Claudio
        copVersion = "20180714_120000" #desired cop table folder - remember to update if patched
#        ALLOCATED_DATA_VOLUME = #MBits # add if required


#        utcstringDaysideNadirStart = "2018JUL14-15:03:00" #in general, choose a time just after passing from day to night
#        utcstringOccultationStart = utcstringDaysideNadirStart
#        utcstringDaysideNadirEnd = "2018AUG11-13:00:00 UTC"
#        utcstringOccultationEnd = utcstringDaysideNadirEnd
#        copVersion = "20180714_120000" #desired cop table folder
#        MAPPS_EVENT_FILE = "LEVF_M004_SOC_PLANNING.EVF" #no modifications for this MTP
#        NADIR_ONLY = False
#        SO_CENTRE_DETECTOR_LINE = 131 #boresight misaligned - sun centred on line 131 now
    
    elif mtpNumber == 5:
        mtpStart = "" #EXMGEO_TD2N start time as specified by Bojan or Claudio
        mtpEnd = "" #EXMGEO_TD2N end time as specified by Bojan or Claudio
        copVersion = "20180714_120000" #desired cop table folder - remember to update if patched
#        ALLOCATED_DATA_VOLUME = #MBits # add if required


#        utcstringDaysideNadirStart = "2018AUG11-14:55:00" #in general, choose a time just after passing from day to night
#        utcstringOccultationStart = utcstringDaysideNadirStart
#        utcstringDaysideNadirEnd = "2018SEP08-13:15:00 UTC"
#        utcstringOccultationEnd = utcstringDaysideNadirEnd
#        copVersion = "20180714_120000" #desired cop table folder
#        MAPPS_EVENT_FILE = "LEVF_M005_SOC_PLANNING.EVF"
#        NADIR_ONLY = False
#        SO_CENTRE_DETECTOR_LINE = 128 #boresight corrected from MTP005 onwards
    
    elif mtpNumber == 6:
        mtpStart = "" #EXMGEO_TD2N start time as specified by Bojan or Claudio
        mtpEnd = "" #EXMGEO_TD2N end time as specified by Bojan or Claudio
        copVersion = "20180714_120000" #desired cop table folder - remember to update if patched
#        ALLOCATED_DATA_VOLUME = #MBits # add if required


#        utcstringDaysideNadirStart = "2018SEP08-15:15:00 UTC" #in general, choose a time just after passing from day to night. Bojan will specify which orbit to start on!
#        utcstringOccultationStart = utcstringDaysideNadirStart
#        utcstringDaysideNadirEnd = "2018OCT06-13:15:00 UTC" #in general, choose a time just after the end of the event file on the nightside
#        utcstringOccultationEnd = utcstringDaysideNadirEnd
#        copVersion = "20180714_120000" #desired cop table folder
#        MAPPS_EVENT_FILE = "LEVF_M006_SOC_PLANNING.EVF"
#        NADIR_ONLY = False
#        SO_CENTRE_DETECTOR_LINE = 128 #boresight corrected from MTP005 onwards
    
    elif mtpNumber == 7:
        mtpStart = "" #EXMGEO_TD2N start time as specified by Bojan or Claudio
        mtpEnd = "" #EXMGEO_TD2N end time as specified by Bojan or Claudio
        copVersion = "20181006_120000" #desired cop table folder - remember to update if patched
#        ALLOCATED_DATA_VOLUME = #MBits # add if required


#        utcstringDaysideNadirStart = "2018OCT06-15:05:00 UTC" #in general, choose a time a few minutes after passing from day to night. Bojan will specify which orbit to start on!
#        utcstringOccultationStart = utcstringDaysideNadirStart
#        utcstringDaysideNadirEnd = "2018NOV03-12:15:00 UTC" #in general, choose a time just after the end of the event file on the nightside
#        utcstringOccultationEnd = utcstringDaysideNadirEnd
#        copVersion = "20181006_120000" #desired cop table folder
#        MAPPS_EVENT_FILE = "LEVF_M007_SOC_PLANNING.EVF"
#        NADIR_ONLY = False
#        SO_CENTRE_DETECTOR_LINE = 128 #boresight corrected from MTP005 onwards
    
    
        """begin new obs planning software"""
    elif mtpNumber == 8: #2018-11-03T13:00:13Z (actually started orbit after:2018-11-03T14:58:06Z)     EXMGEO_TN2D - 2018-12-01T12:02:30Z     EXMGEO_TD2N
        mtpStart = "2018-11-03T14:58:06Z" #EXMGEO_TD2N start time as specified by Bojan or Claudio
        mtpEnd = "2018-12-01T12:02:30Z" #EXMGEO_TD2N end time as specified by Bojan or Claudio
        copVersion = "20181006_120000" #desired cop table folder - remember to update if patched
#        ALLOCATED_DATA_VOLUME = #MBits # add if required
    
    elif mtpNumber == 9: #2018-12-01T14:00:32Z EXMGEO_TD2N - 2018-12-29T12:14:53Z EXMGEO_TD2N 
        mtpStart = "2018-12-01T14:00:32Z" #EXMGEO_TD2N start time as specified by Bojan or Claudio
        mtpEnd = "2018-12-29T12:14:53Z" #EXMGEO_TD2N end time as specified by Bojan or Claudio
        copVersion = "20181006_120000" #desired cop table folder - remember to update if patched
#        ALLOCATED_DATA_VOLUME = #MBits # add if required
    
    elif mtpNumber == 10:
        mtpStart = "2018-12-29T14:12:47Z" #EXMGEO_TD2N start time as specified by Bojan or Claudio
        mtpEnd = "2019-01-26T12:49:26Z" #EXMGEO_TD2N end time as specified by Bojan or Claudio
        copVersion = "20181229_113000" #desired cop table folder - remember to update if patched
#        ALLOCATED_DATA_VOLUME = #MBits # add if required

    elif mtpNumber == 11:
        mtpStart = "2019-01-26T14:47:51Z" #EXMGEO_TD2N start time as specified by Bojan or Claudio
        mtpEnd = "2019-02-23T12:49:34Z" #EXMGEO_TD2N end time as specified by Bojan or Claudio
        copVersion = "20181229_113000" #desired cop table folder - remember to update if patched
#        ALLOCATED_DATA_VOLUME = #MBits # add if required
    
    elif mtpNumber == 12: # > EXMGEO_TD2N -  > EXMGEO_TD2N
        mtpStart = "2019-02-23T14:47:29Z" #EXMGEO_TD2N start time as specified by Bojan or Claudio
        mtpEnd = "2019-03-23T13:13:40Z" #EXMGEO_TD2N end time as specified by Bojan or Claudio
        copVersion = "20181229_113000" #desired cop table folder - remember to update if patched
#        ALLOCATED_DATA_VOLUME = #MBits # add if required
    
    elif mtpNumber == 13:
        mtpStart = "2019-03-23T15:11:46Z" #EXMGEO_TD2N start time as specified by Bojan or Claudio
        mtpEnd = "2019-04-20T13:16:29Z" #EXMGEO_TD2N end time as specified by Bojan or Claudio
        copVersion = "20190323_120000" #desired cop table folder - remember to update if patched
#        ALLOCATED_DATA_VOLUME = #MBits # add if required
    
    elif mtpNumber == 14:
        mtpStart = "2019-04-20T15:14:22Z" #EXMGEO_TD2N start time as specified by Bojan or Claudio
        mtpEnd = "2019-05-18T13:39:12Z" #EXMGEO_TD2N end time as specified by Bojan or Claudio
        copVersion = "20190323_120000" #desired cop table folder - remember to update if patched
#        ALLOCATED_DATA_VOLUME = #MBits # add if required

    elif mtpNumber == 15:
        mtpStart = "2019-05-18T15:37:10Z" #EXMGEO_TD2N start time as specified by Bojan or Claudio
        mtpEnd = "2019-06-15T11:37:56Z" #EXMGEO_TD2N end time as specified by Bojan or Claudio
        copVersion = "20190323_120000" #desired cop table folder - remember to update if patched
#        ALLOCATED_DATA_VOLUME = #MBits # add if required

    elif mtpNumber == 16:
        mtpStart = "2019-06-15T15:33:38Z" #EXMGEO_TD2N start time as specified by Bojan or Claudio
        mtpEnd = "2019-07-13T12:48:23Z" #EXMGEO_TD2N end time as specified by Bojan or Claudio
        copVersion = "20190323_120000" #desired cop table folder - remember to update if patched
#        ALLOCATED_DATA_VOLUME = #MBits # add if required

    elif mtpNumber == 17:
        mtpStart = "2019-07-13T14:46:20Z" #EXMGEO_TD2N start time as specified by Bojan or Claudio
        mtpEnd = "2019-08-10T12:57:59Z" #EXMGEO_TD2N end time as specified by Bojan or Claudio
        copVersion = "20190323_120000" #desired cop table folder - remember to update if patched
#        ALLOCATED_DATA_VOLUME = #MBits # add if required

    elif mtpNumber == 18:
        mtpStart = "2019-08-10T14:55:55Z" #EXMGEO_TD2N start time as specified by Bojan or Claudio
        mtpEnd = "2019-08-22T12:00:55Z" #EXMGEO_TD2N end time as specified by Bojan or Claudio
        copVersion = "20190323_120000" #desired cop table folder - remember to update if patched
#        ALLOCATED_DATA_VOLUME = #MBits # add if required

    elif mtpNumber == 19:
        mtpStart = "2019-09-14T16:36:17Z" #EXMGEO_TD2N start time as specified by Bojan or Claudio
        mtpEnd = "2019-10-05T13:48:59Z" #EXMGEO_TD2N end time as specified by Bojan or Claudio
        copVersion = "20190323_120000" #desired cop table folder - remember to update if patched
#        ALLOCATED_DATA_VOLUME = #MBits # add if required

    elif mtpNumber == 20:
        mtpStart = "2019-10-05T15:46:51Z" #EXMGEO_TD2N start time as specified by Bojan or Claudio
        mtpEnd = "2019-11-02T13:09:33Z" #EXMGEO_TD2N end time as specified by Bojan or Claudio
        copVersion = "20190323_120000" #desired cop table folder - remember to update if patched
#        ALLOCATED_DATA_VOLUME = #MBits # add if required

    elif mtpNumber == 21:
        mtpStart = "2019-11-02T15:07:25Z" #EXMGEO_TD2N start time as specified by Bojan or Claudio
        mtpEnd = "2019-11-30T13:15:03Z" #EXMGEO_TD2N end time as specified by Bojan or Claudio
        copVersion = "20191102_120000" #desired cop table folder - remember to update if patched
#        ALLOCATED_DATA_VOLUME = #MBits # add if required

    elif mtpNumber == 22:
        mtpStart = "2019-11-30T15:12:58Z" #EXMGEO_TD2N start time as specified by Bojan or Claudio
        mtpEnd = "2019-12-28T13:50:48Z" #EXMGEO_TD2N end time as specified by Bojan or Claudio
        copVersion = "20191102_120000" #desired cop table folder - remember to update if patched
#        ALLOCATED_DATA_VOLUME = #MBits # add if required

    elif mtpNumber == 23:
        mtpStart = "2019-12-28T15:48:47Z" #EXMGEO_TD2N start time as specified by Bojan or Claudio
        mtpEnd = "2020-01-25T12:11:37Z" #EXMGEO_TD2N end time as specified by Bojan or Claudio
        copVersion = "20191102_120000" #desired cop table folder - remember to update if patched
#        ALLOCATED_DATA_VOLUME = #MBits # add if required

    elif mtpNumber == 24:
        mtpStart = "2020-01-25T14:09:32Z" #EXMGEO_TD2N start time as specified by Bojan or Claudio
        mtpEnd = "2020-02-22T13:15:02Z" #EXMGEO_TD2N end time as specified by Bojan or Claudio
        copVersion = "20191102_120000" #desired cop table folder - remember to update if patched
#        ALLOCATED_DATA_VOLUME = #MBits # add if required

    elif mtpNumber == 25:
        mtpStart = "2020-02-22T15:12:59Z" #EXMGEO_TD2N start time as specified by Bojan or Claudio
        mtpEnd = "2020-03-21T13:26:01Z" #EXMGEO_TD2N end time as specified by Bojan or Claudio
        copVersion = "20200222_120000" #desired cop table folder - remember to update if patched
#        ALLOCATED_DATA_VOLUME = #MBits # add if required

    elif mtpNumber == 26:
        mtpStart = "2020-03-21T15:23:55Z" #EXMGEO_TD2N start time as specified by Bojan or Claudio
        mtpEnd = "2020-04-18T12:19:28Z" #EXMGEO_TD2N end time as specified by Bojan or Claudio
        copVersion = "20200222_120000" #desired cop table folder - remember to update if patched
#        ALLOCATED_DATA_VOLUME = #MBits # add if required

    elif mtpNumber == 27:
        mtpStart = "2020-04-18T14:17:29Z" #EXMGEO_TD2N start time as specified by Bojan or Claudio
        mtpEnd = "2020-05-16T12:37:22Z" #EXMGEO_TD2N end time as specified by Bojan or Claudio
        copVersion = "20200222_120000" #desired cop table folder - remember to update if patched
#        ALLOCATED_DATA_VOLUME = #MBits # add if required

    elif mtpNumber == 28:
        mtpStart = "2020-05-16T14:35:18Z" #EXMGEO_TD2N start time as specified by Bojan or Claudio
        mtpEnd = "2020-06-13T13:19:57Z" #EXMGEO_TD2N end time as specified by Bojan or Claudio
        copVersion = "20200222_120000" #desired cop table folder - remember to update if patched
#        ALLOCATED_DATA_VOLUME = #MBits # add if required

    elif mtpNumber == 29:
        mtpStart = "2020-06-13T15:17:54Z" #EXMGEO_TD2N start time as specified by Bojan or Claudio
        mtpEnd = "2020-07-11T13:34:20Z" #EXMGEO_TD2N end time as specified by Bojan or Claudio
        copVersion = "20200222_120000" #desired cop table folder - remember to update if patched
#        ALLOCATED_DATA_VOLUME = #MBits # add if required

    elif mtpNumber == 30:
        mtpStart = "2020-07-11T15:32:12Z" #EXMGEO_TD2N start time as specified by Bojan or Claudio
        mtpEnd = "2020-08-08T12:50:58Z" #EXMGEO_TD2N end time as specified by Bojan or Claudio
        copVersion = "20200222_120000" #desired cop table folder - remember to update if patched
#        ALLOCATED_DATA_VOLUME = #MBits # add if required

    elif mtpNumber == 31:
        mtpStart = "2020-08-08T14:48:51Z" #EXMGEO_TD2N start time as specified by Bojan or Claudio
        mtpEnd = "2020-09-05T13:02:23Z" #EXMGEO_TD2N end time as specified by Bojan or Claudio
#        copVersion = "20200808_120000" #desired cop table folder - remember to update if patched
        copVersion = "mtp031_proposed" #desired cop table folder - remember to update if patched
#        ALLOCATED_DATA_VOLUME = #MBits # add if required

    elif mtpNumber == 32:
        mtpStart = "" #EXMGEO_TD2N start time as specified by Bojan or Claudio
        mtpEnd = "" #EXMGEO_TD2N end time as specified by Bojan or Claudio
        copVersion = "" #desired cop table folder - remember to update if patched
#        ALLOCATED_DATA_VOLUME = #MBits # add if required

    elif mtpNumber == 33:
        mtpStart = "" #EXMGEO_TD2N start time as specified by Bojan or Claudio
        mtpEnd = "" #EXMGEO_TD2N end time as specified by Bojan or Claudio
        copVersion = "" #desired cop table folder - remember to update if patched
#        ALLOCATED_DATA_VOLUME = #MBits # add if required

    elif mtpNumber == 34:
        mtpStart = "" #EXMGEO_TD2N start time as specified by Bojan or Claudio
        mtpEnd = "" #EXMGEO_TD2N end time as specified by Bojan or Claudio
        copVersion = "" #desired cop table folder - remember to update if patched
#        ALLOCATED_DATA_VOLUME = #MBits # add if required

    elif mtpNumber == 35:
        mtpStart = "" #EXMGEO_TD2N start time as specified by Bojan or Claudio
        mtpEnd = "" #EXMGEO_TD2N end time as specified by Bojan or Claudio
        copVersion = "" #desired cop table folder - remember to update if patched
#        ALLOCATED_DATA_VOLUME = #MBits # add if required





    #add corrections for certain changes in planning since beginning of mission
    mappsEventFilename = "LEVF_M%03d_SOC_PLANNING.EVF" %mtpNumber
    if mtpNumber < 13:
        acsStartAltitude = 250 #km
    else:
        acsStartAltitude = 200 #km

    if mtpNumber == 2:
        soCentreDetectorLine = 130 #boresight corrected by moving detector readout region
    elif mtpNumber in [3, 4]:
        soCentreDetectorLine = 131 #detector readout region improved
    else:
        soCentreDetectorLine = 128 #boresight corrected from MTP005 onwards

    #convert input times if given, if not leave blank and throw error in main script asking for inputs
    if mtpStart != "":
        utcstringStart = convertInputTimeStrings(mtpStart)
    else:
        utcstringStart = ""
        
    if mtpEnd != "":
        utcstringEnd = convertInputTimeStrings(mtpEnd)
    else:
        utcstringEnd = ""
    
    mtpConstantsDict = {"mtpNumber":mtpNumber, \
                        "utcStringStart":utcstringStart, \
                        "utcStringEnd":utcstringEnd, \
                        "copVersion":copVersion, \
                        "mappsEventFilename":mappsEventFilename, \
                        "soCentreDetectorLine":soCentreDetectorLine, \
                        "acsStartAltitude":acsStartAltitude}
    
    return mtpConstantsDict
            


