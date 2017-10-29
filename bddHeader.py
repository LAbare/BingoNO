#!/usr/bin/python
# coding: utf8

from __future__ import unicode_literals
import cgi, cgitb
cgitb.enable()

import MySQLdb, base64
from logins import Logins

def to_page(string):
	print(string.encode('utf8'))

class bdd:
	def __init__(self):
		self.login = Logins()
		self.bdd = MySQLdb.connect(host=self.login.host, user=self.login.name, passwd=base64.b64decode(self.login.passwd), db=self.login.dbname, charset='utf8', use_unicode=True)
		self.cursor = self.bdd.cursor()
	
	def getCursor(self):
		return self.cursor
	
	def getBdd(self):
		return self.bdd

if __name__ == "__main__":
	bdd()
	to_page("Content-type: text/html; charset=utf-8\n\nOK, test réussi")