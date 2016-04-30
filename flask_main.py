#!/usr/bin/python
# -*- coding: utf-8 -*-

# A very simple Flask Hello World app for you to get started with...

from flask import Flask, session, render_template, \
                url_for, request, redirect, flash, jsonify
import gc
import os
from SQLlikeapig import MyPig, MyPigTable

app = Flask(__name__)
db = MyPig()


# ---------------- NAV ROUTES -------------------
@app.route('/')
def index():
    return redirect(url_for('bestilling_liste'))

@app.route('/bestliste')
def bestilling_liste():
    return render_template('/navpages/bestilling_liste.html')

@app.route('/bestskjema')
def bestilling_skjema():
    return render_template('/navpages/bestilling_skjema.html')

@app.route('/uploadform')
def uploadform():
    return render_template('/navpages/uploadform.html')


# ---------- JAVASCRIPT AJAX ROUTES -------------

@app.route('/postbestilling', methods=["POST"])
def lagre_bestilling():

    best = MyPigTable(db, 'vareliste')
    success = best.lagre_bestilling(request.form)    

    return jsonify(result=success)

@app.route('/poststatus', methods=["POST"])
def lagre_status():

    best = MyPigTable(db, 'bestillinger')
    success = best.lagre_status(request.form)

    return jsonify(result=success)

@app.route('/getbestliste')
def getbestilling_liste():
    table_string = 'empty'
    best = MyPigTable(db, 'bestillinger')

    best_array = best.selecttable_bestillinger()

    return jsonify(tabell=best_array)
    #return jsonify(liste=table_string)

@app.route('/getvareutvalg')
def getvareutvalg():

    table_string = 'empty'
    vareliste = MyPigTable(db, 'vareliste')

    if request.args.get('string'):
        now_string = request.args.get('string')
        table_string = vareliste.searchtable(now_string)
    else:
        table_string = vareliste.selecttable()
    
    #return render_template('test.html', table=json_tuple)
    return jsonify(liste=table_string)

@app.route('/getvarelinje')
def getvarelinje():
    linje_id = request.args.get('ID')

    vareliste = MyPigTable(db, 'vareliste')
    linje_array = vareliste.selectrow(linje_id)

    return jsonify(linje=linje_array)

@app.route('/getsortcolumn')
def getsortcolumn():
    return 0


"""WORK IN PROGRESS

    This is a function that is supposed to run, 
     when a file is uploaded. 
      1. Take file. 
      2. Format file. 
      3. Delete excisting vareliste in MySql-database
      4. Import new vareliste to MySql.

@app.route('/vareupdate')
def update_vareliste():
    
    filnavn = request.args.get('fil')
    vareliste = SQLTable('vareliste')

    success = vareliste.bulk_update('/home/eviate/mysite/uploads/%s.csv' % filnavn)
    return success"""


# set the secret key   