#!/bin/env python3
 
import flask
import requests
from json2html import *
from flask import Markup
import json
import socket

TPL = flask.render_template # Pour éviter de toujours taper flask.render_template...
 
app = flask.Flask(__name__, template_folder='.')
URL = '192.168.99.100:8000' 
URL2 = '192.168.99.100:8001' 
@app.route('/')
def info():
	data = "Bonjour Visiteur bienvenue sur l'application de gestion banquaire"
	r = requests.get('http://' + URL + '/compte/all')
	return TPL("default.html", title='Home', data=data, info=Markup(str(json2html.convert(json = r.text))))

@app.route('/paramget')
def paramget():
	r = requests.get('http://' + URL + '/compte/all')
	data = """\
	Sur quel compte souhaitez vous faire un retrait d'argent ?
    <form action="delete" method="post">
    <input type="text" name="compte_id"/><br/>
    De combien ? \n
    <input type="text" name="montant"/><br/>
    <input type="submit"/>
    </form>
    """
	return TPL("default.html", title="Suppresion d'un compte", delete_id=Markup(data), info=Markup(str(json2html.convert(json = r.text))))
 
@app.route('/paramgetadd')
def paramgetadd():
	r = requests.get('http://' + URL + '/compte/all')
	data = """\
	Sur quel compte souhaitez vous faire un dépot d'argent ?
    <form action="add" method="post">
    <input type="text" name="compte_id"/><br/>
    De combien ?
    <input type="text" name="montant"/><br/>
    <input type="submit"/>
    </form>
    """
	return TPL("default.html", title="Suppresion d'un compte", delete_id=Markup(data), info=Markup(str(json2html.convert(json = r.text))))

@app.route('/faire_virement')
def faire_virement():
    r = requests.get('http://' + URL + '/compte/all')
    data = """\
    <form action="faire_vir" method="post">
    virement de quel compte?
    <input type="text" name="id"/><br/>
    compte de destination ?
    <input type="text" name="idd"/><br/>
    De combien ?
    <input type="text" name="montant"/><br/>
    <input type="submit"/>
    </form>
    """
    return TPL("default.html", title="Virement", delete_id=Markup(data), info=Markup(str(json2html.convert(json = r.text))))
# Renvoie du json
@app.route('/data_json')
def data_json():
	r = requests.get('http://' + URL + '/compte/all')	
	data = """\
	Quel compte souhaitez vous supprimer ?
    <form action="supprimer" method="post">
    <input type="text" name="compte_id"/><br/>
    <input type="submit"/>
    </form>
    """
	return TPL("default.html", title="Suppresion d'un compte", delete_id=Markup(data), info=Markup(str(json2html.convert(json = r.text))))

@app.route('/data_json_creation')
def data_json_creation():
	r = requests.get('http://' + URL + '/compte/all')	
	data = """\
	exemple d'entree :     {
        "iban": "FR7630004000031234567cdc890144",
        "typedecompte": "courant",
        "interet": 0,
        "frais": "gratuit",
        "solde": 98
    }
	Votre nouveau compte en json
    <form action="creer" method="post">
    <input type="text" name="compte_id"/><br/>
    <input type="submit"/>
    </form>
    """
	return TPL("default.html", title="Suppresion d'un compte", delete_id=Markup(data), info=Markup(str(json2html.convert(json = r.text))))

@app.route('/modif_ope')
def modif_ope():
    r = requests.get('http://' + URL2 + '/operation/all')   
    data = """\
    exemple d'entree :     {
        "type": "virement",
        "ibansource": "FR7630224000031234567cdc885143",
        "ibandest": "FR76300040000987634567cdc890155",
        "montant": 1000,
        "date": "1995-12-10"
    }
    Votre nouveau compte en json
    <form action="modifier_ope" method="post">
    Json contenant les informations du compte a modifier
    <input type="text" name="compte_id"/><br/>
    identifiant du compte a modifier
    <input type="text" name="idd"/><br/>
    <input type="submit"/>
    </form>
    """
    return TPL("default.html", title="Suppresion d'un compte", delete_id=Markup(data), info=Markup(str(json2html.convert(json = r.text))))

@app.route('/modif_com')
def modif_com():
    r = requests.get('http://' + URL + '/compte/all')   
    data = """\
    exemple d'entree :         {
        "iban": "FR7630004000031234567cdc890143",
        "typedecompte": "courant",
        "interet": 0,
        "frais": "gratuit",
        "solde": 100
    }
    Votre nouveau compte en json
    <form action="modifier_ope" method="post">
    Json contenant les informations du compte a modifier
    <input type="text" name="compte_id"/><br/>
    identifiant du compte a modifier
    <input type="text" name="idd"/><br/>
    <input type="submit"/>
    </form>
    """
    return TPL("default.html", title="Suppresion d'un compte", delete_id=Markup(data), info=Markup(str(json2html.convert(json = r.text))))


