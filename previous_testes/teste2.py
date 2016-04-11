from spacy.en import English
nlp = English()
#sentence = 'LIB system shall keep track of all data required by copyright licensing agencies In the Kingdom and elsewhere'
sentence = 'Michael Wasalsky and Phil Sulivan could have scarried those children'
doc = nlp(unicode(sentence))

print("-----------------NOUNS")
for chunk in doc.noun_chunks:
    print(chunk.label_, chunk.orth_, '<--', chunk.root.head.orth_)
print("------------------TREE")
print(sentence)
for token in doc:
    print(token.orth_, token.dep_, token.head.orth_, [t.orth_ for t in token.lefts], [t.orth_ for t in token.rights])

leftRoot = []
rightRoot = []
for token in doc:
	if token.dep_  == u'ROOT':
		print("I found the Root Token:")
		print(token)
		leftRoot.append([token.orth_,[t.orth_ for t in token.lefts]])
		rightRoot.append([token.orth_,[t.orth_ for t in token.rights]])
		print(leftRoot)
		print(rightRoot)
leftSubj=[]
rightSubj=[]
print("------Left elements")
for root in leftRoot:
	for element in root[1]:
		for token in doc:
			if token.orth_ == unicode(element):
				if token.dep_ == u'nsubj':
					leftSubj.append(token) 

		print(element)
print("-----Right elements")
for root in rightRoot:
	for element in root[1]:
		for token in doc:
			if token.orth_ == unicode(element):
				if token.dep_ == u'nsubj':
					rightSubj.append(token)
print("------- subj")
print(leftSubj)
print(rightSubj)
#a = list(set(a)) --> Get unique elements
# ====================DETALHES
#-Visualizar Arvore
#	https://spacy.io/demos/displacy
#print da linha 12 = (Palavra[seta chegada],Dependencia,Palavra[Seta saida],[setas de saida para esquerda],[setas de saida direita]) 