from spacy.en import English
from nltk.stem.wordnet import WordNetLemmatizer
from pattern.en import singularize

verb = WordNetLemmatizer()
nlp = English()
# sentence = 'LIB system shall keep track of all data required by copyright licensing agencies In the Kingdom and elsewhere'
sentence = 'Michael Wasalsky and Phil Sulivan could have frightened those children'
# sentence = 'The book was read by me'
# sentence = 'Because the boys went to the park, they did not go to the zoo'
doc = nlp(unicode(sentence))
print(doc.ents)
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
		print("-===I found the Root Token:===-")
		print(token, token.pos_)
		leftRoot.append([token.orth_,[t.orth_ for t in token.lefts]])
		rightRoot.append([token.orth_,[t.orth_ for t in token.rights]])
		print(leftRoot)
		print(rightRoot)
leftSubj=[]
rightSubj=[]
print("------Left elements")


for elements in leftRoot[0][1]:
	for token in doc:
		if token.orth_ == elements:
			print(token.orth_, token.pos_)
print("-----SUBJECT")
su = []
rootCounter = 0
for token in doc:
	if token.dep_ == u'ROOT':
		rootCounter += 1
	su.append(token)
print("_______________")
preRoot= []
for t in su:
	if t.dep_ == u'ROOT':
		break
	print(t.orth_,t.pos_,t.dep_)
	preRoot.append(t)
	
print(len(preRoot))
print("/*-/*-/*-/*-/-*/-*/*-/*-")
name = ""
stakeholders = []
for t in preRoot:
	if t.pos_ == u'NOUN':
		if name == "":
			name = t.orth_
		else:
			name = name + ' ' + t.orth_
	else:
		stakeholders.append(name)
		name = ""
stakeholders = filter(None, stakeholders)
print(stakeholders)
print(verb.lemmatize(leftRoot[0][0].encode('ascii','replace'),'v'))
print(singularize(rightRoot[0][1][0].encode('ascii','replace')))

#a = list(set(a)) --> Get unique elements
# ====================DETALHES
#-Visualizar Arvore
#	https://spacy.io/demos/displacy
#print da linha 12 = (Palavra[seta chegada],Dependencia,Palavra[Seta saida],[setas de saida para esquerda],[setas de saida direita]) 
#pip install pattern