@app.route('/formulaire')
def formulaire():
    data = """\
    Rechercher par ID
    <form action="validate" method="post">
    <input type="text" name="compte_id"/><br/>
    <input type="submit"/>
    </form>
    """
    data += """\
    Rechercher par IBAN
    <form action="validate1" method="post">
    <input type="text" name="compte_id"/><br/>
    <input type="submit"/>
    </form>
    """
    data += """\
    Rechercher par type
    <form action="validate2" method="post">
    <input type="text" name="compte_id"/><br/>
    <input type="submit"/>
    </form>
    """
    return TPL("default.html", title='Formulaire', data=Markup(data))


@app.route('/retrait_depot')
def retrait_depot():
    data = """\
    Depot
    <form action="depot" method="post">
    Montant
    <input type="text" name="montant"/><br/>
    compte id
    <input type="text" name="idd"/><br/>
    <input type="submit"/>
    </form>
    """
    data += """\
    Retrait
    <form action="retrait" method="post">
    montant
    <input type="text" name="montant"/><br/>
    compte id
    <input type="text" name="idd"/><br/>
    <input type="submit"/>
    </form>
    """
    return TPL("default.html", title='Formulaire', data=Markup(data))

@app.route('/formulaire2')
def formulaire2():
    data = """\
    Rechercher par ID
    <form action="validate_ope" method="post">
    <input type="text" name="compte_id"/><br/>
    <input type="submit"/>
    </form>
    """
    data += """\
    Rechercher par date
    <form action="validate1_ope" method="post">
    <input type="text" name="compte_id"/><br/>
    <input type="submit"/>
    </form>
    """
    data += """\
    Rechercher par type
    <form action="validate2_ope" method="post">
    <input type="text" name="compte_id"/><br/>
    <input type="submit"/>
    </form>
    """
    return TPL("default.html", title='Formulaire', data=Markup(data))
 
# Récupération des données d'un formulaire, en POST uniquement
# Si les données sont postées en json et non en 
# application/x-www-form-urlencoded ou multipart/form-data 
# utiliser flask.request.get_json()  au lieu
# de flask.request.form
@app.route('/validate_ope', methods=["POST"])
def validate_ope():
    compte_id = flask.request.form['compte_id']
    r = requests.get('http://' + URL2 + '/operation/byId/'+ compte_id)
    return TPL("default.html", title='Validate', data=Markup(str(json2html.convert(json = r.text))))

@app.route('/validate1_ope', methods=["POST"])
def validate1_ope():
    compte_id = flask.request.form['compte_id']
    r = requests.get('http://' + URL2 + '/operation/bydate?date='+ compte_id)
    return TPL("default.html", title='Validate', data=Markup(str(json2html.convert(json = r.text))))

@app.route('/validate2_ope', methods=["POST"])
def validate2_ope():
    compte_id = flask.request.form['compte_id']
    r = requests.get('http://' + URL2 + '/operation/byType/'+ compte_id)
    return TPL("default.html", title='Validate', data=Markup(str(json2html.convert(json = r.text))))

@app.route('/validate', methods=["POST"])
def validate():
    compte_id = flask.request.form['compte_id']
    r = requests.get('http://' + URL + '/compte/byId/'+ compte_id)
    return TPL("default.html", title='Validate', data=Markup(str(json2html.convert(json = r.text))))

@app.route('/validate1', methods=["POST"])
def validate1():
    compte_id = flask.request.form['compte_id']
    r = requests.get('http://' + URL + '/compte/byIban/'+ compte_id)
    return TPL("default.html", title='Validate', data=Markup(str(json2html.convert(json = r.text))))

@app.route('/validate2', methods=["POST"])
def validate2():
    compte_id = flask.request.form['compte_id']
    r = requests.get('http://' + URL + '/compte/byType/'+ compte_id)
    return TPL("default.html", title='Validate', data=Markup(str(json2html.convert(json = r.text))))

@app.route('/depot', methods=["POST"])
def depot():
    montant = flask.request.form['montant']
    idd = flask.request.form['idd']
    r = requests.get('http://' + URL2 + '/operation/deposer?montant='+ montant + '&id=' +idd)
    return TPL("default.html", title='Validate', data=Markup(str(json2html.convert(json = r.text))))

@app.route('/retrait', methods=["POST"])
def retrait():
    montant = flask.request.form['montant']
    idd = flask.request.form['idd']
    r = requests.get('http://' + URL2 + '/operation/retirer?montant='+ montant + '&id=' +idd)
    return TPL("default.html", title='Validate', data=Markup(str(json2html.convert(json = r.text))))

