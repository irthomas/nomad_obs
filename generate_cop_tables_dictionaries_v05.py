# -*- coding: utf-8 -*-
"""
Created on Mon Aug 12 14:32:11 2019

@author: iant


COP TABLE DICTIONARIES
"""

MAX_EXECUTION_TIME = {1:850000, 2:1750000, 4:3600000, 8:7600000, 15:14600000} #us
MIN_EXECUTION_TIME = {1:700000, 2:1500000, 4:3200000, 8:7200000, 15:14200000} #us
MAX_ROWS = {"fixed":257, "stepping":257, "science":4097, "sub_domain":4097} #rows plus header

DIFFRACTION_ORDERS = {
        "so":[0] + list(range(110, 225)), 
        "lno":[0] + list(range(110, 205)),
        }


#channel steppingCode [orders, inttime, rhythm]
WINDOW_STEPPING_ROWS = {
        "so":{
                "WINDOW_STEPPING_2STEPS":[[120, 167, 190], 4000, 1],
                },
        "lno":{
                "WINDOW_STEPPING_2STEPS":[[120, 167, 190], 4000, 1],
                "WINDOW_STEPPING_7STEPS":[[120, 167, 190], 4000, 1],
                },
        }

#channel steppingCode [orders, nrows, inttime start, accumulations, rhythm]
INTEGRATION_TIME_STEPPING_ROWS = {
        "so":{
                "SOLAR_INTTIME_STEPPING":[[120, 167, 190], 24, 1, 1, 1],
                "DARK_INTTIME_STEPPING":[[120, 167, 190], 24, 1, 1, 4],
                },
        "lno":{
                "SOLAR_INTTIME_STEPPING":[[120, 167, 190], 24, 1, 1, 1],
                "DARK_INTTIME_STEPPING":[[120, 167, 190], 24, 1, 1, 4],
                },
        }





