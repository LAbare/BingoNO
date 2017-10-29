#!/usr/bin/python
# coding: utf8

from __future__ import unicode_literals
import cgi, cgitb
cgitb.enable()

import random

import bddHeader
from user import UserInfo
import generateName
import getGrid
to_page = bddHeader.to_page

#bingoNO_admins: Name, Password, SID
#bingoNO_grids: Name, Version, Content, SID
#bingoNO_cells: CellKey (int, AI), Cell, Happened (int), Validated (int), Version


to_page("Content-type: text/html; charset=utf-8")

bdd = bddHeader.bdd()
cursor = bdd.getCursor()
user = UserInfo(cursor)


#Récupération de la version et des cases disponibles
with open('version_info.txt', 'r') as versionFile:
	version = versionFile.read().strip()
all_cells = {
	-1: { 'content': "L'admin a pas mis assez de cases", 'happened': 1 }
}
cursor.execute("SELECT * FROM bingoNO_cells WHERE Validated = 1") #0: CellKey (AI), 1: Cell, 2: Happened (int), 3: Validated (int), 4: Version
cells_query = cursor.fetchall()
for cell in cells_query:
	all_cells[cell[0]] = { 'content': cell[1], 'happened': cell[2] }


if user.sid != '':
	to_page("\n") #Sortie des headers
else:
	#Génération de cookie SID et d'une grille
	user.createSID()
	to_page(user.getSID())
	to_page("\n") #Sortie des headers


no = ""
if version != 'closed':
	no = " n°" + version
to_page("<!DOCTYPE html>")
to_page("<head><title>Bingo de la Nuit Originale" + no + "</title><meta charset='UTF-8' /><link href='css.css' rel='stylesheet' type='text/css' /></head>")
to_page("<body>")
getGrid.printGrid(version, all_cells, user.infos, True)
to_page("<script src='functions.js'></script>")
to_page("</body>")
to_page("</html>")
	