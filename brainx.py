#!/usr/local/bin/python3.3
# -*- coding: utf-8 -*-

#BI-PYT
#Semestralni projekt
#Interpretr jazyka brainfuck
#FIT CVUT LS 2012/2013
#
#Autor: Petr Chmelar (chmelpe7)
#E-mail: chmelpe7@fit.cvut.cz
#
#Zdroje:
#http://docs.python.org
#http://vyuka.ookami.cz/@CVUT_2012+13-LS_BI-PYT/
#http://vyuka.ookami.cz/@CVUT_2012+13-LS_BI-SKJ/

import sys

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
            print("Error: Can't use ! more than once", file=sys.stderr)
            sys.exit(1)
        
        # inicializace proměnných
        self.memory = memory
        self.memory_pointer = memory_pointer
        
        # DEBUG a testy
        # a) paměť výstupu
        self.output = ''

        #spusteni interpretru
        self.lets_brainfuck()
    
    #
    # pro potřeby testů
    #
    def get_memory(self):
        # Nezapomeňte upravit získání návratové hodnoty podle vaší implementace!
        return self.memory

    #vlastni implementace
    def lets_brainfuck(self):
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
                else: #mimo vstup
                    arr[ptr] = 0 

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

'''

class BrainLoller():
    """Třída pro zpracování jazyka brainloller."""
    
    def __init__(self, filename):
        """Inicializace interpretru brainlolleru."""
        
        # self.data obsahuje rozkódovaný zdrojový kód brainfucku..
        self.data = ''
        # ..který pak předhodíme interpretru
        self.program = BrainFuck(self.data)


class BrainCopter():
    """Třída pro zpracování jazyka braincopter."""
    
    def __init__(self, filename):
        """Inicializace interpretru braincopteru."""
        
        # self.data obsahuje rozkódovaný zdrojový kód brainfucku..
        self.data = ''
        # ..který pak předhodíme interpretru
        self.program = BrainFuck(self.data)

'''
