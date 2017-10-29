#!/usr/bin/python
# coding: utf8

from __future__ import unicode_literals
import cgi, cgitb
cgitb.enable()

import sys, os, random
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

login_ok = False
gratin = ""
parameters = cgi.FieldStorage()

#Connexion
passwd = parameters.getvalue('login')
tn = parameters.getvalue('tn')
if passwd:
	cursor.execute("SELECT * FROM bingoNO_admins WHERE Password = %s", (passwd))
	login_query = cursor.fetchone()
	if login_query:
		#Connexion réussie
		if tn and tn == login_query[0]:
			if not user.sid:
				user.createSID()
			cursor.execute("UPDATE bingoNO_admins SET SID = %s, LastLogin = %s WHERE Password = %s", (user.sid, str(datetime.now()), passwd))
			bdd.getBdd().commit()
			login_ok = True
			if not login_query[3]:
				gratin = "<p>Bienvenue au club !</p><img class='gratin' src='img/carte_gratin_bingo.png' />"

		#ID valide, on demande l'ID Twitter
		else:
			to_page("<!DOCTYPE html>")
			to_page("<head><title>Bingo de la Nuit Originale</title><meta charset='UTF-8' /><link href='css_admin.css' rel='stylesheet' type='text/css' /></head>")
			to_page("<body>")
			to_page("<h1>Connecxtion</h1>")
			silly_texts = ["Commander une pizza", "Faire une raclette", "Entrer dans le labo secret", "Cliquer sur le bouton suspect", "Élever des robinets dans le Jura", "Devenir maître du monde", "Envoyer de l'amour à tout l'Internet", "Prendre un café avec Karim Debbache"]
			silly_button = silly_texts[random.randint(0, len(silly_texts) - 1)]
			to_page("<p style='text-align: center;'>Entre ton ID Twitter pour te connecter au super labo secret du bingo :</p>")
			to_page("<form class='centerdiv' action='admin.py' method='post'>")
			to_page("<div class='loginline'><input type='text' name='tn' required /></div>")
			to_page("<input style='display: none;' type='text' name='login' value='{}' required />".format(passwd))
			to_page("<div onclick='wrongLever();'>{}</div> ou <input type='submit' value='Se connecter' />".format(silly_button))
			to_page("</form>")
			to_page("<div id='wrongLever'><img src='img/wrong_lever.png' alt='Wrong leveeeeeer…' /></div>")
			to_page("<script src='functions_admin.js'></script>")
			to_page("</body>")
			to_page("</html>")
			sys.exit()
	
	#ID non valides
	else:
		to_page("<!DOCTYPE html>")
		to_page("<head><title>Bingo de la Nuit Originale</title><meta charset='UTF-8' /><link href='css_admin.css' rel='stylesheet' type='text/css' /></head>")
		to_page("<body>")
		to_page("<p>Ce lien n'est pas ou plus valide. Il a rendu l'âme, n'a peut-être même jamais existé, et tu n'en vois maintenant que la pierre tombale nue et délaissée. Ci-gît {}, un simple numéro qui n'a pas trouvé sa place dans un monde de zéros et de uns. À qui la faute ? Une société qui rejette ses pions inutiles ? Une descente aux enfers sur le fil du rasoir ? Un hacker en herbe qui croyait pouvoir berner l'admin ? On ne le saura jamais. Paix à son âme.</p>".format(passwd))
		to_page("<p>Après ce bel hommage, tu peux t'en aller <a href='admin.py'>sur la page de connexion</a> ou <a href='/BingoNO/'>à l'accueil du bingo</a>.</p>")
		to_page("</body>")
		to_page("</html>")
		sys.exit()

elif user.sid:
	cursor.execute("SELECT * FROM bingoNO_admins WHERE SID = %s", (user.sid))
	login_query = cursor.fetchone()
	if login_query:
		cursor.execute("UPDATE bingoNO_admins SET LastLogin = %s WHERE SID = %s", (str(datetime.now()), user.sid))
		bdd.getBdd().commit()
		login_ok = True

if not login_ok:
	to_page("<!DOCTYPE html>")
	to_page("<head><title>Bingo de la Nuit Originale</title><meta charset='UTF-8' /><link href='css_admin.css' rel='stylesheet' type='text/css' /></head>")
	to_page("<body>")
	to_page("<p>Bravo, t'as trouvé la page admin. Mais bon, faut être admin, faut pas déconner. Si t'as pas reçu ton lien, tu peux <a href='/BingoNO/'>retourner à l'accueil du bingo</a>. Ou tu peux poireauter là et peut-être que dans dix mille ans les portes vont s'ouvrir toutes seules. Si Internet a pas fondu avant.</p>")
	to_page("</body>")
	to_page("</html>")
	sys.exit()


