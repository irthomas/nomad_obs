# -*- coding: utf-8 -*-
# pylint: disable=E1103
# pylint: disable=C0301
"""
Created on Wed Oct 18 13:56:09 2017

@author: ithom

PATCHES:
    ADD LOTS MORE LINES WITH SBSF OFF
    E.G. CH4 133, 134, 135, 136, 137, 167
    E.G. CH4 133, 134, 135, 136, 137, 168
    E.G. CH4 133, 134, 135, 136, 137, 169
    
    ADD CO NON-SATURATED TO NOMINAL MEASUREMENT
    E.G. 121, 149, 165, 186, 188, 190
    E.G. 121, 134, 149, 165, 168, 186
    
    ADD LNO OCCULTATION USING SAME ORDER
    ADD LNO FIXED LINE FOR OCC 16 ROWS
    
    
    

"""


__project__   = "NOMAD Observation Planning"
__author__    = "Ian Thomas"
__contact__   = "ian.thomas@aeronomie.be"



#ACS joint observation names. Don't modify unless instructed to do so by SOC/ACS.
SOC_JOINT_OBSERVATION_NAMES = {
        "Nominal Science 1xCO2 LA01":"NOM_01",
        "Dust H2O 01":"DUST01",
        "Water Ice 01":"ICE_01",
        "AER 01":"AER_01"
        }
SOC_JOINT_OBSERVATION_TYPES = [
        "OCCEG",
        "OCCIN",
        "OCCME",
        "OCCGR"
        ]
        


"""make the observation dictionaries of all the desired measurement types
DON'T MODIFY OR DELETE ANY OBSERVATIONS - JUST ADD NEW ONES"""
#name:[[orders], int time, rhythm, lines, so=0/lno=1]
occultationObservationDict = {
"BgSubTest 03":[[121,134,149,165,168,190], 4, 1, 16, 0],
"BgSubTest 04":[[119,136,148,166,168,189], 4, 1, 16, 0],

"Dust H2O 01":[[119,130,145,171,191,0], 4, 1, 16, 0],
"Water Ice 01":[[119,140,153,170,191,0], 4, 1, 16, 0],
"CO 01":[[167,188,189,190,191,0], 4, 1, 16, 0],
"HDO 01":[[168,134,124,129,190,0], 4, 1, 16, 0],
"AER 01":[[119,133,143,154,169,0], 4, 1, 16, 0],
"CH4 01":[[168,133,134,135,136,0], 4, 1, 16, 0],

"Nominal Science 1xCO2 LA01":[[168,134,190,121,149,0], 4, 1, 16, 0], #no CO2 50-120km
"Nominal Science 1xCO2 HA01":[[168,134,190,121,165,0], 4, 1, 16, 0],
"Nominal Science 1xCO2 LA02":[[168,134,190,119,149,0], 4, 1, 16, 0], #no CO2 50-120km
"Nominal Science 1xCO2 HA02":[[168,134,190,119,165,0], 4, 1, 16, 0],

"Nominal Science 1xCO2 LA03":[[168,134,189,121,149,0], 4, 1, 16, 0], #no CO2 50-120km
"Nominal Science 1xCO2 HA03":[[168,134,189,121,165,0], 4, 1, 16, 0],
"Nominal Science 1xCO2 LA04":[[168,136,189,119,149,0], 4, 1, 16, 0], #no CO2 50-120km
"Nominal Science 1xCO2 HA04":[[168,136,189,119,165,0], 4, 1, 16, 0],


"Nominal Science with CO 01":[[169,134,186,121,147,0], 4, 1, 16, 0], #186 for CO

"All Fullscan Fast":[["COP#293"], 0, 1, 16, 0],
"All Fullscan Slow":[["COP#107"], 0, 1, 24, 0],

"CO2 Fullscan Fast":[["COP#239"], 0, 1, 16, 0],
"CO Fullscan Fast":[["COP#254"], 0, 1, 16, 0],
                      
"ACS Ridealong Science 6SUBD 01":[[121,134,149,165,168,190], 10, 4, 20, 0],
"ACS Ridealong Science 6SUBD 02":[[121,134,149,165,168,190], 20, 4, 20, 0],
"ACS Ridealong Science 2SUBD 01":[[164,165], 40, 4, 24, 0],

"LNO Occultation Nominal Science 1xCO2 01":[["COP#697"], 2, 1, 20, 1],
"LNO Occultation Fullscan 01":[["COP#93"], 2, 1, 20, 1],
"LNO Occultation Fullscan 02":[["COP#93"], 2, 1, 16, 1], #MTP013+

"119 with 1xDark":[["COP#1460"], 4, 1, 16, 0],
"120 with 1xDark":[["COP#1461"], 4, 1, 16, 0],
"121 with 1xDark":[["COP#1462"], 4, 1, 16, 0],
"122 with 1xDark":[["COP#1463"], 4, 1, 16, 0],
"123 with 1xDark":[["COP#1464"], 4, 1, 16, 0],

"132 with 1xDark":[["COP#1465"], 4, 1, 16, 0],
"133 with 1xDark":[["COP#1466"], 4, 1, 16, 0],
"134 with 1xDark":[["COP#1467"], 4, 1, 16, 0],
"135 with 1xDark":[["COP#1468"], 4, 1, 16, 0],
"136 with 1xDark":[["COP#1469"], 4, 1, 16, 0],
"190 with 1xDark":[["COP#1487"], 4, 1, 16, 0],



                    
"134 with 5xDark":[["COP#4088"], 4, 1, 16, 0], #MTP010+
"136 with 5xDark":[["COP#4090"], 4, 1, 16, 0], #MTP010+
"Nominal Science 1xCO2 TOA":[[168,135,190,121,164,0], 4, 1, 16, 0], #MTP010+

                    
                    
#old
"BgSubTest 01":[[121,134,149,165,167,190], 4, 1, 16, 0],
"BgSubTest 02":[[168,136,189,119,166,148], 4, 1, 16, 0],
"CO2 01":[[167,146,147,148,154,0], 4, 1, 16, 0],
"CO2 02":[[167,155,159,164,148,0], 4, 1, 16, 0],
"Dust H2O 02":[[121,130,145,169,195,0], 4, 1, 16, 0],
"AER 02":[[120,133,143,154,181,0], 4, 1, 16, 0],
"CO2 Fullscan":[["COP#239"], 0, 1, 16, 0],

"ACS Ridealong Science":[["COP#1550"], 0, 1, 16, 0],
"ACS Ridealong Science All Fullscan Fast":[["COP#294"], 0, 1, 16, 0],
                                            
}



