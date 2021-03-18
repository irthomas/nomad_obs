# -*- coding: utf-8 -*-
"""
Created on Mon Apr 27 12:37:20 2020

@author: iant
"""



# import os
# import configparser
import decimal
import datetime
import sqlite3
# import re

from nomad_obs.config.constants import SPICE_DATETIME_FORMAT





def connect_db(db_path):
    print("Connecting to database %s" %db_path)
    con = sqlite3.connect(db_path)
    return con


def close_db(con):
    con.close()


def query(con, input_query):
    print(input_query)
    cur = con.cursor()
    
    c = cur.execute(input_query)
    con.commit()
    output = c.fetchall()
    return output


def new_table(table_name, table_fields):
    query_string = "CREATE TABLE %s (" %table_name
    for field in table_fields:
        query_string += "%s %s, " %(field["name"], field["type"])
    query_string = query_string[:-2]
    query_string += ")"
    print("Creating table %s" %table_name)
    return query_string


def empty_db(con, table_name, table_fields):
    """delete table and rebuild empty"""
    print("Deleting table")

    cur = con.cursor()
    
    cur.execute('DROP TABLE IF EXISTS %s' %table_name)
    create_table_string = new_table(table_name, table_fields)
    cur.execute(create_table_string)


def convert_table_datetimes(table_fields, table_rows):
    """convert all spice format strings to datetimes in preparation for writing sql"""
    table_fields_not_key_datetimes = [True if ("datetime" in field["type"]) or ("timestamp" in field["type"]) else False for field in table_fields if "primary" not in field.keys()]
    table_rows_datetime = []
    for table_row in table_rows:
        table_row_datetime = []
        for table_element, table_is_datetime in zip(table_row, table_fields_not_key_datetimes):
            if table_is_datetime and table_element != "-": #normal datetimes
                table_row_datetime.append(datetime.datetime.strptime(table_element, SPICE_DATETIME_FORMAT))
            elif table_element == "-": #any blank values in datetime or other
                table_row_datetime.append("NULL")
            else:
                table_row_datetime.append(table_element)
        table_rows_datetime.append(table_row_datetime)
    
    return table_rows_datetime


def read_table(con, table_name):
    query_string = "SELECT * FROM %s" %table_name
    table = query(con, query_string)

    new_table_data = []
    for row in table:
        new_table_data.append([float(element) if type(element) == decimal.Decimal else element for element in row])
    
    return new_table_data




def find_record_id(con, search_table_name, search_field, search_value, return_duplicates=False):
    
    query_str = "SELECT * FROM %s WHERE %s LIKE '%s'" %(search_table_name, search_field, search_value)
    found_record = query(con, query_str)
    if len(found_record) == 0:
        print("Warning: matching record not found for query %s" %query_str)
    elif len(found_record) > 1:
        print("Warning: multiple matching records found for query %s" %query_str)
        for each_found_record in found_record:
            print(each_found_record)
        found_record
        if return_duplicates:
            return [duplicate_found_record[0] for duplicate_found_record in found_record]
    else:
        found_record_id = found_record[0][0]

        return found_record_id
    
    
def update_row(con, table_name, existing_table_row_id, table_fields, new_row_data):
    
    table_fields_not_key = [field["name"] for field in table_fields if "primary" not in field.keys()]

    subquery = ""
    for table_field, new_row_value in zip(table_fields_not_key, new_row_data):
        subquery += "%s = '%s', " %(table_field, new_row_value)
    subquery = subquery[:-2]
    query_str = "UPDATE %s SET %s WHERE obs_id = %s" %(table_name, subquery, existing_table_row_id)
    query_str = query_str.replace("'NULL'", "NULL") #NULLs must not be surrounded by commas
    print(query_str)
    query(con, query_str)



def insert_rows(con, table_name, table_fields, table_rows, check_duplicates=False, duplicate_columns=[]):
    table_fields_not_key = [field["name"] for field in table_fields if "primary" not in field.keys()]
    if len(table_fields_not_key) != len(table_rows[0]):
        print("Error: Field names and data are not the same length")
        
    if check_duplicates: #check if any column value already exists. Use on datetimes primarily
        existing_table = read_table(con, table_name) 
        

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
            record_id = find_record_id(con, table_name, search_field_name, search_value)
            update_row(con, table_name, record_id, table_fields, table_row)

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
                elif type(table_element) == datetime.datetime: #datetimes must be written as strings
                    query_string += "\"%s\", " %table_element
                else: #values must not have inverted commas
                    query_string += "%s, " %table_element
            query_string = query_string[:-2]
            query_string += ")"
            query(con, query_string)




# def make_db():

# """sort through data and add it to empty sql db"""
# con = connect_db(SQLITE_PATH)
# empty_db(con, table_name, occultation_table_fields_sqlite)

# close_db(con)


