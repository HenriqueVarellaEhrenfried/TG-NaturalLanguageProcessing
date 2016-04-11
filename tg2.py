from spacy.en import English
from nltk.stem.wordnet import WordNetLemmatizer
from pattern.en import singularize
import re

# sentence = 'The man in the room is our teacher.'
# sentence = 'LIB system shall keep track of all data required by copyright licensing agencies In the Kingdom and elsewhere'
sentence = 'Michael Wasalsky and Phil Sulivan could have frightened those children'
# sentence = 'The book was read by me'
# sentence = 'Because the boys went to the park, they did not go to the zoo'
problem = "A Company needs a new system called, Payroll System, to allow employees to record timecard information electronically and automatically generate paychecks based on the number of hours worked and total amount of sales(for commissioned employees). The new system will be state of art and will have a Windows-based desktop interface to allow employees to enter timecard information, enter purchase orders, change employee preferences (such as payment method) and create various reports. The system will run on individual employee desktops throughout the entire company.The system will retain information on all employees in the company. The system must pay each employee the correct amount, on time, by the method that they specify.Some employees work by the hour and are paid an hourly rate. They submit timecards that record the date and number of hours worked for a particular charge number. Some employees are paid a flat salary. Even though they are paid a flat salary, they submit timecards that record the date and hours worked. Some of the salaried employees also receive a commission based on their sales. They submit purchase orders that reflect the date and amount of the sale.One of the most requested features of the new system is employee reporting.Employees will be able to query the system for hours worked, totals of all hours billed to a project, total pay received year to date, etc.,Employees can choose their method of payment. They can have their paychecks mailed to the postal address of their choice, or they can request direct deposit and have their paycheck deposited into a bank account of their choosing. The employee may also choose to pick their paychecks up at the offices. The Payroll Administrator maintains employee information. He is responsible for adding new employees, deleting employees and changing all employee information such as name, address and payment classification(hourly, salaried, commissioned), as well as running administrative reports.The Payroll application will run automatically every Friday and on the last working day of month. It will pay the appropriate employees on those days. The system will be told what date employees are to be paid, so it will generate payments for records from the last time the employee was paid to the specified date. The new system is being designed so that the payroll will always be generated automatically and there will be need for any manual intervention"
sentences = problem.split(".")

nlp = English()
# doc = nlp(unicode(sentence))
verb = WordNetLemmatizer()


def get_subject(doc):
    subject_init_token = []
    for token in doc:
        if (re.match(r'nsubj', token.dep_)):
            subject_init_token.append(token)
    subjects = []
    for token in subject_init_token:
        partial_subtree_subject = []
        for t in token.subtree:
            partial_subtree_subject.append(t)
        subjects.append(partial_subtree_subject)
    return (subjects, subject_init_token)


def get_infinitive_verb(vb):
    verbs = []
    for v in vb:
        verbs.append(verb.lemmatize(v.text.encode('ascii', 'replace'), 'v'))
    return verbs


def get_verb(subj):
    verbs = []
    for s in subj[1]:
        verb_in_sentence = s.head
        verbs.append(verb_in_sentence)
    return verbs


# def get_object(verbs): 
# 	object_init_token =[]
# 	for token in verbs:
# 		for t in token.children:
# 			if (re.match(r'.*obj.*',t.dep_)):
# 				object_init_token.append(t)
# 	objects = []
# 	for token in object_init_token:
# 		partial_subtree_object = []
# 		for t in token.subtree:
# 			partial_subtree_object.append(t)
# 		objects.append(partial_subtree_object)
# 	return(objects, object_init_token)

def get_coplement(verbs):
    objects = []
    for token in verbs:
        for t in token.rights:
            partial_subtree_object = []
            for t1 in t.subtree:
                partial_subtree_object.append(t1)
            objects.append(partial_subtree_object)
    return (objects)


# doc = nlp(unicode(sentence))
# subj = get_subject(doc)
# verbs = get_verb(subj)
# infinitive_verbs = get_infinitive_verb(verbs)
# obj = get_object(verbs)

# subj = get_subject(doc)	
# verb = get_infinitive_verb(subj)
# obj = get_object(doc)
# print(subj)
# print(get_infinitive_verb(verbs))
# print(obj)
allSentence = []

for sentence in sentences:
    doc = nlp(unicode(sentence))
    subj = get_subject(doc)
    verbs = get_verb(subj)
    infinitive_verbs = get_infinitive_verb(verbs)
    obj = get_coplement(verbs)
    allSentence.append([{'Sujeito': subj, 'Verbo': verbs, 'Objeto': obj, 'Frase': sentence}])


# for i in allSentence:
#     print(i)
#     print(" ")

# The way to acces the dictionary
# print(allSentence[0][0]["Sujeito"])
