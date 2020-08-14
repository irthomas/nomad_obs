# -*- coding: utf-8 -*-
# pylint: disable=E1103
# pylint: disable=C0301
"""
Created on Wed Oct 18 13:56:09 2017

@author: iant


   #add Surface Ice obs to final orbit plan when beta angle is high
   #replace 191 and most 190 obs by 189!

"""


__project__   = "NOMAD Observation Planning"
__author__    = "Ian Thomas"
__contact__   = "ian . thomas AT aeronomie . be"






"""make the observation dictionaries of all the desired measurement types
DON'T MODIFY OR DELETE ANY OBSERVATIONS - JUST ADD NEW ONES"""
#name:[[orders], int time, rhythm, lines, so=0/lno=1]
occultationObservationDict = {
        
#new MTP031+
"HCL #4":[[121, 134, 129, 129, 129, 129], 4, 1, 16, 0],
"HCL #5":[[121, 134, 130, 130, 130, 130], 4, 1, 16, 0],
"HCL #8":[[121, 136, 129, 129, 129, 129], 4, 1, 16, 0],
"HCL #9":[[121, 136, 130, 130, 130, 130], 4, 1, 16, 0],
"HCL #10":[[121, 134, 126, 127, 129, 130], 4, 1, 16, 0],
"HCL #11":[[121, 136, 126, 127, 129, 130], 4, 1, 16, 0],

"6SUBD Nominal #42":[[121, 134, 169, 129, 149, 165], 4, 1, 16, 0],
"6SUBD Nominal #45":[[121, 136, 169, 129, 149, 165], 4, 1, 16, 0],
"6SUBD Nominal #48":[[121, 134, 129, 169, 186, 190], 4, 1, 16, 0],
"6SUBD Nominal #51":[[121, 136, 129, 169, 186, 190], 4, 1, 16, 0],
"6SUBD Nominal #11":[[121, 134, 126, 129, 169, 190], 4, 1, 16, 0],
"6SUBD Nominal #12":[[121, 134, 127, 129, 169, 190], 4, 1, 16, 0],
       
        
         

        
        
#new MTP025+
"6SUBD CO2 #1":[[156,116,118,140,154,158], 4, 1, 16, 0],
"6SUBD CO2 #10":[[156,116,118,169,154,158], 4, 1, 16, 0],
"6SUBD CO2 Dipole #1":[[132, 133, 134, 136, 137, 169], 4, 1, 16, 0],

        
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


"CO2 Fullscan Fast #2":[["COP#41"], 4, 1, 16, 0], #160-170
"CO2 Fullscan Fast #3":[["COP#34"], 4, 1, 16, 0], #125-135
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

"Surface 3SUBD 02":[[191,194,196], 205, 15, 144, 1], #USE FOR F.ALTIERI NADIR TARGETS MTP010-030



#More 189 orders for CO
"H2O CO 3SUBD #2":[[168,189,190], 205, 15, 144, 1], #MTP031+
"H2O CO 2SUBD #1":[[168,189], 200, 15, 144, 1], #GOOD
"CH4 CO 2SUBD #3":[[189,136], 200, 15, 144, 1], #MTP031+
"CH4 CO 2SUBD #4":[[189,134], 200, 15, 144, 1], #MTP031+
"Surface 3SUBD #3":[[189,194,196], 205, 15, 144, 1], #MTP031+. USE FOR F.ALTIERI NADIR TARGETS MTP010+ (NOW WITH 189)
"Ice CO 2SUBD #2":[[193,189], 200, 15, 144, 1], #MTP031+

"Nominal 6SUBD #2":[[196,189,168,149,134,121], 220, 15, 144, 1], #GOOD
"Nominal 4SUBD #2":[[168,134,121,189], 195, 15, 144, 1], #GOOD

#OH Meinel Bands
"Night Limb #1":[[158,153], 200, 15, 144, 1], #SUBOPTIMAL BUT ORDER 158 ONLY DOESN'T EXIST YET
"Night Limb #2":[[158,158], 200, 15, 144, 1], #NEEDS PATCH




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

    

    