#name:[[orders], int time, rhythm, lines, channel (not used)]
nadirObservationDict = {
"Nominal 6SUBD 01":[[149,134,168,119,190,196], 220, 15, 144, 1],
"H2O 2SUBD 01":[[167,169], 200, 15, 144, 1],
"HDO CO 3SUBD 01":[[167,121,190], 205, 15, 144, 1],
"AER H2Oi 3SUBD 01":[[169,131,127], 205, 15, 144, 1],
"CH4 2SUBD 02":[[134,136], 200, 15, 144, 1], #USE FOR CURIOSITY
"CH4 3SUBD 01":[[168,134,136], 205, 15, 144, 1],
"CO 2SUBD 02":[[167,189], 200, 15, 144, 1],
"HDO Fullscan":[["COP#140"], 0, 15, 144, 1],

"HDO H2O 2SUBD 02":[[168,124], 200, 15, 144, 1], #USE FOR SOFIA/EXES JOINT TARGETS
                 
"Surface 3SUBD 01":[[168, 190, 191], 205, 15, 144, 1], #OLD TARGET FOR FA NADIR TARGETS
                 
"Limb 2SUBD 01":[[161,162], 200, 15, 144, 1],
"Limb 2SUBD 02":[[162,163], 200, 15, 144, 1],
"Limb 2SUBD 03":[[163,164], 200, 15, 144, 1],
"Limb 2SUBD 04":[[164,165], 200, 15, 144, 1],
"Limb 2SUBD 05":[[165,166], 200, 15, 144, 1],
"Limb 2SUBD 06":[[166,167], 200, 15, 144, 1],

"CO2 Fullscan":[["COP#144"], 0, 15, 144, 1],
"CO Fullscan":[["COP#124"], 0, 15, 144, 1],
"H2O Fullscan":[["COP#116"], 0, 15, 144, 1],
"CH4 Fullscan":[["COP#104"], 0, 15, 144, 1],

"Nominal Nightside 02":[[162,163], 200, 15, 144, 1],
"Nominal Limb 01":[[164,169], 200, 15, 144, 1],

#surface ice variable rhythms  #MTP010+ when lst is low
"Surface Ice 4SUBD 8S 01":[[199, 194, 193, 187], 220, 8, 144, 1],
"Surface Ice 6SUBD 8S 01":[[199, 198, 194, 193, 187, 186], 205, 8, 144, 1],
"Surface Ice 4SUBD 8S 02":[[199, 189, 188, 187], 220, 8, 144, 1],
"Surface Ice 3SUBD 8S 01":[[199, 194, 188], 180, 8, 144, 1],

"Surface Ice 4SUBD 01":[[199, 194, 193, 187], 195, 15, 144, 1],
#"Surface Ice 6SUBD 01":[[199, 198, 194, 193, 187, 186], 220, 15, 144, 1], #ERROR IN COP TABLES
"Surface Ice 4SUBD 02":[[199, 189, 188, 187], 195, 15, 144, 1],
"Surface Ice 3SUBD 01":[[199, 194, 188], 205, 15, 144, 1],
    
"Surface Ice 2SUBD 4S 01":[[199, 193], 205, 4, 144, 1],
"Surface Ice 2SUBD 4S 02":[[198, 194], 205, 4, 144, 1],
"Surface Ice 2SUBD 4S 03":[[193, 194], 205, 4, 144, 1],
"Surface Ice 2SUBD 4S 04":[[199, 187], 205, 4, 144, 1],

"LNO Ice Index 2SUBD 01":[[153, 158], 200, 15, 144, 1], #MTP013+ FS


"Surface 3SUBD 02":[[191,194,196], 205, 15, 144, 1], #USE FOR FA NADIR TARGETS MTP010+





#old
"Nominal 6SUBD 02":[[167,134,168,121,189,197], 220, 15, 144, 1],
"Nominal 4SUBD 01":[[168,134,121,190], 195, 15, 144, 1],
"Nominal 3SUBD 01":[[167,169,190], 205, 15, 144, 1],

"CH4 2SUBD 01":[[167,134], 200, 15, 144, 1],
"D/H 2SUBD 01":[[121,169], 200, 15, 144, 1],
"D/H 3SUBD 01":[[167,121,169], 205, 15, 144, 1],
"HDO 3SUBD 01":[[121,171,124], 205, 15, 144, 1],
"AER H2Oi CO2i 4SUBD 01":[[164,169,131,127], 195, 15, 144, 1],
"HDO H2O 2SUBD 01":[[121,169], 200, 15, 144, 1],

"Nominal Nightside 01":[[169,190], 200, 15, 144, 1],


}

    

    
####################################MTP CONSTANTS#####################################################################
"""set start times for mtps. Note that program will stop if an observation is allowed at the given start time.
Start time must not be in an occultation and must be on nightside, prior to in ingress.
The first observation must be an Ingress (or merged/grazing if beta angle is high).
End time should be 2 orbits later than real MTP end to avoid discontinuties in planning.
First orbit must match with Bojan/Claudio. Don't generate an MTP plan and then delete/add the first line - change the start time instead!
Define a few extra observations and then delete them from the final observation plan.
CHECK START TIMES IN COSMOGRAPHIA OR SOC EVENT FILE"""
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


        #TODO: convert these to correct format
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
        mtpStart = "" #EXMGEO_TD2N start time as specified by Bojan or Claudio
        mtpEnd = "" #EXMGEO_TD2N end time as specified by Bojan or Claudio
        copVersion = "" #desired cop table folder - remember to update if patched
