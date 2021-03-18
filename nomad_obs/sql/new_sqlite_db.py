# -*- coding: utf-8 -*-
"""
Created on Thu Mar 18 10:37:44 2021

@author: iant

CODE TO MAKE EMPTY OBS.DB SQLITE DATABASE
"""


"""code to make empty db. Load kernels first"""
from nomad_obs.config.paths import SQLITE_PATH
from nomad_obs.sql.obs_database_sqlite import connect_db, close_db, empty_db
from nomad_obs.sql.db_fields import occultation_table_fields_sqlite
from nomad_obs.sql.db_fields import nadir_table_fields_sqlite


con = connect_db(SQLITE_PATH)
empty_db(con, "occultations", occultation_table_fields_sqlite)
empty_db(con, "nadirs", nadir_table_fields_sqlite)
close_db(con)