#Page d'administration
to_page("<!DOCTYPE html>")
to_page("<head><title>Bingo de la Nuit Originale</title><meta charset='UTF-8' /><link href='css_admin.css' rel='stylesheet' type='text/css' /></head>")
to_page("<body>")
to_page("<p><a href='/BingoNO/'>Retour au bingo</a></p>")
if gratin:
	to_page(gratin)
to_page("<p>Note : si les champs de texte foirent au rafraîchissement de la page, Ctrl+F5.</p>")

#Version
with open('version_info.txt', 'r') as versionFile:
	version = versionFile.read().strip()
to_page("<div class='admingroup'>")
to_page("<h2>Version du bingo</h2>")
to_page("<input type='text' value='{}' />".format(version))
to_page("<button onclick='update(this, \"version\");'>Changer la version</button>")
to_page("</div>")

#Gestion des cases
#bingoNO_cells: CellKey (int, AI, Primary), Cell, Happened (int), Validated (int), Version
cursor.execute("SELECT * FROM bingoNO_cells WHERE Validated = 1")
all_cells = cursor.fetchall()
to_page("<div class='admingroup'>")
to_page("<h2>Cases du bingo ({})</h2>".format(len(all_cells)))
to_page("<p>Note : possibilité que les gens proposent des cases, ce serait facile à implémenter<br />La checkbox 'Coché' sert juste à avoir des cases précochées si quelqu'un se crée une grille en cours de nuit, c'est pas un cochage général. Je sais pas si c'est utile, mais au m.</p>")
for cell in all_cells:
	checked = ''
	if cell[2]:
		checked = 'checked'
	to_page("<div class='cellline' data-id='{}'>".format(cell[0]))
	to_page("<input type='text' value='{}' />".format(cell[1].replace("'", "&#39;")))
	to_page("<label for='cellhappened-{}'>Coché : </label><input type='checkbox' name='cellhappened-{}' {} />".format(cell[0], cell[0], checked))
	to_page("<button onclick='celltest(this);'>Aperçu</button>")
	to_page("<button onclick='update(this, \"update_cell\");'>Mettre à jour</button>")
	to_page("<button onclick='update(this, \"delete_cell\");'>Supprimer</button>")
	to_page("</div><br />")
to_page("<div class='cellline addcell'>")
to_page("<input type='text' />")
to_page("<button onclick='celltest(this);'>Aperçu</button>")
to_page("<button onclick='update(this, \"add_cell\");'>Ajouter</button>")
to_page("</div>")
to_page("<br /><div id='celltest'>Case de test</div>")
to_page("</div>")


#Chevals : verbes
to_page("<div class='admingroup chevals'>")
to_page("<h2>Chevals : verbes</h2>")
to_page("<p><b>Structure :</b> <i>verbe:genre</i> (m, f, n=neutre)</p>")
with open('chevals/verbs.txt', 'r') as verbsFile:
	to_page("<textarea>{}</textarea>".format(verbsFile.read().decode('utf8')))
	to_page("<button data-type='verbs' onclick='update(this, \"update_chevals\");'>Mettre à jour</button>")
to_page("</div>")

#Chevals : noms
to_page("<div class='admingroup chevals'>")
to_page("<h2>Chevals : noms</h2>")
to_page("<p><b>Structure :</b> <i>nom:genre</i> (si élision (« D'Artichaut ») : <i>nom:genre:elide</i>)</p>")
with open('chevals/names.txt', 'r') as namesFile:
	to_page("<textarea>{}</textarea>".format(namesFile.read().decode('utf8')))
	to_page("<button data-type='names' onclick='update(this, \"update_chevals\");'>Mettre à jour</button>")
to_page("</div>")

#Chevals : adjectifs
to_page("<div class='admingroup chevals'>")
to_page("<h2>Chevals : adjectifs</h2>")
to_page("<p><b>Structure :</b> si neutre : <i>adjectif</i> ; si genré : <i>masculin:féminin</i></p>")
with open('chevals/adj.txt', 'r') as adjFile:
	to_page("<textarea>{}</textarea>".format(adjFile.read().decode('utf8')))
	to_page("<button data-type='adj' onclick='update(this, \"update_chevals\");'>Mettre à jour</button>")
to_page("</div>")

#Chevals : adverbes
to_page("<div class='admingroup chevals'>")
to_page("<h2>Chevals : adverbes</h2>")
to_page("<p><b>Structure :</b> si neutre : <i>adjectif</i> ; si genré : <i>masculin:féminin</i></p>")
with open('chevals/adv.txt', 'r') as advFile:
	to_page("<textarea>{}</textarea>".format(advFile.read().decode('utf8')))
	to_page("<button data-type='adv' onclick='update(this, \"update_chevals\");'>Mettre à jour</button>")
to_page("</div>")


to_page("<script src='functions_admin.js'></script>")
to_page("</body>")
to_page("</html>")