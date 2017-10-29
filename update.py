#!/usr/bin/python
# coding: utf8

from __future__ import unicode_literals
import cgi, cgitb
cgitb.enable()

import sys
import bddHeader
from user import UserInfo
import detectBingo
to_page = bddHeader.to_page

bdd = bddHeader.bdd()
cursor = bdd.getCursor()
user = UserInfo(cursor)

#Récupération et typage des paramètres
grid_name = cgi.FieldStorage().getvalue('name')
grid_x = cgi.FieldStorage().getvalue('x')
grid_y = cgi.FieldStorage().getvalue('y')
grid_set = cgi.FieldStorage().getvalue('set')
if not grid_name or not grid_x or not grid_y or not grid_set:
	to_page("Content-type: text/html; charset=utf-8\n\nErreur : paramètres manquants")
	sys.exit()
grid_name = grid_name.decode('utf8')
grid_x = int(grid_x)
grid_y = int(grid_y)
if grid_set != '1':
	grid_set = '0'

#Vérification de la grille
cursor.execute("SELECT * FROM bingoNO_grids WHERE Name = %s", (grid_name))
grid_query = cursor.fetchone() #grid_query: (grid_name, version, result, sid)
if grid_query == None:
	to_page("Content-type: text/html; charset=utf-8\n\nErreur : grille inexistante")
	sys.exit()
if grid_query[3] != user.sid:
	to_page("Content-type: text/html; charset=utf-8\n\nErreur : accès non autorisé")
	sys.exit()

#Modification de la grille avant envoi
updated = False
result = ''
r = grid_query[2].split("||")
for y in range(0, len(r)):
	row = r[y].split("|")
	for x in range(0, len(row)):
		if x == grid_x and y == grid_y:
			updated = True
			c = row[x].split(':')
			result += c[0] + ':' + grid_set + '|'
		else:
			result += row[x] + '|'
	result += '|'
result = result[:-2]
if not updated:
	to_page("Content-type: text/html; charset=utf-8\n\nErreur : case hors de la grille")
	sys.exit()


cursor.execute("UPDATE `bingoNO_grids` SET `Content`=%s WHERE `SID`=%s", (result.encode('utf8'), user.sid.encode('utf8')))
bdd.getBdd().commit()
to_page("Content-type: text/html; charset=utf-8\n\nOK")
to_page('$bingo$' + detectBingo.detectBingo(result))