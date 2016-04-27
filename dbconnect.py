#!/usr/bin/python
# -*- coding: utf-8 -*-

# DOCS @ http://mysql-python.sourceforge.net/MySQLdb.html#mysqldb
import MySQLdb
import csv
import gc

class SQLTable():
    def __init__(self, tabell):
        
        self.host = 'eviate.mysql.pythonanywhere-services.com'
        self.user = 'eviate'
        self.passwd = 'Snemeis16'
        self.db = 'eviate$eviate_main'
        self.use_unicode = True
        self.charset = 'utf8'
        self.tabell = tabell
    
    def connect(self):
        conn = MySQLdb.connect(host = self.host,
                               user = self.user,
                               passwd= self.passwd,
                               db = self.db,
                               use_unicode=self.use_unicode, 
                               charset=self.charset)  
        c = conn.cursor()
        return c, conn


    def selecttable(self):
        c, conn = self.connect()
        c.execute("SELECT Artnr, Merke, Modell, Utsalgspris FROM %s" % self.tabell) 
        array = c.fetchall()

        # Mandatory stuff
        conn.commit()
        c.close()
        conn.close()
        gc.collect()

        return array

    def bulk_update(self, file):
        """WORK IN PROGRESS"""
        c, conn = self.connect()
        c.execute("DELETE FROM %s" % self.tabell)

        conn.commit()
        c.close()
        conn.close()
        gc.collect()

        stop = 10
        with open(file, newline='') as csvfile:
            vareliste = csv.reader(csvfile, delimiter=';')
            # Build SQL query string
            
            for row in vareliste:
                sql_string = "INSERT INTO vareliste VALUES("
                for cell in row[0:stop]:

                    sql_string += '\'' + cell + '\'' + ',' 
                sql_string += '\'' + row[stop] + '\'' + ')'

                if row[3] != "":
                    # Format string
                    if 'æ' or 'Æ' in sql_string:
                        sql_string = sql_string.replace('æ', 'ae')
                        sql_string = sql_string.replace('Æ', 'Ae')
                    if 'ø' or 'Ø' in sql_string:
                        sql_string = sql_string.replace('ø','oe')
                        sql_string = sql_string.replace('Ø','Oe')
                    if 'å' or 'Å' in sql_string:
                        sql_string = sql_string.replace('å', 'aa')
                        sql_string = sql_string.replace('Å', 'Aa')


                    # Open, execute , close
                    c, conn = self.connect()
                    c.execute(sql_string)
                    conn.commit()

                    c.close()
                    conn.close()
                    gc.collect()

        return "<h1> Vareliste UPDATED</h1>"




                









