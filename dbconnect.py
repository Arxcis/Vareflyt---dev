
# DOCS @ http://mysql-python.sourceforge.net/MySQLdb.html#mysqldb
import MySQLdb

def connection():

    conn = MySQLdb.connect(host = 'eviate.mysql.pythonanywhere-services.com',
                           user = 'eviate',
                           passwd= 'Snemeis16',
                           db = 'eviate$eviate_main')

    c = conn.cursor()

    return c, conn