#channel, code [stepping pointer, value, parameter, count, speed]. step is 0 to 5
STEPPING_ROWS = {
            "so":{
                "EMPTY ROW":[0,0, "INTEGRATION_TIME", 0, 0],
                "WINDOW_STEPPING_2STEPS":[1,24, "WINDOW_TOP", 1, 0],

                "SOLAR_INTTIME_STEPPING":[3,100, "INTEGRATION_TIME", 255, 0], #100ms so
                "DARK_INTTIME_STEPPING":[4,3400, "INTEGRATION_TIME", 255, 0],
                "FULLSCAN_10ORDERS_1SUBDS":[5,1, "AOTF_IX", 10, 0],

                "FULLSCAN_10ORDERS_6SUBDS":[7,1, "AOTF_IX", 10, 5],

                "FULLSCAN_30ORDERS_1SUBDS":[8,1, "AOTF_IX", 30, 0],

                "FULLSCAN_30ORDERS_6SUBDS":[10,1, "AOTF_IX", 30, 5],

                "FULLSCAN_80ORDERS_1SUBDS":[11,1, "AOTF_IX", 80, 0],

                "FULLSCAN_80ORDERS_6SUBDS":[13,1, "AOTF_IX", 80, 5],

                "FULLSCAN_115ORDERS_1SUBDS":[14,1, "AOTF_IX", 115, 0], #115 orders so

                "FULLSCAN_115ORDERS_6SUBDS":[16,1, "AOTF_IX", 115, 5], #115 orders so

                "MINISCAN_1KHZ_1SUBDS":[17,53687, "AOTF_FREQ", 255, 0],
                "MINISCAN_1KHZ_6SUBDS":[18,53687, "AOTF_FREQ", 255, 5],
                "MINISCAN_2KHZ_1SUBDS":[19,107374, "AOTF_FREQ", 255, 0],
                "MINISCAN_2KHZ_6SUBDS":[20,107374, "AOTF_FREQ", 255, 5],
                "MINISCAN_4KHZ_1SUBDS":[21,214748, "AOTF_FREQ", 255, 0],
                "MINISCAN_4KHZ_6SUBDS":[22,214748, "AOTF_FREQ", 255, 5],
                "MINISCAN_8KHZ_1SUBDS":[23,429496, "AOTF_FREQ", 255, 0],
                "MINISCAN_8KHZ_6SUBDS":[24,429496, "AOTF_FREQ", 255, 5],
                },
            "lno":{
                "EMPTY ROW":[0,0, "INTEGRATION_TIME", 0, 0],
                "WINDOW_STEPPING_2STEPS":[1,24, "WINDOW_TOP", 1, 0],
                "WINDOW_STEPPING_7STEPS":[2,24, "WINDOW_TOP", 6, 0], #7 steps lno only
                "SOLAR_INTTIME_STEPPING":[3,50, "INTEGRATION_TIME", 255, 0], #50ms lno
                "DARK_INTTIME_STEPPING":[4,3400, "INTEGRATION_TIME", 255, 0],
                "FULLSCAN_10ORDERS_1SUBDS":[5,1, "AOTF_IX", 10, 0],
                "FULLSCAN_10ORDERS_3SUBDS":[6,1, "AOTF_IX", 10, 2], #lno nadir only
                "FULLSCAN_10ORDERS_6SUBDS":[7,1, "AOTF_IX", 10, 5],

                "FULLSCAN_30ORDERS_1SUBDS":[8,1, "AOTF_IX", 30, 0],
                "FULLSCAN_30ORDERS_3SUBDS":[9,1, "AOTF_IX", 30, 2], #lno nadir only
                "FULLSCAN_30ORDERS_6SUBDS":[10,1, "AOTF_IX", 30, 5],

                "FULLSCAN_80ORDERS_1SUBDS":[11,1, "AOTF_IX", 80, 0],
                "FULLSCAN_80ORDERS_3SUBDS":[12,1, "AOTF_IX", 80, 2], #lno nadir only
                "FULLSCAN_80ORDERS_6SUBDS":[13,1, "AOTF_IX", 80, 5],

                "FULLSCAN_105ORDERS_1SUBDS":[14,1, "AOTF_IX", 105, 0], #105 orders lno
                "FULLSCAN_105ORDERS_3SUBDS":[15,1, "AOTF_IX", 105, 2], #105 orders lno#lno nadir only
                "FULLSCAN_105ORDERS_6SUBDS":[16,1, "AOTF_IX", 105, 5], #105 orders lno

                "MINISCAN_1KHZ_1SUBDS":[17,53687, "AOTF_FREQ", 255, 0],
                "MINISCAN_1KHZ_6SUBDS":[18,53687, "AOTF_FREQ", 255, 5],
                "MINISCAN_2KHZ_1SUBDS":[19,107374, "AOTF_FREQ", 255, 0],
                "MINISCAN_2KHZ_6SUBDS":[20,107374, "AOTF_FREQ", 255, 5],
                "MINISCAN_4KHZ_1SUBDS":[21,214748, "AOTF_FREQ", 255, 0],
                "MINISCAN_4KHZ_6SUBDS":[22,214748, "AOTF_FREQ", 255, 5],
                "MINISCAN_8KHZ_1SUBDS":[23,429496, "AOTF_FREQ", 255, 0],
                "MINISCAN_8KHZ_6SUBDS":[24,429496, "AOTF_FREQ", 255, 5],
                },
            }
            



#channel nrows rhythm nsubd [step, inttime, comment]
MINISCAN_ROWS = {
        "so":{
                24:{
                        1:{
                                1:[[1,2,4,8], 4000, "OCCULTATION_MINISCAN_SLOW"],
                                6:[[1,2,4,8], 4000, "OCCULTATION_MINISCAN_FAST"],
                        },
                },
                16:{
                        1:{
                                6:[[1,2,4,8], 4000, "OCCULTATION_MINISCAN_FAST"],
                        },
                },
                20:{
                        1:{
                                6:[[1,2,4,8], 4000, "OCCULTATION_MINISCAN_FAST"],
                        },
                },
        },
        "lno":{
                24:{
                        1:{
                                1:[[1,2,4,8], 2000, "OCCULTATION_MINISCAN_SLOW"],
                                6:[[1,2,4,8], 2000, "OCCULTATION_MINISCAN_FAST"],
                        },
                },
#                144:{
#                        15:{
#                                1:[[1,2,4,8], 190000, "NADIR_MINISCAN_SLOW"],
#                                4:[[1,2,4,8], 195000, "NADIR_MINISCAN_FAST"],
#                        },
#                },
                16:{
                        1:{
                                6:[[1,2,4,8], 2000, "OCCULTATION_MINISCAN_FAST"],
                        },
                },
                20:{
                        1:{
                                6:[[1,2,4,8], 2000, "OCCULTATION_MINISCAN_FAST"],
                        },
                },
        },
}

