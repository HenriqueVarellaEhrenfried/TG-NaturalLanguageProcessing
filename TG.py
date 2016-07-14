from spacy.en import English
from nltk.stem.wordnet import WordNetLemmatizer
from itertools import chain
import inflection
import re

class Text:
    def __init__(self, nlp, verb_processor, text=None): 
        self.nlp = nlp
        self.verb_processor = verb_processor
        self.sentences = Text.gen_sentences(self,text)
        self.tokenized_sentences = Text.tokenize(self, self.nlp, self.sentences)
    def gen_sentences(self, text):
        if text!=None:
            sentences = text.split(".")
            return sentences
        else:
            sys.exit("Invalid Text!!")
    def tokenize(self, nlp, sentences):
        all_sentences = []
        for sntc in sentences:
            temp = nlp(sntc)
            all_sentences.append(temp)
        return all_sentences

class Sentence:
    def __init__(self, sentence): 
        self.original_sentence = sentence
        self.subjects=Sentence.get_subject(self, self.original_sentence)
        self.verbs=Sentence.get_verb(self, self.subjects)
        self.complements=Sentence.get_comp(self, self.verbs)

    def get_subject(self, sent):
        subject_init_token = []
        for token in sent:
            if (re.match(r'nsubj', token.dep_)):
                subject_init_token.append(token)
        subjects = []
        for token in subject_init_token:
            partial_subtree_subject = []
            for tk in token.subtree:
                partial_subtree_subject.append(tk)
            subjects.append(partial_subtree_subject)
        return (subjects, subject_init_token)

    def get_verb(self, subj):
        verbs = []
        for s in subj[1]:
            verb_in_sentence = s.head
            verbs.append(verb_in_sentence)
        return verbs

    def get_comp(self, verbs):
        objects = []
        for token in verbs:
            partial_subtree_object = []
            for tk in token.rights:
                for t1 in tk.subtree:
                    partial_subtree_object.append(t1)
            objects.append([partial_subtree_object,[tk.head, tk]])
        return (objects)
                 

t = Text(English(),WordNetLemmatizer(),'I like pizza')
s = []
for sntc in t.tokenized_sentences:
    s.append(Sentence(sntc))
print(s[0])
print(s[0].subjects)
print(s[0].verbs)
print(s[0].complements)