@app.route('/delete', methods=["POST"])
def delete():
	compte_id = flask.request.form['compte_id']
	montant = flask.request.form['montant']
	r = requests.put('http://' + URL + '/compte/retirer/'+ compte_id + "?montant=" + montant)
	res = requests.get('http://' + URL + '/compte/all')
	return TPL("default.html", title='Validate', data=Markup(str(json2html.convert(json = res.text))))

@app.route('/add', methods=["POST"])
def add():
	compte_id = flask.request.form['compte_id']
	montant = flask.request.form['montant']
	r = requests.put('http://' + URL + '/compte/retirer/'+ compte_id + "?montant=" + "-" + montant)
	res = requests.get('http://' + URL + '/compte/all')
	return TPL("default.html", title='Validate', data=Markup(str(json2html.convert(json = res.text))))
 
@app.route('/supprimer', methods=["POST"])
def supprimer():
	compte_id = flask.request.form['compte_id']
	r = requests.delete('http://' + URL + '/compte/supprimer/'+ compte_id)
	res = requests.get('http://' + URL + '/compte/all')
	return TPL("default.html", title='Validate', data=Markup(str(json2html.convert(json = res.text))))

@app.route('/creer', methods=["POST"])
def creer():
	compte_id = flask.request.form['compte_id']
	headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
	r = requests.post('http://' + URL + '/compte/creer/', data = compte_id,headers=headers)
	res = requests.get('http://' + URL + '/compte/all')
	return TPL("default.html", title="Creation compte", data=Markup(str(json2html.convert(json = res.text))))

@app.route('/modifier_ope', methods=["POST"])
def modifier_ope():
    compte_id = flask.request.form['compte_id']
    idd = flask.request.form['idd']
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    r = requests.put('http://' + URL2 + '/operation/MAJOperation/' + idd , data = compte_id,headers=headers)
    res = requests.get('http://' + URL2 + '/operation/all')
    return TPL("default.html", title="Creation compte", data=Markup(str(json2html.convert(json = res.text))))

@app.route('/modifier_com', methods=["POST"])
def modifier_com():
    compte_id = flask.request.form['compte_id']
    idd = flask.request.form['idd']
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    r = requests.put('http://' + URL + '/compte/MAJCompte/' + idd , data = compte_id,headers=headers)
    res = requests.get('http://' + URL + '/compte/all')
    return TPL("default.html", title="Creation compte", data=Markup(str(json2html.convert(json = res.text))))


# Code de retour :
# https://fr.wikipedia.org/wiki/Liste_des_codes_HTTP
@app.route('/virement')
def virement():
    r = requests.get('http://' + URL2 + '/operation/all')
    data = """\
        Ajouter une operation :
    <form action="addOperation" method="post">
    <input type="text" name="compte_id"/><br/>
    <input type="submit"/>
    </form>

    exemple d'entree :     {
        "type": "virement",
        "ibansource": "FR7630004000031234567cdc890143",
        "ibandest": "FR7630004000031234567cdc890155",
        "montant": 100,
        "date": "1995-12-10"
    }
    <br/>
     supprimer une operation :
    <form action="deleteOperation" method="post">
    <input type="text" name="operation_id"/><br/>
    <input type="submit"/>
    </form>

    """
    return TPL("default.html", title='Home', delete_id=Markup(data), info=Markup(str(json2html.convert(json = r.text))))

@app.route('/addOperation', methods=["POST"])
def addOperation():
    compte_id = flask.request.form['compte_id']
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    r = requests.post('http://' + URL2 + '/operation/creer/', data = compte_id,headers=headers)
    res = requests.get('http://' + URL2 + '/operation/all')
    return TPL("default.html", title="Creation compte", data=Markup(str(json2html.convert(json = res.text))))

@app.route('/deleteOperation', methods=["POST"])
def deleteOperation():
    operation_id = flask.request.form['operation_id']
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    r = requests.delete('http://' + URL2 + '/operation/supprimer/'+ operation_id)
    res = requests.get('http://' + URL2 + '/operation/all')
    return TPL("default.html", title="Creation compte", data=Markup(str(json2html.convert(json = res.text))))

@app.route('/faire_vir', methods=["POST"])
def faire_vir():
    id1 = flask.request.form['id']
    id2 = flask.request.form['idd']
    montant = flask.request.form['montant']
    req = 'http://' + URL2 + '/operation/virement' + "?montant=" + montant + "&id1=" + id1 + "&id2=" + id2
    r = requests.put(req)
    res = requests.get('http://' + URL + '/compte/all')
    return TPL("default.html", title='Validate', data=Markup(str(json2html.convert(json = res.text))))



@app.route('/redirect_me')
def redirect_me():
    return flask.redirect(flask.url_for('info'))

 
print("PATH =====>", app.instance_path)
if __name__ == '__main__':
    app.config['DEBUG'] = True
    app.secret_key = 'mysecretkey3*lezneri123445'
    app.run(host='0.0.0.0', port=5000)

    if __name__ == __main__:
    	app.run(debug=True)