#khzstep [starting orders]
MINISCAN_STARTING_ORDERS = {
        "so":{
                1:[105,107,120,126,130,134,141,142,146,151,156,162,164,166,167,168,169,171,172,178,180,182,188,191,194,196,197,199,201,210],
                2:list(range(110, 210, 3)),
                4:list(range(110, 210, 3)),
                8:list(range(110, 210, 6)),
                },
        "lno":{
                1:[105,107,120,126,130,134,141,142,146,151,156,162,164,166,167,168,169,171,172,178,180,182,188,191,194,196,197,199,201,210],
                2:list(range(110, 210, 3)),
                4:list(range(110, 210, 3)),
                8:list(range(110, 210, 6)),
                },
    }


#channel nrows stepspeed nsteps [starting orders, inttime, rhythm, comment]
FULLSCAN_ROWS = {
        "so":{
                24:{
                        1:{
                            10:[[115, 120, 125, 130, 135, 140, 145, 150, 155, 160, 165, 170, 175, 180, 185, 190], 4000, 1, "OCCULTATION_FULLSCAN_SLOW"],
                            30:[[110, 140, 170, 195], 4000, 1, "OCCULTATION_FULLSCAN_SLOW"],
                            80:[[115], 4000, 1, "OCCULTATION_FULLSCAN_SLOW"],
                            115:[[110], 4000, 1, "OCCULTATION_FULLSCAN_SLOW"],
                        },
                },
                16:{
                        6:{
                            10:[[115, 120, 125, 130, 135, 140, 145, 150, 155, 160, 165, 170, 175, 180, 185, 190], 4000, 1, "OCCULTATION_FULLSCAN_FAST"],
                            30:[[110, 140, 170, 195], 4000, 1, "OCCULTATION_FULLSCAN_FAST"],
                            80:[[115], 4000, 1, "OCCULTATION_FULLSCAN_FAST"],
                            115:[[110], 4000, 1, "OCCULTATION_FULLSCAN_FAST"],
                        },
                },
        },
        "lno":{
                24:{
                        1:{
                            10:[[115, 120, 125, 130, 135, 140, 145, 150, 155, 160, 165, 170, 175, 180, 185, 190], 2000, 1, "OCCULTATION_FULLSCAN_SLOW"],
                            30:[[110, 140, 170, 195], 2000, 1, "OCCULTATION_FULLSCAN_SLOW"],
                            80:[[115], 2000, 1, "OCCULTATION_FULLSCAN_SLOW"],
                            105:[[110], 2000, 1, "OCCULTATION_FULLSCAN_SLOW"],
                        },
                },
                16:{
                        6:{
                            10:[[115, 120, 125, 130, 135, 140, 145, 150, 155, 160, 165, 170, 175, 180, 185, 190], 2000, 1, "OCCULTATION_FULLSCAN_FAST"],
                            30:[[110, 140, 170, 195], 2000, 1, "OCCULTATION_FULLSCAN_FAST"],
                            80:[[115], 2000, 1, "OCCULTATION_FULLSCAN_FAST"],
                            105:[[110], 2000, 1, "OCCULTATION_FULLSCAN_FAST"],
                        },
                },
                144:{
                        1:{
                            10:[[115, 120, 125, 130, 135, 140, 145, 150, 155, 160, 165, 170, 175, 180, 185, 190], 190000, 15, "NADIR_FULLSCAN_SLOW"],
                            30:[[110, 140, 170, 195], 190000, 15, "NADIR_FULLSCAN_SLOW"],
                            80:[[115], 190000, 15, "NADIR_FULLSCAN_SLOW"],
                            105:[[110], 190000, 15, "NADIR_FULLSCAN_SLOW"],
                        },
                        3:{
                            10:[[115, 120, 125, 130, 135, 140, 145, 150, 155, 160, 165, 170, 175, 180, 185, 190], 205000, 15, "NADIR_FULLSCAN_FAST"],
                            30:[[110, 140, 170, 195], 205000, 15, "NADIR_FULLSCAN_FAST"],
                            80:[[115], 205000, 15, "NADIR_FULLSCAN_FAST"],
                            105:[[110], 205000, 15, "NADIR_FULLSCAN_FAST"],
                        },
                },
        },
}