#        ALLOCATED_DATA_VOLUME = #MBits # add if required

    elif mtpNumber == 18:
        mtpStart = "" #EXMGEO_TD2N start time as specified by Bojan or Claudio
        mtpEnd = "" #EXMGEO_TD2N end time as specified by Bojan or Claudio
        copVersion = "" #desired cop table folder - remember to update if patched
#        ALLOCATED_DATA_VOLUME = #MBits # add if required

    elif mtpNumber == 19:
        mtpStart = "" #EXMGEO_TD2N start time as specified by Bojan or Claudio
        mtpEnd = "" #EXMGEO_TD2N end time as specified by Bojan or Claudio
        copVersion = "" #desired cop table folder - remember to update if patched
#        ALLOCATED_DATA_VOLUME = #MBits # add if required

    elif mtpNumber == 20:
        mtpStart = "" #EXMGEO_TD2N start time as specified by Bojan or Claudio
        mtpEnd = "" #EXMGEO_TD2N end time as specified by Bojan or Claudio
        copVersion = "" #desired cop table folder - remember to update if patched
#        ALLOCATED_DATA_VOLUME = #MBits # add if required



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
            















    
    
"""select +- search range for the regions of interest listed below"""
LATITUDE_RANGE = 2 #degrees
LONGITUDE_RANGE = 2 #degress

