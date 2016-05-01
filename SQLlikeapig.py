#!/usr/bin/python
# -*- coding: utf-8 -*-

# DOCS @ http://mysql-python.sourceforge.net/MySQLdb.html#mysqldb
import MySQLdb
import csv
import gc

class MyPigFarm:
    def __init__(self):
        self.host = 'localhost'
        self.user = 'root'
        self.passwd = 'Snemeis15'
        self.name = 'stereo'
        self.use_unicode = True
        self.charset = 'utf8'


class MyPig:
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


    def format_tostring(self, array):
        table_s = str(array)
        table_s = table_s.replace('(','')
        table_s = table_s.replace(')','')
        table_s = table_s.replace('\'','')

        return table_s


    # ------------------------------------------ #
    """  FUNKSJONER TIL BESTILLING - SKJEMA  """
    # ----------------------------------------- #

    def selecttable(self):
        # --- OPEN, EXECUTE, FETCHALL, CLOSE ---
        c, conn = self.open()
        c.execute("SELECT ID, Varegruppe, Merke, Modell, Utsalgspris "
                  "FROM vareliste") 
        array = c.fetchall()
        self.close(c, conn)

        return array

    def searchtable(self, string):
        # --- OPEN, EXECUTE, FETCHALL, CLOSE ---
        c, conn = self.open()
        c.execute("SELECT ID, Varegruppe, Merke, Modell, Utsalgspris "
                  "FROM vareliste WHERE CONCAT_WS"
                  "('', ID, Varegruppe, Merke, Modell, Utsalgspris) "
                  "LIKE '%" + string + "%'")
        array = c.fetchall()
        self.close(c, conn)
      
        return array

    def selectrow(self, identity):
        # --- OPEN, EXECUTE, FETCHALL, CLOSE ---
        c, conn = self.open()
        c.execute("SELECT ID, Merke, Modell, Utsalgspris FROM vareliste WHERE ID=%s" % identity)
        array = c.fetchall()
        self.close(c, conn)

        # ------ FORMAT to STRING -------
        return array

    def lagre_bestilling(self, ny_bestilling):
        # nybestilling is a dictionary of [navn, telefon, varer, verdi]
        # --- OPEN, EXECUTE, FETCHALL, CLOSE ---
        c, conn = self.open()
        c.execute("INSERT INTO bestillinger"
                  "(Kundenavn, Telefon, Varer, Verdi, Antall, Ny, status) "
                  "VALUES ('%s', '%s', '%s', '%s', '%s', "
                  "CURRENT_TIMESTAMP(), 'Ny')"
                   % (ny_bestilling['navn'],
                  ny_bestilling['telefon'],
                  ny_bestilling['varer'],
                  ny_bestilling['verdi'],
                  ny_bestilling['antall']))
        self.close(c, conn)

        return 'success'

    # ------------------------------------------ #
    """  FUNKSJONER TIL BESTILLINGSLISTE  """
    # ----------------------------------------- #

    def selecttable_bestillinger(self):
        # --- OPEN, EXECUTE, FETCHALL, CLOSE ---
        c, conn = self.open()
        c.execute("SELECT ID, Kundenavn, Verdi, Antall, Ny, sist_oppdatert, status "
                  "FROM bestillinger ORDER BY statnr, ID DESC") 
        array = c.fetchall()
        self.close(c, conn)

        # ------ FORMAT to STRING -------
        #return self.format_tostring(array)
        return array

    def lagre_status(self, ny_status):

        dato_columns = {
            'Ny': 1,
            'Bestilt': 2,
            'Mottatt' : 3,
            'Levert' : 4  }

        c, conn = self.open()
        c.execute("UPDATE bestillinger SET status='%s', %s=CURRENT_TIMESTAMP(), "
                  "statnr=%d WHERE ID='%s'" 
                   % (ny_status['status'],
                      ny_status['status'],
                      dato_columns[ny_status['status']],
                      ny_status['id']))

        self.close(c, conn)
        return 'success'

    # ------------------------------------------ #
    """  FUNKSJONER TIL INNLOGGING  """
    # ----------------------------------------- #

    def select_ifusername(self, username):

        c, conn = self.open()
        c.execute("SELECT * FROM brukere WHERE brukernavn='%s'" % username)
        data = c.fetchone()[2]
        self.close(c, conn)
        return data


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




                









