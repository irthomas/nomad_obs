# -*- coding: utf-8 -*-
# pylint: disable=E1103
# pylint: disable=C0301
"""
Created on Wed Oct 18 13:56:09 2017

@author: iant



   #add orders 126-129 to planning
   
   #add Surface Ice obs to final orbit plan when beta angle is high


"""


__project__   = "NOMAD Observation Planning"
__author__    = "Ian Thomas"
__contact__   = "ian . thomas AT aeronomie . be"



#ACS joint observation names. Don't modify unless instructed to do so by SOC/ACS.
#SOC_JOINT_OBSERVATION_NAMES = {
##        "Nominal Science 1xCO2 LA01":"NOM_01",
##        "Dust H2O 01":"DUST01",
##        "Water Ice 01":"ICE_01",
##        "AER 01":"AER_01"
#
#        }

SOC_JOINT_OBSERVATION_NAMES = {
    "NOM_02":["6SUBD Nominal #1", "6SUBD Nominal #2"],
    "NOM_03":["6SUBD Nominal #3"],
    "CO_001":["6SUBD Nom CO #1", "6SUBD Nom CO #2", "6SUBD Nom CO #3", "6SUBD Nom CO #4", "6SUBD Nom CO #5"],
    "CO2_01":["6SUBD Nom CO2 #1", "6SUBD Nom CO2 #2"],
    
    "AER_01":["AER 01"],
    "DUST01":["Dust H2O 01"],
    "HDO_01":["HDO 01"],
    "ICE_01":["Water Ice 01"],
    
    "NOM_01":["Nominal Science 1xCO2 LA01"],
    }



SOC_JOINT_OBSERVATION_TYPES = [
        "OCCEG",
        "OCCIN",
        "OCCME",
#        "OCCGR" #ACS doesn't run grazings
        ]
        