#name, min lat, max lat, min lon, max lon
occultationRegionsOfInterest = \
[
["ACIDALIA MUD VOLCANOES NE", 11, 44.68-LATITUDE_RANGE,44.68+LATITUDE_RANGE,-20.80-LONGITUDE_RANGE,-20.80+LONGITUDE_RANGE],
["ACIDALIA MUD VOLCANOES BASIN", 10, 40.93-LATITUDE_RANGE,40.93+LATITUDE_RANGE,-25.61-LONGITUDE_RANGE,-25.61+LONGITUDE_RANGE],
["NILI FOSSAE FORSTERITE", 9, 21.72-LATITUDE_RANGE,21.72+LATITUDE_RANGE,78.51-LONGITUDE_RANGE,78.51+LONGITUDE_RANGE],
["NILI FOSSAE FAULT", 8, 23.93-LATITUDE_RANGE,23.93+LATITUDE_RANGE,78.79-LONGITUDE_RANGE,78.79+LONGITUDE_RANGE],
["AEOLIS MENSAE MFF", 7, -2.8-LATITUDE_RANGE,-2.8+LATITUDE_RANGE,145.7-LONGITUDE_RANGE,145.7+LONGITUDE_RANGE],
["CERBERUS FOSSAE", 6, 10.14-LATITUDE_RANGE,10.14+LATITUDE_RANGE,157.40-LONGITUDE_RANGE,157.40+LONGITUDE_RANGE],
["UTOPIA", 5, 32.97-LATITUDE_RANGE,32.97+LATITUDE_RANGE,88.18-LONGITUDE_RANGE,88.18+LONGITUDE_RANGE],
["ARGYRE", 4, -39.54-LATITUDE_RANGE,-39.54+LATITUDE_RANGE,-38.25-LONGITUDE_RANGE,-38.25+LONGITUDE_RANGE],
["VERNAL CRATER", 3, 5.64-LATITUDE_RANGE,5.64+LATITUDE_RANGE,-4.40-LONGITUDE_RANGE,-4.40+LONGITUDE_RANGE],
["CURIOSITY", 1, -4.5895-LATITUDE_RANGE,-4.5895+LATITUDE_RANGE,137.4417-LONGITUDE_RANGE,137.4417+LONGITUDE_RANGE],
["INSIGHT", 2, 4.5-LATITUDE_RANGE,4.5+LATITUDE_RANGE,135.0-LONGITUDE_RANGE,135.0+LONGITUDE_RANGE],

["OLYMPUS MONS", 12, 17.5-LATITUDE_RANGE,17.5+LATITUDE_RANGE,-133.5-LONGITUDE_RANGE,-133.5+LONGITUDE_RANGE],
["ARSIA MONS", 13, -7.0-LATITUDE_RANGE,-7.0+LATITUDE_RANGE,-122.5-LONGITUDE_RANGE,-122.5+LONGITUDE_RANGE],
["PAVONIS MONS", 14, 2.5-LATITUDE_RANGE,2.5+LATITUDE_RANGE,-113.5-LONGITUDE_RANGE,-113.5+LONGITUDE_RANGE],
["ASCRAEUS MONS", 15, 11.5-LATITUDE_RANGE,11.5+LATITUDE_RANGE,-105.0-LONGITUDE_RANGE,-105.0+LONGITUDE_RANGE],
["EASTERN COPRATES", 16, -13.5-LATITUDE_RANGE,-13.5+LATITUDE_RANGE,-59.0-LONGITUDE_RANGE,-59.0+LONGITUDE_RANGE],
["ELYSIUM CERBERUS PHLEGRA", 17, 35.0-LATITUDE_RANGE,35.0+LATITUDE_RANGE,169.0-LONGITUDE_RANGE,169.0+LONGITUDE_RANGE],
["OLYMPICA FOSSAE-JOVIS THOLUS", 18, 20.0-LATITUDE_RANGE,20.0+LATITUDE_RANGE,-116.0-LONGITUDE_RANGE,-116.0+LONGITUDE_RANGE],
["CERAUNIUS FOSSAE", 19, 25.0-LATITUDE_RANGE,25.0+LATITUDE_RANGE,-105.5-LONGITUDE_RANGE,-105.5+LONGITUDE_RANGE],
["CLARITAS RISE", 20, -28.5-LATITUDE_RANGE,-28.5+LATITUDE_RANGE,-100.0-LONGITUDE_RANGE,-100.0+LONGITUDE_RANGE],
["SOUTH THAUMASIA", 21, -39.5-LATITUDE_RANGE,-39.5+LATITUDE_RANGE,-92.5-LONGITUDE_RANGE,-92.5+LONGITUDE_RANGE],
["EAST THAUMASIA", 22, -31.0-LATITUDE_RANGE,-31.0+LATITUDE_RANGE,-71.0-LONGITUDE_RANGE,-71.0+LONGITUDE_RANGE],
["ULYSSES FOSSAE", 23, 10.5-LATITUDE_RANGE,10.5+LATITUDE_RANGE,-122.5-LONGITUDE_RANGE,-122.5+LONGITUDE_RANGE],
["COPRATES RISE", 24, -21.0-LATITUDE_RANGE,-21.0+LATITUDE_RANGE,-60.0-LONGITUDE_RANGE,-60.0+LONGITUDE_RANGE],
["NILI FOSSAE COLOE FOSSAE", 25, 29.0-LATITUDE_RANGE,29.0+LATITUDE_RANGE,64.5-LONGITUDE_RANGE,64.5+LONGITUDE_RANGE]
]

