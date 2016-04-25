#!/usr/bin/python
# -*- coding: utf-8 -*-

# External library
from flask import Flask, render_template, request, redirect, url_for, session
import gc

# From local file
from dbconnect import connection


app = Flask(__name__)

#@app.route('/')
#def innlogging():
#   return render_template('innlogging.html')


@app.route('/')
def index():
    # I have to simplify this somehow
    switch = {'active1': '1', 'active2': '0'}

    # MYSQL ------------------------------- QUERY
    # SELECT columns FROM table ORDER BY ID DESC;
    c, conn = connection()
    c.execute("SELECT ID, varenavn, kundenavn, levnavn FROM "
              "ordreliste_test ORDER BY ID DESC")

    header_list = [i[0] for i in c.description]
    liste_avtuples = c.fetchall()

    #Close of and collect garbage
    c.close()
    conn.close()
    gc.collect()
    # ------------------------------------------

    return render_template('index.html', switch=switch, 
                    tabellh=header_list, tabell=liste_avtuples)

@app.route('/ordreform')
def ordreform():
    # I have to simplify this somehow
    switch = {'active1': '0', 'active2': '1'}
    return render_template('ordreform.html', switch=switch)

@app.route('/edit-ordreform/', methods=['GET'])
def edit_ordre():
    ordre_id = request.args.get('ID')

    # MYSQL -------------------------------- QUERY
    # SELECT * FROM table WHERE ID=ordre_id
    c, conn = connection()
    c.execute("SELECT * FROM ordreliste_test WHERE ID='%s'" % ordre_id)
    ordre_info = c.fetchone()

    #Close of and collect garbage
    c.close()
    conn.close()
    gc.collect()
    # ------------------------------------------
    switch = {'active1': '0', 'active2': '1'}
    return render_template('editordre.html', ordre=ordre_info, 
                                            switch=switch)



@app.route('/nyordre', methods=['POST'])
def nyordre():
    if request.form['submit'] == 'Submit':

        # MYSQL ----------------------------------- QUERY
        # INSERT INTO table(columns) VALUES (cell-data);
        c, conn = connection()
        c.execute("INSERT INTO ordreliste_test(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)" 
                  "VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')" % 
                      ('varenavn', 'vareID', 'vareantall',
                       'kundenavn', 'kundeID', 'kundetelefon', 
                       'kundemail', 'kundeadresse', 'kundepostboks',
                       'levnavn', 'levID', 'levtelefon', 'levmail', 
                       'levadresse', 'levpostboks',
                       request.form['varenavn'],
                       request.form['vareID'],
                       request.form['vareantall'],
                       request.form['kundenavn'],
                       request.form['kundeID'],
                       request.form['kundetelefon'],
                       request.form['kundemail'],
                       request.form['kundeadresse'],
                       request.form['kundepostboks'],
                       request.form['levnavn'],
                       request.form['levID'],
                       request.form['levtelefon'],
                       request.form['levmail'],
                       request.form['levadresse'],
                       request.form['levpostboks']))
        conn.commit()

        #Close of and collect garbage
        c.close()
        conn.close()
        gc.collect()
        # -------------------------------------------------

    return redirect(url_for('index'))

@app.route('/updateordre', methods=['POST'])
def update_ordre():
    if request.form['submit'] == 'Submit':
        """UPDATE table_name
        SET column1=value1,column2=value2,...
        WHERE some_column=some_value;"""

        c, conn = connection()
        c.execute("UPDATE ordreliste_test "
                  "SET "
                  "varenavn='%s', "
                  "vareID=%s, "
                  "vareantall='%s', "
                  "kundenavn='%s', "
                  "kundeID=%s, "
                  "kundetelefon='%s', "
                  "kundemail='%s', "
                  "kundeadresse='%s', "
                  "kundepostboks='%s', "
                  "levnavn='%s', "
                  "levID=%s, "
                  "levtelefon='%s', "
                  "levmail='%s', "
                  "levadresse='%s', "
                  "levpostboks='%s' "
                  "WHERE "
                  "ID=%s" %
                  (request.form['varenavn'],
                   request.form['vareID'],
                   request.form['vareantall'],
                   request.form['kundenavn'],
                   request.form['kundeID'],
                   request.form['kundetelefon'],
                   request.form['kundemail'],
                   request.form['kundeadresse'],
                   request.form['kundepostboks'],
                   request.form['levnavn'],
                   request.form['levID'],
                   request.form['levtelefon'],
                   request.form['levmail'],
                   request.form['levadresse'],
                   request.form['levpostboks'],
                   request.form['ID']))

        #Close of and collect garbage
        c.close()
        conn.close()
        gc.collect()
        # -------------------------------------------------

    return redirect(url_for('index'))


#if __name__ == "__main__":
#    app.debug = True
#    app.run()