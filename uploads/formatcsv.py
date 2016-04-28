import csv
import gc
import time

def format_csv(file):  
        stop = 10
        with open(file, newline='') as csvfile:
            vareliste = csv.reader(csvfile, delimiter=';')
            # Build SQL query string
            sql_string = "INSERT INTO vareliste VALUES('ID',"
            counter = 0
            for row in vareliste:

                if counter == 0:
                    counter += 1
                    continue
                    
                for cell in row[0:stop]:
                    
                    if ',' in cell:
                        test = cell
                        test = test.replace(',','')
                        
                        try: 
                            testint = int(test)
                            cell = cell.replace(',','.')
                        except ValueError:
                            cell = cell.replace(',','')

                    sql_string += '\'' + cell + '\'' + ',' 
                sql_string += '\'' + row[stop] + '\'' + ')'

                if row[3] != "":
                    if 'æ' or 'Æ' in sql_string:
                        sql_string = sql_string.replace('æ', 'æ')
                        sql_string = sql_string.replace('Æ', 'Æ')
                    if 'ø' or 'Ø' in sql_string:
                        sql_string = sql_string.replace('ø','ø')
                        sql_string = sql_string.replace('Ø','Ø')
                    if 'å' or 'Å' in sql_string:
                        sql_string = sql_string.replace('å', 'å')
                        sql_string = sql_string.replace('Å', 'Å')

                with open('vareliste.txt', 'a') as ffile:
                    ffile.write(sql_string + '; ')

                print(sql_string)
                sql_string = "INSERT INTO vareliste VALUES('ID',"
                



format_csv('vareliste.csv')