#[print("\"%s\":\"CH4 01\"," %region[0]) for region in occultationRegionsOfInterest]
occultationRegionsObservations = \
{
"ACIDALIA MUD VOLCANOES NE":"CH4 01",
"ACIDALIA MUD VOLCANOES BASIN":"CH4 01",
"NILI FOSSAE FORSTERITE":"CH4 01",
"NILI FOSSAE FAULT":"CH4 01",
"AEOLIS MENSAE MFF":"CH4 01",
"CERBERUS FOSSAE":"CH4 01",
"UTOPIA":"CH4 01",
"ARGYRE":"CH4 01",
"VERNAL CRATER":"CH4 01",
"CURIOSITY":"CH4 01",
"INSIGHT":"BgSubTest 03",

"OLYMPUS MONS":"CH4 01",
"ARSIA MONS":"CH4 01",
"PAVONIS MONS":"CH4 01",
"ASCRAEUS MONS":"CH4 01",
"EASTERN COPRATES":"CH4 01",
"ELYSIUM CERBERUS PHLEGRA":"CH4 01",
"OLYMPICA FOSSAE-JOVIS THOLUS":"CH4 01",
"CERAUNIUS FOSSAE":"CH4 01",
"CLARITAS RISE":"CH4 01",
"SOUTH THAUMASIA":"CH4 01",
"EAST THAUMASIA":"CH4 01",
"ULYSSES FOSSAE":"CH4 01",
"COPRATES RISE":"CH4 01",
"NILI FOSSAE COLOE FOSSAE":"CH4 01",
}

LATITUDE_RANGE = 5 #degrees
LONGITUDE_RANGE = 5 #degress

