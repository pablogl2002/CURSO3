#!/usr/bin/env python
#! -*- encoding: utf8 -*-
# 3.- Mono Library

import pickle
import random as rd
import re
import sys
from typing import List, Optional, TextIO

## Nombres: Jorge Baeza García, Pablo García Lopez

########################################################################
########################################################################
###                                                                  ###
###  Todos los métodos y funciones que se añadan deben documentarse  ###
###                                                                  ###
########################################################################
########################################################################


def convert_to_lm_dict(d: dict):
    for k in d:
        l = sorted(((y, x) for x, y in d[k].items()), reverse=True)
        d[k] = (sum(x for x, _ in l), l)


class Monkey():

    def __init__(self):
        self.r1 = re.compile('[.;?!]')
        self.r2 = re.compile('\W+')
        self.info = {}

    def get_n(self):
        return self.info.get('n', 0)
    
    # funcion que devuelve una tupla con los primeros n elementos de la lista
    def get_elements(self, lista, n):
        hist = lista[:n-1] # variable que almacena los n primero elementos
        return tuple(hist) # devolvemos un casting a tuple de la variable anterior

    def index_sentence(self, sentence:str):
        #tamaño ngramas
        n = self.info['n'] 

        cont = 1
        # recorremos hasta el numero maximo de ngramas (n) para ir rellanando el diccionario
        for c in range(2, n+1):
        
            # pasamos la frase de string a un array [$, pal1, pal2, pal3..., $]
            words =  sentence.split()
            # bucle que recorre el tamaño del ngrama, y poner antes de la frase tantos '$' como toquen (c - 1)
            for w in range(c - 1): 
                words = ['$'] + words # añadimos delante del array un '$' por iteracion


            for w in range(len(words) - (c-1)):
                #obtenemos un historial de los terminos
                hist = self.get_elements(words[w:], c)
                #si no lo encontramos, lo creamos
                if self.info['lm'][c].get(hist) == None:
                    self.info['lm'][c][hist] = {}
                
                encontrado = False

                #Se actualizan las estadísticas internas de los términos
                for term, value in self.info['lm'][c][hist].items():
                    
                    #se comprueba que exista el siguiente término y se actualiza la frecuencia
                    if not encontrado and cont + w < len(words) and term.strip() == words[cont+w].strip():
                        self.info['lm'][c][hist][term] = value + 1
                        encontrado = True
                        break

                #si el diccionario está vacio y no lo has encontrado, se inicializan los ngramas
                if not encontrado and cont + w < len(words):
                    self.info['lm'][c][hist][words[cont+w]] = 1
            cont += 1

    def compute_lm(self, filenames:List[str], lm_name:str, n:int):
        self.info = {'name': lm_name, 'filenames': filenames, 'n': n, 'lm': {}}
        buffer = None #Se inicializa el buffer vacío
        for i in range(2, n+1):
            self.info['lm'][i] = {}
        for filename in filenames:
            for line in open(filename, encoding='utf-8'):

                #se pasan las lineas del texto quitando los simbolos
                line = self.r1.split(line.strip())

                #para cada parte de la frase le quitamos los simbolos y lo ponemos en minúsculas
                for f in range(len(line)):
                    line[f] = (re.sub(self.r2,' ',line[f])).lower()

                #Si el buffer está vacío
                if buffer == None:

                    #comprobamos que la ultima parte de la línea sea una frase completa, y si no lo es,
                    #guardamos esta última parte en un buffer
                    if line[-1] != '':
                        buffer = line[-1]

                    #llamamos a index_sentence para todas las frases completas
                    for f in line[:-1]:
                        # añadimos ya el simbolo '$' para indicar el final de la frase
                        self.index_sentence(f + ' $')

                #Si el buffer NO está vacío
                else:

                    #Comprobamos que la linea que estamos leyendo no esté vacia para poder eliminar el \n\n
                    if len(line) == 1 and line[0] == '':
                        #llamamos a index_sentence para la frase ya con el dolar indicando final de frase
                        self.index_sentence(buffer + ' $')
                        buffer = None #se elimina el buffer
                    
                    #Si la línea no está vacía
                    else:
                        #la primera frase se junta con el buffer de la linea anterior
                        line[0] = buffer + " " + line[0]

                        #si la linea contiene una frase sin acabar, la guarda en el buffer
                        if line[-1] != '':
                            buffer = line[-1]
                        else:
                            buffer = None #se elimina el buffer

                        #llamamos a index_sentence para todas las frases completas
                        for f in line[:-1]:
                            # frase + '$' final de frase
                            self.index_sentence(f + ' $')
        # en el caso de que se quede en el buffer la ultima frase, por no tener un doble salto de linea o un indicativo de final de linea
        if buffer != None:
            # llamamos a index_sentencence de lo q resta de buffer (ultima frase) con el simbolo '$' indicando el final de frase
            self.index_sentence(buffer + ' $')
                        
        for i in range(2, n+1):
            convert_to_lm_dict(self.info['lm'][i])

    def load_lm(self, filename:str):
        with open(filename, "rb") as fh:
            self.info = pickle.load(fh)

    def save_lm(self, filename:str):
        with open(filename, "wb") as fh:
            pickle.dump(self.info, fh)

    def save_info(self, filename:str):
        with open(filename, "w", encoding='utf-8', newline='\n') as fh:
            self.print_info(fh=fh)

    def show_info(self):
        self.print_info(fh=sys.stdout)

    def print_info(self, fh:TextIO):
        print("#" * 20, file=fh)
        print("#" + "INFO".center(18) + "#", file=fh)
        print("#" * 20, file=fh)
        print(f"language model name: {self.info['name']}", file=fh)
        print(f'filenames used to learn the language model: {self.info["filenames"]}', file=fh)
        print("#" * 20, file=fh)
        print(file=fh)
        for i in range(2, self.info['n']+1):
            print("#" * 20, file=fh)
            print("#" + f'{i}-GRAMS'.center(18) + "#", file=fh)
            print("#" * 20, file=fh)
            for prev in sorted(self.info['lm'][i].keys()):
                wl = self.info['lm'][i][prev]
                print(f"'{' '.join(prev)}'\t=>\t{wl[0]}\t=>\t{', '.join(['%s:%s' % (x[1], x[0]) for x in wl[1]])}" , file=fh)


    def generate_sentences(self, n:Optional[int], nsentences:int=10, prefix:Optional[str]=None):
        
        pref = ""
        aux = ""
        max_palabras = 50
        
        #Si no pasan ningun prefijo, completalo con '$'
        if prefix == None:
            aux = ['$'] * (n-1)

        #Si nos pasan el prefijo:
        else:
            prefix = (re.sub(self.r2,' ',prefix)).lower()
            prefix = prefix.split()
            
            #Comprobamos que el prefijo no sobrepase la n
            if len(prefix) >= n - 1:
                aux = prefix[-(n-1):]

            #Si no lo sobrepasa completa con $ el principio del prefijo
            else:
                pref = (self.r2.sub(' ',prefix)).lower()
                for _ in range(n - 1 - len(prefix)):
                    prefix = ['$'] + prefix
                aux = prefix

        #prefijo inicial de n-1 palabras que se utiliza para reestablecer el prefijo "aux" en cada frase distinta
        aux2 = tuple(aux)

        #Para cada frase que vamos a generar
        for _ in range(nsentences):

            #Primero escribimos el prefijo para cada frase
            print(pref + " ", end='')
            #tupla de n-1 palabras de la frase que se van generando
            aux = aux2
            
            #si no supera el limite de palabras
            for _ in range(max_palabras):
                #escoge la clave que corresponda al preijo
                c = self.info['lm'][n][aux]
                values = c[1] #guarda los valores
                weights = [v[0] for v in values] #guarda los pesos
                palabras = [w[1] for w in values] #guarda las palabras

                #para la siguiente palabra haz una elección random
                next_word = rd.choices(palabras, weights, k = 1)
                #si la siguiente palabra es un '$' acaba la frase
                if next_word == ['$']:
                    break
                #el prefijo pasa a ser (w1, w2) a (w2, w3) siendo w3 la palabra escogida anteriormente
                aux = aux[1:] + tuple(next_word)
                #escribe la palabra por pantalla
                print(' '.join(next_word) + " ", end='')
            print()
            
    
            




if __name__ == "__main__":
    print("Este fichero es una librería, no se puede ejecutar directamente")


