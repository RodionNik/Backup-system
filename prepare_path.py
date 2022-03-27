#!/usr/bin/env python
# coding: utf-8

import os
import sys
import win32api

import pyodbc
from datetime import datetime

#Пути к файлам
list_copy = r'C:\Python\Data\DbBackUp\list_copy.txt'

dir_backup = {}
for line in open(list_copy,'r'):
    key = win32api.GetShortPathName( line.split(':')[0] )
    item = line.split(':')[1]
    clear_label = line.split(':')[2]
    dir_backup[key] = [ item, clear_label ]



#function connect_sql() described in bdsql_operation.py file
def fill_table(src, dst, table):
    
    cnxn = connect_sql()
    cursor = cnxn.cursor()
    query = "INSERT INTO %s (source, destination, name, date_create, date_modify, send ) VALUES (?,?,?,?,?,?)" %table
    
    for (directoris, sub, files) in os.walk(src):
        
        for file in files:
            
            try:
                patch = os.path.join  ( win32api.GetShortPathName(directoris),file )
            except:
                print(file,"не найден в функции fill_table")
                continue
            
            try:
                data_triple = (
                    src,   #источник
                    dst,   #путь dbx
                    patch, #путь к файлу
                    os.path.getctime(patch), 
                    os.path.getmtime(patch),
                    0 )
            except:
                continue
            
               
            
            cursor.execute(query,data_triple)
    
    cursor.commit()
    cursor.close()
    cnxn.close()


for key, item in dir_backup.items():
        sourse = key 
        rezult = item[0] 
        fill_table(sourse, rezult, 'table')