#name, priority, min lat, max lat, min lon, max lon
nadirRegionsOfInterest = \
[
["NILI FOSSAE", 25, 23.0-LATITUDE_RANGE, 23.0+LATITUDE_RANGE, 73.0-LONGITUDE_RANGE, 73.0+LONGITUDE_RANGE],
["MAWRTH VALLIS-ARAM CHAOS", 24, 14.0-LATITUDE_RANGE, 14.0+LATITUDE_RANGE, -20.0-LONGITUDE_RANGE, -20.0+LONGITUDE_RANGE],
["MERIDIANI SULPHATES", 23, 0.0-LATITUDE_RANGE, 0.0+LATITUDE_RANGE, 0.0-LONGITUDE_RANGE, 0.0+LONGITUDE_RANGE],

["AEOLIS MENSAE MFF", 3, -2.8-LATITUDE_RANGE,-2.8+LATITUDE_RANGE,145.7-LONGITUDE_RANGE,145.7+LONGITUDE_RANGE],
["INSIGHT", 2, 4.5-LATITUDE_RANGE,4.5+LATITUDE_RANGE,135.0-LONGITUDE_RANGE,135.0+LONGITUDE_RANGE],
["CURIOSITY", 1, -4.5895-LATITUDE_RANGE,-4.5895+LATITUDE_RANGE,137.4417-LONGITUDE_RANGE,137.4417+LONGITUDE_RANGE],
]

LATITUDE_RANGE = 1 #degrees
LONGITUDE_RANGE = 1 #degress


nadirRegionsOfInterest.extend( [
["ACIDALIA MUD VOLCANOES NE", 4, 44.68-LATITUDE_RANGE,44.68+LATITUDE_RANGE,-20.80-LONGITUDE_RANGE,-20.80+LONGITUDE_RANGE],
["ACIDALIA MUD VOLCANOES BASIN", 5, 40.93-LATITUDE_RANGE,40.93+LATITUDE_RANGE,-25.61-LONGITUDE_RANGE,-25.61+LONGITUDE_RANGE],
["CERBERUS FOSSAE", 6, 10.14-LATITUDE_RANGE,10.14+LATITUDE_RANGE,157.40-LONGITUDE_RANGE,157.40+LONGITUDE_RANGE],
["UTOPIA", 7, 32.97-LATITUDE_RANGE,32.97+LATITUDE_RANGE,88.18-LONGITUDE_RANGE,88.18+LONGITUDE_RANGE],
["ARGYRE", 8, -39.54-LATITUDE_RANGE,-39.54+LATITUDE_RANGE,-38.25-LONGITUDE_RANGE,-38.25+LONGITUDE_RANGE],
["VERNAL CRATER", 9, 5.64-LATITUDE_RANGE,5.64+LATITUDE_RANGE,-4.40-LONGITUDE_RANGE,-4.40+LONGITUDE_RANGE],

["OLYMPUS MONS", 10, 17.5-LATITUDE_RANGE,17.5+LATITUDE_RANGE,-133.5-LONGITUDE_RANGE,-133.5+LONGITUDE_RANGE],
["ARSIA MONS", 11, -7.0-LATITUDE_RANGE,-7.0+LATITUDE_RANGE,-122.5-LONGITUDE_RANGE,-122.5+LONGITUDE_RANGE],
["PAVONIS MONS", 12, 2.5-LATITUDE_RANGE,2.5+LATITUDE_RANGE,-113.5-LONGITUDE_RANGE,-113.5+LONGITUDE_RANGE],
["ASCRAEUS MONS", 13, 11.5-LATITUDE_RANGE,11.5+LATITUDE_RANGE,-105.0-LONGITUDE_RANGE,-105.0+LONGITUDE_RANGE],
["EASTERN COPRATES", 14, -13.5-LATITUDE_RANGE,-13.5+LATITUDE_RANGE,-59.0-LONGITUDE_RANGE,-59.0+LONGITUDE_RANGE],
["ELYSIUM CERBERUS PHLEGRA", 15, 35.0-LATITUDE_RANGE,35.0+LATITUDE_RANGE,169.0-LONGITUDE_RANGE,169.0+LONGITUDE_RANGE],
["OLYMPICA FOSSAE-JOVIS THOLUS", 16, 20.0-LATITUDE_RANGE,20.0+LATITUDE_RANGE,-116.0-LONGITUDE_RANGE,-116.0+LONGITUDE_RANGE],
["CERAUNIUS FOSSAE", 17, 25.0-LATITUDE_RANGE,25.0+LATITUDE_RANGE,-105.5-LONGITUDE_RANGE,-105.5+LONGITUDE_RANGE],
["CLARITAS RISE", 18, -28.5-LATITUDE_RANGE,-28.5+LATITUDE_RANGE,-100.0-LONGITUDE_RANGE,-100.0+LONGITUDE_RANGE],
["SOUTH THAUMASIA", 19, -39.5-LATITUDE_RANGE,-39.5+LATITUDE_RANGE,-92.5-LONGITUDE_RANGE,-92.5+LONGITUDE_RANGE],
["EAST THAUMASIA", 20, -31.0-LATITUDE_RANGE,-31.0+LATITUDE_RANGE,-71.0-LONGITUDE_RANGE,-71.0+LONGITUDE_RANGE],
["ULYSSES FOSSAE", 21, 10.5-LATITUDE_RANGE,10.5+LATITUDE_RANGE,-122.5-LONGITUDE_RANGE,-122.5+LONGITUDE_RANGE],
["COPRATES RISE", 22, -21.0-LATITUDE_RANGE,-21.0+LATITUDE_RANGE,-60.0-LONGITUDE_RANGE,-60.0+LONGITUDE_RANGE],
])



