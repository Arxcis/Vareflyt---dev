#!/usr/bin/python
# -*- coding: utf-8 -*-

from flask import Flask, session, render_template, \
                url_for, request, redirect, flash, jsonify
from functools import wraps
import gc
import os
from SQLlikeaPig import MyPigFarm, MyPig

app = Flask(__name__)

# ---- INIT SQL-pigs ---------
db = MyPigFarm()
vareliste = MyPig(db, 'vareliste')
best = MyPig(db, 'bestillinger')
brukere = MyPig(db, 'brukere')

statusdict = {
         'Ny' : '1',
    'Bestilt' : '2',
    'Mottatt' : '3',
     'Levert' : '4'
}

# This wrapper safeguards locked down sites
def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'innlogget' in session:
            return f(*args, **kwargs)
        else:
            return redirect(url_for('index'))
    return wrap

# -------------------------------------------#
"""             LOGIN ROUTES              """
# -------------------------------------------#

@app.route('/')
def index():
    if 'innlogget' in session:
        return redirect(url_for('bestilling_liste'))
    else:
        return render_template('login.html')


@app.route('/login', methods=["POST"])
def login():

    brukernavn = request.form['brukernavn']
    passord = request.form['passord']
    try:
        data = brukere.select_ifusername(brukernavn)
        if True:
            session['innlogget'] = True
            session['brukernavn'] = brukernavn

            return redirect(url_for('bestilling_liste'))
        else:
            return render_template('login.html', error = 'Feil brukernavn eller passord')

    except Exception as e:
        return render_template('login.html', error = e)

# -------------------------------------------#
"""               NAV ROUTES             """
# -------------------------------------------#

@app.route('/bestliste')
@login_required
def bestilling_liste():

    return render_template('/navpages/bestilling_liste.html')


@app.route('/bestskjema')
@login_required
def bestilling_skjema():

    return render_template('/navpages/bestilling_skjema.html')


@app.route('/uploadform')
@login_required
def uploadform():

    return render_template('/navpages/uploadform.html')

@app.route('/logout')
@login_required
def logout():
    try:
        session.clear()
        gc.collect()  
        return render_template('login.html', error= "Du ble logget ut")
    except Exception as e:
        return render_template('login.html', error = e)

# -------------------------------------------#
"""               VIEW ROUTES            """
# -------------------------------------------#

@app.route('/viewenkelbest')
@login_required
def view_enkelbest():
    try:
        best_id = request.args.get('ID')
        # kolonner:  navn=1, telefon=2, varer=3, notat=13, notat=14
        navn, telefon, varer, notat1, notat2 = best.select([1,2,3,13,14], best_id)
        info = navn, telefon
        notater = notat1, notat2


        array = varer.split(",")
        vareid_array = []
        antall_array = []
        for i in range(0, len(array)):
            if i % 2 != 0:
                antall_array.append(array[i])
            else:
                vareid_array.append(array[i])

        varetabell = vareliste.select_multirows(vareid_array)
        try:  
            return render_template('views/enkelbestilling.html', bestid=best_id, 
                                                                tabell=varetabell, 
                                                                antall=antall_array, 
                                                                    notater=notater,
                                                                    kundeinfo=info)
        except Exception as e:
            return render_template('login.html', error = "HERE " + str(e))

    except Exception as e:
        return render_template('login.html', error = e)


@app.route('/postnotater', methods=['POST'])
def post_notater():

    best_id = ''
    notat1 = ''
    notat2 = ''
    try:
        best_id = request.form['submit']

        if request.form['notatbutikk']:
            notat1 = request.form['notatbutikk']
            best.rowupdate(['Notat'], [notat1], best_id)

        if request.form['notatadmin']:
            notat2 = request.form['notatadmin']
            best.rowupdate(['NotatAdmin'], [notat2], best_id)

        return redirect('/viewenkelbest?ID=' + best_id)

    except Exception as e:
        return render_template('login.html', error = e)


# ---------- JAVASCRIPT AJAX ROUTES -------------
# -------------------------------------------#
"""    ROUTES FRA BESTILLING - SKJEMA      """
# -------------------------------------------#

@app.route('/postbestilling', methods=["POST"])
def lagre_bestilling():

    success = best.lagre_bestilling(request.form)    

    return jsonify(result=success)


@app.route('/getvareutvalg')
def getvareutvalg():

    if request.args.get('columns'):
        indexes = request.args.get('columns').split(',')
        table_array = vareliste.select(indexes)

    if request.args.get('string'):
        now_string = request.args.get('string')
        table_array = vareliste.searchtable(now_string)
    
    return jsonify(tabell=table_array)


@app.route('/getvarelinje')
def getvarelinje():

    indexes = request.args.get('columns').split(',')
    vare_id = request.args.get('ID')
    linje_array = vareliste.select(indexes, vare_id)

    return jsonify(linje=linje_array)


# -------------------------------------------#
"""    ROUTES FRA BESTILLING - LISTE   """
# -------------------------------------------#

@app.route('/getbestliste')
def getbestilling_liste():

    indexes = request.args.get('columns').split(',')

    best_array = best.select(indexes, '', 'statnr')
    return jsonify(tabell=best_array)


@app.route('/poststatus', methods=['POST'])
def lagre_status():

    nystatus = request.form['status']
    best_id = request.form['id']
    try:
        success = best.rowupdate(['status', nystatus, 'statnr'],
                                 [nystatus, 'CURRENT_TIMESTAMP()', statusdict[nystatus]],
                                 best_id)
        return jsonify(result=success)

    except Exception as e:
        return jsonify(result= "Server ERROR: " + str(e))


@app.route('/postdeletebest')
def delete_best():
    try:
        best_id = request.args.get('ID')
        success = best.delete_bestilling(best_id)
        return jsonify(result = str(success))

    except Exception as e:
        return render_template('login.html', error = e)


if __name__ == "__main__":
	app.run()
