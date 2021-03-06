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


# Modulos
##########
import nltk
import ancora  # (Modulo para leer AnCora)

# Otros modulos
################
from collections import defaultdict
from string import punctuation, split, join
from nltk.util import LazyMap
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


# Auxiliares
#############
def lemmatized_sents(corpus,fileids=None):
	"""
	Retorna árboles cuyas hojas son parejas (word,lemma)
	"""
	from nltk import tree
	from nltk.corpus.reader.util import concat
	def lemmatized(element):
		if element:
			subtrees = map(lemmatized, element)
			subtrees = [t for t in subtrees if t]
			return tree.Tree(element.tag, subtrees)
		elif element.get('elliptic') == 'yes': return None
		else: return tree.Tree(element.get('pos') or element.get('ne') or 'unk', [(element.get('wd'),element.get('lem'))])
	if not fileids: fileids = corpus.xmlreader.fileids()
	return LazyMap(lemmatized, concat([list(corpus.xmlreader.xml(fileid)) for fileid in fileids]))

def lexicalize(tree, grup=None):
	"""
	Lexicaliza un árbol en el primer nivel y opcionalmente en algún grupo
	"""
	if not isinstance(tree, tuple):
		new_tree = nltk.Tree(tree.label(), [])
		if len(tree) == 1 and isinstance(tree[0], tuple):
			new_tree.set_label(u"%s-%s"%(tree.label(),tree[0][1]))
		elif grup and tree.label() == grup:
			verbs_pos = filter(lambda pos: pos[1][0] == grup[5], tree.pos()) # Devuelve una lista de ((palabra,lema),cat) siendo cat un verbo
			lemmas = map(lambda x: x[0][1], verbs_pos) # Devuelve una lista de lemas de verbos
			lemmas = "-".join(lemmas)
			new_tree.set_label(u"%s-%s"%(tree.label(),lemmas))
		for child in tree:
			new_tree.append(lexicalize(child,grup))
		return new_tree
	else: return tree[0]


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
        # return sum([len(sentence.split()) for sentence in sentences])/len(sentences)

    # d.
    def palabras_frecs(self):
        """
        Retorna un diccionario (dict) palabra-frecuencia de las palabras del corpus.
        (considerar las palabras en minúsculas)
        """
        tokens = self.corpus.tagged_words()
        dictionary = defaultdict(lambda: 0)
        for (word,_) in tokens:
            if not word: continue # OBS - Hay word = None
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
		parsed = self.corpus.parsed_sents()
		lemmatized = lemmatized_sents(self.corpus)
		return map(lambda x:x[0], 
					filter( lambda x: any([lem == lema for (_,lem) in x[1].leaves()]), 
							zip(parsed,lemmatized)))   
		
		
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

    def __init__(self, corpus_path='./relative-path/'):
		corpus = Corpus(corpus_path)
		self.wordfrecs = corpus.palabras_frecs()
		self.grammar = self._induce_pcfg(corpus)
		self.parser  = self._generate_parser()

    ## Parte 2.1 (grammar)
    def _induce_pcfg(self, corpus):
		"""
		Induce PCFG del corpus.
		"""
		prods = sum((t.productions() for t in corpus.corpus.parsed_sents()),[])
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
        return map(lambda x: x.lhs(), filter(lambda rule: rule.is_lexical(), self.grammar.productions()))

    # c
    def reglas_lexicas(self, c):
        """
        Retorna las reglas léxicas de categoría 'c'
        """
        return filter(lambda rule: rule.is_lexical() and str(rule.lhs()) == c, self.grammar.productions())

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
		def induce_unk(tree):
			for prod in tree.productions():
				if prod.is_lexical() and self.wordfrecs[prod.rhs()[0]] == 1:
					yield nltk.Production(prod.lhs(),["UNK"])
				else: yield prod
		prods = sum((list(induce_unk(t)) for t in corpus.corpus.parsed_sents()), [])
		S = nltk.Nonterminal('sentence')
		return nltk.induce_pcfg(S, prods)


    # Parte 3.2 (y 3.3)
    def parse(self, sentence):
		"""
		Retorna el análisis sintáctico de la oración contemplando palabras UNK.
		"""
		words = ["UNK" if word.lower() not in self.wordfrecs.keys()
						or self.wordfrecs[word.lower()] == 1
					else word
					for word in sentence.split()]
		return self.parser.parse(words)



# Parte 4 - PCFG lexicalizada
##############################

# 1
class PCFG_LEX(PCFG):
    """
    PCFG de AnCora con lexicalización en primer nivel.
    """

    sents = [   u'El juez vino que avión .', # a
            ]                

    def _induce_pcfg(self, corpus):
		"""
		Induce PCFG del corpus considerando lexicalización en primer nivel.
		"""
		prods = sum((lexicalize(t).productions() for t in lemmatized_sents(corpus.corpus)), [])
		S = nltk.Nonterminal('sentence')
		return nltk.induce_pcfg(S, prods)


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
		prods = sum((lexicalize(t, grup="grup.verb").productions() for t in lemmatized_sents(corpus.corpus)), [])			
		S = nltk.Nonterminal('sentence')
		return nltk.induce_pcfg(S, prods)
