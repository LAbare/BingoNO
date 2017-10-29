#!/usr/bin/python
# coding: utf8

from __future__ import unicode_literals
import cgi, cgitb
cgitb.enable()

import sys
import bddHeader
import detectBingo
to_page = bddHeader.to_page

cursor = bddHeader.bdd().getCursor()


def printGrid(version, cells_info, grid_info, is_own_grid):
	#grid_info: (grid_name, version, result, user.sid)
	if str(version) != str(grid_info[1]):
		to_page("<p>Cette grille de bingo date de la Nuit Originale n°{}.</p>".format(grid_info[1]))
	to_page("<h3>Grille " + grid_info[0] + "</h3>")
	to_page("<p><a href='http://labare.net/BingoNO/{}'>Lien vers la grille</a> — <a href='http://labare.net/BingoNO/{}.png'>Lien vers l'image</a></p>".format(grid_info[0], grid_info[0]))
	
	to_page("<table class='bingo'>")
	r = grid_info[2].split("||")
	for y in range(0, len(r)):
		to_page("<tr>")
		row = r[y].split("|")
		for x in range(0, len(row)):
			c = row[x].split(':')
			cell = cells_info[int(c[0])]
			if int(c[1]):
				if is_own_grid:
					to_page("<td data-pos='{}:{}' class='happened'><a href='update.py?name={}&x={}&y={}&set=0'>{}</a></td>".format(x, y, grid_info[0], x, y, cell['content']))
				else:
					to_page("<td data-pos='{}:{}' class='happened'>{}</td>".format(x, y, cell['content']))
			else:
				if is_own_grid:
					to_page("<td data-pos='{}:{}'><a href='update.py?name={}&x={}&y={}&set=1'>{}</a></td>".format(x, y, grid_info[0], x, y, cell['content']))
				else:
					to_page("<td data-pos='{}:{}'>{}</td>".format(x, y, cell['content']))
		to_page("</tr>")
	to_page("</table>")
	to_page("<div id='bingoinfo'>" + detectBingo.detectBingo(grid_info[2]) + "</div>")



if __name__ == "__main__":
	import os, Cookie, datetime, random
	from user import UserInfo
	user = UserInfo(cursor)
	query = cgi.FieldStorage().getvalue('name')
	if query:
		query = query.decode('utf8')
	else:
		to_page("Content-type: text/html; charset=utf-8\n")
		to_page("<!DOCTYPE html>")
		to_page("<head><title>Bingo de la Nuit Originale</title><meta charset='UTF-8' /><link href='css.css' rel='stylesheet' type='text/css' /></head>")
		to_page("<body>")
		to_page("<p style='text-align: center;'>Ça ne marchera pas si tu ne donnes pas de nom.<br /><a href='/BingoNO/'>Accueil</a></p>")
		to_page("</body>")
		to_page("</html>")
		sys.exit()
	
	#Récupération de la version et des cases disponibles
	with open('version_info.txt', 'r') as version_file:
		version = version_file.read().strip()
	all_cells = {
		-1: { 'content': "L'admin a pas mis assez de cases", 'happened': 1 }
	}
	cursor.execute("SELECT * FROM bingoNO_cells WHERE Validated = 1") #0: CellKey (AI), 1: Cell, 2: Happened (int), 3: Validated (int), 4: Version
	cells_query = cursor.fetchall()
	for cell in cells_query:
		all_cells[cell[0]] = { 'content': cell[1], 'happened': cell[2] }
	
	cursor.execute("SELECT * FROM bingoNO_grids WHERE Name = %s", (query))
	grid_query = cursor.fetchone()
	if grid_query == None:
		to_page("Content-type: text/html; charset=utf-8\n")
		to_page("<!DOCTYPE html>")
		to_page("<head><title>Bingo de la Nuit Originale</title><meta charset='UTF-8' /><link href='css.css' rel='stylesheet' type='text/css' /></head>")
		to_page("<body>")
		to_page("<p style='text-align: center;'>Cette grille n'existe pas.<br /><a href='/BingoNO/'>Accueil</a></p>")
		to_page("</body>")
		to_page("</html>")
		sys.exit()
	is_own_grid = False
	if user.sid == grid_query[3]:
		is_own_grid = True
	
	to_page("Content-type: text/html; charset=utf-8\n")
	to_page("<!DOCTYPE html>")
	to_page("<head><title>Bingo de la Nuit Originale n°{}</title><meta charset='UTF-8' /><link href='css.css' rel='stylesheet' type='text/css' /></head>".format(grid_query[1]))
	to_page("<body>")
	printGrid(version, all_cells, grid_query, is_own_grid)
	to_page("<script src='functions.js'></script>")
	to_page("</body>")
	to_page("</html>")