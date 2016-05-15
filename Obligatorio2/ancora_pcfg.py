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
#  Estudiante 3:    Santiago Vidal Aguade      	- 4.651.496-6
#
#


#import nltk
import nltk
import ancora  # (Modulo para leer AnCora)

# Otros modulos de utilidad
from collections import defaultdict
from string import punctuation, split, join


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
        return ' '.join(max(sentences, key=lambda sentence: len(sentence)))


    # c.
    def largo_promedio_oracion(self):
        """
        Retorna el largo de oracion promedio.
        """
        sentences = list(self.corpus.sents())
        return sum([len(sentence) for sentence in sentences])/len(sentences)

    # d.
    def palabras_frecs(self):
        """
        Retorna un diccionario (dict) palabra-frecuencia de las palabras del corpus.
        (considerar las palabras en minúsculas)
        """
        tokens = self.corpus.tagged_words()
        dictionary = defaultdict(lambda: 0)
        for (word,_) in tokens:
            if not word: # OBS - Hay word = None
                continue
            dictionary[word.lower()] += 1
        return dictionary

    # e.
    def palabras_frecs_cat(self):
        """
        Retorna un diccionario (dict) palabra-lista de las palabras del corpus.
        Cada lista contiene la frecuencia por cada categoría de la palabra.
        (considerar las palabras en minúsculas)
        """
        from itertools import groupby
        tokens = sorted(self.corpus.tagged_words(),key=lambda x:x[0])
        dictionary = defaultdict(lambda: [])
        for word,word_category_lst in groupby(tokens,lambda x:x[0]):
            if not word: continue # OBS - Hay word = None
            categories_word = sorted(map(lambda x:x[1],list(word_category_lst)))
            dictionary[word.lower()] = sum((
                    [(category,len(list(set_same_category)))] # (cat,cant)
                        for category,set_same_category in groupby(categories_word,lambda x:x)
                ),[])
        return dictionary


    ## Parte 1.2
    # a
    def arbol_min_nodos(self):
        """
        Retorna el árbol del corpus con la mínima cantidad de nodos.
        (el primero si hay mas de uno con la misma cantidad)
        """
        trees = self.corpus.parsed_sents()
        return min(trees, key=lambda tree : len(tree.treepositions()))

    def arbol_max_nodos(self):
        """
        Retorna el árbol del corpus con la máxima cantidad de nodos.
        (el primero si hay mas de uno con la misma cantidad)
        """
        trees = self.corpus.parsed_sents()
        return max(trees, key=lambda tree : len(tree.treepositions()))


    # b
    def arboles_con_lema(self, lema):
		"""
		Retorna todos los árboles que contengan alguna palabra con lema 'lema'.
		"""
		#trees = self.corpus.parsed_sents() # FIXME - El corpus da palabras, no lemas. ¿Que hacer?
		#return filter(lambda tree : lema in tree.leaves(), trees)
		from nltk import tree
		from nltk.corpus.reader.util import concat
		from nltk.util import LazyMap
		parsed_sents = self.corpus.parsed_sents()
		def lemmatized(element): # Subprocedimiento recursivo que deja en las hojas los lemas
			if element:
				subtrees = map(lemmatized, element)
				subtrees = [t for t in subtrees if t is not None]
				return tree.Tree(element.tag, subtrees)
			else:
				if element.get('elliptic') == 'yes':
					return None
				else:
					return tree.Tree(element.get('lem') or 'unk', [element.get('wd')])
		fileids = self.corpus.xmlreader.fileids()
		lemmatized_sents = LazyMap(lemmatized, concat([list(self.corpus.xmlreader.xml(fileid)) for fileid in fileids]))
		trees_with_lemma = []
		for i in range(len(parsed_sents)):
			words_for_lemma = set([subtree.leaves()[0] 
								   for subtree in lemmatized_sents[i].subtrees(lambda s: s.label() == lema)])
			if any([word in words_for_lemma for word in parsed_sents[i].leaves()]):
				trees_with_lemma.append(parsed_sents[i])
		return trees_with_lemma   


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

    def __init__(self, corpus_path='./relative-path/'): # FIXME - Antes no existía 'corpus_path'
        corpus = Corpus(corpus_path)
        self.wordfrecs = corpus.palabras_frecs()
        self.grammar = self._induce_pcfg(corpus)
        self.parser  = self._generate_parser()

    ## Parte 2.1 (grammar)
    def _induce_pcfg(self, corpus):
        """
        Induce PCFG del corpus.
        """
        prods = sum((t.productions() for t in corpus.corpus.parsed_sents()), [])
        S = nltk.Nonterminal('sentence')
        grammar = nltk.induce_pcfg(S, prods)
        return grammar

    # a
    def reglas_no_lexicas(self):
        """
        Retornas las reglas que no son léxicas.
        """
        return filter(lambda rule: rule.is_nonlexical(), self.grammar.productions())

    # b 
    def categorias_lexicas(self):
        """
        Retorna las categorías léxicas (se infieren de las reglas léxicas).
        """
        # Primero filtra las reglas lexicas, y despues se queda con el lado izquierdo de la regla
        # O sea el "lhs"
        return map(lambda x: x.lhs(), filter(lambda rule: rule.is_lexical(), self.grammar.productions()))
        

    # c
    def reglas_lexicas(self, c):
        """
        Retorna las reglas léxicas de categoría 'c'
        """
        return filter(lambda rule: rule.is_lexical() and rule.lhs() == c, self.grammar.productions())

    ## Parte 2.2 (parser)
    def _generate_parser(self):
        """
        Generate Viterbi parser from grammar.
        """
        return nltk.ViterbiParser(self.grammar)

    ## Parte 2.3 (sentences)
    def parse(self, sentence):
        """
        Parse sentence and return ProbabilisticTree.
        """
        return self.parser.parse(sentence.split())



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
        prods = sum((t.productions() for t in corpus.corpus.parsed_sents()), [])
        one_time_words = filter(lambda word: self.wordfrecs[word] == 1, self.wordfrecs.keys())
        unk_symbol = nltk.Nonterminal("UNK")

        aux = 0
        total = len(prods)
        for prod in prods:
            aux = aux + 1
            print "Checking " + str(aux) + "/" + str(total)
            if len(prod.rhs()) == 1 and prod.rhs()[0] in one_time_words:
                print "DEBUG: Regla sustituida por UNK"
                prods.remove(prod)
                prods.append(nltk.Production(prod.lhs(),[unk_symbol]))

        S = nltk.Nonterminal('sentence')
        return nltk.induce_pcfg(S, prods)


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
