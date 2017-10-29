#!/usr/bin/python
# coding: utf8

from __future__ import unicode_literals

class Logins:
	def __init__(self):
		self.host = "" #Adresse de la BDD
		self.dbname = "" #Nom de la BDD
		self.name = "" #Nom d'utilisateur
		self.passwd = "" #Mot de passe, encodé en base64 juste pour qu'on puisse pas le lire par-dessus l'épaule (le décodage se fait dans bddHeader.py)