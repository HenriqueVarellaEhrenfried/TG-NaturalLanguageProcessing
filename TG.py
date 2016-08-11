from spacy.en import English
from nltk.stem.wordnet import WordNetLemmatizer
from itertools import chain
import inflection
import re
import sys
import json

problem = "A Company needs a new system called, Payroll System, to allow employees to record timecard information electronically and automatically generate paychecks based on the number of hours worked and total amount of sales(for commissioned employees). The new system will be state of art and will have a Windows-based desktop interface to allow employees to enter timecard information, enter purchase orders, change employee preferences (such as payment method) and create various reports. The system will run on individual employee desktops throughout the entire company.The system will retain information on all employees in the company. The system must pay each employee the correct amount, on time, by the method that they specify.Some employees work by the hour and are paid an hourly rate. They submit timecards that record the date and number of hours worked for a particular charge number. Some employees are paid a flat salary. Even though they are paid a flat salary, they submit timecards that record the date and hours worked. Some of the salaried employees also receive a commission based on their sales. They submit purchase orders that reflect the date and amount of the sale.One of the most requested features of the new system is employee reporting.Employees will be able to query the system for hours worked, totals of all hours billed to a project, total pay received year to date, etc.,Employees can choose their method of payment. They can have their paychecks mailed to the postal address of their choice, or they can request direct deposit and have their paycheck deposited into a bank account of their choosing. The employee may also choose to pick their paychecks up at the offices. The Payroll Administrator maintains employee information. He is responsible for adding new employees, deleting employees and changing all employee information such as name, address and payment classification(hourly, salaried, commissioned), as well as running administrative reports.The Payroll application will run automatically every Friday and on the last working day of month. It will pay the appropriate employees on those days. The system will be told what date employees are to be paid, so it will generate payments for records from the last time the employee was paid to the specified date. The new system is being designed so that the payroll will always be generated automatically and there will be need for any manual intervention"

globalSubject = []
globalIndexSubject = -1
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
            s[0]=s[0].lstrip()
            if s[2]==2:
                evaluate = (s[0].capitalize() in subject_pronouns) or (s[0].capitalize() in relative_pronouns) or (s[0].split( )[0].capitalize() in adjective_possessive) or (s[0].split( )[0].capitalize() in possessive_pronouns)
                if evaluate:
                    s[2] = 0
                else:
                    s[2] = 1
                    
        last_computed_index = -1
        for i, s in enumerate(subjects):
            global globalSubject
            globalSubject.append(s[0])
            global globalIndexSubject
            globalIndexSubject+=1

            if s[2]==0:
                if (s[0].capitalize() in subject_pronouns) or (s[0].capitalize() in relative_pronouns):
                    s[0]=globalSubject[globalIndexSubject-1]
                    globalSubject[globalIndexSubject]=s[0]
                elif (s[0].split( )[0].capitalize() in adjective_possessive):
                    actual_computed_index = i
                    if last_computed_index+1 != actual_computed_index:
                        owner=globalSubject[globalIndexSubject-1]
                        globalSubject[globalIndexSubject]=owner
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
    

class MainClass:
    def __init__(self, data): 
        self.data = self.menu(data)
        self.t = Text(English(), WordNetLemmatizer(), self.data)
        self.s = self.call_senteces(self.t)
    def menu(self, data):
        return data[-1]        
    def call_senteces(self, t):
        s = []
        for sntc in t.tokenized_sentences:
            s.append(Sentence(sntc))
        return s
    def print_sentences(s):
        for result in s:
            print(result.subjects)
            print(result.verbs)
            print(result.complements)
            print("-------------------------------------")
    def format_sentence(s):
        for result in s:
            i = 0
            subjs = result.subjects[1]
            verbs = result.verbs
            comps = result.complements
            iterate_until = max(len(verbs), len(comps), len(subjs))
            while i < iterate_until:
                print("Actor = " + subjs[i][0])
                print("Action = " + verbs[i].orth_)
                print("Complement = " + Text.token_to_string(comps[i][0]))
                print("---")
                i+=1
    def generate_json(s):
        data=[]
        j = 0
        for result in s:
            i = 0
            subjs = result.subjects[1]
            verbs = result.verbs
            comps = result.complements
            iterate_until = max(len(verbs), len(comps), len(subjs))
            while i < iterate_until:
                data_temp={}
                data_temp["id"]=j+1
                data_temp["actor"]=subjs[i][0]
                data_temp["action"]=verbs[i].orth_
                data_temp["complement"]=Text.token_to_string(comps[i][0])
                data.append(data_temp)
                i+=1
                j+=1
        json_data = json.dumps(data)
        return json_data

result = MainClass(sys.argv)
# MainClass.print_sentences(result.s)
# MainClass.format_sentence(result.s)
print(MainClass.generate_json(result.s))