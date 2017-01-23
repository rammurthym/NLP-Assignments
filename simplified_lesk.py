# Name: Rammurthy Mudimadugula
# NetID: RXM163730
# Homework #3

import nltk
from nltk.corpus import wordnet as wn

#*******************************************************************************
#                           Method Definitions
#*******************************************************************************

def simplified_lesk (word, sentence):
	syn_set = wn.synsets(word)
	best_sense = None
	max_overlap = 0
	context = ignoreFunctionWords(sentence)
	context.remove(word)

	for sense in syn_set:
		overlap = compute_overlap(sense, context)
		print('Sense: ' + sense.definition() + ', Overlap count: ' + str(overlap))
		if overlap > max_overlap:
			max_overlap = overlap
			best_sense = sense

	return (best_sense, max_overlap)

def compute_overlap (sense, context):
	definition = sense.definition()
	example = sense.examples()
	example = ' '.join(example)

	temp = definition + ' ' + example

	def_context = ignoreFunctionWords(temp)

	count = 0

	for c in def_context:
		if c in context:
			count += 1

	return count

def ignoreFunctionWords (sentence):
	tags = ['DT', 'MD', 'IN', 'PRP']
	out = []

	pos_tags = nltk.pos_tag(nltk.word_tokenize(sentence))

	for token in pos_tags:
		if token[1] not in tags:
			out.append(token[0])
	return out

#*******************************************************************************
#                           Method Calls
#*******************************************************************************

sentence = '''The bank can guarantee deposits will eventually cover future 
tuition costs because it invests in adjustable-rate mortgage securities'''

word = 'bank'

(bs, ol) = simplified_lesk(word, sentence)

print()

print('Best sense: ' + bs.definition())
print('Overlap count: ' + str(ol))
