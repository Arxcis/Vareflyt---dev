#!/usr/bin/python
# -*- coding: utf-8 -*-

# DOCS @ http://mysql-python.sourceforge.net/MySQLdb.html#mysqldb
import MySQLdb
import csv
import gc

class MyPig:

    def __init__(self):
        self.host = 'eviate.mysql.pythonanywhere-services.com'
        self.user = 'eviate'
        self.passwd = 'Snemeis16'
        self.name = 'eviate$eviate_main'
        self.use_unicode = True
        self.charset = 'utf8'


class MyPigTable:
    def __init__(self, database, tabell):
        
        self.db = database
        self.tabell = tabell

    def open(self):
        conn = MySQLdb.connect(host = self.db.host,
                               user = self.db.user,
                               passwd= self.db.passwd,
                               db = self.db.name,
                               use_unicode=self.db.use_unicode, 
                               charset=self.db.charset)  
        c = conn.cursor()
        return c, conn

    def close(self, c, conn):
        conn.commit()
        c.close()
        conn.close()
        gc.collect()

    def selecttable(self):
        # --- OPEN, EXECUTE, FETCHALL, CLOSE ---
        c, conn = self.open()
        c.execute("SELECT ID, Artnr, Merke, Modell, Utsalgspris FROM vareliste LIMIT 300") 
        array = c.fetchall()
        self.close(c, conn)

        # ------ FORMAT to STRING -------
        table_s = str(array)
        table_s = table_s.replace('(','')
        table_s = table_s.replace(')','')
        table_s = table_s.replace('\'','')

        return table_s

    def selectrow(self, identity):
        # --- OPEN, EXECUTE, FETCHALL, CLOSE ---
        c, conn = self.open()
        c.execute("SELECT ID, Merke, Modell, Utsalgspris FROM vareliste WHERE ID=%s" % identity)
        array = c.fetchall()
        self.close(c, conn)

        # ------ FORMAT to STRING -------
        row_s = str(array)
        row_s = row_s.replace('(','')
        row_s = row_s.replace(')','')
        row_s = row_s.replace('\'','')

        return row_s

    """WORK IN PROGRESS

    def bulk_update(self, file):
        
        c, conn = self.connect()
        c.execute("DELETE FROM %s" % self.tabell)

        self.close(c, conn)

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

        return "<h1> Vareliste UPDATED</h1>" """




                









