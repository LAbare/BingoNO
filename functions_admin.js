function wrongLever() {
	document.getElementById('wrongLever').style.display = 'block';
	return false;
}

function update(el, action) {
	var cells = document.querySelectorAll('.cellline:not(.addcell)');
	for (var i = 0; i < cells.length; i++) {
		cells[i].style.backgroundColor = '#EC6';
	}
	var func = null;
	var params = '';
	if (action == 'version') {
		el.textContent = "Changer la version (…)";
		var v = el.previousElementSibling.value;
		params = 'action=' + action + '&version=' + encodeURIComponent(v);
		func = function() {
			var data = this.responseText;
			if (/OK/.test(data)) {
				el.textContent = "Changer la version (OK)";
			}
			else {
				el.textContent = "Changer la version (Erreur)";
			}
		};
	}
	else if (action == 'update_cell') {
		var line = el.parentNode;
		var text = line.querySelector('input[type="text"]').value;
		var checked = line.querySelector('input[type="checkbox"]').checked;
		line.style.backgroundColor = '#EC6';
		params = 'action=update_cell&cell_id=' + line.getAttribute('data-id') + '&content=' + encodeURIComponent(text) + '&checked=' + checked;
		func = function() {
			var data = this.responseText;
			if (/OK/.test(data)) {
				line.style.backgroundColor = '#6E6';
			}
			else {
				line.style.backgroundColor = '#E66';
			}
		};
	}
	else if (action == 'delete_cell') {
		var line = el.parentNode;
		var text = line.querySelector('input[type="text"]').value;
		line.style.backgroundColor = '#EC6';
		if (confirm("Supprimer la case « " + text + " » ?")) {
			params = 'action=delete_cell&cell_id=' + line.getAttribute('data-id');
			func = function() {
				var data = this.responseText;
				if (/OK/.test(data)) {
					line.parentNode.removeChild(line.previousElementSibling); //<br />
					line.parentNode.removeChild(line);
				}
				else {
					line.style.backgroundColor = '#E66';
				}
			};
		}
	}
	else if (action == 'add_cell') {
		//bingoNO_cells: CellKey (int, AI, Primary), Cell, Happened (int), Validated (int), Version
		var line = el.parentNode;
		var text = line.querySelector('input[type="text"]').value;
		line.style.backgroundColor = '#BFB';
		params = 'action=add_cell&content=' + encodeURIComponent(text);
		func = function() {
			var data = this.responseText;
			if (/OK/.test(data)) {
				//Ajout d'une nouvelle ligne avec les valeurs entrées (text) et reçues (newid)
				line.querySelector('input[type="text"]').value = '';
				var newid = data.split('$')[1];
				var newline = document.createElement('div');
				newline.className = 'cellline';
				newline.setAttribute('data-id', newid);
				newline.style.backgroundColor = '#6E6';
				
				var input = document.createElement('input');
				input.setAttribute('type', 'text');
				input.setAttribute('value', text);
				newline.appendChild(input);
				newline.innerHTML += "\n";
				
				var label = document.createElement('label');
				label.setAttribute('for', 'cellhappened-' + newid);
				label.textContent = "Coché : ";
				newline.appendChild(label);
				
				var checkbox = document.createElement('input');
				checkbox.setAttribute('type', 'checkbox');
				checkbox.setAttribute('name', 'cellhappened-' + newid);
				newline.appendChild(checkbox);
				newline.innerHTML += "\n";
				
				var butpreview = document.createElement('button');
				butpreview.setAttribute('onclick', 'celltest(this);');
				butpreview.textContent = "Aperçu";
				newline.appendChild(butpreview);
				newline.innerHTML += "\n";
				
				var butupdate = document.createElement('button');
				butupdate.setAttribute('onclick', 'update(this, "update_cell");');
				butupdate.textContent = "Mettre à jour";
				newline.appendChild(butupdate);
				newline.innerHTML += "\n";
				
				var butdelete = document.createElement('button');
				butdelete.setAttribute('onclick', 'update(this, "delete_cell");');
				butdelete.textContent = "Supprimer";
				newline.appendChild(butdelete);
				
				line.parentNode.insertBefore(newline, line);
				line.parentNode.insertBefore(document.createElement('br'), line);
			}
			else {
				line.style.backgroundColor = '#E66';
			}
		};
	}
	else if (action == 'update_chevals') {
		el.textContent = "Mettre à jour (…)";
		var type = el.getAttribute('data-type');
		var textarea = el.previousElementSibling;
		if (type == 'names') {
			var names = textarea.value.split("\n");
			var check = [];
			//Test pour rappeler les éventuels noms à élider
			for (var i = 0; i < names.length; i++) {
				if ("AÂÄEÉÈÊËHIÎÏOÔÖUÛÜY".indexOf(names[i][0]) != -1 && !(/:elide$/.test(names[i]))) {
					check.push(names[i]);
				}
			}
			if (check.length) {
				if (!confirm("Les mots " + check.join(";") + " pourraient avoir besoin du drapeau ':elide'. 'Annuler' pour modifier, 'OK' si tout est bon.")) {
					el.textContent = "Mettre à jour";
					return false;
				}
			}
		}
		params = 'action=chevals&type=' + type + '&content=' + encodeURIComponent(textarea.value);
		func = function() {
			var data = this.responseText;
			if (/OK/.test(data)) {
				textarea.value = data.split('$')[1];
				el.textContent = "Mettre à jour (OK)";
			}
			else {
				el.textContent = "Mettre à jour (Erreur)";
			}
		};
	}
	
	
	var request = new XMLHttpRequest();
	request.open('POST', 'http://' + document.domain + '/BingoNO/admin_update.py', true);
	request.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
	request.onload = func;
	request.send(params);
}

function celltest(el) {
	var c = document.getElementById('celltest');
	c.innerHTML = el.parentNode.querySelector('input[type="text"]').value;
	//On se laisse quand même une marge de 10px avant d'alerter
	if (c.clientWidth > 110) {
		alert("La case dépasse de " + (c.clientWidth - 100) + " pixels en largeur.")
	}
	if (c.clientHeight > 110) {
		alert("La case dépasse de " + (c.clientHeight - 100) + " pixels en hauteur.")
	}
}