#channel nrows rhythm [windowtops, comment]
DEFAULT_FIXED_ROWS = {
        "so":{
                12:{1:[[122], "DEFAULT_OCCULTATION"]},
                16:{1:[[120], "DEFAULT_OCCULTATION"]},
                20:{1:[[118], "DEFAULT_OCCULTATION"]},
                24:{1:[[116], "DEFAULT_CALIBRATION"]},
                },
        "lno":{
                144:{15:[[80], "DEFAULT_NADIR"]},
                16:{1:[[144], "DEFAULT_OCCULTATION"]},
                20:{1:[[142], "DEFAULT_OCCULTATION"]},
                24:{1:[[140], "DEFAULT_CALIBRATION"]},
                },
        }

#channel nrows rhythm [windowtops, comment]
FIXED_ROWS = {
        "so":{
                12:{
                        1:[[118, 119, 120, 121, 123, 124, 125, 126], "OCCULTATION"],
                        2:[[118, 119, 120, 121, 122, 123, 124, 125, 126], "OCCULTATION"],
                        4:[[118, 119, 120, 121, 122, 123, 124, 125, 126], "OCCULTATION"],
                        },
                16:{
                        1:[[116, 117, 118, 119, 121, 122, 123, 124], "OCCULTATION"],
                        2:[[116, 117, 118, 119, 120, 121, 122, 123, 124], "OCCULTATION"],
                        4:[[116, 117, 118, 119, 120, 121, 122, 123, 124], "OCCULTATION"],
                        },
                20:{
                        1:[[114, 115, 116, 117, 119, 120, 121, 122], "OCCULTATION"],
                        2:[[114, 115, 116, 117, 118, 119, 120, 121, 122], "OCCULTATION"],
                        4:[[114, 115, 116, 117, 118, 119, 120, 121, 122], "OCCULTATION"],
                        },
                24:{
                        1:[[104, 
                            112, 113, 114, 115, 117, 118, 119, 120], "CALIBRATION"],
                        2:[[112, 113, 114, 115, 116, 117, 118, 119, 120], "CALIBRATION"],
                        4:[[112, 113, 114, 115, 116, 117, 118, 119, 120], "CALIBRATION"],
                        },
                },
        "lno":{
                144:{
                        4:[[76, 77, 78, 79, 80, 81, 82, 83, 84], "NADIR"],
                        8:[[76, 77, 78, 79, 80, 81, 82, 83, 84], "NADIR"],
                        15:[[76, 77, 78, 79, 81, 82, 83, 84], "NADIR"],
                        },
                72:{
                        4:[[112, 113, 114, 115, 116, 117, 118, 119, 120], "NADIR"],
                        8:[[112, 113, 114, 115, 116, 117, 118, 119, 120], "NADIR"],
                        15:[[112, 113, 114, 115, 116, 117, 118, 119, 120], "NADIR"],
                        },
                16:{
                        1:[[140, 141, 142, 143, 145, 146, 147, 148], "OCCULTATION"],
                        2:[[140, 141, 142, 143, 144, 145, 146, 147, 148], "OCCULTATION"],
                        4:[[140, 141, 142, 143, 144, 145, 146, 147, 148], "OCCULTATION"],
                        },
                20:{
                        1:[[138, 139, 140, 141, 143, 144, 145, 146], "OCCULTATION"],
                        2:[[138, 139, 140, 141, 142, 143, 144, 145, 146], "OCCULTATION"],
                        4:[[138, 139, 140, 141, 142, 143, 144, 145, 146], "OCCULTATION"],
                        },
                24:{
                        1:[[68, 128,
                            136, 137, 138, 139, 141, 142, 143, 144], "CALIBRATION"],
                        2:[[136, 137, 138, 139, 140, 141, 142, 143, 144], "CALIBRATION"],
                        4:[[136, 137, 138, 139, 140, 141, 142, 143, 144], "CALIBRATION"],
                        },
                },
        }





