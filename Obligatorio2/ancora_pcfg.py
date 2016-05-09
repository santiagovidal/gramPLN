# -*- encoding: utf-8 -*-

#
#  Gramáticas Formales para el Lenguaje Natural
#  Grupo de PLN (InCo) - 2016
#
#  Entrega 2 - Treebanks, PCFG y Parsing
#
#  Este template define clases por sección y tiene metodos a ser completados.
#  Completar las secciones siguiendo su especificación y la letra de la entrega.
#
#
#  Grupo: 11
#
#  Estudiante 1:    Nicolás Mechulam Burstin    - 4.933.997-7
#  Estudiante 2:    Damián Salvia Varela        - 4.452.120-0
#  Estudiante 3:    Santiago Vidal Aguirre      - 4.651.496-6
#
#


import nltk
import ancora  # (Modulo para leer AnCora)

# Otros modulos de utilidad
import collections
import string


# Parte 1 - Corpus
###################

class Corpus:
    """
    Clase de funcionalidades sobre el corpus AnCora.
    """

    def __init__(self, corpus_path='./relative-path/'):
        # Cargar corpus desde 'corpus_path'
        self.corpus =  ancora.AncoraCorpusReader(corpus_path)

    ## Parte 1.1
    # a.
    def cant_oraciones(self):
        """
        Retorna la cantidad de oraciones del corpus.
        """
        sentences = list(self.corpus.sents())
        return len(sentences)

    # b.
    def oracion_mas_larga(self):
        """
        Retorna la oracion mas larga.
        (la primera si hay mas de una con el mismo largo)
        """
        sentences = list(self.corpus.sents())
        return max(sentences, key=lambda x: len(nltk.word_tokenize(x)))


    # c.
    def largo_promedio_oracion(self):
        """
        Retorna el largo de oracion promedio.
        """
        sentences = list(self.corpus.sents())
        #words = list(self.corpus.tagged_words())
        #return len(words)/len(sentences)
        return sum([len(nltk.word_tokenize(sentence)) for sentence in sentences])/len(sentences)

    # d.
    def palabras_frecs(self):
        """
        Retorna un diccionario (dict) palabra-frecuencia de las palabras del corpus.
        (considerar las palabras en minúsculas)
        """
        tokens = self.corpus.tagged_words()
        dictionary = collections.defaultdict(lambda: 0)
        for (word,_) in tokens:
            if word not in string.punctuation: # FIXME - No se si es necesario
                dictionary[word.lower()] += 1
        return dictionary

    # e.
    def palabras_frecs_cat(self):
        """
        Retorna un diccionario (dict) palabra-lista de las palabras del corpus.
        Cada lista contiene la frecuencia por cada categoría de la palabra.
        (considerar las palabras en minúsculas)
        """
        tokens = self.corpus.tagged_words()
        dictionary = collections.defaultdict(lambda: [])
        for (word,category) in tokens:
            if word not in string.punctuation: # FIXME - No se si es necesario 
                flag = false
                for (category2, number) in dictionary[word.lower()]:
                    if category2 == category:
                        dictionary[word.lower()].remove((category2, number))
                        dictionary[word.lower()].append((category2, number+1))
                        flag = true
                if not flag:    
                    dictionary[word.lower()].append((category2, 1))
        return dictionary



    ## Parte 1.2
    # a
    def arbol_min_nodos(self):
        """
        Retorna el árbol del corpus con la mínima cantidad de nodos.
        (el primero si hay mas de uno con la misma cantidad)
        """
        return # ...

    def arbol_max_nodos(self):
        """
        Retorna el árbol del corpus con la máxima cantidad de nodos.
        (el primero si hay mas de uno con la misma cantidad)
        """
        return # ...


    # b
    def arboles_con_lema(self, lema):
        """
        Retorna todos los árboles que contengan alguna palabra con lema 'lema'.
        """
        # TODO - Posiblemente recursivo por la estructura del corpus
        return # ...

   


# Parte 2 - PCFG y Parsing
###########################


class PCFG:
    """
    Clase de funcionalidades sobre PCFG de AnCora.
    """

    sents = [   u'El juez manifestó que las medidas exigidas por el gobierno actual son muy severas .', #a
                u'El partido entre los equipos europeos tendrá lugar este viernes .', #b
                u'El domingo próximo se presenta la nueva temporada de ópera .', #c
            ]

    def __init__(self):
        corpus = Corpus()
        self.wordfrecs = corpus.palabras_frecs()
        self.grammar = self._induce_pcfg(corpus)
        self.parser  = self._generate_parser()

    ## Parte 2.1 (grammar)
    def _induce_pcfg(self, corpus):
        """
        Induce PCFG del corpus.
        """
        return # ...

    # a
    def reglas_no_lexicas(self):
        """
        Retornas las reglas que no son léxicas.
        """
        return # ...

    # b 
    def categorias_lexicas(self):
        """
        Retorna las categorías léxicas (se infieren de las reglas léxicas).
        """
        return # ...
        

    # c
    def reglas_lexicas(self, c):
        """
        Retorna las reglas léxicas de categoría 'c'
        """
        return # ...

    ## Parte 2.2 (parser)
    def _generate_parser(self):
        """
        Generate Viterbi parser from grammar.
        """
        return # ...

    ## Parte 2.3 (sentences)
    def parse(self, sentence):
        """
        Parse sentence and return ProbabilisticTree.
        """
        return # ...



# Parte 3 - PCFG con palabras desconocidas
##########################################


class PCFG_UNK(PCFG):
    """
    Clase de funcionalidades sobre PCFG de AnCora con UNK words.
    """

    sents = [   u'El domingo próximo se presenta la nueva temporada de ópera .', #a (2.3.c)
                u'Pedro y Juan jugarán el campeonato de fútbol .', #b 
            ]


    # Parte 3.1
    def _induce_pcfg(self, corpus):
        """
        Induce PCFG grammar del corpus (treebank) considerando palabras UNK.
        """
        return # ...


    # Parte 3.2 (y 3.3)

    def parse(self, sentence):
        """
        Retorna el análisis sintáctico de la oración contemplando palabras UNK.
        """
        return # ...



# Parte 4 - PCFG lexicalizada
##############################

# 1

class PCFG_LEX(PCFG):
    """
    PCFG de AnCora con lexicalización en primer nivel.
    """

    sents = [   u'El juez vino que avión .', #
            ]                

    def _induce_pcfg(self, corpus):
        """
        Induce PCFG del corpus considerando lexicalización en primer nivel.
        """
        return # ...





# 2

class PCFG_LEX_VERB(PCFG):
    """
    PCFG de AnCora con lexicalización en primer nivel y grupos verbales (grup.verb).
    """

    sents = [   u'El juez manifestó su apoyo al gobierno .', # i
                u'El juez opinó su apoyo al gobierno .', # ii

                u'El juez manifestó que renunciará .', # 4.2.c
            ]                

    def _induce_pcfg(self, corpus):
        """
        Induce PCFG del corpus considerando lexicalización en primer nivel y grupos verbales.
        """
        return # ...


# FIXME - http://www.cs.famaf.unc.edu.ar/~francolq/jcc
