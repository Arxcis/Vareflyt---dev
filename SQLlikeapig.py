#!/usr/bin/python
# -*- coding: utf-8 -*-

# DOCS @ http://mysql-python.sourceforge.net/MySQLdb.html#mysqldb
import MySQLdb
import csv
import gc
import codecs

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
        """
        column_indexes = a list of column ints f.ex: [1,3,4,5,11]
        ID = a unique key to the row
        ordreby = the string which is to be inserted after ORDER BY f.ex: "cats, dogs"
        """
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
        c, conn = self.open()

        zipped_string = ''
        modvalue = ''

        for column, value in zip(columns, values):

            if value == 'CURRENT_TIMESTAMP()':
                zipped_string += column + '=' + value + ', '
            else:
                zipped_string += column + '=\'' + value + '\', '
        zipped_string = zipped_string[0:-2]

        sql = ("UPDATE %s SET " % self.table) + zipped_string + (" WHERE ID=%s" % rowid)
        c.execute(sql)

        self.close(c, conn)
        return 'success'

    # ------ SPECIAL METHODS -> varer/ordre_ny.html ----

    def searchtable(self, string):
        c, conn = self.open()

        c.execute("SELECT ID, Varegruppe, Merke, Modell, Utsalgspris "
                  "FROM varer WHERE CONCAT_WS"
                  "('', ID, Varegruppe, Merke, Modell, Utsalgspris) "
                  "LIKE '%" + string + "%' LIMIT 300")
        array = c.fetchall()

        self.close(c, conn)
        return array

    def lagre_vareordre(self, ny_ordre):
        c, conn = self.open()

        c.execute("INSERT INTO vareordre"
                  "(Kundenavn, Kontakt, Varer, Verdi, Antall, Signatur, Ny, status) "
                  "VALUES ('%s', '%s', '%s', '%s', '%s', '%s', "
                  "CURRENT_TIMESTAMP(), 'Ny')"
                   % (ny_ordre['navn'],
                  ny_ordre['kontakt'],
                  ny_ordre['varer'],
                  ny_ordre['verdi'],
                  ny_ordre['antall'],
                  ny_ordre['signatur']))

        self.close(c, conn)
        return 'success'

    def lagre_serviceordre(self, ny_ordre):

        c, conn = self.open()
        c.execute("INSERT INTO serviceordre "
                  "(Navn, Telefon, Mail, Signatur, Varenavn, Beskrivelse, Status, Opprettet) "
                  "VALUES ('%s', '%s', '%s', '%s', '%s', '%s', 'Ny', CURRENT_TIMESTAMP())"
                   % (ny_ordre['kundenavn'],
                      ny_ordre['telefon'],
                      ny_ordre['mail'],
                      ny_ordre['signatur'],
                      ny_ordre['varenavn'],
                      ny_ordre['beskrivelse']
                     ))

        self.close(c, conn)
        return 'success'

    # ------ SPECIAL METHODS -> varer/ordre_liste.html ----

    def select_multirows(self, id_array):
        c, conn = self.open()

        id_string = ",".join([str(i) for i in id_array])
        c.execute("SELECT ID, Varegruppe, Merke, Modell, Utsalgspris "
                  "FROM varer WHERE ID in (%s)" % id_string)

        varetabell = c.fetchall()

        self.close(c, conn)
        return varetabell

    # ------ SPECIAL METHODS -> varer/ordre_enkel.html ----

    def delete_vareordre(self, rowid):
        c, conn = self.open()

        c.execute("DELETE FROM vareordre WHERE ID=%s" % rowid)

        self.close(c, conn)
        return "success"

    # ------ SPECIAL METHODS -> login.html ----

    def select_ifusername(self, username):
        c, conn = self.open()

        c.execute("SELECT * FROM brukere WHERE brukernavn='%s'" % username)
        data = c.fetchone()

        self.close(c, conn)
        return data

    """
    # ---------BATCH UPDATE STUFF ----------------------


    def format_incomming(self, file):  
        stop = 11
        vareliste = csv.reader((codecs.open(file, 'rb', 'ascii')), dialect='excel', delimiter=";")   
        counter = 0


        vareliste_mod = []

        for row in vareliste:
            
            if counter == 0:
                counter += 1
                continue

            new_row = []
            for cell in row[0:stop]:
                
                if ',' in cell:
                    # Remove all commas from cell to check if cell can convert to int.
                    test = cell
                    test = test.replace(',','')
                    
                    try: 
                        #try to change commas to periods in all numbers
                        testint = int(test)
                        cell = cell.replace(',','.')
                    except ValueError:
                        cell = cell.replace(',','')
                new_row.append(cell)

            vareliste_mod.append(tuple(new_row))
        return vareliste_mod


    def batchupdate(self, filename):

        c, conn = self.open()
        sql = "DELETE FROM varer"
        c.execute(sql) 
        self.close(c, conn)

        liste = self.format_incomming(filename)

        c, conn = self.open()
        sql = ("INSERT INTO varer "
               "(Leverandør, Artnr, Merke, Modell, Varebeskrivelse, Varegruppe, Undergruppe, MVA, Nettopris, Utsalgspris, DG) "
               "VALUES "
               "(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)")

        c.executemany(sql, liste)
        self.close(c, conn)

        return 'success'
        """

if __name__ == "__main__":

    db = MyPigFarm()
    utvalg = MyPig(db, 'varer')

    print(utvalg.batchupdate('vareliste.csv'))