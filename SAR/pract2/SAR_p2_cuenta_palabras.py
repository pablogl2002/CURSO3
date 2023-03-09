#! -*- encoding: utf8 -*-

## Nombres: Pablo García López y Jorge Baeza García

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

    # he añadido el argumento bigrams para saber si se tienen que mostrar las lineas correspondientes a los bigramas
    def write_stats(self, filename:str, stats:dict, use_stopwords:bool, full:bool, bigrams:bool):
        """
        Este método escribe en fichero las estadísticas de un texto
            
        :param 
            filename: el nombre del fichero destino.
            stats: las estadísticas del texto.
            use_stopwords: booleano, si se han utilizado stopwords
            full: boolean, si se deben mostrar las stats completas
        """
        with open(filename, 'w', encoding='utf-8', newline='\n') as fh:
        # ---------------------------- #
        # ---- impresion de datos ---- #
        # ---------------------------- #
           
            print(f"Lines: {stats['nlines']}", file=fh) # numero lineas
            print(f"Number words (including stopwords): {stats['nwords']}", file=fh) # numero palabras incluyendo stopwords
            
            if use_stopwords: # comprueba si se tienen q filtrar las stopwords
                print(f"Number words (without stopwords): {self.sum_freq(stats['word'])}", file=fh) # numero palabras sin incluir stopwords                

            print(f"Vocabulary size: {len(stats['word'])}", file=fh) # tamaño de vocabulario (numero de palabras distintas)
            print(f"Number of symbols: {self.sum_freq(stats['symbol']) }", file=fh) # numero de simbolos totales
            print(f"Number of different symbols: {len(stats['symbol'])}", file=fh)  # numero de simbolos diferente
            
            print(f"Words (alphabetical order):" , file=fh) # palabras en orden alfabetico
            self.mostrar_dict(sorted(stats['word'].items()), fh, full) # llamada a una funcion que imprime una lista con cierto formato, en este caso las palabras y su frecuencia de aparicion, en orden alfabetico
            print("Words (by frequency):", file=fh) # palabras en orden de frecuencia
            self.mostrar_dict(sort_dic_by_values(stats['word']), fh, full) # llamada a una funcion que imprime una lista con cierto formato, en este caso las palabras y su frecuencia de aparicion, segun la frecuencia
            print("Symbols (alphabetical order):", file=fh)    # simbolos en orden alfabetico
            self.mostrar_dict(sorted(stats['symbol'].items()), fh, full)   # llamada a una funcion que imprime una lista con cierto formato, en este caso los simbolos y su frecuencia de aparicion, en orden alfabetico
            print("Symbols (by frequency):", file=fh)  # simbolos en orden de frecuencia
            self.mostrar_dict(sort_dic_by_values(stats['symbol']), fh, full) # llamada a una funcion que imprime una lista con cierto formato, en este caso los simbolos y su frecuencia de aparicion, segun la frecuencia           
            
            if bigrams: # comprueba si se debe contar segun bigramas
                print("Word pairs (alphabetical order):", file=fh) # pares de palabras en orden alfabetico
                self.mostrar_dict(sorted(stats['biword'].items()), fh, full) # llamada a una funcion que imprime una lista con cierto formato, en este caso los pares de palabras y su frecuencia de aparicion, en orden alfabetico
                print("Word pairs (by frequency):", file=fh) # pares de palabras segun frecuencia
                self.mostrar_dict(sort_dic_by_values(stats['biword']), fh, full) # llamada a una funcion que imprime una lista con cierto formato, en este caso los pares de palabras y su frecuencia de aparicion, segun frecuencia

                print("Symbol pairs (alphabetical order):", file=fh) # pares de simbolos en orden alfabetico
                self.mostrar_dict(sorted(stats['bisymbol'].items()), fh, full) # llamada a una funcion que imprime una lista con cierto formato, en este caso los pares de simbolos y su frecuencia de aparicion, en orden alfabetico
                print("Symbol pairs (by frequency):", file=fh) # pares de simbolos segun frecuencia
                self.mostrar_dict(sort_dic_by_values(stats['bisymbol']), fh, full) # llamada a una funcion que imprime una lista con cierto formato, en este caso los pares de simbolos y su frecuencia de aparicion, segun frecuencia

            print("Prefixes (by frequency):", file=fh) # prefijos en orden de frecuencia
            self.mostrar_dict(sort_dic_by_values(stats['prefix']), fh, full) # llamada a una funcion que imprime una lista con cierto formato, en este caso los prefijos y su frecuencia de aparicion, segun frecuencia
            print("Suffixes (by frequency):", file=fh) # sufijos en orden de frecuencia
            self.mostrar_dict(sort_dic_by_values(stats['suffix']), fh, full) # llamada a una funcion que imprime una lista con cierto formato, en este caso los sufijos y su frecuencia de aparicion, segun frecuencia
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
            print(f"\t{key}: {value}", file=filename)
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

    # funcion que devuelve un diccionario con los pares de palabras de una linea que se le pasa como argumento, 
    #    filtrando los pares de palabras que contengan un stopword (se pasan a traves de una lista 'st')
    def bigram_word(self, d:dict, lineAr, st):
        # igualamos el diccionario solucion al diccionario incial
        res:dict = d
        # añadimos simbolos '$' al inicio y final de la linea
        lineAr = ['$'] + lineAr + ['$']

        i = 0
        # bucle que recorre las palabras de la linea
        while i < len(lineAr) - 1:
            # cogemos las dos palabras consecutivas
            word1 = lineAr[i]
            word2 = lineAr[i + 1]
            # en el caso de que esté una de las dos palabras en la lista de stopwords no añadimos al diccionario
            if word1 not in st and word2 not in st:                
                aux = word1 + " " + word2
                # filtramos las lineas en blanco
                if aux != '$ $':
                    # añadimos al diccionario solucion el par de palabras con frecuencia 1, si ya estaba, su frecuencia se incrementa en 1
                    res[aux] = res.get(aux, 0) + 1
            # recorremos el siguiente par
            i += 1               
        # devuelve el diccionario resultado
        return res

    # funcion que devuelve un diccionario con los pares de simbolos de una palabra que se el pasa como argumento
    def bigram_symbol(self, d:dict, word):
        # igualamos el diccionario solucion al diccionario incial
        res:dict = d
        
        i = 0
        # bucle que recorre los simbolos de la palabra
        while i < len(word) - 1:
            # cogemos el par de simbolos consecutivos
            s1 = word[i]
            s2 = word[i + 1]

            aux = s1 + s2
            # añadimos al diccionario solucion el par de simbolos con frecuencia 1, si ya estaba, su frecuencia se incrementa en 1
            res[aux] = res.get(aux, 0) + 1
            # recorremos el siguiente par
            i += 1
        # devuelve el diccionario resultado
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
                # en el caso de tener q hacer en analisis por bigramas
                if bigrams:
                    # igualamos el diccionario bigramas a una funcion que añade las palabras de una linea por bigramas al diccionario
                    sts['biword'] = self.bigram_word(sts['biword'], line, stopwords)
                # recorremos las palabras de la lista de palabras 'line'
                for word in line:
                    # si se pide en minusculas
                    if lower:
                        # se pasa la palabra a minusculas
                        word = word.lower()
                    # por cada palabra en la lista incrementamos en 1 la variable del diccionario nwords
                    sts['nwords'] += 1
                    # filtramos los stopwords
                    if word not in stopwords: 
                        # checkeamos que la palabra esté en el diccionario y le incrementamos 1 a su valor
                        #   en el caso de que no haya palabras se añade y su valor será 1
                        sts['word'][word] = sts['word'].get(word, 0) + 1
                        # en el caso de tener q hacer en analisis por bigramas
                        if bigrams:
                            # igualamos el diccionario bigramas a una funcion que añade los simbolos de una palabra por bigramas al diccionario                    
                            sts['bisymbol'] = self.bigram_symbol(sts['bisymbol'], word)
                        # variables auxiliares para los prefijos y sufijos
                        pref = ""
                        suf = ""
                        # variable para recorrer la palabra al reves y poder sacar los sufijos al mismo tiempo
                        i = len(word) - 1
                        # bucle que recorre los simbolos de una palabra
                        for s in word:
                            # checkeamos que el simbolo esté en el diccionario y le incrementamos 1 a su valor
                            #   en el caso de que no esté el simbolo se añade y su valor será 1
                            sts['symbol'][s] = sts['symbol'].get(s, 0) + 1
                            # añadimos el simbolo 's' a la variable auxiliar pref
                            pref += s
                            # comprueba q el prefijo es apto
                            if len(pref) > 1 and len(pref) <= 4 and len(pref) < len(word):
                                # añade el prefijo al diccionario de prefijos
                                sts['prefix'][pref + "-"] = sts['prefix'].get(pref + "-", 0) + 1
                            # añadimos una letra en la posicion i al sufijo 
                            suf = word[i] + suf
                            # comprueba que el sufijo es apto
                            if len(suf) > 1 and len(suf) <= 4 and len(suf) < len(word):
                                # añade el sufijo al diccionario de prefijos
                                sts['suffix']["-" + suf] = sts['suffix'].get("-" + suf, 0) + 1
                            # decrementa la variable i para recorrer la proxima letra
                            i -= 1

        filename, ext0 = os.path.splitext(fullfilename)            

        # añade una '_' al nombre del archivo
        filename += '_'
        # variable q se pondrá en True si se le pasa algun parametro q deba modificar el nombre
        param = False
        # si --lower || -l
        if lower:
            # añidmos una 's' al nombre
            filename += 'l'
            param = True

        # si --stop || -s
        if stopwordsfile is not None:
            # añidmos una 's' al nombre
            filename += 's'
            param = True

        # si --bigram || -b
        if bigrams:
            # añidmos una 'b' al nombre
            filename += 'b'
            param = True

        # si --full || -b
        if full:
            # añidmos una 'f' al nombre
            filename += 'f'
            param = True

        # si hay algun parametro q añada una letra al nombre 
        if param:
            # añade una nueva barra baja ('_')
            filename += '_'

        # el nombre del nuevo fichero será el mismo que el anterior pero añadiendo _stats antes de la extension
        new_filename = filename + "stats" + ext0 # cambiar
        self.write_stats(new_filename, sts, stopwordsfile is not None, full, bigrams)

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
