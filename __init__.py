#!/usr/bin/python
# -*- coding: utf-8 -*-

from flask import Flask, session, render_template, \
                url_for, request, redirect, flash, jsonify
from functools import wraps
import gc
import os
import json
from bson import json_util

from SQLlikeaPig import MyPigFarm, MyPig

app = Flask(__name__)

# ---- INIT SQL-pigs ---------
db = MyPigFarm()

utvalg = MyPig(db, 'varer')  
vareordre = MyPig(db, 'vareordre')
serviceordre = MyPig(db, 'serviceordre')
brukere = MyPig(db, 'brukere')


# Konverters for the status-texts
statusdict = {
         'Ny' : '1',
    'Bestilt' : '2',
    'Mottatt' : '3',
     'Levert' : '4'
}

servicedict = {
    'Ny'    : '1',
    u'Påbegynt' : '2',
    u'Fullført' : '3',
    'Henteklar' : '4',
    'Levert' : '5'
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
        return redirect(url_for('varer'))
    else:
        return render_template('login.html')


@app.route('/login', methods=["POST"])
def login():

    brukernavn = request.form['brukernavn']
    passord = request.form['passord']
    try:
        data = brukere.select_ifusername(brukernavn)
        if passord == data[2]:
            session['innlogget'] = True
            session['brukernavn'] = brukernavn

            return redirect(url_for('varer'))
        else:
            return render_template('login.html', error = 'Feil brukernavn eller passord')

    except Exception as e:
        return render_template('login.html', error = e)

# -------------------------------------------#
"""               NAV ROUTES             """
# -------------------------------------------#

@app.route('/varer')
@login_required
def varer():
    ordtabell = vareordre.select([0,1,5,4,7,6,11,12,16], '', "ORDER BY StatusNr, ID DESC");
    return render_template('/varer/ordre_liste.html', 
                            tabell=json.dumps(ordtabell, default=json_util.default))


@app.route('/service')
@login_required
def service():

    tabell = serviceordre.select([0,1,9,8,7], '', 'ORDER BY ID DESC')

    return render_template('service/service_liste.html', tabell=tabell)


@app.route('/nyordre')
@login_required
def nyordre():

    pick = request.args.get('pick')
    
    if pick == 'vare':
        varetabell = utvalg.select([1,7,4,5,11]) 
        return render_template('/varer/ordre_ny.html', varetabell=json.dumps(varetabell))

    elif pick == 'service':
        return render_template('/service/service_ny.html')

    else: 
        return "WTF!"

@app.route('/update')
@login_required
def  update():

    return render_template('/update/update.html')


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

@app.route('/enkelvareordre')
@login_required
def enkelvareordre():
    try:
        ordre_id = request.args.get('ID')
        # kolonner:  navn=1, telefon=2, varer=3, notat=13, notat=14
        navn, telefon, vareinfo, notat1, notat2, signatur, status = vareordre.select([1,2,3,13,14,15,11], ordre_id)
        info = navn, telefon
        notater = notat1, notat2


        array = vareinfo.split(",")
        vareid_array = []
        antall_array = []
        for i in range(0, len(array)):
            if i % 2 != 0:
                antall_array.append(array[i])
            else:
                vareid_array.append(array[i])

        varetabell = utvalg.select_multirows(vareid_array)

        if request.args.get('type') == 'JSON':
             return jsonify(varer=varetabell, 
                            notater=notater, 
                            antall=antall_array)    

        try:  
            return render_template('varer/ordre_enkel.html', bestid=ordre_id, 
                                                                tabell=varetabell, 
                                                                antall=antall_array, 
                                                                    notater=notater,
                                                                    kundeinfo=info,
                                                                    sign=signatur, 
                                                                    status=status)
        except Exception as e:
            return render_template('login.html', error = "HERE " + str(e))

    except Exception as e:
        return render_template('login.html', error = e)

@app.route('/enkelservice')
@login_required
def enkelservice():

    service_id = request.args.get('id')

    serviceinfo = serviceordre.select([0,1,2,3,4,5,6], service_id)

    return render_template('service/service_enkel.html', info=serviceinfo)


# ---------- JAVASCRIPT AJAX ROUTES -------------
# -------------------------------------------#
"""    ROUTES FRA varer/ordre_ny.html     """
# -------------------------------------------#

@app.route('/postvareordre', methods=["POST"])
@login_required
def lagre_vareordre():
    try:
        success = vareordre.lagre_vareordre(request.form)    
        return jsonify(result=success)

    except Exception as e:
        return jsonify(result="Server ERROR: " + str(e))


@app.route('/getvarelinje')
def getvarelinje():

    indexes = request.args.get('columns').split(',')
    vare_id = request.args.get('ID')
    linje_array = utvalg.select(indexes, vare_id)

    return jsonify(linje=linje_array)


# -------------------------------------------#
"""    ROUTES FRA varer/ordre_liste.html   """
# -------------------------------------------#


@app.route('/poststatus', methods=['POST'])
@login_required
def lagre_status():

    nystatus = request.form['status']
    ordre_id = request.form['id']
    ulest = request.form['ulest']
    try:
        success = vareordre.rowupdate(['status', nystatus, 'StatusNr', 'Ulest'],
                                 [nystatus, 'CURRENT_TIMESTAMP()', statusdict[nystatus], ulest],
                                 ordre_id)
        return jsonify(result=success)

    except Exception as e:
        return jsonify(result= "Server ERROR: " + str(e))

@app.route('/markasread', methods=['POST'])
@login_required
def markas_read():

    try:
        ordre_id = request.form['id']
        lest = request.form['lest']

        success = vareordre.rowupdate(['Ulest'], [lest], ordre_id)
        return jsonify(result=success)

    except Exception as e:
        return jsonify(result= "Server ERROR: " + str(e))



# -------------------------------------------#
"""    ROUTES FRA varer/ordre_enkel.html   """
# -------------------------------------------#

@app.route('/postkanseller', methods=['POST'])
@login_required
def kanseller():
    try:
        ordre_id = request.form['ID']
        ulest = request.form['ulest']
        success = vareordre.rowupdate(['status', 'StatusNr', 'Ulest'], 
                                      ['Kansellert', '5', ulest], 
                                       ordre_id)
        return jsonify(result=str(success))

    except Exception as e:
        return jsonify(result=e)


@app.route('/postnotater', methods=['POST'])
@login_required
def post_notater():

    ordre_id = ''
    notat1 = ''
    notat2 = ''
    try:
        ordre_id = request.form['submit']

        if request.form['notatbutikk']:
            notat1 = request.form['notatbutikk']
            vareordre.rowupdate(['Notat', 'Ulest'], [notat1, 'admin'], ordre_id)

        if request.form['notatadmin']:
            notat2 = request.form['notatadmin']
            vareordre.rowupdate(['NotatAdmin','Ulest'], [notat2, 'butikk'], ordre_id)

        return redirect('/varer')

    except Exception as e:
        return render_template('login.html', error = e)

# -------------------------------------------#
"""    ROUTES FRA service/service_ny.html   """
# -------------------------------------------#


@app.route('/postserviceordre', methods=['POST'])
@login_required
def lagre_serviceordre():

    try:
        success = serviceordre.lagre_serviceordre(request.form)
        return redirect(url_for('service'))

    except Exception as e: 
        return render_template('login.html', error = e)


@app.route('/updateservice', methods=['POST'])
@login_required
def update_service():

    success = serviceordre.rowupdate(['Navn', 'Telefon', 'Mail', 'Signatur', 'Varenavn', 'Beskrivelse'],
                                         [request.form['kundenavn'], request.form['telefon'], request.form['mail'], 
                                          request.form['signatur'], request.form['varenavn'], request.form['beskrivelse']], request.form['serviceid'])

    return redirect(url_for('service'))


# -------------------------------------------#
"""    ROUTES FRA service/service_liste.html   """
# -------------------------------------------#

@app.route('/getserviceordre')
def service_ordreliste():
    try:
        indexes = request.args.get('columns').split(',')
        ordre_array = serviceordre.select(indexes, '', 'ORDER BY StatusNr, ID DESC')
        return jsonify(tabell=ordre_array)
        
    except Exception as e:
        return render_template('login.html', error = e)

@app.route('/postservicestatus', methods=['POST'])
@login_required
def lagre_servicestatus():

    nystatus = request.form['status']
    ordre_id = request.form['id']
    try:
        success = serviceordre.rowupdate(['status', nystatus, 'StatusNr'],
                                 [nystatus, 'CURRENT_TIMESTAMP()', servicedict[nystatus]],
                                 ordre_id)
        return jsonify(result=success)

    except Exception as e:
        return jsonify(result= "Server ERROR: " + str(e))


# -------------------------------------------#
"""    ROUTES FRA service/service_enkel.html   """
# -------------------------------------------#

@app.route('/postdeleteservice')
@login_required
def delete_service():
    try:
        ordre_id = request.args.get('ID')
        success = serviceordre.delete_service(ordre_id)
        return jsonify(result = str(success))
    except Exception as e:
        return render_template('login.html', error = e)



if __name__ == "__main__":
    app.run()
