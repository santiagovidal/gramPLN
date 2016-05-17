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
#  Estudiante 1: 	Nicolás Mechulam Burstin 	- 4.933.997-7
#  Estudiante 2: 	Damián Salvia Varela 		- 4.452.120-0
#  Estudiante 3: 	Santiago Vidal Aguade 		- 4.651.496-6
#
#

from ancora_pcfg import Corpus, PCFG, PCFG_UNK, PCFG_LEX, PCFG_LEX_VERB
from string import split,join
from random import randint
from nltk.grammar import Nonterminal

# Cofiguracion
path= raw_input("Relative path: ")
if not path: path = 'C:/data/ancora-3.0.1es/'

# ----------------------------
# class Corpus
# ----------------------------
corpus = Corpus(path)
# 1.1
print "\n====================== PARTE 1.1 ======================\n"
cant_oraciones         = corpus.cant_oraciones()
print '%-23s %i\n'     % ("cant_oraciones", cant_oraciones)
oracion_mas_larga      = corpus.oracion_mas_larga()
print '%-23s %i palabras\n\t%s\n' % ("oracion_mas_larga", len(oracion_mas_larga.split(' ')), oracion_mas_larga[:50]+"...")
largo_promedio_oracion = corpus.largo_promedio_oracion()
print '%-23s %i\n'     % ("largo_promedio_oracion", largo_promedio_oracion)
palabras_frecs         = corpus.palabras_frecs()
print '%-23s\n\t%s\n'  % ("palabras_frecs", '\n\t'.join(map(str,sorted(palabras_frecs.items(),key=lambda x:x[1],reverse=True)[:20])))
palabras_frecs_cat     = corpus.palabras_frecs_cat()
print '%-23s\n\t%s\n'  % ("palabras_frecs_cat", '\n\t'.join(map(str,sorted(palabras_frecs_cat.items(),key=lambda x:len(x[1]),reverse=True)[:20])))

# 1.2
print "\n====================== PARTE 1.2 ======================\n"
arbol_min_nodos 		 = corpus.arbol_min_nodos()
print '%-23s %i nodos\n' % ("arbol_min_nodos", len(arbol_min_nodos.treepositions()))
arbol_max_nodos 		 = corpus.arbol_max_nodos()
print '%-23s %i nodos\n' % ("arbol_max_nodos", len(arbol_max_nodos.treepositions()))
lema = "mostrar"
arboles_con_lema 		 = corpus.arboles_con_lema(lema)
print '%-23s %i arboles con \'%s\'\n\t%s\n' % ("arboles_con_lema", len(arboles_con_lema), lema,' '.join(arboles_con_lema[randint(0,len(arboles_con_lema)-1)].leaves()))


# ----------------------------
# class PCFG
# ----------------------------
#pcfg = PCFG(path)
pcfg = PCFG(path)
# 2.1
print "\n====================== PARTE 2.1 ======================\n"
print '%-23s %i reglas\n' % ("_indice_pcfg",len(pcfg.grammar.productions()))

# a
reglas_no_lexicas = pcfg.reglas_no_lexicas()
print '%-23s %i reglas\n' % ("reglas_no_lexicas",len(reglas_no_lexicas))

# b
categorias_lexicas = pcfg.categorias_lexicas()
print '%-23s %i reglas\n' % ("categorias_lexicas",len(categorias_lexicas))

# c
categoria = "sentence"
reglas_lexicas = pcfg.reglas_lexicas(Nonterminal(categoria))
print '%-23s %i reglas para \'%s\'\n' % ("reglas_lexicas",len(reglas_lexicas),categoria)


# 2.2
print '%-23s %s\n' % ("_generate_parser",str(pcfg.parser))

# 2.3
parse_a = pcfg.parse(pcfg.sents[0])
parse_b = pcfg.parse(pcfg.sents[1])
parse_c = pcfg.parse(pcfg.sents[2])
print '%-23s \n%s\n%s\n%s\n' % ("parse",
	"\t---- A ----\n\t"+len(list(parse_a)),
	"\t---- B ----\n\t"+len(list(parse_b)),
	"\t---- C ----\n\t"+len(list(parse_c)))

# ----------------------------
# class PCFG_UNK
# ----------------------------
pcfg_unk = PCFG_UNK(path)
print "\n====================== PARTE 3.1 ======================\n"

# ----------------------------
# class PCFG_LEX
# ----------------------------
pcfg_lex = PCFG_LEX(path)
print "\n====================== PARTE 4.1 ======================\n"

# ----------------------------
# class PCFG_LEX_VERB
# ----------------------------
pcfg_lex_verb = PCFG_LEX_VERB(path)
print "\n====================== PARTE 4.2 ======================\n"