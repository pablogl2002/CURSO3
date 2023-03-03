#! -*- encoding: utf8 -*-

## Nombres: 

########################################################################
########################################################################
###                                                                  ###
###  Todos los métodos y funciones que se añadan deben documentarse  ###
###                                                                  ###
########################################################################
########################################################################

import argparse
import os
import re
from typing import Optional

def sort_dic_by_values(d:dict) -> list:
    return sorted(d.items(), key=lambda a: (-a[1], a[0]))

class WordCounter:

    def __init__(self):
        """
           Constructor de la clase WordCounter
        """
        self.clean_re = re.compile('\W+')

    def write_stats(self, filename:str, stats:dict, use_stopwords:bool, full:bool):
        """
        Este método escribe en fichero las estadísticas de un texto
            
        :param 
            filename: el nombre del fichero destino.
            stats: las estadísticas del texto.
            use_stopwords: booleano, si se han utilizado stopwords
            full: boolean, si se deben mostrar las stats completas
        """
        with open(filename, 'w', encoding='utf-8', newline='\n') as fh:
        # --------------------------- #
        # ---- impresion de datos ----#
        # --------------------------- #
           
            print(f"Lines: {stats['nlines']}", file=fh) # numero lineas
            print(f"Number words (including stopwords) : {stats['nwords']}", file=fh)    # numero palabras sin incluir stopwords
            print(f"Vocabulary size: {len(stats['word'])}", file=fh)    # tamaño de vocabulario (numero de palabras distintas)
            print(f"Number of symbols: {self.sum_freq(stats['symbol']) }", file=fh) # numero de simbolos totales
            print(f"Number of different symbols: {len(stats['symbol'])}", file=fh)  # numero de simbolos diferente
            print(f"Words (alphabetical order): " , file=fh)    # palabras en orden alfabetico
            dicW = stats['word'].items()                        # variable que contiene la lista de elementos del diccionario word
            self.mostrar_dict(sorted(dicW), fh, full)           # llamada a una funcion que imprime una lista con cierto formato, en este caso las palabras y su frecuencia de aparicion, en orden alfabetico
            print("Words (by frequency): ", file=fh)    # palabras en orden de frecuencia
            self.mostrar_dict(sorted(dicW, key=lambda x: x[1], reverse=True), fh, full) # llamada a una funcion que imprime una lista con cierto formato, en este caso las palabras y su frecuencia de aparicion, segun la frecuencia          
            print("Symbols (alphabetical order): ", file=fh)    # simbolos en orden alfabetico
            dicL = stats['symbol'].items()  # variable que contiene la lista de elementos del diccionario symbol
            self.mostrar_dict(sorted(dicL), fh, full)   # llamada a una funcion que imprime una lista con cierto formato, en este caso los simbolos y su frecuencia de aparicion, en orden alfabetico
            print("Symbols (by frequency): ", file=fh)  # simbolos en orden de frecuencia
            self.mostrar_dict(sorted(dicL, key=lambda x: x[1], reverse=True), fh, full) # llamada a una funcion que imprime una lista con cierto formato, en este caso los simbolos y su frecuencia de aparicion, segun la frecuencia           
            print("Prefixes (by frequency): ", file=fh) # prefijos en orden de frecuencia
            print("Suffixes (by frequency): ", file=fh) # sufijos en orden de frecuencia
            pass

    # funcion que muestra (formateado) un diccionario que se le pasa como la lista de sus elementos
    def mostrar_dict(self, l, filename, cond):
        # si la condicion es negativa limita el numero de elementos visibles de la lista a 20
        i = 0
        if not cond:
            limit = 20
        for key, value in l:
            # si !cond y el numero de elementos supera el limite salta del bucle
            if not cond and i >= limit:
                break
            # escribe en el fichero que le hemos pasado como parametro las key y los valores con el formato key:value
            print(f"\t{key} : {value}", file=filename)
            i += 1
    
    # funcion que devuelve al suma de las frecuencias de los valores de todas las keys en un diccionario
    #   en este caso lo utilizamos para saber la suma de las frecuencias de aparicion de todos los simbolos
    def sum_freq(self, f:dict):
        res = 0
        # bucle en el que recorremos todos los elementos del diccionario
        for key, value in f.items():
            # vamos sumando las frecuecias en una variables resultado
            res += value
        # devolvemos el total
        return res

    def file_stats(self, fullfilename:str, lower:bool, stopwordsfile:Optional[str], bigrams:bool, full:bool):
        """
        Este método calcula las estadísticas de un fichero de texto

        :param 
            fullfilename: el nombre del fichero, puede incluir ruta.
            lower: booleano, se debe pasar todo a minúsculas?
            stopwordsfile: nombre del fichero con las stopwords o None si no se aplican
            bigram: booleano, se deben calcular bigramas?
            full: booleano, se deben montrar la estadísticas completas?
        """

        stopwords = [] if stopwordsfile is None else open(stopwordsfile, encoding='utf-8').read().split()

        # variables for results

        sts = {
                'nwords': 0,
                'nlines': 0,
                'word': {},
                'symbol': {},
                'prefix': {},
                'suffix': {}
                }

        if bigrams:
            sts['biword'] = {}
            sts['bisymbol'] = {}

        # COMPLETAR
        # AYUDA: line = self.clean_re.sub(' ', line)
        with open(fullfilename, 'r', encoding='utf-8') as fh:
            # recorremos todas las lineas en el fichero
            for line in fh:
                # por cada linea incrementamos la variable del diccionario nlines en 1
                sts['nlines'] += 1
                # cambiamos los simbolos que no sean letras y/o numeros y los sustituimos por espacios en blanco
                line = self.clean_re.sub(' ', line)
                # dividimos la linea en una lista que contiene todas las palabras de la linea
                line = line.split()
                # recorremos las palabras de la lista 
                for word in line:
                    # por cada palabra en la lista incrementamos en 1 la variable del diccionario nwords
                    sts['nwords'] += 1
                    # checkeamos que la palabra esté en el diccionario y le incrementamos 1 a su valor
                    #   en el caso de que no haya palabras se añade y su valor será 1
                    sts['word'][word] = sts['word'].get(word, 0) + 1
                    for s in word:
                        # checkeamos que el simbolo esté en el diccionario y le incrementamos 1 a su valor
                        #   en el caso de que no esté el simbolo se añade y su valor será 1
                        sts['symbol'][s] = sts['symbol'].get(s, 0) + 1


        filename, ext0 = os.path.splitext(fullfilename)

        # el nombre del nuevo fichero será el mismo que el anterior pero añadiendo _stats antes de la extension
        new_filename = filename + "_stats" + ext0 # cambiar
        self.write_stats(new_filename, sts, stopwordsfile is not None, full)


    def compute_files(self, filenames:str, **args):
        """
        Este método calcula las estadísticas de una lista de ficheros de texto

        :param 
            filenames: lista con los nombre de los ficheros.
            args: argumentos que se pasan a "file_stats".

        :return: None
        """

        for filename in filenames:
            self.file_stats(filename, **args)

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Compute some statistics from text files.')
    parser.add_argument('file', metavar='file', type=str, nargs='+',
                        help='text file.')

    parser.add_argument('-l', '--lower', dest='lower',
                        action='store_true', default=False, 
                        help='lowercase all words before computing stats.')

    parser.add_argument('-s', '--stop', dest='stopwords', action='store',
                        help='filename with the stopwords.')

    parser.add_argument('-b', '--bigram', dest='bigram',
                        action='store_true', default=False, 
                        help='compute bigram stats.')

    parser.add_argument('-f', '--full', dest='full',
                        action='store_true', default=False, 
                        help='show full stats.')

    args = parser.parse_args()
    wc = WordCounter()
    wc.compute_files(args.file,
                     lower=args.lower,
                     stopwordsfile=args.stopwords,
                     bigrams=args.bigram,
                     full=args.full)
