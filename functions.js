function highlightBingos(bingos) {
	//C'est un poil le bordel, ça risque d'être retravaillé si on modifie l'affichage des cases bingo
	var reset = [].slice.call(document.getElementsByClassName('isbingo')); //slice.call, sinon l'array se modifie tout seul au cours de la boucle et bordel pas possible
	for (var i = 0; i < reset.length; i++) {
		reset[i].className = reset[i].className.replace(/ ?isbingo/, '');
	}
	for (var i = 0; i < bingos.length; i++) {
		var b = bingos[i].split('-');
		if (b.length < 3) {
			continue;
		}
		var type = b[0];
		var start = b[1].split(':');
		start = { x: start[0], y: start[1] };
		var end = b[2].split(':');
		end = { x: end[0], y: end[1] };

		switch (b[0]) {
			case 'l':
				var line = document.querySelectorAll('.bingo tr')[start.y].getElementsByTagName('td');
				for (var j = 0; j < line.length; j++) {
					var c = line[j];
					if (!(/isbingo/.test(c.className))) {
						c.className += ' isbingo';
					}
				}
				break;

			case 'c':
				var lines = document.querySelectorAll('.bingo tr');
				for (var j = 0; j < lines.length; j++) {
					var cells = lines[j].getElementsByTagName('td');
					var c = cells[start.x];
					if (!(/isbingo/.test(c.className))) {
						c.className += ' isbingo';
					}
				}
				break;

			case 'ddo':
				var lines = document.querySelectorAll('.bingo tr');
				for (var j = 0; j < lines.length; j++) {
					var cells = lines[j].getElementsByTagName('td');
					var c = cells[j];
					if (!(/isbingo/.test(c.className))) {
						c.className += ' isbingo';
					}
				}
				break;

			case 'dup':
				var lines = document.querySelectorAll('.bingo tr');
				for (var j = 0; j < lines.length; j++) {
					var cells = lines[j].getElementsByTagName('td');
					var c = cells[(lines.length - 1 - j)];
					if (!(/isbingo/.test(c.className))) {
						c.className += ' isbingo';
					}
				}
				break;
		}
	}
}


var cell_links = document.querySelectorAll('.bingo td a');
for (var i = 0; i < cell_links.length; i++) {
	cell_links[i].style.textDecoration = 'none';
	cell_links[i].setAttribute('onclick', 'return false;');
	cell_links[i].parentNode.style.cursor = 'pointer';
	cell_links[i].parentNode.addEventListener('click', function() {
		var cell = this;
		var link = cell.firstElementChild;
		var href = link.getAttribute('href');
		var set = href.match(/set=(0|1)/);
		if (set) {
			set = set[1];
		}
		var request = new XMLHttpRequest();
		request.open('GET', 'http://' + document.domain + '/BingoNO/' + href);
		request.onload = function() {
			var data = this.responseText;
			if (/OK/.test(data)) {
				if (set == '1') {
					cell.className = 'happened';
					link.setAttribute('href', href.replace('set=1', 'set=0'));
				}
				else {
					cell.className = '';
					link.setAttribute('href', href.replace('set=0', 'set=1'));
				}
				highlightBingos(data.split('$bingo$')[1].split('$'));
			}
			else {
				console.log(data);
			}
		};
		request.send(null);
		return false;
	});
}

highlightBingos(document.getElementById('bingoinfo').textContent.split('$'));