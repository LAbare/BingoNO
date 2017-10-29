#!/usr/bin/python
# coding: utf8

from __future__ import unicode_literals
import cgi, cgitb
cgitb.enable()

import os, Cookie, datetime, random
import bddHeader
bdd = bddHeader.bdd()
cursor = bdd.getCursor()
import generateName
to_page = bddHeader.to_page


class UserInfo:
	def __init__(self, cursor):
		self.sid = ''
		self.infos = None
		try:
			self.cookie = Cookie.SimpleCookie(os.environ["HTTP_COOKIE"])
		except Cookie.CookieError:
			self.cookie = Cookie.SimpleCookie()
		if b"BingoNO_SID" in self.cookie and self.cookie[b"BingoNO_SID"].value != '':
			self.sid = self.cookie[b"BingoNO_SID"].value
			cursor.execute("SELECT * FROM bingoNO_grids WHERE SID = %s", (self.sid))
			self.infos = cursor.fetchone()
			if self.infos == None:
				self.sid = '' #Pas de SID correspondant dans la base
	
	def createSID(self):
		new_sid = ''
		for i in range(0, 64):
			new_sid += "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"[random.randint(0, 35)]
		self.sid = new_sid
		#Byte strings partouuuuuuuuuut sinon ça plante
		self.cookie[b"BingoNO_SID"] = str(new_sid)
		self.cookie[b"BingoNO_SID"][b"domain"] = b"labare.net"
		self.cookie[b"BingoNO_SID"][b"path"] = b"/"
		self.cookie[b"BingoNO_SID"][b"expires"] = str((datetime.datetime.now() + datetime.timedelta(days=365)).strftime("%a, %d-%b-%Y %H:%M:%S UTC"))
		
		#Récupération de la version et des cases disponibles
		with open('version_info.txt', 'r') as version_file:
			version = version_file.read().strip()
		all_cells = {}
		cursor.execute("SELECT * FROM bingoNO_cells WHERE Validated = 1") #0: CellKey (AI), 1: Cell, 2: Happened (int), 3: Validated (int), 4: Version
		cells_query = cursor.fetchall()
		for cell in cells_query:
			all_cells[cell[0]] = { 'content': cell[1], 'happened': cell[2] }
		
		#Génération d'une grille
		if version != 'closed': #version:closed = période de propositions, pas de génération de grilles possible
			#Génération d'un nom
			name_ok = False
			while not name_ok:
				grid_name = generateName.generateName()
				cursor.execute("SELECT * FROM bingoNO_grids WHERE Name = %s", (grid_name.encode('utf8')))
				if cursor.fetchone() == None:
					name_ok = True
			
			#Génération d'une grille	
			shuffled = all_cells.keys()
			if len(shuffled) < 25:
				shuffled += [-1] * (25 - len(all_cells))
				all_cells[-1] = { 'content': "L'admin a pas mis assez de cases", 'happened': 1 }
			random.shuffle(shuffled)
			i = 0
			result = ""
			for y in range(0, 5):
				for x in range(0, 5):
					result += str(shuffled[i])
					result += ":" + str(all_cells[shuffled[i]]['happened']) #:0 ou :1
					result += "|"
					i += 1
				result += "|"
			result = result[:-2]
			
			cursor.execute("INSERT INTO bingoNO_grids(Name, Version, Content, SID) VALUES(%s, %s, %s, %s)", (grid_name.encode('utf8'), version, result, self.sid))
			bdd.getBdd().commit()
			self.infos = (grid_name, version, result, self.sid)
	
	def getSID(self):
		return self.cookie.output()

#Test
if __name__ == "__main__":
	u = UserInfo(cursor)
	to_page("Content-type: text/html; charset=utf-8\n\n")
	if not u.sid:
		u.createSID()
		to_page(u.getSID())
		to_page("\nOK\nNew SID : " + u.sid)
	else:
		to_page("\n")
		to_page("SID : " + u.sid)