#!/usr/bin/env python
# coding: utf-8

import pyodbc
import os
import sys
from datetime import datetime


def connect_sql():
    server = 'tcp:<IP address MS SQL server>'
    cnxn = pyodbc.connect('DRIVER={SQL Server};SERVER=%s;DATABASE=<nameBD>;UID=<login>;PWD=<password>'%server)
    return cnxn

def rename_table(new_t, old_t):
    
    query_rename = 'sp_rename %s , %s;' % (old_t, new_t)
    cnxn = connect_sql()
    cursor = cnxn.cursor()
    cursor.execute(query_rename)
    cursor.commit()
    cursor.close()
    cnxn.close() 

def del_table(table):
    
    name_table = '[dbo].['+table+']'
    
    drop_query = "DROP TABLE if exists %s" %table
    cnxn = connect_sql()
    cursor = cnxn.cursor()
    cursor.execute(drop_query)
    cursor.commit()
    cursor.close()
    cnxn.close() 

#filling the table for sending to dropbox
def fill_table_dbx(new_t, old_t, dbx_t):
    
    cnxn = connect_sql()
    cursor = cnxn.cursor()
    query_diff = 'SELECT source, destination, name, date_create, date_modify, send FROM %s EXCEPT SELECT source, destination, name, date_create, date_modify, send FROM %s' % (new_t,old_t)
    cursor.execute(query_diff)
    result_forDBX = cursor.fetchall()
    query_exp = "INSERT INTO %s (source, destination, name, date_create, date_modify, send ) VALUES (?,?,?,?,?,?)" %dbx_t
    cursor.executemany(query_exp, result_forDBX)
    cursor.commit()
    
    cursor.close()
    cnxn.close() 

def check_empty_table(table):
    
    
    try:
        cnxn = connect_sql()
        cnxn.timeout = 5
        cursor = cnxn.cursor()
        cursor.execute( "IF OBJECT_ID ('{0}') IS NOT NULL SELECT COUNT(*) from {1}".format(table,table)   )        
        count=cursor.fetchall()
        cursor.close()
        cnxn.close() 
    except:
        return -1 #table does not exist
    
    return count[0][0]


def del_row(id_t, table):
    
    cnxn = connect_sql()
    cursor = cnxn.cursor()
    cursor.execute('DELETE FROM %s WHERE id = %s' % (table, id_t)  )
    cursor.commit()
    cursor.close()
    cnxn.close() 