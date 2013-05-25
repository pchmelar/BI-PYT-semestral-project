#!/usr/local/bin/python3.3
# -*- coding: utf-8 -*-

#BI-PYT
#Semestralni projekt
#Interpretr jazyka brainfuck - uzivatelske rozhrani
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
import brainx
from argparse import ArgumentParser

#definovani a nacteni argumentu pro vstupni data
parser = ArgumentParser()
parser.add_argument("input", help="Input file/string")
args = parser.parse_args()

#nacteni dat ze souboru/stringu
if (os.path.isfile(args.input) == True):
    with open (args.input, encoding="utf-8") as data_input:
        content = data_input.read()
else:
    content = args.input

bf = brainx.BrainFuck(content)
#print(bf.get_memory())