#channel nrows rhythm nsubd [inttimes, orders, sbsfs, comment]
SCIENCE_ROWS = {
        "so":{
                12:{
                        1:{
                                6:[[2000, 4000], DIFFRACTION_ORDERS["so"], [0, 1], "OCCULTATION"],
                                },
                        2:{
                                6:[[2000, 4000], DIFFRACTION_ORDERS["so"], [0, 1], "OCCULTATION"],
                                },
                        },
                16:{
                        1:{
                                6:[[2000, 4000], DIFFRACTION_ORDERS["so"], [0, 1], "OCCULTATION"],
                                },
                        2:{
                                6:[[2000, 4000], DIFFRACTION_ORDERS["so"], [0, 1], "OCCULTATION"],
                                },
                        },
                20:{
                        1:{
                                6:[[2000, 4000], DIFFRACTION_ORDERS["so"], [0, 1], "OCCULTATION"],
                                },
                        2:{
                                6:[[4000], DIFFRACTION_ORDERS["so"], [0, 1], "OCCULTATION"],
                                },
                        4:{
                                6:[[10000,20000], [121,134,149,165,168,190], [1], "OCCULTATION"],
                                },
                        },
                24:{
                        1:{
                                1:[[2000, 4000], DIFFRACTION_ORDERS["so"], [0, 1], "OCCULTATION"],
                                },
                        4:{
                                1:[[40000], DIFFRACTION_ORDERS["so"], [0, 1], "OCCULTATION"],
                                2:[[40000], DIFFRACTION_ORDERS["so"], [0, 1], "OCCULTATION"],
                                },
                        },
        },
        "lno":{
                16:{
                        1:{
                                6:[[2000], DIFFRACTION_ORDERS["lno"], [0, 1], "OCCULTATION"],
                                },
                        },
                20:{
                        1:{
                                6:[[2000], DIFFRACTION_ORDERS["lno"], [0, 1], "OCCULTATION"],
                                },
                        },
                24:{
                        1:{
                                1:[[2000], DIFFRACTION_ORDERS["lno"], [0, 1], "OCCULTATION"],
                                },
                        },
                144:{
                        4:{
                                2:[[205000], DIFFRACTION_ORDERS["lno"], [1], "NADIR"],
                                },
                        8:{
                                3:[[180000], DIFFRACTION_ORDERS["lno"], [1], "NADIR"],
                                4:[[220000], DIFFRACTION_ORDERS["lno"], [1], "NADIR"],
                                6:[[205000], DIFFRACTION_ORDERS["lno"], [1], "NADIR"],
                                },
                        15:{
                                1:[[50000,100000,190000,390000], DIFFRACTION_ORDERS["lno"], [1], "NADIR"],
                                2:[[50000,100000,200000,380000], DIFFRACTION_ORDERS["lno"], [1], "NADIR"],
                                3:[[60000,100000,205000], DIFFRACTION_ORDERS["lno"], [1], "NADIR"],
                                4:[[50000,110000,195000], DIFFRACTION_ORDERS["lno"], [1], "NADIR"],
                                6:[[50000,95000,220000], DIFFRACTION_ORDERS["lno"], [1], "NADIR"],
                                },
                        },
                72:{
                        15:{
                                1:[[205000], DIFFRACTION_ORDERS["lno"], [1], "NADIR"],
                                2:[[195000], DIFFRACTION_ORDERS["lno"], [1], "NADIR"],
                                3:[[205000], DIFFRACTION_ORDERS["lno"], [1], "NADIR"],
                                4:[[50000,110000,190000], DIFFRACTION_ORDERS["lno"], [1], "NADIR"],
                                6:[[195000], DIFFRACTION_ORDERS["lno"], [1], "NADIR"],
                                },
                        },
        },
}





#channel nrows rhythm nsubd [inttimes]
SUBDOMAIN_SCIENCE_ROWS = {
        "so":{
                12:{
                        1:{
                                6:[2000,4000],
                        },
                },
                16:{
                        1:{
                                6:[4000],
                        },
                },
                20:{
                        1:{
                                6:[2000,4000],
                        },
                },
                24:{
                        1:{
                                1:[2000,4000],
                        },
                        4:{
                                2:[40000],
                        },
                },
        },
        "lno":{
                16:{
                        1:{
                                6:[2000],
                        },
                },
                144:{
#                        4:{
#                                2:[205000],
#                        },
#                        8:{
#                                3:[180000],
#                                4:[220000],
#                                6:[205000],
#                        },
                        15:{
                                1:[100000,190000,390000],
                                2:[50000,100000,200000,380000],
                                3:[60000,100000,205000],
                                4:[110000,195000],
                                6:[220000],
#                                1:[100000,190000,390000],
#                                2:[50000,100000,200000,380000],
#                                3:[60000,100000,205000],
#                                4:[50000,110000,195000],
#                                6:[95000,220000],
                        },
                },
#                72:{
#                        15:{
#                                1:{1:[120000,205000]},
#                                2:{1:[95000,195000]},
#                                3:[100000,205000],
#                                4:{1:[50000,110000,190000]},
#                                6:{1:[45000,90000,195000]},
#                                },
#                        },
        }
}





