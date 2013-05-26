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
		print(self.header)
		if self.header != b'\x89\x50\x4E\x47\x0D\x0A\x1A\x0A':
			raise PNGWrongHeaderError

		#kontrola datove casti IHDR chunku
		self.ihdr = self.parser(self.data,16,29)
		if self.ihdr[8:] != b'\x08\x02\x00\x00\x00':
			raise PNGNotImplementedError

	#vyparsovani pozadovane casti a spojeni do binarniho retezce
	def parser(self,data,start,end):
		s = b""
		for i in range(start,end):
			s += data[i]
		return s

	#slozeni 4B cisla ulozeneho v BigEndianu
	def BE_convert(self,start):
		num = self.data[start] * 16777216
		num += self.data[start+1] * 65536
		num += self.data[start+2] * 256
		num += self.data[start+3]
		return num

	#vypis
	def png_print(self):
		for i in self.data:
			print(i, end=' ')

		print(end="\n")
		print("---------------------------")

		print("Header: " + str(self.header))
		print("IHDR: " + str(self.ihdr))


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
