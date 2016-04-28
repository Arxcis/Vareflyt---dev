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
    return redirect(url_for('bestliste'))

@app.route('/bestliste')
def bestliste():
    return render_template('/navpages/bestliste.html')

@app.route('/bestform')
def bestform():
    return render_template('/navpages/bestform.html')

@app.route('/vareliste')
def vareliste():
    return render_template('/navpages/vareliste.html')

@app.route('/uploadform')
def uploadform():
    return render_template('/navpages/uploadform.html')


# ---------- AJAX ROUTES -------------
@app.route('/getvareutvalg')
def getvareutvalg():

    vareliste = MyPigTable(db, 'vareliste')
    table_string = vareliste.selecttable()
    
    #return render_template('test.html', table=json_tuple)
    return jsonify(liste=table_string)

@app.route('/getvarelinje')
def getvarelinje():
    linje_id = request.args.get('ID')

    vareliste = MyPigTable(db, 'vareliste')
    row_string = vareliste.selectrow(linje_id)

    return jsonify(row=row_string)




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