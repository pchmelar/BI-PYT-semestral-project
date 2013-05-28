#!/usr/local/bin/python3.3
# -*- coding: utf-8 -*-

#BI-PYT
#Semestralni projekt
#Interpretr jazyka brainfuck/brainloller/braincopter
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
import image_png
from argparse import ArgumentParser

class BrainFuck:
    """Interpretr jazyka brainfuck."""
    
    def __init__(self, data, memory=b'\x00', memory_pointer=0):
        """Inicializace interpretru brainfucku."""

        # data programu
        if data.count("!") == 0:
            self.data = data
            self.input = ""

        #oddeleni kodu programu od jeho vstupu
        elif data.count("!") == 1:
            self.data = data[0:data.find("!")]
            self.input = data[data.find("!")+1:]

        else:
            print("Error: Your brainfuck program can't use ! more than once", file=sys.stderr)
            sys.exit(1)
        
        # inicializace proměnných
        self.memory = memory
        self.memory_pointer = memory_pointer
        
        # DEBUG a testy
        # a) paměť výstupu
        self.output = ''

        #spusteni interpretru
        self.brainfuck()
    
    #
    # pro potřeby testů
    #
    def get_memory(self):
        # Nezapomeňte upravit získání návratové hodnoty podle vaší implementace!
        return self.memory

    #implementace brainfuck interpretru
    def brainfuck(self):
        src = self.data #vstupni string
        left = 0 #pocatecni index vstupniho stringu
        right = len(self.data) - 1 #koncovy index vstupniho stringu
        data = self.input #vstup brainfuck programu
        idx = 0 #pocatecni index vstupu brainfuck programu

        if len(src) == 0: return
        if left < 0: left = 0
        if left >= len(src): left = len(src) - 1
        if right < 0: right = 0
        if right >= len(src): right = len(src) - 1

        arr = [] #pamet
        ptr = self.memory_pointer #ukazatel do pameti

        #ulozeni pocatecniho stavu pameti
        s = str(self.memory,encoding="utf-8")
        for i in range(0,len(s)):
            arr.append(ord(s[i]))

        #pokud neni pocatecni stav pameti
        if len(arr) == 0:
            arr.append(0)

        i = left
        while i <= right:
            s = src[i]

            #posun ukazatele doprava
            if s == '>': 
                ptr += 1
                if ptr >= len(arr): #natahovani pameti
                    arr.append(0)

            #posun ukazatele doleva
            elif s == '<':
                ptr -= 1

            #zvyseni hodnoty aktualni bunky o 1
            elif s == '+':
                arr[ptr] += 1

            #snizeni hodnoty aktualni bunky o 1
            elif s == '-':
                arr[ptr] -= 1

            #vypis aktualni bunky
            elif s == '.':
                self.output += chr(arr[ptr])

            #ulozeni vstupu do aktualni bunky
            elif s == ',':
                if idx >= 0 and idx < len(data):
                    arr[ptr] = ord(data[idx])
                    idx += 1
                else: #mimo vstup - nacteni ze stdin
                    print("Waiting for user input...")
                    arr[ptr] = ord(sys.stdin.read(1))

            #posun instrukcniho ukazatele doprava
            elif s =='[':
                if arr[ptr] == 0:
                    loop = 1
                    while loop > 0:
                        i += 1
                        c = src[i]
                        if c == '[':
                            loop += 1
                        elif c == ']':
                            loop -= 1

            #posun instrukcniho ukazatele doleva
            elif s == ']':
                loop = 1
                while loop > 0:
                    i -= 1
                    c = src[i]
                    if c == '[':
                        loop -= 1
                    elif c == ']':
                        loop += 1
                i -= 1
            i += 1

        #ulozeni konecneho stavu pameti
        s = ""
        for i in range(0,len(arr)):
            s += chr(arr[i])
        self.memory = bytes(s,encoding="utf-8")
        self.memory_pointer = ptr

        #vystup brainfuck programu
        print(self.output, end="")


class BrainLoller():
    """Třída pro zpracování jazyka brainloller."""
    
    def __init__(self, filename):
        """Inicializace interpretru brainlolleru."""

        # self.data obsahuje rozkódovaný zdrojový kód brainfucku..
        self.data = ''

        #dekomprese vstupniho PNG souboru
        self.png = image_png.PngReader
        self.image = self.png(filename)

        #spusteni interpretru
        self.brainloller()

        # ..který pak předhodíme interpretru
        self.program = BrainFuck(self.data)

    #implementace prekladace brainlolleru na brainfuck
    def brainloller(self):

        #nastaveni smeru cteni
        start = 0
        end = self.image.width
        itr = 1

        #generovani zdrojoveho kodu pro brainfuck
        for i in range(0,self.image.height):
            for j in range(start,end,itr):
                if self.image.rgb[i][j] == (255,0,0):
                    self.data += ">"
                elif self.image.rgb[i][j] == (128,0,0):
                    self.data += "<"
                elif self.image.rgb[i][j] == (0,255,0):
                    self.data += "+"
                elif self.image.rgb[i][j] == (0,128,0):
                    self.data += "-"
                elif self.image.rgb[i][j] == (0,0,255):
                    self.data += "."
                elif self.image.rgb[i][j] == (0,0,128):
                    self.data += ","
                elif self.image.rgb[i][j] == (255,255,0):
                    self.data += "["
                elif self.image.rgb[i][j] == (128,128,0):
                    self.data += "]"
                elif self.image.rgb[i][j] == (0,255,255):
                    start = self.image.width-1
                    end = -1
                    itr = -1
                elif self.image.rgb[i][j] == (0,128,128):
                    start = 0
                    end = self.image.width
                    itr = 1


class BrainCopter():
    """Třída pro zpracování jazyka braincopter."""
    
    def __init__(self, filename):
        """Inicializace interpretru braincopteru."""
        
        # self.data obsahuje rozkódovaný zdrojový kód brainfucku..
        self.data = ''
        # ..který pak předhodíme interpretru
        self.program = BrainFuck(self.data)


#--------------------------MAIN--------------------------
if __name__ == '__main__':

    #definovani a nacteni prepinacu/argumentu pro vstupni data
    parser = ArgumentParser()
    parser.add_argument("input", help="Input file/string")
    parser.add_argument("-l", "--brainloller", action="store_true", default=False, help="Input file in brainloller")
    parser.add_argument("-c", "--braincopter", action="store_true", default=False, help="Input file in braincopter")
    args = parser.parse_args()

    #kontrola prepinacu
    if args.brainloller == True and args.braincopter == True:
        print("Error: Can't proccess input in brainloller and braincopter languages at once. Choose only one.", file=sys.stderr)
        sys.exit(1)

    #vstupem je program v jazyce brainloller
    if args.brainloller == True:
        if (os.path.isfile(args.input) == True):
            bf = BrainLoller(args.input)
        else:
            print("Error: Can't open given file.", file=sys.stderr)
            sys.exit(1)

    #vstupem je program v jazyce braincopter
    elif args.braincopter == True:
        if (os.path.isfile(args.input) == True):
            bf = BrainCopter(args.input)
        else:
            print("Error: Can't open given file.", file=sys.stderr)
            sys.exit(1)

    #vstupem je program v jazyce brainfuck
    else:
        if (os.path.isfile(args.input) == True):
            with open (args.input, encoding="utf-8") as data_input:
                content = data_input.read()
        else:
            content = args.input

        bf = BrainFuck(content)
