#!/usr/local/bin/python3.3
# -*- coding: utf-8 -*-

#BI-PYT
#Semestralni projekt
#Dekoder grafickeho formatu PNG
#FIT CVUT LS 2012/2013
#
#Autor: Petr Chmelar (chmelpe7)
#E-mail: chmelpe7@fit.cvut.cz
#
#Zdroje:
#http://docs.python.org
#http://vyuka.ookami.cz/@CVUT_2012+13-LS_BI-PYT/
#http://vyuka.ookami.cz/@CVUT_2012+13-LS_BI-SKJ/

import os
import sys
import zlib
import math
from argparse import ArgumentParser

class PNGWrongHeaderError(Exception):
	"""Výjimka oznamující, že načítaný soubor zřejmě není PNG-obrázkem."""
	pass

class PNGNotImplementedError(Exception):
	"""Výjimka oznamující, že PNG-obrázek má strukturu, kterou neumíme zpracovat."""
	pass

class PngReader():
	"""Třída pro práci s PNG-obrázky."""
    
	def __init__(self, filepath):
        
        # RGB-data obrázku jako seznam seznamů řádek,
        #   v každé řádce co pixel, to trojce (R, G, B)
		self.rgb = []

        #nacteni dat PNG souboru
		self.data = []
		with open(filepath, 'rb') as stream:
			while stream.peek():
				self.data.append(stream.read(1))

		#kontrola hlavicky PNG souboru
		self.header = self.parser(self.data,0,8)
		if self.header != b'\x89\x50\x4E\x47\x0D\x0A\x1A\x0A':
			raise PNGWrongHeaderError

		#kontrola datove casti IHDR chunku
		self.ihdr = self.parser(self.data,16,29)
		if self.ihdr[8:] != b'\x08\x02\x00\x00\x00':
			raise PNGNotImplementedError

		#ziskani vysky/sirky PNG souboru
		self.width = self.BE_convert(self.data,16)
		self.height = self.BE_convert(self.data,20)

		#vyriznuti vsech IDAT chunku
		#predpoklada navaznost IDAT chunku
		#33 = 8 (PNG hlavicka) + 25 (IHDR)
		#12 = velikost IEND
		self.idat = self.data[33:-12]

		#slozeni datovych casti vice IDAT chunku
		self.idat_data = self.IDAT_merge()

		#dekomprese
		self.idat_decompress = zlib.decompress(self.idat_data)

		#nahrani dekompresovanych dat do seznamu
		rgb_temp = []
		for i in range(0,len(self.idat_decompress)):
			rgb_temp.append(self.idat_decompress[i])

		#ulozeni radkovych filtru
		self.filters = []
		delete = []
		for i in range(0,len(self.idat_decompress),(self.width*3)+1):
			self.filters.append(rgb_temp[i])
			delete.append(i)

		#vymazani filtru ze seznamu
		for i in range(len(delete)-1,-1,-1):
			del(rgb_temp[delete[i]])

		#utvoreni n-tic a ulozeni do self.rgb
		rgb_row = []
		for i in range(0,len(rgb_temp)+1,3):
			rgb_row.append(tuple(rgb_temp[i:i+3]))
			if len(rgb_row) == self.width:
				self.rgb.append(rgb_row)
				rgb_row = []

		#aplikace filtru
		for i in range(0,self.height):
			if self.filters[i] == 0: #none
				pass
			elif self.filters[i] == 1: #sub
				self.filter_sub(i)
			elif self.filters[i] == 2: #up
				self.filter_up(i)
			elif self.filters[i] == 3: #average
				self.filter_average(i)
			elif self.filters[i] == 4: #paeth
				self.filter_paeth(i) 

	#vyparsovani pozadovane casti a spojeni do binarniho retezce
	def parser(self,data,start,end):
		s = b""
		for i in range(start,end):
			s += data[i]
		return s

	#spojeni datovych casti vice IDAT chunku
	def IDAT_merge(self):
		data = b""
		start = 8 #8 = delka a typ aktualniho
		while(start < len(self.idat)):
			end = start + self.BE_convert(self.idat,start-8) 
			data += self.parser(self.idat,start,end)
			start = end + 12 #12 = 4 (kontrolniho soucet predchoziho) + 8 (delka a typ aktualniho)
		return data

	#slozeni 4B cisla ulozeneho v BigEndianu
	def BE_convert(self,data,start):
		num = ord(data[start]) * 16777216
		num += ord(data[start+1]) * 65536
		num += ord(data[start+2]) * 256
		num += ord(data[start+3])
		return num

	#funkce secte prvky dvou triprvkovych ntic
	def tuples_sum(self,a,b):
		c = (a[0] + b[0], a[1] + b[1], a[2] + b[2])
		return c

	#funkce odecte prvky dvou triprvkovych ntic
	def tuples_sub(self,a,b):
		c = (a[0] - b[0], a[1] - b[1], a[2] - b[2])
		return c

	#funkce vydeli vsechny prvky triprvkove ntice
	def tuples_div(self,a,div):
		c = (math.floor(a[0] / div), math.floor(a[1] / div), math.floor(a[2] / div))
		return c

	#funkce provede modulo vsech prvku triprvkove ntice
	def tuples_mod(self,a,mod):
		c = (a[0] % mod, a[1] % mod, a[2] % mod)
		return c

	#funkce provede absolutni hodnotu vsech prvku triprvkove ntice
	def tuples_abs(self,a):
		c = (abs(a[0]),abs(a[1]),abs(a[2]))
		return c

	#radkove PNG filtry berou v potaz sousedni pixely
	#schema:
	# c b
	# a x

	#vertikalni filtr
	def filter_sub(self,row):
		for i in range(0,self.width):
			if i == 0: #y = x + 0
				self.rgb[row][i] = self.tuples_sum(self.rgb[row][i],(0,0,0))
			else: #y = x + a
				self.rgb[row][i] = self.tuples_mod(self.tuples_sum(self.rgb[row][i],self.rgb[row][i-1]),256)

	#horizontalni filtr
	def filter_up(self,row):
		for i in range(0,self.width):
			if row == 0: #y = x + 0
				self.rgb[row][i] = self.tuples_sum(self.rgb[row][i],(0,0,0))
			else: #y = x + b
				self.rgb[row][i] = self.tuples_mod(self.tuples_sum(self.rgb[row][i],self.rgb[row-1][i]),256)

	#uhlopricny filtr
	def filter_average(self,row):
		for i in range(0,self.width):
			if i == 0 and row == 0: #y = x + floor((0 + 0) / 2)
				self.rgb[row][i] = self.tuples_mod(self.tuples_sum(self.rgb[row][i],self.tuples_div((0,0,0),2)),256)
			elif i > 0 and row == 0: #y = x + floor((a + 0) / 2)
				self.rgb[row][i] = self.tuples_mod(self.tuples_sum(self.rgb[row][i],self.tuples_div(self.tuples_sum(self.rgb[row][i-1],(0,0,0)),2)),256)
			elif i == 0 and row > 0: #y = x + floor((0 + b) / 2)
				self.rgb[row][i] = self.tuples_mod(self.tuples_sum(self.rgb[row][i],self.tuples_div(self.tuples_sum((0,0,0),self.rgb[row-1][i]),2)),256)
			else: #y = x + floor((a + b) / 2)
				self.rgb[row][i] = self.tuples_mod(self.tuples_sum(self.rgb[row][i],self.tuples_div(self.tuples_sum(self.rgb[row][i-1],self.rgb[row-1][i]),2)),256)

	#paeth filtr
	def filter_paeth(self,row):
		for i in range(0,self.width):
			if i == 0 and row == 0: #y = x + paeth(0,0,0)
				self.rgb[row][i] = self.tuples_mod(self.tuples_sum(self.rgb[row][i],self.paeth((0,0,0),(0,0,0),(0,0,0))),256)
			elif i > 0 and row == 0: #y = x + paeth(a,0,0)
				self.rgb[row][i] = self.tuples_mod(self.tuples_sum(self.rgb[row][i],self.paeth(self.rgb[row][i-1],(0,0,0),(0,0,0))),256)
			elif i == 0 and row > 0: #y = x + paeth(0,b,0)
				self.rgb[row][i] = self.tuples_mod(self.tuples_sum(self.rgb[row][i],self.paeth((0,0,0),self.rgb[row-1][i],(0,0,0))),256)
			else: #y = x + paeth(a,b,c)
				self.rgb[row][i] = self.tuples_mod(self.tuples_sum(self.rgb[row][i],self.paeth(self.rgb[row][i-1],self.rgb[row-1][i],self.rgb[row-1][i-1])),256)

	#paeth predictor
	def paeth(self,a,b,c):
		p = self.tuples_sub(self.tuples_sum(a,b),c)
		pa = self.tuples_abs((self.tuples_sub(p,a)))
		pb = self.tuples_abs((self.tuples_sub(p,b)))
		pc = self.tuples_abs((self.tuples_sub(p,c)))

		result = []
		for i in range(0,3):
			if pa[i] <= pb[i] and pa[i] <= pc[i]:
				result.append(a[i])
			elif pb[i] <= pc[i]:
				result.append(b[i])
			else:
				result.append(c[i])

		return(result[0],result[1],result[2])

	#vypis
	def png_print(self):
		for i in self.data:
			print(i, end=' ')

		print(end="\n")
		print("---------------------------")

		print("Header: " + str(self.header))
		print("IHDR: " + str(self.ihdr))
		print("Width: " + str(self.width))
		print("Height: " + str(self.height))
		print("IDAT: " + str(self.idat))
		print("IDAT_DATA: " + str(self.idat_data))
		print("IDAT_DECOMPRESSED: " + str(self.idat_decompress))
		print("Row filters: " + str(self.filters))
		print("RGB pixels: " + str(self.rgb))


#--------------------------MAIN--------------------------
if __name__ == '__main__':

	#definovani a nacteni argumentu pro vstupni PNG soubor
	parser = ArgumentParser()
	parser.add_argument("input", help="Input PNG file")
	args = parser.parse_args()

	#overeni cesty k PNG souboru
	if (os.path.isfile(args.input) == True):
		#spusteni png dekoderu
		png = PngReader(args.input)
		png.png_print()
	else:
		print("Error: Can't open input file", file=sys.stderr)
		sys.exit(1)
