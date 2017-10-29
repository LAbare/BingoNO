#!/usr/bin/python
# coding: utf8

from __future__ import unicode_literals
import cgi, cgitb
cgitb.enable()

def detectBingo(result):
	bingos = ''
	grid = []
	rows = result.split('||')
	for y in range(0, len(rows)):
		grid.append([])
		cells = rows[y].split('|')
		for x in range(0, len(cells)):
			cell = cells[x].split(':')
			grid[y].append(int(cell[1]))
	
	#Colonnes
	columns = [0] * len(grid[0])
	#Diagonales
	diagNO = 0 #NO-SE
	diagSO = 0 #SO-NE
	#Lignes
	for y in range(0, len(grid)):
		if sum(grid[y]) == len(grid[y]):
			bingos += 'l-0:{}-{}:{}$'.format(y, len(grid[y]) - 1, y)
		for x in range(0, len(grid[y])):
			columns[x] += grid[y][x]
		if grid[y][y]: #x = y
			diagNO += 1
	for x in range(0, len(columns)):
		if columns[x] == len(grid):
			bingos += 'c-{}:0-{}:{}$'.format(x, x, len(grid) - 1)
		if grid[(len(grid) - 1) - x][x]: #Pour len(grid)=5: 4:0, 3:1, 2:2…
			diagSO += 1
	if diagNO == len(grid):
		bingos += 'ddo-0:0-{}:{}$'.format(len(columns) - 1, len(grid) - 1)
	if diagSO == len(grid):
		bingos += 'dup-0:{}-{}:0$'.format(len(grid) - 1, len(columns) - 1)
	return bingos[:-1]