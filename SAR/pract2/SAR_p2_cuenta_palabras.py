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

            #print(stats)

            print(f"Lines: {stats['nlines']}", file=fh)
            print(f"Number words (including stopwords) : {stats['nwords']}", file=fh)
            print(f"Vocabulary size: {len(stats['word'])}", file=fh)
            print(f"Number of symbols: {self.sum_freq(stats['symbol']) }", file=fh)
            print(f"Number of different symbols: {len(stats['symbol'])}", file=fh)
            print(f"Words (alphabetical order): {self.mostrar_dict(stats['word'], fh)}" , file=fh)
            print("Words (by frequency): ", file=fh)
            print("Symbols (alphabetical order): ", file=fh)
            print("Symbols (by frequency): ", file=fh)
            print("Prefixes (by frequency): ", file=fh)
            print("Suffixes (by frequency): ", file=fh)
            pass


    def mostrar_dict(self, dic:dict, filename):
        for item in dic.items():
            print(f"{item} \n", file=filename)
    
    def sum_freq(self, f:dict):
        res = 0
        
        for key, value in f.items():
            res += value

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
            for line in fh:
                sts['nlines'] += 1
                line = self.clean_re.sub(' ', line)
                line = line.split()
                for word in line:
                    sts['nwords'] += 1
                    sts['word'][word] = sts['word'].get(word, 0) + 1
                    for s in word:
                        sts['symbol'][s] = sts['symbol'].get(s, 0) + 1


        filename, ext0 = os.path.splitext(fullfilename)

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