"""make the observation dictionaries of all the desired measurement types
DON'T MODIFY OR DELETE ANY OBSERVATIONS - JUST ADD NEW ONES"""
#name:[[orders], int time, rhythm, lines, so=0/lno=1]
occultationObservationDict = {
        
        
#new MTP025+
"6SUBD CO2 #1":[[156,116,118,140,154,158], 4, 1, 16, 0],
"6SUBD CO2 #10":[[156,116,118,169,154,158], 4, 1, 16, 0],

        
#new MTP021+
"6SUBD Nominal #1":[[121, 134, 149, 169, 186, 190], 4, 1, 16, 0],
"6SUBD Nominal #2":[[119, 136, 149, 169, 186, 189], 4, 1, 16, 0],
"6SUBD Nominal #3":[[121, 136, 167, 169, 190, 192], 4, 1, 16, 0],

"6SUBD Nom CO2 #1":[[121, 134, 149, 164, 165, 169], 4, 1, 16, 0],
"6SUBD Nom CO2 #2":[[121, 149, 164, 165, 186, 190], 4, 1, 16, 0],

"6SUBD Nom CH4 #1":[[134, 136, 148, 164, 187, 190], 4, 1, 16, 0],
"6SUBD Nom CH4 #2":[[134, 136, 164, 169, 186, 190], 4, 1, 16, 0],



"6SUBD Nom CO #1":[[121, 149, 186, 187, 189, 190], 4, 1, 16, 0],
"6SUBD Nom CO #2":[[134, 169, 186, 187, 189, 190], 4, 1, 16, 0],
"6SUBD Nom CO #3":[[136, 169, 186, 187, 189, 190], 4, 1, 16, 0],
"6SUBD Nom CO #4":[[121, 136, 190, 191, 192, 193], 4, 1, 16, 0],
"6SUBD Nom CO #5":[[121, 136, 168, 169, 189, 193], 4, 1, 16, 0],

"6SUBD CH4 #1":[[121, 133, 134, 135, 136, 169], 4, 1, 16, 0],

"6SUBD CO H2O #1":[[134,169,186,187,189,190], 4, 1, 16, 0],
"6SUBD CO H2O #2":[[136,169,186,187,189,190], 4, 1, 16, 0],

"6SUBD CO2 CO #1":[[119,149,164,165,186,190], 4, 1, 16, 0],

"6SUBD CH4 H2O #1":[[169,132,133,134,136,137], 4, 1, 16, 0],



"All Fullscan Fast #2":[["COP#53"], 4, 1, 16, 0],
"All Fullscan Slow #2":[["COP#31"], 4, 1, 24, 0],
#
"CO2 Fullscan Fast #2":[["COP#41"], 4, 1, 16, 0], #160-170
"CO Fullscan Fast #2":[["COP#46"], 4, 1, 16, 0], #185-195
"LNO Occultation Fullscan Fast #2":[["COP#56"], 2, 1, 16, 1],


"119 only #2":[[119, 119, 119, 119, 119, 119], 4, 1, 16, 0],
"120 only #2":[[120, 120, 120, 120, 120, 120], 4, 1, 16, 0],
"121 only #2":[[121, 121, 121, 121, 121, 121], 4, 1, 16, 0],
"122 only #2":[[122, 122, 122, 122, 122, 122], 4, 1, 16, 0],
"123 only #2":[[123, 123, 123, 123, 123, 123], 4, 1, 16, 0],

"126 only #2":[[126, 126, 126, 126, 126, 126], 4, 1, 16, 0],
"127 only #2":[[127, 127, 127, 127, 127, 127], 4, 1, 16, 0],
"129 only #2":[[129, 129, 129, 129, 129, 129], 4, 1, 16, 0],

"132 only #2":[[132, 132, 132, 132, 132, 132], 4, 1, 16, 0],
"133 only #2":[[133, 133, 133, 133, 133, 133], 4, 1, 16, 0],
"134 only #2":[[134, 134, 134, 134, 134, 134], 4, 1, 16, 0],
"135 only #2":[[135, 135, 135, 135, 135, 135], 4, 1, 16, 0],
"136 only #2":[[136, 136, 136, 136, 136, 136], 4, 1, 16, 0],


#old to be phased out
"BgSubTest 03":[[121,134,149,165,168,190], 4, 1, 16, 0],
"BgSubTest 04":[[119,136,148,166,168,189], 4, 1, 16, 0],
"BgSubTest 05":[[121,134,148,167,169,190], 4, 1, 16, 0], #SWITCHING TO 169 FOR WATER
"BgSubTest 06":[[121,136,148,167,169,189], 4, 1, 16, 0], #SWITCHING TO 169 FOR WATER
"Nominal Science 1xCO2 LA05":[[190,169,148,136,121,0], 4, 1, 16, 0], #SWITCHING TO 169 FOR WATER. NO SCI2
"Nominal Science 1xCO2 LA06":[[190,169,148,134,121,0], 4, 1, 16, 0], #SWITCHING TO 169 FOR WATER. NO SCI2

"CO2 100km #1":[[167,155,159,164,148,0], 4, 1, 16, 0],

        
#old pre MTP021
"Nominal Science 1xCO2 LA01":[[168,134,190,121,149,0], 4, 1, 16, 0], #no CO2 50-120km
"Nominal Science 1xCO2 HA01":[[168,134,190,121,165,0], 4, 1, 16, 0],
"Nominal Science 1xCO2 LA02":[[168,134,190,119,149,0], 4, 1, 16, 0], #no CO2 50-120km
"Nominal Science 1xCO2 HA02":[[168,134,190,119,165,0], 4, 1, 16, 0],

"Nominal Science 1xCO2 LA03":[[168,134,189,121,149,0], 4, 1, 16, 0], #no CO2 50-120km
"Nominal Science 1xCO2 HA03":[[168,134,189,121,165,0], 4, 1, 16, 0],
"Nominal Science 1xCO2 LA04":[[168,136,189,119,149,0], 4, 1, 16, 0], #no CO2 50-120km
"Nominal Science 1xCO2 HA04":[[168,136,189,119,165,0], 4, 1, 16, 0],

"Nominal Science with CO 01":[[169,134,186,121,147,0], 4, 1, 16, 0], #186 for CO


"Dust H2O 01":[[119,130,145,171,191,0], 4, 1, 16, 0],
"Water Ice 01":[[119,140,153,170,191,0], 4, 1, 16, 0],
"CO 01":[[167,188,189,190,191,0], 4, 1, 16, 0],
"HDO 01":[[168,134,124,129,190,0], 4, 1, 16, 0],
"AER 01":[[119,133,143,154,169,0], 4, 1, 16, 0],
"CH4 01":[[168,133,134,135,136,0], 4, 1, 16, 0],



#old not used
"All Fullscan Fast":[["COP#293"], 0, 1, 16, 0],
"All Fullscan Slow":[["COP#107"], 0, 1, 24, 0],
"CO2 Fullscan Fast":[["COP#239"], 0, 1, 16, 0],
"CO Fullscan Fast":[["COP#254"], 0, 1, 16, 0],
"ACS Ridealong Science 6SUBD 01":[[121,134,149,165,168,190], 10, 4, 20, 0],
"ACS Ridealong Science 6SUBD 02":[[121,134,149,165,168,190], 20, 4, 20, 0],
"ACS Ridealong Science 2SUBD 01":[[164,165], 40, 4, 24, 0],
"LNO Occultation Nominal Science 1xCO2 01":[["COP#697"], 2, 1, 20, 1],
"LNO Occultation Fullscan 01":[["COP#93"], 2, 1, 20, 1],
"119 with 1xDark":[[119,119,119,119,119,0], 4, 1, 16, 0],
"120 with 1xDark":[[120,120,120,120,120,0], 4, 1, 16, 0],
"121 with 1xDark":[[121,121,121,121,121,0], 4, 1, 16, 0],
"122 with 1xDark":[[122,122,122,122,122,0], 4, 1, 16, 0],
"123 with 1xDark":[[123,123,123,123,123,0], 4, 1, 16, 0],
"132 with 1xDark":[[132,132,132,132,132,0], 4, 1, 16, 0],
"133 with 1xDark":[[133,133,133,133,133,0], 4, 1, 16, 0],
"134 with 1xDark":[[134,134,134,134,134,0], 4, 1, 16, 0],
"135 with 1xDark":[[135,135,135,135,135,0], 4, 1, 16, 0],
"136 with 1xDark":[[136,136,136,136,136,0], 4, 1, 16, 0],
"190 with 1xDark":[[190,190,190,190,190,0], 4, 1, 16, 0],
"134 with 5xDark":[[134,0,0,0,0,0], 4, 1, 16, 0], #MTP010+
"136 with 5xDark":[[136,0,0,0,0,0], 4, 1, 16, 0], #MTP010+
"Nominal Science 1xCO2 TOA":[[168,135,190,121,164,0], 4, 1, 16, 0], #MTP010+
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
"Nominal 4SUBD 01":[[168,134,121,190], 195, 15, 144, 1],
"Nominal 3SUBD 01":[[167,169,190], 205, 15, 144, 1],

"H2O 2SUBD 01":[[167,169], 200, 15, 144, 1],
"HDO CO 3SUBD 02":[[168,121,190], 205, 15, 144, 1],
"CH4 3SUBD 01":[[168,134,136], 205, 15, 144, 1],

"CH4 H2O 2SUBD 02":[[168,136], 200, 15, 144, 1], #USE FOR CURIOSITY ALTERNATING WITH CO. ORDER 136 IS BETTER FOR CH4 THAN 134
"CH4 H2O 2SUBD 01":[[168,134], 200, 15, 144, 1], #OLD TARGET FOR CURIOSITY. USE OCCASIONALLY, ALTERNATING WITH CO

"CH4 2SUBD 03":[[136,136], 200, 15, 144, 1], #ORDER 136 IS BETTER FOR CH4 THAN 134
"CH4 2SUBD 02":[[134,136], 200, 15, 144, 1], #OLD TARGET FOR CURIOSITY. USE OCCASIONALLY

"CH4 CO 2SUBD 01":[[190,136], 200, 15, 144, 1], #CH4 AND OTHER ORDER
"CH4 CO 2SUBD 02":[[190,134], 200, 15, 144, 1], #CH4 AND OTHER ORDER

"HDO H2O 2SUBD 02":[[168,124], 200, 15, 144, 1], #S.AOKI
"HDO H2O 2SUBD 03":[[121,168], 200, 15, 144, 1],

"H2O CO 2SUBD 01":[[168,189], 200, 15, 144, 1],
"CO H2O 3SUBD 01":[[191,190,168], 205, 15, 144, 1],
                 
"Nominal Limb 01":[[164,169], 200, 15, 144, 1], #NEW LIMB <50KM
"Limb 2SUBD 07":[[164,164], 200, 15, 144, 1], #NEW LIMB >50KM


"CO Fullscan #2":[["COP#71"], 0, 15, 144, 1], #ORDERS 185-195
"H2O Fullscan #2":[["COP#67"], 0, 15, 144, 1], #ORDERS 165-175



#surface ice variable rhythms  #MTP010+ when lst is low
"Surface Ice 4SUBD 8S 01":[[199, 194, 193, 187], 220, 8, 144, 1],
"Surface Ice 6SUBD 8S 01":[[199, 198, 194, 193, 187, 186], 205, 8, 144, 1],
"Surface Ice 4SUBD 8S 02":[[199, 189, 188, 187], 220, 8, 144, 1],
"Surface Ice 3SUBD 8S 01":[[199, 194, 188], 180, 8, 144, 1],

"Surface Ice 4SUBD 01":[[199, 194, 193, 187], 195, 15, 144, 1],
"Surface Ice 6SUBD 01":[[199, 198, 194, 193, 187, 186], 220, 15, 144, 1], #ERROR IN COP TABLES BEFORE MTP021
"Surface Ice 4SUBD 02":[[199, 189, 188, 187], 195, 15, 144, 1],
"Surface Ice 3SUBD 01":[[199, 194, 188], 205, 15, 144, 1],
    
"Surface Ice 2SUBD 4S 01":[[199, 193], 205, 4, 144, 1],
"Surface Ice 2SUBD 4S 02":[[198, 194], 205, 4, 144, 1],
"Surface Ice 2SUBD 4S 03":[[193, 194], 205, 4, 144, 1],
"Surface Ice 2SUBD 4S 04":[[199, 187], 205, 4, 144, 1],

#F Schmidt order 193 + something else
"Ice CH4 2SUBD #1":[[193,136], 200, 15, 144, 1],
"Ice H2O 2SUBD #1":[[193,168], 200, 15, 144, 1],
"Ice CO 2SUBD #1":[[193,190], 200, 15, 144, 1],

"Surface 3SUBD 02":[[191,194,196], 205, 15, 144, 1], #USE FOR F.ALTIERI NADIR TARGETS MTP010+




#old
"HDO CO 3SUBD 01":[[167,121,190], 205, 15, 144, 1],
"CO 2SUBD 02":[[167,189], 200, 15, 144, 1],

"CO2 Fullscan":[["COP#144"], 0, 15, 144, 1],
"CO Fullscan":[["COP#124"], 0, 15, 144, 1],
"H2O Fullscan":[["COP#116"], 0, 15, 144, 1],
"CH4 Fullscan":[["COP#104"], 0, 15, 144, 1],

"HDO Fullscan":[["COP#140"], 0, 15, 144, 1],
"AER H2Oi 3SUBD 01":[[169,131,127], 205, 15, 144, 1],

"Nominal 6SUBD 02":[[167,134,168,121,189,197], 220, 15, 144, 1],

"CH4 2SUBD 01":[[167,134], 200, 15, 144, 1],
"D/H 2SUBD 01":[[121,169], 200, 15, 144, 1],
"D/H 3SUBD 01":[[167,121,169], 205, 15, 144, 1],
"HDO 3SUBD 01":[[121,171,124], 205, 15, 144, 1],
"AER H2Oi CO2i 4SUBD 01":[[164,169,131,127], 195, 15, 144, 1],
"HDO H2O 2SUBD 01":[[121,169], 200, 15, 144, 1],
"Surface 3SUBD 01":[[168, 190, 191], 205, 15, 144, 1], #OLD TARGET FOR FA NADIR TARGETS

"Limb 2SUBD 01":[[161,162], 200, 15, 144, 1],
"Limb 2SUBD 02":[[162,163], 200, 15, 144, 1],
"Limb 2SUBD 03":[[163,164], 200, 15, 144, 1],
"Limb 2SUBD 04":[[164,165], 200, 15, 144, 1],
"Limb 2SUBD 05":[[165,166], 200, 15, 144, 1],
"Limb 2SUBD 06":[[166,167], 200, 15, 144, 1],

"Nominal Nightside 01":[[169,190], 200, 15, 144, 1],
"Nominal Nightside 02":[[162,163], 200, 15, 144, 1],

"LNO Ice Index 2SUBD 01":[[153, 158], 200, 15, 144, 1], #OLD <MTP013 F.SCHMIDT SIGNAL TOO LOW
"LNO Ice Index 2SUBD 02":[[193, 194], 200, 15, 144, 1], #OLD MTP013+ F.SCHMIDT NEW. LST 6-8AM AND AT HIGH LATS ONLY

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
        mtpStart = "" #EXMGEO_TD2N start time as specified by Bojan or Claudio
        mtpEnd = "" #EXMGEO_TD2N end time as specified by Bojan or Claudio
        copVersion = "" #desired cop table folder - remember to update if patched
#        ALLOCATED_DATA_VOLUME = #MBits # add if required

    elif mtpNumber == 30:
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
            








    
"""select +- search range for the regions of interest listed below"""
LATITUDE_RANGE = 2 #degrees
LONGITUDE_RANGE = 2 #degress

#name, priority, cycle_type, min lat, max lat, min lon, max lon
occultationRegionsOfInterest = \
[
["ALBA MONS", 30, "OccultationCycleCH4", 40.0-LATITUDE_RANGE,40.0+LATITUDE_RANGE,-109.6-LONGITUDE_RANGE,-109.6+LONGITUDE_RANGE],
["ALBA MONS VOLCANIC CONES S", 29, "OccultationCycleCH4", 23.0-LATITUDE_RANGE,23.0+LATITUDE_RANGE,-110.0-LONGITUDE_RANGE,-110.0+LONGITUDE_RANGE],
["OLYMPUS MONS VOLCANIC CONES E", 28, "OccultationCycleCH4", 15.0-LATITUDE_RANGE,15.0+LATITUDE_RANGE,-127.0-LONGITUDE_RANGE,-127.0+LONGITUDE_RANGE],
["PAVONIS MONS VOLCANIC CONES SE", 27, "OccultationCycleCH4", -2.0-LATITUDE_RANGE,-2.0+LATITUDE_RANGE,-107.0-LONGITUDE_RANGE,-107.0+LONGITUDE_RANGE],
["ARSIA MONS VOLCANIC CONES NE", 26, "OccultationCycleCH4", -5.0-LATITUDE_RANGE,-5.0+LATITUDE_RANGE,-114.0-LONGITUDE_RANGE,-114.0+LONGITUDE_RANGE],

 ["ACIDALIA MUD VOLCANOES NE", 25, "OccultationCycleCH4", 44.68-LATITUDE_RANGE,44.68+LATITUDE_RANGE,-20.80-LONGITUDE_RANGE,-20.80+LONGITUDE_RANGE],
["ACIDALIA MUD VOLCANOES BASIN", 24, "OccultationCycleCH4", 40.93-LATITUDE_RANGE,40.93+LATITUDE_RANGE,-25.61-LONGITUDE_RANGE,-25.61+LONGITUDE_RANGE],
["NILI FOSSAE FORSTERITE", 23, "OccultationCycleCH4", 21.72-LATITUDE_RANGE,21.72+LATITUDE_RANGE,78.51-LONGITUDE_RANGE,78.51+LONGITUDE_RANGE],
["NILI FOSSAE FAULT", 22, "OccultationCycleCH4", 23.93-LATITUDE_RANGE,23.93+LATITUDE_RANGE,78.79-LONGITUDE_RANGE,78.79+LONGITUDE_RANGE],
["AEOLIS MENSAE MFF", 21, "OccultationCycleCH4", -2.8-LATITUDE_RANGE,-2.8+LATITUDE_RANGE,145.7-LONGITUDE_RANGE,145.7+LONGITUDE_RANGE],
["CERBERUS FOSSAE", 20, "OccultationCycleCH4", 10.14-LATITUDE_RANGE,10.14+LATITUDE_RANGE,157.40-LONGITUDE_RANGE,157.40+LONGITUDE_RANGE],
["UTOPIA", 19, "OccultationCycleCH4", 32.97-LATITUDE_RANGE,32.97+LATITUDE_RANGE,88.18-LONGITUDE_RANGE,88.18+LONGITUDE_RANGE],
["ARGYRE", 18, "OccultationCycleCH4", -39.54-LATITUDE_RANGE,-39.54+LATITUDE_RANGE,-38.25-LONGITUDE_RANGE,-38.25+LONGITUDE_RANGE],
["VERNAL CRATER", 17, "OccultationCycleCH4", 5.64-LATITUDE_RANGE,5.64+LATITUDE_RANGE,-4.40-LONGITUDE_RANGE,-4.40+LONGITUDE_RANGE],

["OLYMPUS MONS", 16, "OccultationCycleCH4", 17.5-LATITUDE_RANGE,17.5+LATITUDE_RANGE,-133.5-LONGITUDE_RANGE,-133.5+LONGITUDE_RANGE],
["ARSIA MONS", 15, "OccultationCycleCH4", -7.0-LATITUDE_RANGE,-7.0+LATITUDE_RANGE,-122.5-LONGITUDE_RANGE,-122.5+LONGITUDE_RANGE],
["PAVONIS MONS", 14, "OccultationCycleCH4", 2.5-LATITUDE_RANGE,2.5+LATITUDE_RANGE,-113.5-LONGITUDE_RANGE,-113.5+LONGITUDE_RANGE],
["ASCRAEUS MONS", 13, "OccultationCycleCH4", 11.5-LATITUDE_RANGE,11.5+LATITUDE_RANGE,-105.0-LONGITUDE_RANGE,-105.0+LONGITUDE_RANGE],
["EASTERN COPRATES", 12, "OccultationCycleCH4", -13.5-LATITUDE_RANGE,-13.5+LATITUDE_RANGE,-59.0-LONGITUDE_RANGE,-59.0+LONGITUDE_RANGE],
["ELYSIUM CERBERUS PHLEGRA", 11, "OccultationCycleCH4", 35.0-LATITUDE_RANGE,35.0+LATITUDE_RANGE,169.0-LONGITUDE_RANGE,169.0+LONGITUDE_RANGE],
["OLYMPICA FOSSAE-JOVIS THOLUS", 10, "OccultationCycleCH4", 20.0-LATITUDE_RANGE,20.0+LATITUDE_RANGE,-116.0-LONGITUDE_RANGE,-116.0+LONGITUDE_RANGE],
["CERAUNIUS FOSSAE", 9, "OccultationCycleCH4", 25.0-LATITUDE_RANGE,25.0+LATITUDE_RANGE,-105.5-LONGITUDE_RANGE,-105.5+LONGITUDE_RANGE],
["CLARITAS RISE", 8, "OccultationCycleCH4", -28.5-LATITUDE_RANGE,-28.5+LATITUDE_RANGE,-100.0-LONGITUDE_RANGE,-100.0+LONGITUDE_RANGE],
["SOUTH THAUMASIA", 7, "OccultationCycleCH4", -39.5-LATITUDE_RANGE,-39.5+LATITUDE_RANGE,-92.5-LONGITUDE_RANGE,-92.5+LONGITUDE_RANGE],
["EAST THAUMASIA", 6, "OccultationCycleCH4", -31.0-LATITUDE_RANGE,-31.0+LATITUDE_RANGE,-71.0-LONGITUDE_RANGE,-71.0+LONGITUDE_RANGE],
["ULYSSES FOSSAE", 5, "OccultationCycleCH4", 10.5-LATITUDE_RANGE,10.5+LATITUDE_RANGE,-122.5-LONGITUDE_RANGE,-122.5+LONGITUDE_RANGE],
["COPRATES RISE", 4, "OccultationCycleCH4", -21.0-LATITUDE_RANGE,-21.0+LATITUDE_RANGE,-60.0-LONGITUDE_RANGE,-60.0+LONGITUDE_RANGE],
["NILI FOSSAE COLOE FOSSAE", 3, "OccultationCycleCH4", 29.0-LATITUDE_RANGE,29.0+LATITUDE_RANGE,64.5-LONGITUDE_RANGE,64.5+LONGITUDE_RANGE],
]
LATITUDE_RANGE = 5 #degrees
LONGITUDE_RANGE = 5 #degress

occultationRegionsOfInterest.extend([
["INSIGHT", 2, "OccultationCycleH2O", 4.5-LATITUDE_RANGE,4.5+LATITUDE_RANGE,135.0-LONGITUDE_RANGE,135.0+LONGITUDE_RANGE],
["CURIOSITY", 1, "OccultationCycleCH4", -4.5895-LATITUDE_RANGE,-4.5895+LATITUDE_RANGE,137.4417-LONGITUDE_RANGE,137.4417+LONGITUDE_RANGE],
])
#[print("\"%s\":\"CH4 01\"," %region[0]) for region in occultationRegionsOfInterest]



#name, priority, min lat, max lat, min lon, max lon

LATITUDE_RANGE = 1 #degrees
LONGITUDE_RANGE = 1 #degress

nadirRegionsOfInterest = [
["ACIDALIA MUD VOLCANOES NE", 25, "NadirCycleCH4", 44.68-LATITUDE_RANGE,44.68+LATITUDE_RANGE,-20.80-LONGITUDE_RANGE,-20.80+LONGITUDE_RANGE],
["ACIDALIA MUD VOLCANOES BASIN", 24, "NadirCycleCH4", 40.93-LATITUDE_RANGE,40.93+LATITUDE_RANGE,-25.61-LONGITUDE_RANGE,-25.61+LONGITUDE_RANGE],
["CERBERUS FOSSAE", 23, "NadirCycleCH4", 10.14-LATITUDE_RANGE,10.14+LATITUDE_RANGE,157.40-LONGITUDE_RANGE,157.40+LONGITUDE_RANGE],
["UTOPIA", 22, "NadirCycleCH4", 32.97-LATITUDE_RANGE,32.97+LATITUDE_RANGE,88.18-LONGITUDE_RANGE,88.18+LONGITUDE_RANGE],
["ARGYRE", 21, "NadirCycleCH4", -39.54-LATITUDE_RANGE,-39.54+LATITUDE_RANGE,-38.25-LONGITUDE_RANGE,-38.25+LONGITUDE_RANGE],
["VERNAL CRATER", 20, "NadirCycleCH4", 5.64-LATITUDE_RANGE,5.64+LATITUDE_RANGE,-4.40-LONGITUDE_RANGE,-4.40+LONGITUDE_RANGE],

["OLYMPUS MONS", 19, "NadirCycleCH4", 17.5-LATITUDE_RANGE,17.5+LATITUDE_RANGE,-133.5-LONGITUDE_RANGE,-133.5+LONGITUDE_RANGE],
["ARSIA MONS", 18, "NadirCycleCH4", -7.0-LATITUDE_RANGE,-7.0+LATITUDE_RANGE,-122.5-LONGITUDE_RANGE,-122.5+LONGITUDE_RANGE],
["PAVONIS MONS", 17, "NadirCycleCH4", 2.5-LATITUDE_RANGE,2.5+LATITUDE_RANGE,-113.5-LONGITUDE_RANGE,-113.5+LONGITUDE_RANGE],
["ASCRAEUS MONS", 16, "NadirCycleCH4", 11.5-LATITUDE_RANGE,11.5+LATITUDE_RANGE,-105.0-LONGITUDE_RANGE,-105.0+LONGITUDE_RANGE],
["EASTERN COPRATES", 15, "NadirCycleCH4", -13.5-LATITUDE_RANGE,-13.5+LATITUDE_RANGE,-59.0-LONGITUDE_RANGE,-59.0+LONGITUDE_RANGE],
["ELYSIUM CERBERUS PHLEGRA", 14, "NadirCycleCH4", 35.0-LATITUDE_RANGE,35.0+LATITUDE_RANGE,169.0-LONGITUDE_RANGE,169.0+LONGITUDE_RANGE],
["OLYMPICA FOSSAE-JOVIS THOLUS", 13, "NadirCycleCH4", 20.0-LATITUDE_RANGE,20.0+LATITUDE_RANGE,-116.0-LONGITUDE_RANGE,-116.0+LONGITUDE_RANGE],
["CERAUNIUS FOSSAE", 12, "NadirCycleCH4", 25.0-LATITUDE_RANGE,25.0+LATITUDE_RANGE,-105.5-LONGITUDE_RANGE,-105.5+LONGITUDE_RANGE],
["CLARITAS RISE", 11, "NadirCycleCH4", -28.5-LATITUDE_RANGE,-28.5+LATITUDE_RANGE,-100.0-LONGITUDE_RANGE,-100.0+LONGITUDE_RANGE],
["SOUTH THAUMASIA", 10, "NadirCycleCH4", -39.5-LATITUDE_RANGE,-39.5+LATITUDE_RANGE,-92.5-LONGITUDE_RANGE,-92.5+LONGITUDE_RANGE],
["EAST THAUMASIA", 9, "NadirCycleCH4", -31.0-LATITUDE_RANGE,-31.0+LATITUDE_RANGE,-71.0-LONGITUDE_RANGE,-71.0+LONGITUDE_RANGE],
["ULYSSES FOSSAE", 8, "NadirCycleCH4", 10.5-LATITUDE_RANGE,10.5+LATITUDE_RANGE,-122.5-LONGITUDE_RANGE,-122.5+LONGITUDE_RANGE],
["COPRATES RISE", 7, "NadirCycleCH4", -21.0-LATITUDE_RANGE,-21.0+LATITUDE_RANGE,-60.0-LONGITUDE_RANGE,-60.0+LONGITUDE_RANGE],
]

LATITUDE_RANGE = 3 #degrees
LONGITUDE_RANGE = 3 #degress

nadirRegionsOfInterest.extend([
["NILI FOSSAE", 6, "NadirCycleSurface", 23.0-LATITUDE_RANGE, 23.0+LATITUDE_RANGE, 73.0-LONGITUDE_RANGE, 73.0+LONGITUDE_RANGE],
["MAWRTH VALLIS-ARAM CHAOS", 5, "NadirCycleSurface", 14.0-LATITUDE_RANGE, 14.0+LATITUDE_RANGE, -20.0-LONGITUDE_RANGE, -20.0+LONGITUDE_RANGE],
["MERIDIANI SULPHATES", 4, "NadirCycleSurface", 0.0-LATITUDE_RANGE, 0.0+LATITUDE_RANGE, 0.0-LONGITUDE_RANGE, 0.0+LONGITUDE_RANGE],
])

LATITUDE_RANGE = 5 #degrees
LONGITUDE_RANGE = 5 #degress

nadirRegionsOfInterest.extend([
["AEOLIS MENSAE MFF", 3, "NadirCycleCH4", -2.8-LATITUDE_RANGE,-2.8+LATITUDE_RANGE,145.7-LONGITUDE_RANGE,145.7+LONGITUDE_RANGE],
["INSIGHT", 2, "NadirCycleH2O", 4.5-LATITUDE_RANGE,4.5+LATITUDE_RANGE,135.0-LONGITUDE_RANGE,135.0+LONGITUDE_RANGE],
["CURIOSITY", 1, "NadirCycleCH4", -4.5895-LATITUDE_RANGE,-4.5895+LATITUDE_RANGE,137.4417-LONGITUDE_RANGE,137.4417+LONGITUDE_RANGE],
])







"""For nominal science observations, use a different order combination for low and high altitude?"""
#USE_TWO_SCIENCES = True
USE_TWO_SCIENCES = False

"""don't put 1 odd 1 even (otherwise most ingresses/egresses will be of a particular type!)"""
OCCULTATION_KEYS = [
#        "136 with 1xDark", #MTP010+
#        "132 with 1xDark", #special calibration
#        "BgSubTest 03",
#        "CH4 01",
#        "BgSubTest 04",
#        "AER 01",
#        "Nominal Science with CO 01", 
#        "BgSubTest 05",
#        "BgSubTest 06",
#        "BgSubTest 03",
#        "133 with 1xDark", #special calibration
#        "Dust H2O 01",
#        "Nominal Science 1xCO2 LA05",
#        "BgSubTest 04",
#        "Water Ice 01",
#        "Nominal Science with CO 01",
#        "CO 01",
#        "Nominal Science 1xCO2 LA06",
#        "Nominal Science 1xCO2 LA05",
#        "BgSubTest 05",
#        "BgSubTest 06",
#        "BgSubTest 03",
#        "BgSubTest 04",
#        "134 with 1xDark", #special calibration
#        "HDO 01",
#        "BgSubTest 05",
#        "Nominal Science with CO 01",
#        "BgSubTest 06",
#        "CO 01",
#        "CO Fullscan Fast",
#        "CH4 01",
#        "BgSubTest 03",
#        "AER 01",
#        "BgSubTest 04",
#        "Nominal Science 1xCO2 LA06",
#        "BgSubTest 05",
#        "BgSubTest 06",
#        "135 with 1xDark", #special calibration
#        "Dust H2O 01",
#        "BgSubTest 03",
#        "Water Ice 01",
#        "BgSubTest 04",
#        "BgSubTest 05",
#        "Nominal Science with CO 01",
#        "CO 01",
#        "Nominal Science 1xCO2 LA05",
#        "CO2 Fullscan Fast",
#        "BgSubTest 06",
#        "Nominal Science 1xCO2 LA06",
#        "BgSubTest 05",
#        "BgSubTest 06",
#        "HDO 01",
#        "LNO Occultation Fullscan 01",

    ["6SUBD Nominal #1"] * 20, 
    ["6SUBD Nominal #2"] * 20, 
    ["6SUBD Nominal #3"] * 20, 
    ["6SUBD Nom CO2 #1"] * 5,
    ["6SUBD Nom CO2 #2"] * 5,
    ["6SUBD Nom CH4 #1"] * 5,
    ["6SUBD Nom CH4 #2"] * 5,
    ["6SUBD Nom CO #1"] * 5,
    ["6SUBD Nom CO #2"] * 5,
    ["6SUBD Nom CO #3"] * 5,
    ["6SUBD Nom CO #4"] * 5,
    ["6SUBD Nom CO #5"] * 5,
     
    ["CO2 100km #1"] * 10,
     
    ["6SUBD CH4 #1"] * 3,
    ["6SUBD CO H2O #1"] * 3,
    ["6SUBD CO H2O #2"] * 3,
    ["6SUBD CO2 CO #1"] * 3,
    ["6SUBD CH4 H2O #1"] * 3,
    ["All Fullscan Fast #2"] * 3,
    ["All Fullscan Slow #2"] * 1,
    ["CO2 Fullscan Fast #2"] * 1,
    ["CO Fullscan Fast #2"] * 1,
    ["LNO Occultation Fullscan Fast #2"] * 1,
    ["119 only #2"] * 1,
    ["120 only #2"] * 1,
    ["121 only #2"] * 1,

#    ["126 only #2"] * 2,
    ["127 only #2"] * 5,
    ["129 only #2"] * 3,
     
    ["133 only #2"] * 1,
    ["134 only #2"] * 5,
    ["135 only #2"] * 1,
    ["136 only #2"] * 5,
    ["BgSubTest 03"] * 3, #reduce by one in MTP029
    ["BgSubTest 04"] * 3,
    ["BgSubTest 05"] * 3,
    ["BgSubTest 06"] * 3,
    ["Nominal Science 1xCO2 LA05"] * 2, #reduce by one in MTP029
    ["Nominal Science 1xCO2 LA06"] * 2,
    ["Nominal Science 1xCO2 LA01"] * 2,
    ["Nominal Science 1xCO2 HA01"] * 2,
    ["Nominal Science 1xCO2 LA02"] * 2,
    ["Nominal Science 1xCO2 HA02"] * 2,
    ["Nominal Science 1xCO2 LA03"] * 2,
    ["Nominal Science 1xCO2 HA03"] * 2,
    ["Nominal Science 1xCO2 LA04"] * 2,
    ["Nominal Science 1xCO2 HA04"] * 2,
    ["Dust H2O 01"] * 1,
    ["Water Ice 01"] * 1,
    ["CO 01"] * 1,
    ["HDO 01"] * 1,
    ["AER 01"] * 1,
    
    #new MTP025+
    ["6SUBD CO2 #1"] * 10, #reduce after MTP025
    ["6SUBD CO2 #10"] * 10, #reduce after MTP025


]

        
OCCULTATION_MERGED_KEYS = [
#        ["Nominal Science 1xCO2 LA05"] * 1,
#        ["BgSubTest 05"] * 1,
#        ["Nominal Science 1xCO2 LA05"] * 1,
#        ["BgSubTest 06"] * 1,
#        ["All Fullscan Fast"] * 1,
#        ["CH4 01"] * 1,
#        ["134 with 1xDark"] * 1, #special calibration

    ["6SUBD Nominal #1"] * 2, 
    ["6SUBD Nominal #2"] * 2, 
    ["6SUBD Nominal #3"] * 2, 
    ["6SUBD CH4 #1"] * 1,
    ["All Fullscan Fast #2"] * 1,
    ["134 only #2"] * 1,
    ["136 only #2"] * 1,
    
    
]

        
OCCULTATION_GRAZING_KEYS = [
    ["6SUBD Nominal #1"] * 2, 
    ["6SUBD Nominal #2"] * 2, 
    ["6SUBD Nominal #3"] * 2, 
    ["6SUBD CH4 #1"] * 1,
    ["All Fullscan Fast #2"] * 1,
    ["134 only #2"] * 1,
    ["136 only #2"] * 1,
]

OCCULTATION_ACS_RIDEALONG_KEYS = [
    ["ACS Ridealong Science 2SUBD 01"] * 1,
]




OCCULTATION_CH4_REGION_KEYS = [
    ["134 only #2"] * 1, 
    ["136 only #2"] * 3, 
    ["6SUBD CH4 #1"] * 1,
]


OCCULTATION_H2O_REGION_KEYS = [
    ["6SUBD Nominal #1"] * 3, 
    ["6SUBD Nominal #2"] * 1, 
    ["6SUBD Nominal #3"] * 1, 
]

        
#IN GENERAL, USE LESS CH4 ORDERS AS THESE ARE NORMALLY ADDED WHEN CROSSING OVER INTERESTING REGIONS
NADIR_KEYS = [
#        ["LNO Ice Index 2SUBD 01"] * 1, #MTP013+ F.SCHMIDT
#        ["H2O 2SUBD 01"] * 1, #167 & 169
#        ["HDO H2O 2SUBD 02"] * 1, #168 & 124 S.AOKI
#        ["AER H2Oi 3SUBD 01"] * 1, #127, 131, 169 AEROSOLS
#        ["CH4 3SUBD 01"] * 1, #134, 136, 168
#        ["HDO H2O 2SUBD 03"] * 1, #121 & 168 
#        ["Nominal 6SUBD 01"] * 1, #6 ORDERS DUST
#        ["H2O CO 2SUBD 01"] * 1, #168, 190
#        ["CO H2O 3SUBD 01"] * 1, #191, 190, 168
#        ["CH4 2SUBD 03"] * 1, #136 x 2
#        ["Nominal 4SUBD 01"] * 1, #121, 134, 168, 190

    ["Nominal 6SUBD 01"] * 10,
    ["Nominal 4SUBD 01"] * 10,
    ["Nominal 3SUBD 01"] * 10,
    ["H2O 2SUBD 01"] * 6,
    ["H2O CO 2SUBD 01"] * 6,
    ["CO H2O 3SUBD 01"] * 6,

    ["HDO CO 3SUBD 02"] * 4,
    ["CH4 3SUBD 01"] * 4,
    ["CH4 H2O 2SUBD 02"] * 4,
    ["CH4 H2O 2SUBD 01"] * 4,
    ["CH4 2SUBD 03"] * 4,
    ["CH4 2SUBD 02"] * 4,
    ["CH4 CO 2SUBD 01"] * 4,
    ["CH4 CO 2SUBD 02"] * 4,
    ["HDO H2O 2SUBD 02"] * 4,
    ["HDO H2O 2SUBD 03"] * 4,
    ["CO Fullscan #2"] * 1,
    ["H2O Fullscan #2"] * 1,

    ["Ice CH4 2SUBD #1"] * 5,
    ["Ice H2O 2SUBD #1"] * 5,
    ["Ice CO 2SUBD #1"] * 5,

    ["Surface Ice 4SUBD 01"] * 1, #increase when beta angle high
    ["Surface Ice 6SUBD 01"] * 1,
    ["Surface Ice 4SUBD 02"] * 1,
    ["Surface Ice 3SUBD 01"] * 1,
     
]


        
#limb 3 and 4 are more important than the others
#ORDER 164 FOR LIMBS > 50KM, CONTINUE 163-165 COMBINATIONS FOR CASSIS LIMBS
NADIR_LIMB_KEYS = [
    ["Limb 2SUBD 07"] * 3,
    ["Nominal Limb 01"] * 1,
]

NADIR_NIGHT_LIMB_KEYS = [
    ["Limb 2SUBD 07"] * 3,
    ["Nominal Limb 01"] * 1,
]
        
NADIR_NIGHTSIDE_KEYS = [
    ["Limb 2SUBD 07"] * 1,
]

        
        
        
        
NADIR_CH4_REGION_KEYS = [
    ["CH4 3SUBD 01"] * 1,
    ["CH4 H2O 2SUBD 02"] * 2,
    ["CH4 H2O 2SUBD 01"] * 1,
    ["CH4 2SUBD 03"] * 2,
    ["CH4 2SUBD 02"] * 1,
    ["CH4 CO 2SUBD 01"] * 2,
    ["CH4 CO 2SUBD 02"] * 1,        
]        

NADIR_H2O_REGION_KEYS = [
    ["H2O 2SUBD 01"] * 4,        
    ["Nominal 3SUBD 01"] * 1,
]        
        

NADIR_SURFACE_REGION_KEYS = [
    ["Surface 3SUBD 02"] * 3,
    ["Nominal 3SUBD 01"] * 1,
]
    
observationCycles = {
        "OccultationCycleNominal":["Occultation", [item for sublist in OCCULTATION_KEYS for item in sublist]],
        "OccultationCycleMerged":["Occultation", [item for sublist in OCCULTATION_MERGED_KEYS for item in sublist]],
        "OccultationCycleGrazing":["Occultation", [item for sublist in OCCULTATION_GRAZING_KEYS for item in sublist]],

        "NadirCycleNominal":["Nadir", [item for sublist in NADIR_KEYS for item in sublist]],
        "NadirCycleLimb":["Nadir", [item for sublist in NADIR_LIMB_KEYS for item in sublist]],
        "NadirCycleNightside":["Nadir", [item for sublist in NADIR_NIGHTSIDE_KEYS for item in sublist]],
        "NadirCycleNightLimb":["Nadir", [item for sublist in NADIR_NIGHT_LIMB_KEYS for item in sublist]],

        "OccultationCycleCH4":["Occultation", [item for sublist in OCCULTATION_CH4_REGION_KEYS for item in sublist]],
        "OccultationCycleH2O":["Occultation", [item for sublist in OCCULTATION_H2O_REGION_KEYS for item in sublist]],
        "NadirCycleCH4":["Nadir", [item for sublist in NADIR_CH4_REGION_KEYS for item in sublist]],
        "NadirCycleH2O":["Nadir", [item for sublist in NADIR_H2O_REGION_KEYS for item in sublist]],
        "NadirCycleSurface":["Nadir", [item for sublist in NADIR_SURFACE_REGION_KEYS for item in sublist]],
}


        
        
        




"""list NOMAD ACS joint occultations"""
#for obsLists in SOC_JOINT_OBSERVATION_NAMES.values():
#    for obs in obsLists:
#        orders = occultationObservationDict[obs][0]
#        print ("%s;" %obs + " %i," * len(orders) % tuple(orders))



"""list observation cycles"""
#cycleName = "OccultationCycleNominal"
#cycleName = "NadirCycleNominal"
#cycleName = "NadirCycleCH4"
#
#obsNames = observationCycles[cycleName][1]
#
#uniqueObsNames = list(set(obsNames))
#uniqueObsData = [{"Occultation":occultationObservationDict, "Nadir":nadirObservationDict}[observationCycles[cycleName][0]][obsName] for obsName in uniqueObsNames]
#
#counts = []
#for uniqueObsName in uniqueObsNames:
#    counts.append(obsNames.count(uniqueObsName))
#
##sort by number of counts
#countsSorted = [x for x,_,_ in reversed(sorted(zip(counts,uniqueObsNames,uniqueObsData)))]
#uniqueObsNamesSorted = [x for _,x,_ in reversed(sorted(zip(counts,uniqueObsNames,uniqueObsData)))]
#uniqueObsDataSorted = [x for _,_,x in reversed(sorted(zip(counts,uniqueObsNames,uniqueObsData)))]
#
#totalCounts = sum(counts)
#print("Frequency,Name,Orders")
#for count, obsName, obsData in zip(countsSorted, uniqueObsNamesSorted, uniqueObsDataSorted):
#    print("%0.1f%%,%s,%s" %((count/totalCounts)*100.0, obsName, ("%s" %obsData[0]).replace("[","").replace("]","").replace(" ","")))
    
    
