import ancora_pcfg;
import ancora;
from nltk.draw.tree import draw_trees;
import nltk;
from collections import Counter
from string import join
corpus =  ancora.AncoraCorpusReader("../../ancora-3.0.1es/")

def lexicalize_tree(t):
	if not isinstance(t, tuple):
		new_tree = nltk.Tree(t.label(), [])

		if t.label() == "grup.verb":
			verbs_pos = filter(lambda pos: pos[1][0] == "v", t.pos()) # Devuelve una lista de ((palabra,lema),cat) siendo cat un verbo
			lemmas = map(lambda x: x[0][1], verbs_pos) #Devuelve una lista de lemas de verbos
			lemmas = "-".join(lemmas)

			new_tree.set_label("grup.verb-" + lemmas)

		for child in t:
			new_tree.append(lexicalize_tree(child))

		return new_tree
	else:
		return t[0]


trees = ancora_pcfg.lemmatized_sents(corpus)
lexicalized_trees = map(lambda tree: lexicalize_tree(tree), trees)


