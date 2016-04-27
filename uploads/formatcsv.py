import csv
import gc
import time

def format_csv(file):  
        stop = 10
        with open(file, newline='') as csvfile:
            vareliste = csv.reader(csvfile, delimiter=';')
            # Build SQL query string
            sql_string = "INSERT INTO vareliste VALUES("
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
                        sql_string = sql_string.replace('æ', 'ae')
                        sql_string = sql_string.replace('Æ', 'Ae')
                    if 'ø' or 'Ø' in sql_string:
                        sql_string = sql_string.replace('ø','oe')
                        sql_string = sql_string.replace('Ø','Oe')
                    if 'å' or 'Å' in sql_string:
                        sql_string = sql_string.replace('å', 'aa')
                        sql_string = sql_string.replace('Å', 'Aa')

                with open('vareliste.txt', 'a') as ffile:
                    ffile.write(sql_string + '; ')

                sql_string = "INSERT INTO vareliste VALUES("

                



format_csv('vareliste.csv')