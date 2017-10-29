#!/usr/bin/python
# coding: utf8

from __future__ import unicode_literals
import cgi, cgitb
cgitb.enable()

import sys, locale
from datetime import datetime

import bddHeader
from user import UserInfo
to_page = bddHeader.to_page

#bingoNO_admins: Name (Primary), Password, SID, LastLogin
#bingoNO_grids: Name (Primary), Version, Content, SID
#bingoNO_cells: CellKey (int, AI, Primary), Cell, Happened (int), Validated (int), Version


to_page("Content-type: text/html; charset=utf-8\n")

bdd = bddHeader.bdd()
cursor = bdd.getCursor()
user = UserInfo(cursor)

#Test de connexion
login_ok = False
if user.sid:
	cursor.execute("SELECT * FROM bingoNO_admins WHERE SID = %s", (user.sid))
	login_query = cursor.fetchone()
	if login_query:
		login_ok = True
		cursor.execute("UPDATE bingoNO_admins SET LastLogin = %s WHERE SID = %s", (str(datetime.now()), user.sid))
		bdd.getBdd().commit()

if not login_ok:
	to_page("Erreur : accès non autorisé")
	sys.exit()


#Paramètres
parameters = cgi.FieldStorage()
action = parameters.getvalue('action')

def getParam(param):
	p = parameters.getvalue(param)
	if not p:
		to_page("Erreur : paramètre '{}' manquant".format(param))
		sys.exit()
	return p


if action == "version":
	version = getParam('version')
	with open('version_info.txt', 'w') as versionFile:
		versionFile.write(version)
	to_page("OK")


elif action == "update_cell":
	cell_id = getParam('cell_id')
	content = getParam('content')
	checked = getParam('checked')
	if checked == 'true':
		checked = 1
	else:
		checked = 0
	try:
		cell_id = int(cell_id)
	except:
		to_page("Erreur : ValueError")
		sys.exit()
	cursor.execute("UPDATE bingoNO_cells SET Cell = %s, Happened = %s WHERE CellKey = %s", (content, checked, cell_id))
	bdd.getBdd().commit()
	to_page("OK")

elif action == "delete_cell":
	cell_id = getParam('cell_id')
	try:
		cell_id = int(cell_id)
	except:
		to_page("Erreur : ValueError")
		sys.exit()
	cursor.execute("UPDATE bingoNO_cells SET Validated = 0 WHERE CellKey = %s", (cell_id))
	bdd.getBdd().commit()
	to_page("OK")

elif action == "add_cell":
	content = getParam('content')
	with open('version_info.txt', 'r') as versionFile:
		version = versionFile.read().strip()
	#bingoNO_cells: CellKey (int, AI, Primary), Cell, Happened (int), Validated (int), Version
	cursor.execute("INSERT INTO bingoNO_cells(Cell, Happened, Validated, Version) VALUES(%s, %s, %s, %s)", (content, 0, 1, version))
	bdd.getBdd().commit()
	cursor.execute("SELECT * FROM bingoNO_cells WHERE Cell = %s ORDER BY CellKey DESC", (content))
	newid = cursor.fetchone()
	to_page("OK$" + str(newid[0]))


elif action == "chevals":
	chevals_type = getParam('type')
	content = getParam('content').decode('utf8').split("\n")
	
	if chevals_type not in ('verbs', 'names', 'adj', 'adv'):
		to_page("Erreur : ce type de cheval n'existe pas")
		sys.exit()
	
	locale.setlocale(locale.LC_ALL, str("fr_FR.UTF-8")) #str car setlocale attend une chaîne non-unicode (fuck la logique)
	content.sort(cmp=locale.strcoll) #Sinon les lettres accentuées foirent et viennent après Z
	content = "\n".join(content)
	with open('chevals/' + chevals_type + '.txt', 'w') as chevalsFile:
		chevalsFile.write(content.encode('utf8'))
	to_page("OK$" + content)

else:
	to_page("Erreur : action non reconnue")