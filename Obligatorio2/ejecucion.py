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
import os
import sys
import time

# Solicitar path
path= raw_input("AnCora path: ")
if not path: path = 'C:/data/ancora-3.0.1es/'

# Auxiliar para tomar tiempo
def timer(start,end):
	hours, rem = divmod(end-start, 3600)
	minutes, seconds = divmod(rem, 60)
	print "{:0>2}:{:0>2}:{:05.2f}".format(int(hours),int(minutes),seconds)

# Cargar instancias del problema - FIXME: Demora horas
ini = time.time()
for i in range(3):
	name = "Corpus" if i == 0 else "PCFG" if i == 1 else "PCFG_UNK" if i == 2 else "PCFG_LEX" if i == 3 else "PCFG_LEX_VERB"
	print " (%i/5) Cargando %s...\r" % (i+1,name),
	if   i == 0 : corpus = Corpus(path)
	elif i == 1 : pcfg = PCFG(path)
	elif i == 2	: pcfg_unk = PCFG_UNK(path)
	elif i == 3	: pcfg_lex = PCFG_LEX(path)
	elif i == 4 : pcfg_lex_verb = PCFG_LEX_VERB(path)
end = time.time()
print '\r',' '*20,"\rTiempo transcurrido:"
timer(ini,end)
raw_input("Listo. Enter para continuar...")

# Entrada/Salida
def print_menu():
	print "====================== MENU ======================"
	print "    Parte 1 - Corpus"
	print "       Parte 1.1"
	print "          1  : cant_oraciones"
	print "          2  : oracion_mas_larga"
	print "          3  : largo_promedio_oracion"
	print "          4  : palabras_frecs"
	print "          5  : palabras_frecs_cat"
	print "       Parte 1.2"
	print "          6  : arbol_min_nodos"
	print "          7  : arbol_max_nodos"
	print "          8  : arboles_con_lema"
	print "    Parte 2 - PCFG"
	print "       Parte 2.3"
	print "          9  : Parte (a)"
	print "          10 : Parte (b)"
	print "          11 : Parte (b)"
	print "    Parte 3 - PCFG UNK"
	print "       Parte 3.3"
	print "          12 : Parte (a)"
	print "          13 : Parte (b)"
	print "    Parte 4 - PCFG LEX"
	print "       Parte 4.1"
	print "          14 : Parte (a)"
	print "          15 : Parte (b)"
	print "       Parte 4.2"
	print "          16 : Parte (a) I"
	print "          17 : Parte (a) II"
	print "          18 : Parte (b) I"
	print "          19 : Parte (b) II"
	print "          20 : Parte (c) I"
	print "          21 : Parte (c) II"
	
def make(op):
	if op == 1:
		cant_oraciones = corpus.cant_oraciones()
		print "\rCantidad de oraciones: "
		print cant_oraciones
	elif op == 2:
		oracion_mas_larga = corpus.oracion_mas_larga()
		print "\rOracion mas larga:"
		print len(oracion_mas_larga.split(' ')), "palabras"
		print oracion_mas_larga
	elif op == 3:
		largo_promedio_oracion = corpus.largo_promedio_oracion()
		print "\rLargo promedio de oración:"
		print largo_promedio_oracion
	elif op == 4:
		palabras_frecs = corpus.palabras_frecs()
		print "\rPalabras frecuentes:"
		print '\n\t'.join(map(str,sorted(palabras_frecs.items(),key=lambda x:x[1],reverse=True)[:20]))
	elif op == 5:
		palabras_frecs_cat = corpus.palabras_frecs_cat()
		print "\rPalabras frecuentes por categoria:"
		print '\n\t'.join(map(str,sorted(palabras_frecs_cat.items(),key=lambda x:len(x[1]),reverse=True)[:20]))
	elif op == 6:
		arbol_min_nodos = corpus.arbol_min_nodos()
		print "\rArbol con minima cantidad de nodos:"
		print len(arbol_min_nodos.treepositions()), "nodos"
		arbol_min_nodos.pretty_print() 
	elif op == 7:
		arbol_max_nodos = corpus.arbol_max_nodos()
		print "\rArbol con maxima cantidad de nodos:"
		print len(arbol_max_nodos.treepositions()), "nodos"
		arbol_max_nodos.pretty_print() 
	elif op == 8:
		lema = raw_input('\r'+' '*20+'\rLema > ')
		if not lema: lema = "mostrar"
		arboles_con_lema = corpus.arboles_con_lema(lema)
		print "\rArbol con lema \'",lema,"\'"
		print len(arboles_con_lema), "arboles"
		print "** Ejemplo **"
		print ' '.join(arboles_con_lema[randint(0,len(arboles_con_lema)-1)].leaves())
	elif op == 9:
		sent = pcfg.sents[0]
		parsed = pcfg.parse(sent)
	elif op == 10:
		sent = pcfg.sents[1]
		parsed = pcfg.parse(sent)
	elif op == 11:
		sent = pcfg.sents[2]
		parsed = pcfg.parse(sent)
	elif op == 12:
		sent = pcfg_unk.sents[0]
		parsed = pcfg_unk.parse(sent)
	elif op == 13:
		sent = pcfg_unk.sents[1]
		parsed = pcfg_unk.parse(sent)
	elif op == 14:
		sent = pcfg_lex.sents[0]
		parsed = pcfg.parse(sent)
	elif op == 15:
		sent = pcfg_lex.sents[0]
		parsed = pcfg_lex.parse(sent)
	elif op == 16:
		sent = pcfg_lex_verb.sents[0]
		parsed = pcfg_lex.parse(sent)
	elif op == 17:
		sent = pcfg_lex_verb.sents[1]
		parsed = pcfg_lex.parse(sent)
	elif op == 18:
		sent = pcfg_lex_verb.sents[0]
		parsed = pcfg_lex_verb.parse(sent)
	elif op == 19:
		sent = pcfg_lex_verb.sents[1]
		parsed = pcfg_lex_verb.parse(sent)
	elif op == 20:
		sent = pcfg_lex_verb.sents[2]
		parsed = pcfg_lex.parse(sent)
	elif op == 21:
		sent = pcfg_lex_verb.sents[2]
		parsed = pcfg_lex_verb.parse(sent)
	else:
		print "Comando no valido!"
	if op in range(9,22):
		parsed = [t for t in parsed]
		print "\rOracion:\n",sent,"\n"
		print len(parsed),"reconocedores\n"
		print "** Ejemplo **"
		print parsed[randint(0,len(parsed)-1)]

# Principal
while True:
	os.system('cls' if os.name == 'nt' else 'clear')
	print_menu()
	op = raw_input("> ")
	if not op: op = 0
	else: op = int(op)
	if op == 0: break
	print "\rProcesando...",
	make(op)
	raw_input("\nEnter para continuar...")