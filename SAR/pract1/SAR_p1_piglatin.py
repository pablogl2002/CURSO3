#!/usr/bin/env python
#! -*- encoding: utf8 -*-

# 1.- Pig Latin

import re
import sys
from typing import Text
from os.path import isfile
import string

class Translator():

    def __init__(self, punt:Text=None):
        """
        Constructor de la clase Translator

        :param punt(opcional): una cadena con los signos de puntuación
                                que se deben respetar
        :return: el objeto de tipo Translator
        """
        if punt is None:
            punt = ".,;?'!"
        self.re = re.compile(r"(\w+)([" + punt + r"]*)")

    def translate_word(self, word:Text):
        """
        Recibe una palabra en inglés y la traduce a Pig Latin

        :param word: la palabra que se debe pasar a Pig Latin
        :return: la palabra traducida
        """
        vocales = 'aeiouyAEIOUY'    # definicion de una variable que contenga todas las vocales
        ay = "ay"                   # definicion de una variable ay que añadiremos al final de las palabras (puede cambiar entre minusculas y mayusculas)        
        yay = "yay"                 # definicion de una variable yay que añadiremos al final de las palabras que empiezen por vocal
                                        # (puede cambiar entre minusculas y mayusculas)


        # comprueba si el primer simbolo no es un letra
        if word[0] not in string.ascii_letters:
            # si no es una letra deja la palabra igual
            new_word = word
        else:
            # comprueba si la palabra está escrita en mayúsculas
            if word.upper() == word:
                # si mayusculuas -> cambia los sufijos a mayusculas
                ay = "AY"
                yay = "YAY"
            
            capL = False # variable que indicará si la primera letra de una palabra está en mayusculas (capital letter)
            
            # comprueba si la primera letra está en mayusculas y lo demas en minusculas
            if word[0] in string.ascii_uppercase and word[1:].lower() == word[1:]:
                # convierte la palabra a minusculas 
                word = word.lower()
                # pone la variable capital letter a true para luego poner la primera letra del resultado en mayuscula
                capL = True

            # comprueba si la primera letra es vocal
            if word[0] in vocales:
                # si es vocal el primer simbolo añade yay al final
                new_word = word + yay
            else:
                # si la primera no es vocal recorre la palabra por posiciones
                for i in range(len(word)):

                    hasV = False # variable que indicará si la palabra tiene vocales o no

                    # busca vocales en las posiciones 
                    if word[i] in vocales:
                        # si encuentra vocal añade a partir de la posicion delante y antes de la posicion detrás + ay
                        new_word = word[i:] + word[:i] + ay
                        # pone la variable tiene vocales a True
                        hasV = True
                        # corta el bucle
                        break
                    
                    # comprueba que ha recorrido toda la palabra pero no ha encontrado vocales
                    if hasV == False and i == len(word) - 1:
                        # añade ay a la palabra original
                        new_word = word + ay

            # comprueba si la variable capital letter es true
            if capL:
                # si es true, pone la primera letra del resultado en mayuscula
                new_word = new_word[0].upper() + new_word[1:]

        # devuelve la palabra            
        return new_word

    def translate_sentence(self, sentence:Text):
        """
        Recibe una frase en inglés y la traduce a Pig Latin

        :param sentence: la frase que se debe pasar a Pig Latin
        :return: la frase traducida
        """

        # traducir una frase #
        t = Translator()
        new_sentence = ""

        # separa palabras y simbolos en una lista de duplas 
        tokens = self.re.findall(sentence)

        # recorre la lista de duplas
        for (word, punt) in tokens:
            # para cada palabra en la frase llama a que se traduzca y le añade el correspondiente simbolo después
            new_sentence += t.translate_word(word) + punt + " "

        # devuelve al frase
        return new_sentence

    def translate_file(self, filename:Text):
        """
        Recibe un fichero y crea otro con su tradución a Pig Latin

        :param filename: el nombre del fichero que se debe traducir
        :return: None
        """

        if not isfile(filename):
            print(f'{filename} no existe o no es un nombre de fichero', file=sys.stderr) 
        # COMPLETAR
        else:
            # abre el fichero con el nombre en consola
            f = open(filename, "r")

            # crea un traductor
            t = Translator()
            # separa el nombre del fichero por el punto de la extension
            fileN = filename.split(".")
            # crea un archivo (o "abre" un archivo) con el mismo nombre que el anterior + _latin y lo instancia como file_object
            with open(fileN[0] + "_latin." + ".".join(fileN[1:]), mode='w') as file_object:
                # recorre el fichero por lineas/frases
                for line in f:
                    # escribe en el nuevo fichero las lineas traducidas
                    print(t.translate_sentence(line), file=file_object)

            # cierra el primer fichero
            f.close()

if __name__ == "__main__":
    if len(sys.argv) > 2:
        print(f'Syntax: python {sys.argv[0]} [filename]')
        exit()
    t = Translator()
    if len(sys.argv) == 2:
        t.translate_file(sys.argv[1])
    else:
        sentence = input("ENGLISH: ")
        while len(sentence) > 1:
            print("PIG LATIN:", t.translate_sentence(sentence))
            sentence = input("ENGLISH: ")
