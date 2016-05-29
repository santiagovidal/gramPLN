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
from nltk.draw.tree import draw_trees
import os
import sys
import time

# Constantes
CR = "%s%s%s" % ('\r',' '*50,'\r')

# Solicitar path
path= raw_input("AnCora path: ")
if not path: path = 'C:/data/ancora-3.0.1es/'

# Auxiliar para tomar tiempo
def timer(start,end):
	hours, rem = divmod(end-start, 3600)
	minutes, seconds = divmod(rem, 60)
	return "{:0>2}:{:0>2}:{:05.2f}".format(int(hours),int(minutes),seconds)

# Cargar instancias del problema
case = {
	"Corpus":Corpus,
	"PCFG":PCFG,
	"PCFG_UNK":PCFG_UNK,
	"PCFG_LEX":PCFG_LEX,
	"PCFG_LEX_VERB":PCFG_LEX_VERB
}
inst = {}
_ini = time.time()
for i, (name,obj) in enumerate(case.items()):
	print CR,"(%i/%i) Loading %s..." % (i+1,len(case),name),
	ini = time.time()
	inst[name] = case[name](path) 
	end = time.time()
	print CR,"%-13s - %s" % (name,timer(ini,end))
_end = time.time()
print "Tiempo transcurrido:",timer(_ini,_end)
raw_input("\nEnter para continuar...")

# Entrada/Salida
def print_menu():
	print "====================== MENU ======================"
	print "    0: Datos"
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
	print
	print "Enter para salir..."
	
def make(op):
	if op == 0:
		for name in case.keys():
			if name != "Corpus":
				print name
				print inst[name].grammar
				print inst[name].parser
				print "---"
	elif op == 1:
		cant_oraciones = inst["Corpus"].cant_oraciones()
		print CR,"Cantidad de oraciones: "
		print cant_oraciones
	elif op == 2:
		oracion_mas_larga = inst["Corpus"].oracion_mas_larga()
		print CR,"Oracion mas larga:"
		print len(oracion_mas_larga.split(' ')), "palabras"
		print oracion_mas_larga
	elif op == 3:
		largo_promedio_oracion = inst["Corpus"].largo_promedio_oracion()
		print CR,"Largo promedio de oración:"
		print largo_promedio_oracion
	elif op == 4:
		palabras_frecs = inst["Corpus"].palabras_frecs()
		print CR,"Palabras frecuentes:"
		print '\n\t'.join(map(str,sorted(palabras_frecs.items(),key=lambda x:x[1],reverse=True)[:20]))
	elif op == 5:
		palabras_frecs_cat = inst["Corpus"].palabras_frecs_cat()
		print CR,"Palabras frecuentes por categoria:"
		print '\n\t'.join(map(str,sorted(palabras_frecs_cat.items(),key=lambda x:len(x[1]),reverse=True)[:20]))
	elif op == 6:
		arbol_min_nodos = inst["Corpus"].arbol_min_nodos()
		print CR,"Arbol con minima cantidad de nodos:"
		print len(arbol_min_nodos.treepositions()), "nodos"
		arbol_min_nodos.pretty_print() 
	elif op == 7:
		arbol_max_nodos = inst["Corpus"].arbol_max_nodos()
		print CR,"Arbol con maxima cantidad de nodos:"
		print len(arbol_max_nodos.treepositions()), "nodos"
		arbol_max_nodos.pretty_print() 
	elif op == 8:
		lema = raw_input('\r'+' '*20+'\rLema > ')
		if not lema: lema = "mostrar"
		arboles_con_lema = inst["Corpus"].arboles_con_lema(lema)
		print CR,"Arbol con lema \'",lema,"\'"
		print len(arboles_con_lema), "arboles"
		print "** Ejemplo **"
		print ' '.join(arboles_con_lema[randint(0,len(arboles_con_lema)-1)].leaves())
	elif op == 9:
		sent = inst["PCFG"].sents[0]
		parsed = inst["PCFG"].parse(sent)
	elif op == 10:
		sent = inst["PCFG"].sents[1]
		parsed = inst["PCFG"].parse(sent)
	elif op == 11:
		sent = inst["PCFG"].sents[2]
		parsed = inst["PCFG"].parse(sent)
	elif op == 12:
		sent = inst["PCFG_UNK"].sents[0]
		parsed = inst["PCFG_UNK"].parse(sent)
	elif op == 13:
		sent = inst["PCFG_UNK"].sents[1]
		parsed = inst["PCFG_UNK"].parse(sent)
	elif op == 14:
		sent = inst["PCFG_LEX"].sents[0]
		parsed = inst["PCFG"].parse(sent)
	elif op == 15:
		sent = inst["PCFG_LEX"].sents[0]
		parsed = inst["PCFG_LEX"].parse(sent)
	elif op == 16:
		sent = inst["PCFG_LEX_VERB"].sents[0]
		parsed = inst["PCFG_LEX"].parse(sent)
	elif op == 17:
		sent = inst["PCFG_LEX_VERB"].sents[1]
		parsed = inst["PCFG_LEX"].parse(sent)
	elif op == 18:
		sent = inst["PCFG_LEX_VERB"].sents[0]
		parsed = inst["PCFG_LEX_VERB"].parse(sent)
	elif op == 19:
		sent = inst["PCFG_LEX_VERB"].sents[1]
		parsed = inst["PCFG_LEX_VERB"].parse(sent)
	elif op == 20:
		sent = inst["PCFG_LEX_VERB"].sents[2]
		parsed = inst["PCFG_LEX"].parse(sent)
	elif op == 21:
		sent = inst["PCFG_LEX_VERB"].sents[2]
		parsed = inst["PCFG_LEX_VERB"].parse(sent)
	else:
		print "Comando no valido!"
	if op in range(9,22):
		parsed = list(parsed)
		# parsed = [t for t in parsed]
		print CR,"Oracion:\n%s\n" % sent
		print "Cantidad de reconoceedores:\n%i\n" % len(parsed)
		for i,parse in enumerate(parsed):
			print "************* [%i] *************" % (i+1)
			print parse
			print "Graficando..."
			draw_trees(parse)
		
# Principal
while True:
	os.system('cls' if os.name == 'nt' else 'clear')
	print_menu()
	op = raw_input("> ")
	if not op: break
	op = int(op)
	print CR,"Procesando...",
	make(op)
	raw_input("\nEnter para continuar...")