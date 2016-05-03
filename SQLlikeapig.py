#!/usr/bin/python
# -*- coding: utf-8 -*-

# DOCS @ http://mysql-python.sourceforge.net/MySQLdb.html#mysqldb
import MySQLdb
import csv
import gc

class MyPigFarm:
    # ------------ INITialize database ------------------

    def __init__(self):
        self.host = 'localhost'
        self.user = 'root'
        self.passwd = 'Snemeis15'
        self.name = 'stereo'
        self.use_unicode = True
        self.charset = 'utf8'


class MyPig:
    # --------------- INITialize table  ------------------

    def __init__(self, database, table):
        
        self.db = database
        self.table = table
        self.columns = self.get_columns()

    def get_columns(self):
        c, conn = self.open()
        columns = []
        c.execute('DESCRIBE %s' % self.table)
        fields_info = c.fetchall()

        for i in range(0,len(fields_info)):
            columns.append(fields_info[i][0])

        self.close(c, conn)
        return columns

    # ------------- OPEN, CLOSE connection -------------

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

    # ------------- GENERAL SQL-QUERY methods ---------------

    def select(self, column_indexes, ID='', orderby=''):
        c, conn = self.open()

        selected = []
        column_string = ''

        if column_indexes == '*':
            column_string = column_indexes
        else:
            for index in column_indexes:

                true_index = int(index)
                selected.append(self.columns[true_index])

            column_string = ", ".join(selected)
        
        sql = "SELECT %s FROM %s" % (column_string, self.table)
        where = " WHERE ID='%s'" % ID
        order = " ORDER BY %s" % orderby

        if ID != '':
            sql += where
            c.execute(sql)
            select_result = c.fetchone()
        elif orderby != '':
            sql += order
            c.execute(sql)
            select_result = c.fetchall()
        else:
            c.execute(sql)
            select_result = c.fetchall()

        self.close(c, conn)
        return select_result

    def rowupdate(self, columns, values, rowid):

        zipped_string = ''
        modvalue = ''

        for column, value in zip(columns, values):

            if value == 'CURRENT_TIMESTAMP()':
                zipped_string += column + '=' + value + ', '
            else:
                zipped_string += column + '=\'' + value + '\', '
        zipped_string = zipped_string[0:-2]

        sql = ("UPDATE %s SET " % self.table) + zipped_string + (" WHERE ID=%s" % rowid)

        c, conn = self.open()
        c.execute(sql)
        self.close(c, conn)

        return 'success'

    # ------------------------------------------ #
    """  FUNKSJONER TIL BESTILLING - SKJEMA  """
    # ----------------------------------------- #

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

    def select_multirows(self, id_array):
        c, conn = self.open()
        id_string = ",".join([str(i) for i in id_array])
        c.execute("SELECT ID, Varegruppe, Merke, Modell, Utsalgspris "
                  "FROM vareliste WHERE ID in (%s)" % id_string)

        varetabell = c.fetchall()
        self.close(c, conn)

        return varetabell

    # ------------------------------------------ #
    """  FUNKSJONER TIL ENEKELBESTILLING - VIEW """
    # ----------------------------------------- #

    def delete_bestilling(self, rowid):

        c, conn = self.open()
        c.execute("DELETE FROM bestillinger WHERE ID=%s" % rowid)
        self.close(c, conn)

        return "success"

    # ------------------------------------------ #
    """  FUNKSJONER TIL INNLOGGING  """
    # ----------------------------------------- #

    def select_ifusername(self, username):

        c, conn = self.open()
        c.execute("SELECT brukernavn FROM brukere WHERE brukernavn='%s'" % username)
        data = c.fetchone()
        self.close(c, conn)
        return data

    # ---------------------------------------------------

if __name__ == "__main__":

    db = MyPigFarm()
    best = MyPig(db, 'bestillinger')
    best.rowupdate(['Notat'], ['Det vare åtte ørti fjære'], '41')