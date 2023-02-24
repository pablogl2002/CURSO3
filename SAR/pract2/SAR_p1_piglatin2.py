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
            punt = ".,;?!"
        self.re = re.compile(r"(\w+)([" + punt + r"]*)")

    def translate_word(self, word:Text):
        """
        Recibe una palabra en inglés y la traduce a Pig Latin

        :param word: la palabra que se debe pasar a Pig Latin
        :return: la palabra traducida
        """
        punt = ".,;?!"
        vocales = 'aeiou'

        if word.upper() != word and word[0] in string.ascii_letters:
            capL = False
            if word[0] in string.ascii_uppercase and word[1:].lower() == word[1:]:
                word = word.lower() 
#                capL = True

            for i in range(len(word)):
                hasV = False

                if word[0] in vocales:
                    if word[-1] in punt:
                    #if self.re.search(word):
                        new_word = word[:-1] + "yay" + word[-1]
                    else: new_word = word + "yay"
                    break
                else:
                    if word[i] in vocales:
                        if word[-1] in punt:
    #                    if self.re.search(word):
                            new_word = word[i:-1] + word[:i] + "ay" + word[-1]
                        else:
                            new_word = word[i:] + word[:i] + "ay"
                        hasV = True
                        break

                    if hasV == False and i == len(word) - 1:
                        if word[-1] in punt:
#                        if self.re.search(word):
                            new_word = word[:-1] + "ay" + word[-1]
                        else: new_word = word + "ay"

#                    if capL == True: new_word = new_word[0].upper() + new_word[1:]

        elif word.upper() == word and word[0] in string.ascii_letters:
            for i in range(len(word)):
                hasV = False

                if word[0] in vocales:
                    if self.re.search(word):
                        new_word = word[:-1] + "YAY" + word[-1]
                    else: new_word = word + "YAY"
                    break
                else:
                    if word[i] in vocales:
                        if self.re.search(word):
                            new_word = word[i:-1] + word[:i] + "AY" + word[-1]
                        else:
                            new_word = word[i:] + word[:i] + "AY"
                        hasV = True
                        break

                if hasV == False and i == len(word) - 1:
                    if self.re.search(word):
                        new_word = word[:-1] + "AY" + word[-1]
                    else: new_word = word + "AY"
        #elif word[0] not in string.ascii_letters:
        #    new_word = word


        #new_word = word # SUSTITUIR ESTA PARTE
        
        return new_word

    def translate_sentence(self, sentence:Text):
        """
        Recibe una frase en inglés y la traduce a Pig Latin

        :param sentence: la frase que se debe pasar a Pig Latin
        :return: la frase traducida
        """

        # traducir una frase #

        sentenceL = sentence.split()
        t = Translator()
        new_sentence = ""
        for word in sentenceL:
            # añadir palabras en un str
            #new_sentence.concat(t.translate_word(word) + " ")
            new_sentence += t.translate_word(word) + " "

        # new_sentence = sentence # SUSTITUIR ESTA PARTE

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
            f = open(filename, "r")
            t = Translator()
            with open(filename[:-4] + "_piglatin.txt", mode='w') as file_object:
                for line in f:  
                    print(t.translate_sentence(line), file=file_object)
                    #t.translate_sentence(line)

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
            #print("PIG LATIN:", t.translate_word(sentence))
            sentence = input("ENGLISH: ")
