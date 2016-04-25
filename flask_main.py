# External library
from flask import Flask, render_template, request, redirect, url_for, session
import gc

# From local file
from dbconnect import connection


app = Flask(__name__)

@app.route('/')
def index():
    # I have to simplify this somehow
    switch = {'active1': '1', 'active2': '0'}
    return render_template('index.html', switch=switch)

@app.route('/ordreform')
def ordreform():
    # I have to simplify this somehow
    switch = {'active1': '0', 'active2': '1'}
    return render_template('ordreform.html', switch=switch)

@app.route('/nyordre', methods=['POST'])
def nyordre():
    if request.form['submit'] == 'Submit':
        c, conn = connection()

        #c.execute("INSERT INTO ordreliste_test(varenavn) VALUES ('%s')" % (request.form['varenavn']))
        c.execute("INSERT INTO ordreliste_test(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')" % 
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

    return redirect(url_for('index'))



#if __name__ == "__main__":
#    app.debug = True
#    app.run()