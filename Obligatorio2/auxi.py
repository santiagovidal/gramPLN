import ancora_pcfg;
import ancora;
from nltk.draw.tree import draw_trees;
import nltk;
from collections import Counter
from string import join
corpus =  ancora.AncoraCorpusReader("../../ancora-3.0.1es/")

prods_global = []
for t in ancora_pcfg.lemmatized_sents(corpus):

	print "Cantidad de producciones en t: " + str(len(t.productions()))

	subtrees = list(t.subtrees(lambda x: x.label() == "grup.verb"))

	prods_subt = sum((subt.productions() for subt in subtrees), [])
	prods_t = t.productions()

	n_anterior = len(prods_global)

	prods_global += [nltk.Production(p.lhs(), [p.rhs()[0][0]])
					if p.is_lexical()
					else p
					for p in list((Counter(prods_t) - Counter(prods_subt)).elements())]

	n_despues = len(prods_global)
	n_diff = n_despues - n_anterior
	# print "Cantidad de producciones no grup.verb agregadas: " + str(n_diff)

	acumulador = 0

	for subt in subtrees:
		prods = subt.productions()

		lemas = []
		for p in prods:
			if p.is_lexical() and str(p.lhs())[0] == "v"):
				lemas += [p.rhs()[0][1]]

		lemas = "-".join(lemas)

		acumulador += len(prods)

		for p2 in prods:
			if str(p2.lhs()) == "grup.verb":
				prods_global += [nltk.Production(nltk.Nonterminal("%s-%s" % (str(p2.lhs()), lemas)), p2.rhs())]
			elif p2.is_lexical():
				prods_global += [nltk.Production(p2.lhs(), [p2.rhs()[0][0]])]
			else:
				prods_global += [p2]

	if len(t.productions()) != (n_diff + acumulador):
		print "Error: " + str(acumulador) + " //// " + str(len(t.productions())) + " //// " + str(n_diff)
		draw_trees(t)
		raw_input("")








# prods = [ prod for
# 			possibles in [ [nltk.Production(nltk.Nonterminal(str(possible_prod.lhs())+"-MIO"),possible_prod.rhs())] 
# 				if str(possible_prod.lhs()) == "grup.verb"
# 				else [possible_prod]
# 				for t in ancora_pcfg.lemmatized_sents(corpus)
# 				for possible_prod in t.productions()]
# 			for prod in possibles]

# grammar = ancora_pcfg.PCFG("../../ancora-3.0.1es/")
# from nltk.draw.tree import draw_trees

