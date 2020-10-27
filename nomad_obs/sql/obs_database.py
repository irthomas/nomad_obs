# -*- coding: utf-8 -*-
"""
Created on Mon Apr 27 12:37:20 2020

@author: iant
"""



import os
import configparser
import decimal
from datetime import datetime


from nomad_obs.config.constants import SPICE_DATETIME_FORMAT
from nomad_obs.config.python_version import python_version

#no mysqldb in py3.8
if python_version() >= 3.8:
    CONNECTOR = True
    import mysql.connector
else:    
    CONNECTOR = False
    import MySQLdb



class obsDB(object):
    def connect(self):
        
        if self.server == "BIRA":
            
            config = configparser.ConfigParser()
            config.read(os.path.join(self.paths["SQL_INI_PATH"], "nomad_db.ini"))
            host = config["data_db"]["host"].strip('"')
            user = config["data_db"]["user"].strip('"')
            passwd = config["data_db"]["password"].strip('"')
            dbname = config["data_db"]["database"].strip('"')

        #for testing at home
        elif self.server == "Home":
            host = "localhost"
            user = "root"
            passwd = ""
            dbname = self.dbname

        print("Connecting to database %s" %host)
        if CONNECTOR:
            self.db = mysql.connector.connect(user=user, password=passwd, host=host, database=dbname)
        else:
            self.db = MySQLdb.connect(host=host, user=user, passwd=passwd, db=dbname)
        
    def __init__(self, paths, server="BIRA", dbname=""):
        self.paths = paths
        self.server = server
        self.dbname = dbname
        self.connect()
        self.cursor = self.db.cursor()

    def close(self):
        print("Disconnecting from mysql database")
        self.cursor.close()
        self.db.close()
        

    def query(self, input_query):
        self.cursor.execute((input_query))
        
        if CONNECTOR:
            try:
                output = self.cursor.fetchall()
            except mysql.connector.InterfaceError:
                output = ""
        else:
            output = self.cursor.fetchall()

        return output


    def read_table(self, table_name):
        query_string = "SELECT * FROM %s" %table_name
        table = self.query(query_string)

        new_table = []
        for row in table:
            new_table.append([float(element) if type(element) == decimal.Decimal else element for element in row])
        
        return new_table
    
    def convert_table_datetimes(self, table_fields, table_rows):
        """convert all spice format strings to datetimes in preparation for writing sql"""
        table_fields_not_key_datetimes = [True if "datetime" in field["type"] else False for field in table_fields if "primary" not in field.keys()]
        table_rows_datetime = []
        for table_row in table_rows:
            table_row_datetime = []
            for table_element, table_is_datetime in zip(table_row, table_fields_not_key_datetimes):
                if table_is_datetime and table_element != "-": #normal datetimes
                    table_row_datetime.append(datetime.strptime(table_element, SPICE_DATETIME_FORMAT))
                elif table_element == "-": #any blank values in datetime or other
                    table_row_datetime.append("NULL")
                else:
                    table_row_datetime.append(table_element)
            table_rows_datetime.append(table_row_datetime)
        
        return table_rows_datetime
    
    #column_names = db_obj.query("SELECT * FROM information_schema.columns WHERE table_name = 'nomad_nadirs'")
    #copy table: db_obj.query("CREATE TABLE nomad_nadirs2 LIKE nomad_nadirs"); db_obj.query("INSERT nomad_nadirs2 SELECT * FROM nomad_nadirs")
    
    def find_record_id(self, search_table_name, search_field, search_value, return_duplicates=False):
        
        query = "SELECT * FROM %s WHERE %s LIKE '%s'" %(search_table_name, search_field, search_value)
        found_record = self.query(query)
        if len(found_record) == 0:
            print("Warning: matching record not found for query %s" %query)
        elif len(found_record) > 1:
            print("Warning: multiple matching records found for query %s" %query)
            for each_found_record in found_record:
                print(each_found_record)
            found_record
            if return_duplicates:
                return [duplicate_found_record[0] for duplicate_found_record in found_record]
        else:
            found_record_id = found_record[0][0]

            return found_record_id
        
    def update_row(self, table_name, existing_table_row_id, table_fields, new_row_data):
        
        table_fields_not_key = [field["name"] for field in table_fields if "primary" not in field.keys()]

        subquery = ""
        for table_field, new_row_value in zip(table_fields_not_key, new_row_data):
            subquery += "%s = '%s', " %(table_field, new_row_value)
        subquery = subquery[:-2]
        query = "UPDATE %s SET %s WHERE obs_id = %s" %(table_name, subquery, existing_table_row_id)
        query = query.replace("'NULL'", "NULL") #NULLs must not be surrounded by commas
        print(query)
        self.query(query)
        
    def delete_duplicates(self, table_name):
        
        existing_table = self.read_table(table_name)
        utc_start_times = [value[4] for value in existing_table]
        
        for utc_start_time in utc_start_times:
            duplicate_record_ids = self.find_record_id(table_name, "utc_start_time", utc_start_time, return_duplicates=True)
            
            if not type(duplicate_record_ids) == int: #if more than one record found:
                for duplicate_record_id in duplicate_record_ids[:-1]:
                    query = "DELETE FROM %s WHERE obs_id = %s" %(table_name, duplicate_record_id)
                    print(query)
                    self.query(query)
                    
    
    def insert_rows(self, table_name, table_fields, table_rows, check_duplicates=False, duplicate_columns=[]):
        table_fields_not_key = [field["name"] for field in table_fields if "primary" not in field.keys()]
        if len(table_fields_not_key) != len(table_rows[0]):
            print("Error: Field names and data are not the same length")
            
        if check_duplicates: #check if any column value already exists. Use on datetimes primarily
            existing_table = self.read_table(table_name) 
            

        print("Inserting %i rows into table %s" %(len(table_rows), table_name))
        #loop through new rows
        for row_index, table_row in enumerate(table_rows):
            duplicates = 0
            if check_duplicates:
                for existing_row in existing_table: #loop through existing rows
                    for column_number in duplicate_columns: #loop through specific columns
                        if table_row[column_number] == existing_row[column_number+1]:
                            duplicates += 1
                            
            if duplicates > 0:
                print("Row %i contains elements matching existing rows. Updating" %row_index)
                
                search_field_name = "utc_start_time"
                #find index of search field name in 
                search_field_index = [index for index, table_field in enumerate(table_fields_not_key) if table_field == search_field_name][0]
                search_value = table_row[search_field_index]
                record_id = self.find_record_id(table_name, search_field_name, search_value)
                self.update_row(table_name, record_id, table_fields, table_row)

            else:
                query_string = "INSERT INTO %s (" %table_name
                for table_field in table_fields_not_key:
                    query_string += "%s, " %table_field
                query_string = query_string[:-2]
                query_string += ") VALUES ("
                for table_element in table_row:
                    if type(table_element) == str:
                        if table_element == "NULL":
                            query_string += "%s, " %table_element #nulls must not have inverted commas
                        else:
                            query_string += "\"%s\", " %table_element #other strings must have inverted commas
                    elif type(table_element) == datetime: #datetimes must be written as strings
                        query_string += "\"%s\", " %table_element
                    else: #values must not have inverted commas
                        query_string += "%s, " %table_element
                query_string = query_string[:-2]
                query_string += ")"
                self.query(query_string)

    def new_table(self, table_name, table_fields):
        table_not_key = []
        for field in table_fields:
            if "primary" in field.keys():
                table_key = field["name"]
            else:
                table_not_key.append(field["name"])
        
        query_string = "CREATE TABLE %s" %table_name + "(%s INT NOT NULL AUTO_INCREMENT" %table_key + ", PRIMARY KEY (%s), " %table_key
        for field in table_fields:
            if field["name"] != table_key:
                query_string += "%s %s, " %(field["name"], field["type"])
        query_string = query_string[:-2]
        query_string += ")"

        print("Creating table %s" %table_name)
        self.query(query_string)
    
    def drop_table(self, table_name):
        query_string = "DROP TABLE IF EXISTS %s" %table_name
        print("Dropping table %s" %table_name)
        self.query(query_string)
        