nadirRegionsObservations = \
{
"NILI FOSSAE":"Surface 3SUBD 02",
"MAWRTH VALLIS-ARAM CHAOS":"Surface 3SUBD 02",
"MERIDIANI SULPHATES":"Surface 3SUBD 02",
"AEOLIS MENSAE MFF":"CH4 2SUBD 02",

"INSIGHT":"H2O 2SUBD 01",
"CURIOSITY":"CH4 2SUBD 02",

"ACIDALIA MUD VOLCANOES NE":"CH4 2SUBD 02",
"ACIDALIA MUD VOLCANOES BASIN":"CH4 2SUBD 02",
"CERBERUS FOSSAE":"CH4 2SUBD 02",
"UTOPIA":"CH4 2SUBD 02",
"ARGYRE":"CH4 2SUBD 02",
"VERNAL CRATER":"CH4 2SUBD 02",
"OLYMPUS MONS":"CH4 2SUBD 02",
"ARSIA MONS":"CH4 2SUBD 02",
"PAVONIS MONS":"CH4 2SUBD 02",
"ASCRAEUS MONS":"CH4 2SUBD 02",
"EASTERN COPRATES":"CH4 2SUBD 02",
"ELYSIUM CERBERUS PHLEGRA":"CH4 2SUBD 02",
"OLYMPICA FOSSAE-JOVIS THOLUS":"CH4 2SUBD 02",
"CERAUNIUS FOSSAE":"CH4 2SUBD 02",
"CLARITAS RISE":"CH4 2SUBD 02",
"SOUTH THAUMASIA":"CH4 2SUBD 02",
"EAST THAUMASIA":"CH4 2SUBD 02",
"ULYSSES FOSSAE":"CH4 2SUBD 02",
"COPRATES RISE":"CH4 2SUBD 02",
}



















"""For nominal science observations, use a different order combination for low and high altitude?"""
USE_TWO_SCIENCES = True
#USE_TWO_SCIENCES = False

"""don't put 1 odd 1 even (otherwise most ingresses/egresses will be of a particular type!)"""
OCCULTATION_KEYS = [
#        "134 with 5xDark", #MTP010+
        "136 with 1xDark", #MTP010+


#        "132 with 1xDark", #special calibration
        "BgSubTest 03", 
        "CH4 01",
        "BgSubTest 03",
        "AER 01",
        "Nominal Science with CO 01", 
        "BgSubTest 03", 
        "BgSubTest 03",
        "BgSubTest 04",
#        "133 with 1xDark", #special calibration
        "Dust H2O 01",
        "Nominal Science 1xCO2 LA01",
        "BgSubTest 03",
        "Water Ice 01",
        "Nominal Science with CO 01",
        "CO 01",
        "Nominal Science 1xCO2 LA01",
#        "All Fullscan Fast", #only for long occultations
        "Nominal Science 1xCO2 LA03",
        "BgSubTest 03",
        "BgSubTest 03",
        "BgSubTest 04",
        "Nominal Science 1xCO2 LA02",
        "BgSubTest 03",
        "134 with 1xDark", #special calibration
        "HDO 01",
        "BgSubTest 03",
        "Nominal Science with CO 01",
        "BgSubTest 04",
        "CO 01",
        "CO Fullscan Fast",
        "CH4 01",
        "BgSubTest 03",
        "AER 01",
        "BgSubTest 04",
        "Nominal Science 1xCO2 LA01",
        "BgSubTest 03",
        "BgSubTest 03",
#        "135 with 1xDark", #special calibration
        "Dust H2O 01",
        "Nominal Science 1xCO2 LA01",
        "BgSubTest 03",
        "Water Ice 01",
        "BgSubTest 03",
        "BgSubTest 04",
        "Nominal Science with CO 01",
        "CO 01",
        "Nominal Science 1xCO2 LA01",
        "CO2 Fullscan Fast",
        "BgSubTest 03",
        "Nominal Science 1xCO2 LA03",
        "BgSubTest 03",
#        "134 with 1xDark", #special calibration
        "Nominal Science 1xCO2 LA02",
        "BgSubTest 03",
#        "All Fullscan Slow", #use very rarely, good for checking boresight alignment
        "HDO 01",

        "LNO Occultation Fullscan 01",

        ] * 100

