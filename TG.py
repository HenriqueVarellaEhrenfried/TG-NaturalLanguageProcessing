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
    def token_to_string(a): # Receive an array of tokens, Return a string
        st = ''
        for item in a:
            st+=item.orth_+' '
        return st[:-1]

class Sentence:
    def __init__(self, sentence): 
        self.original_sentence = sentence
        self.subjects=Sentence.get_subject(self, self.original_sentence)
        self.verbs=Sentence.get_verb(self, self.subjects[0]) # subjects[0]=normal subjects, subject[1]=agreagated subjects
        self.complements=Sentence.get_comp(self, self.verbs)

    def agregate_subj(self, subj_to_agregate):
        subjSum = 0
        subjects=[]
        subject_pronouns=['I','He','She','It','You','We','They']
        relative_pronouns=['Who','Which','Whose','That','Where','When']
        adjective_possessive=['My','Your','His','Her','Its','Our','Their']
        possessive_pronouns=['Mine','Yours','His','Hers','Its','Ours','Theirs']
        for b in subj_to_agregate[0]:
            vet = Text.token_to_string(b)
            subjects.append([vet, b, 2]) # 3rd element is the control -> 0 = Not Valid, 1 = Valid, 2 = Not Verified
        for s in subjects:
            if s[2]==2:
                evaluate = (s[0].capitalize() in subject_pronouns) or (s[0].capitalize() in relative_pronouns) or (s[0].split( )[0].capitalize() in adjective_possessive) or (s[0].split( )[0].capitalize() in possessive_pronouns)
                if evaluate:
                    s[2] = 0
                else:
                    s[2] = 1
                    
        last_computed_index = -1
        for i, s in enumerate(subjects):
            if s[2]==0:
                if (s[0].capitalize() in subject_pronouns) or (s[0].capitalize() in relative_pronouns):
                    s[0]=subjects[i-1][0]
                elif (s[0].split( )[0].capitalize() in adjective_possessive):
                    actual_computed_index = i
                    if last_computed_index+1 != actual_computed_index:
                        owner=subjects[i-1][0]
                        if owner.endswith('s'):
                            owner = owner + '\' '
                        else:
                            owner = owner + '\'s '
                        temp_subj = s[0]
                        array_list = temp_subj.split()
                        array_list[0] = owner
                        string_subj_temp=''
                        for sub in array_list:
                            string_subj_temp+=sub
                        s[0] = string_subj_temp
                    else:
                        temp_subj = s[0]
                        array_list = temp_subj.split()
                        array_list[0] = owner
                        string_subj_temp=''
                        for sub in array_list:
                            string_subj_temp+=sub
                        s[0] = string_subj_temp
                        
                    last_computed_index = actual_computed_index

        return subjects             


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
        partial_subject = (subjects, subject_init_token)
        return (partial_subject, self.agregate_subj(partial_subject))

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