#!/usr/bin/python
# coding: utf8

from __future__ import unicode_literals
import cgi, cgitb
cgitb.enable()

import random

def generateName():
	verbs = [] #{ 'value': "Vole", 'gender': 'n' }
	with open('chevals/verbs.txt', 'r') as verbsFile:
		for line in verbsFile:
			verb = line.strip().decode('utf8').split(':')
			verbs.append({ 'value': verb[0], 'gender': verb[1] })

	names = [] #{ 'value': "Nuit", 'gender': 'f' }, #{ 'value': "Oignon", 'gender': 'm', 'elide': True }
	with open('chevals/names.txt', 'r') as namesFile:
		for line in namesFile:
			name = line.strip().decode('utf8').split(':')
			if len(name) == 3:
				names.append({ 'value': name[0], 'gender': name[1], 'elide': True })
			else:
				names.append({ 'value': name[0], 'gender': name[1] })

	adj = [] #{ 'n': "Sexy" }, #{ 'm': "Soyeux", 'f': "Soyeuse" }
	with open('chevals/adj.txt', 'r') as adjFile:
		for line in adjFile:
			ad = line.strip().decode('utf8').split(':')
			if len(ad) == 2:
				adj.append({ 'm': ad[0], 'f': ad[1] })
			else:
				adj.append({ 'n': ad[0] })

	adv = [] #{ 'n': "Super" }, #{ 'm': "Tout", 'f': "Toute" }
	with open('chevals/adv.txt', 'r') as advFile:
		for line in advFile:
			av = line.strip().decode('utf8').split(':')
			if len(av) == 2:
				adv.append({ 'm': av[0], 'f': av[1] })
			else:
				adv.append({ 'n': av[0] })
	
	horse = ""
	first_word = {}
	
	dice = random.randint(1, 3)
	
	while horse == "" or len(horse) > 18:
		if dice < 3: #Premier mot : nom
			first_word = names[random.randint(0, len(names) - 1)]
			horse = first_word['value']

			if dice == 1: #NomDeNom
				second_word = {}
				while second_word == {} or second_word == first_word:
					second_word = names[random.randint(0, len(names) - 1)]
				if 'elide' in second_word:
					horse += "D'" + second_word['value']
				else:
					horse += "De" + second_word['value']

			else: #Nom(Adverbe)Adjectif
				#On définit un genre si le nom est neutre
				if first_word['gender'] == 'n':
					if random.random() < 0.5:
						first_word['gender'] = 'm'
					else:
						first_word['gender'] = 'f'

				#Adverbe (ne pas mettre de seuil trop bas vu que pas mal de résultats seront trop longs)
				if random.random() < 0.4:
					adverb = adv[random.randint(0, len(adv) - 1)]
					if 'n' in adverb:
						horse += adverb['n']
					else:
						horse += adverb[first_word['gender']]

				#Recherche d'adjectif
				second_word = adj[random.randint(0, len(adj) - 1)]
				if 'n' in second_word:
					horse += second_word['n']
				else:
					horse += second_word[first_word['gender']]

		else: #Premier mot : verbe = Verbe-Nom
			first_word = verbs[random.randint(0, len(verbs) - 1)]
			if first_word['gender'] != 'n': #Préfixes non-neutres
				second_word = names[random.randint(0, len(names) - 1)]
				while second_word['gender'] != 'n' and second_word['gender'] != first_word['gender']:
					second_word = names[random.randint(0, len(names) - 1)]
			else:
				second_word = names[random.randint(0, len(names) - 1)]
			horse = first_word['value'] + "-" + second_word['value']
	
	return horse


if __name__ == "__main__":
	print("Content-type: text/html; charset=utf-8\n\n" + generateName().encode('utf8'))