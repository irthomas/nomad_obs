# -*- coding: utf-8 -*-
"""
Created on Wed Mar 17 10:47:54 2021

@author: iant

SQL TABLE AND FIELD INFO
"""


occultation_table_fields = [
        {"name":"obs_id", "type":"int NOT NULL AUTO_INCREMENT", "primary":True}, \
        {"name":"prime_instrument", "type":"varchar(100) NOT NULL"}, \
        {"name":"orbit_number", "type":"int NOT NULL"}, \
        {"name":"occultation_type", "type":"varchar(100) NOT NULL"}, \
        {"name":"utc_start_time", "type":"datetime NOT NULL"}, \
        {"name":"utc_transition_time", "type":"datetime NULL DEFAULT NULL"}, \
        {"name":"utc_end_time", "type":"datetime NOT NULL"}, \
        {"name":"duration", "type":"decimal NOT NULL"}, \
        
        {"name":"start_longitude", "type":"decimal NOT NULL"}, \
        {"name":"transition_longitude", "type":"decimal NULL DEFAULT NULL"}, \
        {"name":"end_longitude", "type":"decimal NOT NULL"}, \

        {"name":"start_latitude", "type":"decimal NOT NULL"}, \
        {"name":"transition_latitude", "type":"decimal NULL DEFAULT NULL"}, \
        {"name":"end_latitude", "type":"decimal NOT NULL"}, \

        {"name":"transition_local_time", "type":"decimal NULL DEFAULT NULL"}, \
        
        {"name":"orbit_type", "type":"int NOT NULL"}, \
        {"name":"ir_observation_name", "type":"varchar(100) NULL DEFAULT NULL"}, \
        {"name":"ir_description", "type":"varchar(1000) NULL DEFAULT NULL"}, \
        {"name":"uvis_description", "type":"varchar(1000) NULL DEFAULT NULL"}, \
        {"name":"orbit_comment", "type":"varchar(1000) NULL DEFAULT NULL"}, \
]

occultation_table_fields_sqlite = [
        {"name":"obs_id", "type":"INTEGER PRIMARY KEY AUTOINCREMENT", "primary":True}, \
        {"name":"prime_instrument", "type":"TEXT NOT NULL"}, \
        {"name":"orbit_number", "type":"INT NOT NULL"}, \
        {"name":"occultation_type", "type":"TEXT NOT NULL"}, \
        {"name":"utc_start_time", "type":"TIMESTAMP NOT NULL"}, \
        {"name":"utc_transition_time", "type":"TIMESTAMP NULL DEFAULT NULL"}, \
        {"name":"utc_end_time", "type":"TIMESTAMP NOT NULL"}, \
        {"name":"duration", "type":"REAL NOT NULL"}, \
        
        {"name":"start_longitude", "type":"REAL NOT NULL"}, \
        {"name":"transition_longitude", "type":"REAL NULL DEFAULT NULL"}, \
        {"name":"end_longitude", "type":"REAL NOT NULL"}, \

        {"name":"start_latitude", "type":"REAL NOT NULL"}, \
        {"name":"transition_latitude", "type":"REAL NULL DEFAULT NULL"}, \
        {"name":"end_latitude", "type":"REAL NOT NULL"}, \

        {"name":"transition_local_time", "type":"REAL NULL DEFAULT NULL"}, \
        
        {"name":"orbit_type", "type":"INT NOT NULL"}, \
        {"name":"ir_observation_name", "type":"TEXT NULL DEFAULT NULL"}, \
        {"name":"ir_description", "type":"TEXT NULL DEFAULT NULL"}, \
        {"name":"uvis_description", "type":"TEXT NULL DEFAULT NULL"}, \
        {"name":"orbit_comment", "type":"TEXT NULL DEFAULT NULL"}, \
]


nadir_table_fields = [
        {"name":"obs_id", "type":"int NOT NULL AUTO_INCREMENT", "primary":True}, \
        {"name":"orbit_number", "type":"int NOT NULL"}, \
        {"name":"nadir_type", "type":"varchar(100) NOT NULL"}, \
        {"name":"utc_start_time", "type":"datetime NOT NULL"}, \
        {"name":"utc_centre_time", "type":"datetime NOT NULL"}, \
        {"name":"utc_end_time", "type":"datetime NOT NULL"}, \
        {"name":"duration", "type":"decimal NOT NULL"}, \
        
        {"name":"start_longitude", "type":"decimal NOT NULL"}, \
        {"name":"centre_longitude", "type":"decimal NOT NULL"}, \
        {"name":"end_longitude", "type":"decimal NOT NULL"}, \

        {"name":"start_latitude", "type":"decimal NOT NULL"}, \
        {"name":"centre_latitude", "type":"decimal NOT NULL"}, \
        {"name":"end_latitude", "type":"decimal NOT NULL"}, \

        {"name":"centre_incidence_angle", "type":"decimal NOT NULL"}, \
        {"name":"centre_local_time", "type":"decimal NOT NULL"}, \
        
        {"name":"orbit_type", "type":"int NOT NULL"}, \
        {"name":"ir_observation_name", "type":"varchar(100) NULL DEFAULT NULL"}, \
        {"name":"ir_description", "type":"varchar(1000) NULL DEFAULT NULL"}, \
        {"name":"uvis_description", "type":"varchar(1000) NULL DEFAULT NULL"}, \
        {"name":"orbit_comment", "type":"varchar(1000) NULL DEFAULT NULL"}, \
        ]

    

nadir_table_fields_sqlite = [
        {"name":"obs_id", "type":"INTEGER PRIMARY KEY AUTOINCREMENT", "primary":True}, \
        {"name":"orbit_number", "type":"INT NOT NULL"}, \
        {"name":"nadir_type", "type":"TEXT NOT NULL"}, \
        {"name":"utc_start_time", "type":"TIMESTAMP NOT NULL"}, \
        {"name":"utc_centre_time", "type":"TIMESTAMP NOT NULL"}, \
        {"name":"utc_end_time", "type":"TIMESTAMP NOT NULL"}, \
        {"name":"duration", "type":"REAL NOT NULL"}, \
        
        {"name":"start_longitude", "type":"REAL NOT NULL"}, \
        {"name":"centre_longitude", "type":"REAL NOT NULL"}, \
        {"name":"end_longitude", "type":"REAL NOT NULL"}, \

        {"name":"start_latitude", "type":"REAL NOT NULL"}, \
        {"name":"centre_latitude", "type":"REAL NOT NULL"}, \
        {"name":"end_latitude", "type":"REAL NOT NULL"}, \

        {"name":"centre_incidence_angle", "type":"REAL NOT NULL"}, \
        {"name":"centre_local_time", "type":"REAL NOT NULL"}, \
        
        {"name":"orbit_type", "type":"INT NOT NULL"}, \
        {"name":"ir_observation_name", "type":"TEXT NULL DEFAULT NULL"}, \
        {"name":"ir_description", "type":"TEXT NULL DEFAULT NULL"}, \
        {"name":"uvis_description", "type":"TEXT NULL DEFAULT NULL"}, \
        {"name":"orbit_comment", "type":"TEXT NULL DEFAULT NULL"}, \
        ]

    

