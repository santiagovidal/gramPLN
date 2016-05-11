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
#  Estudiante 3: 	Santiago Vidal Aguirre 	- 4.651.496-6
#
#

from ancora_pcfg import Corpus
from string import split

# Cofiguracion
path= raw_input("Relative path: ") # 'C:/data/ancora-3.0.1es/'
if not path: path = 'C:/data/ancora-3.0.1es/'

# ----------------------------
# class Corpus
# ----------------------------
corpus = Corpus(path)
# 1.1
cant_oraciones         = corpus.cant_oraciones()
print '%-23s %i\n'      % ("cant_oraciones", cant_oraciones)
oracion_mas_larga      = corpus.oracion_mas_larga()
print '%-23s (%i) %s\n' % ("oracion_mas_larga", len(oracion_mas_larga.split(' ')), oracion_mas_larga[:50]+"...")
largo_promedio_oracion = corpus.largo_promedio_oracion()
print '%-23s %i\n'      % ("largo_promedio_oracion", largo_promedio_oracion)
N = raw_input("Cantidad a ver: "); N = int(N)
palabras_frecs         = corpus.palabras_frecs()
print '%-23s\n%s\n'      % ("palabras_frecs", '\n'.join(map(str,palabras_frecs.items()[:N])))
palabras_frecs_cat     = corpus.palabras_frecs_cat()
print '%-23s\n%s\n'      % ("palabras_frecs_cat", '\n'.join(map(str,palabras_frecs_cat.items()[:N])))

# 1.2
arbol_min_nodos = corpus.arbol_min_nodos()
print '%-23s %s\n' % ("arbol_min_nodos", str(arbol_min_nodos))
arbol_max_nodos = corpus.arbol_max_nodos()
print '%-23s %s\n' % ("arbol_max_nodos", str(arbol_max_nodos))
lema = raw_input("Lema: ")
arboles_con_lema = corpus.arboles_con_lema(lema)
print '%-23s %s\n' % ("arboles_con_lema", str(arboles_con_lema))


# ----------------------------
# class PCFG
# ----------------------------



# ----------------------------
# class PCFG_UNK
# ----------------------------



# ----------------------------
# class PCFG_LEX
# ----------------------------
