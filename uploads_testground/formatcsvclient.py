
#!/usr/bin/python
# -*- coding: utf-8 -*-


import csv
import codecs

progress = 0

def format_incomming(file):  
    # Return [] String.
    stop = 12
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

            if 'ø' in cell: 
                cell = cell.replace('ø','ø')
            if 'Ø' in cell:
                cell = cell.replace('Ø','Ø')
            if 'å' in cell:
                cell = cell.replace('å','å')
            if 'Å' in cell:
                cell = cell.replace('Å','Å')
            if 'æ' in cell: 
                cell = cell.replace('æ','æ')
            if 'Æ' in cell:
                cell = cell.replace('Æ','Æ')

            new_row.append(cell)

        vareliste_mod.append(tuple(new_row))
    return vareliste_mod

def write_newfile(liste):
    # Void 
    with open('vareliste-fixed.csv','a', newline='') as csvfile:
        file = csv.writer(csvfile, delimiter=',')

        for row in liste:
            file.writerow(row)


rdyliste = format_incomming('vareliste.csv')
write_newfile(rdyliste)



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
    

