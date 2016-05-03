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
        c.execute("SELECT Varenr, Varegruppe, Merke, Modell, Utsalgspris "
                  "FROM vareliste") 
        array = c.fetchall()
        self.close(c, conn)

        return array

    def searchtable(self, string):
        # --- OPEN, EXECUTE, FETCHALL, CLOSE ---
        c, conn = self.open()
        c.execute("SELECT Varenr, Varegruppe, Merke, Modell, Utsalgspris "
                  "FROM vareliste WHERE CONCAT_WS"
                  "('', Varenr, Varegruppe, Merke, Modell, Utsalgspris) "
                  "LIKE '%" + string + "%'")
        array = c.fetchall()
        self.close(c, conn)
      
        return array

    def selectrow(self, identity):
        # --- OPEN, EXECUTE, FETCHALL, CLOSE ---
        c, conn = self.open()
        c.execute("SELECT Varenr, Merke, Modell, Utsalgspris FROM vareliste WHERE Varenr='%s'" % identity)
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

    def get_varearray(self, ident):

        c, conn = self.open()
        c.execute("SELECT Varer FROM bestillinger WHERE ID='%s'" % ident)
        array = c.fetchone()
        self.close(c, conn)
        return array

    def get_varetabell(self, id_array):
        c, conn = self.open()
        id_string = ",".join([str(i) for i in id_array])
        c.execute("SELECT Varenr, Varegruppe, Merke, Modell, Utsalgspris FROM vareliste WHERE Varenr in (%s)" % id_string)

        varetabell = c.fetchall()
        self.close(c, conn)

        return varetabell

    def delete_bestilling(self, ident):

        c, conn = self.open()
        c.execute("DELETE FROM bestillinger WHERE ID=%s" % ident)
        self.close(c, conn)

        return "success"

    def save_butikknotes(self, bestid, note):
        c, conn = self.open()
        c.execute("UPDATE bestillinger SET Notat='%s' WHERE ID='%s'" % (note, bestid))
        self.close(c, conn)

        return "success"

    def save_adminnotes(self, bestid, note):
        c, conn = self.open()
        c.execute("UPDATE bestillinger SET NotatAdmin='%s' WHERE ID='%s'" % (note, bestid))
        self.close(c, conn)

        return "success"

    def get_notes(self, bestid):

        c, conn = self.open()
        c.execute("SELECT Notat, NotatAdmin FROM bestillinger WHERE ID='%s'" % bestid)
        notes = c.fetchall()
        self.close(c, conn)

        return notes



    # ------------------------------------------ #
    """  FUNKSJONER TIL INNLOGGING  """
    # ----------------------------------------- #

    def select_ifusername(self, username):

        c, conn = self.open()
        c.execute("SELECT * FROM brukere WHERE brukernavn='%s'" % username)
        data = c.fetchone()[2]
        self.close(c, conn)
        return data


if __name__ == "__main__":
    db = MyPigFarm()
    vareliste = MyPig(db, 'vareliste')

    print(vareliste.get_notes('44'))

