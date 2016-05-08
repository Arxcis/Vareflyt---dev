
#!/usr/bin/python
# -*- coding: utf-8 -*-


import csv
import codecs

progress = 0


    # ---------------------------------------------------


    # ---------BATCH UPDATE STUFF ----------------------


def format_incomming(self, file):  
    stop = 11
    vareliste = csv.reader((codecs.open(file, 'r')), dialect='excel', delimiter=";")   
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
    conn.commit()

    liste = self.format_incomming(filename)

    sql = ("INSERT INTO varer "
           "(ID, Leverandør, Artnr, Merke, Modell, Varebeskrivelse, Varegruppe, Undergruppe, MVA, Nettopris, Utsalgspris, DG) "
           "VALUES "
           "('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')")

    c.executemany(sql, liste)

    conn.commit()

    self.close(c, conn)

    return 'success'
    