UVIS_OCCULTATION_KEYS = [
        "UV 01",#
        "UV HBin 01",#
        "UV Vis 01",
        "UV Vis 01",
        ] * 100
        
OCCULTATION_MERGED_KEYS = [
        "Nominal Science 1xCO2 LA01",
        "BgSubTest 03",
        "Nominal Science 1xCO2 LA04",
        "BgSubTest 03",
        "All Fullscan Fast",
        "CH4 01",
        "134 with 1xDark", #special calibration
        ] * 10

        
OCCULTATION_GRAZING_KEYS = [
        "Nominal Science 1xCO2 LA01",
        "All Fullscan Fast",
        "Nominal Science 1xCO2 LA01",
        "CH4 01",
        "Nominal Science 1xCO2 LA01",
        ] * 10

OCCULTATION_ACS_RIDEALONG_KEYS = [
        "ACS Ridealong Science 6SUBD 01",
        "ACS Ridealong Science 6SUBD 02",
        "ACS Ridealong Science 2SUBD 01",
        ]

        
NADIR_KEYS = [
        "LNO Ice Index 2SUBD 01", #MTP013+
        "H2O 2SUBD 01",
        "HDO H2O 2SUBD 01",
        "HDO CO 3SUBD 01",
        "AER H2Oi 3SUBD 01",
        "CH4 2SUBD 02",
        "LNO Ice Index 2SUBD 01", #MTP013+
        "CH4 3SUBD 01",
        "CO 2SUBD 02",
        "Nominal 6SUBD 01",
        "CH4 2SUBD 02",
        "CO 2SUBD 02",
        "HDO H2O 2SUBD 01",
        

#        "Surface Ice 4SUBD 8S 01",  #MTP010+ #only to be added when 6 < LST < 7
#        "Surface Ice 6SUBD 8S 01",
#        "Surface Ice 4SUBD 8S 02",
#        "Surface Ice 3SUBD 8S 01",
#        "Surface Ice 4SUBD 01",
#        "Surface Ice 6SUBD 01",
#        "Surface Ice 4SUBD 02",
#        "Surface Ice 3SUBD 01",
#        "Surface Ice 2SUBD 4S 01",
#        "Surface Ice 2SUBD 4S 02",
#        "Surface Ice 2SUBD 4S 03",
#        "Surface Ice 2SUBD 4S 04",


        ] * 100

UVIS_NADIR_KEYS = [
        "UV 01",#
        "UV HBin 01",#
        "UV Vis 01",
        "UV Vis 01",
        ] * 100

        
#limb 3 and 4 are more important than the others
NADIR_LIMB_KEYS = [
#        "Limb 2SUBD 01",
        "Limb 2SUBD 03",
        "Limb 2SUBD 04",
#        "Limb 2SUBD 02",
#        "Limb 2SUBD 03",
#        "Limb 2SUBD 04",
#        "Limb 2SUBD 05",
#        "Limb 2SUBD 03",
#        "Limb 2SUBD 04",
#        "Limb 2SUBD 06",
#        "Limb 2SUBD 03",
#        "Limb 2SUBD 04",
        ] * 15

NADIR_NIGHTSIDE_KEYS= [
        "Nominal Nightside 02",
        ] * 100

        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        

#windows only
#run planning script in pop-out window so user can continue working
#import os
#import sys
#if sys.platform == "win32":
#    if __name__ == "__main__":
#        os.system("python -i observation_planning_v05.py")













