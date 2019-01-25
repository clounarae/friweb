import re
import os
from math import log, exp
import nltk
import numpy as np
import matplotlib.pyplot as plt

path = './Data/CACM/cacm.all'
reg='\. |\.\n|,| - |\n| |: |\(|\)|\/|\{|\}|=|\"|<|>|,...,|,...;|\+|\||\[|\]|\;|\?|\!|\''

'''Methods'''

def create_lowercase_text(path):
    file_obj = open(path, 'r')
    lines = file_obj.readlines()
    I = None
    string_of_interesting_data = ""
    for (i, line) in enumerate(lines):
        if line[0] == '.':
            if line[1] == "I":
                I = line[3:]
                string_of_interesting_data += I
            elif line[1] in ["T","W","K"]:
                string_of_interesting_data += select_text_from_doc_part(i, lines)
    return string_of_interesting_data.lower()

def select_text_from_doc_part(i, lines):
    j = i + 1
    text_block = ""
    while (lines[j][0] != "."):
        text_block = text_block + lines[j]
        j = j + 1
    return text_block

def tokenize(text):
    splitting = re.split(reg, text)
    splitting[:] = [x for x in splitting if x != '']
    return splitting

def vocabulary(tokens):
    return sorted(set(tokens))

def create_inverted_index(path):
    file_obj = open(path, 'r')
    lines = file_obj.readlines()
    inverted_index = {}
    docID = None
    for (i,line) in enumerate(lines):
        if line[0] == '.':
            if line[1] == 'I':
                docID = int(line[3:])
            elif line[1] in ['T','W','K'] and docID != None:
                for word in vocabulary(tokenize(select_text_from_doc_part(i, lines).lower())):
                    try :
                        inverted_index[word].append(docID)
                    except :
                        inverted_index[word] = [docID]
    for word in inverted_index.keys():
        inverted_index[word] = sorted(list(set(inverted_index[word])))
    return inverted_index


def ComputeLinearReg(lowercase_string_of_interesting_data):
    half_doc_of_interest = lowercase_string_of_interesting_data[:len(lowercase_string_of_interesting_data)//2]
    linear_reg = []
    T1 = len(tokenize(lowercase_string_of_interesting_data))
    M1=len(vocabulary(tokenize(lowercase_string_of_interesting_data)))
    linear_reg.append([log(T1),log(M1)])
    T2 = len(tokenize(half_doc_of_interest))
    M2=len(vocabulary(tokenize(half_doc_of_interest)))
    linear_reg.append([log(T2),log(M2)])

    beta = (linear_reg[1][1] - linear_reg[0][1])/(linear_reg[1][0] - linear_reg[0][0])
    K = exp(1/2*(linear_reg[1][1] + linear_reg[0][1] - beta*(linear_reg[1][0]+linear_reg[0][0])))
    return beta, K

''' Q1'''

lowercase_string_of_interesting_data = create_lowercase_text(path)
tokenized_text = tokenize(lowercase_string_of_interesting_data)

vocab=vocabulary(tokenized_text)

'''Q2'''

print("Le vocabulaire de l'ensemble a %i éléments distincts." %(len(vocab)))

'''Q3'''

beta_reg = None
K_reg = None
beta_reg, K_reg = ComputeLinearReg(lowercase_string_of_interesting_data)
print("La loi de Heap : b = %f,  K = %f" %(beta_reg, K_reg))

'''Q4'''

print("Pour un million : %f " %(K_reg*((10**6)**beta_reg)))

'''Q5'''
#
# word_freq = sorted([tokenized_text.count(w) for w in vocab], reverse=True)    #frequency
# x = [i+1 for i in range(len(word_freq))]  #rank
# print("Drawing graph")
# plt.plot(x,word_freq, color='r')
# plt.xlabel("rank")
# plt.ylabel("frequency")
# plt.title("Frequency depending on rank")
# plt.show()
# print("Drawing log graph")
# plt.plot(np.log(x),np.log(word_freq), color='b')
# plt.xlabel("log(rank)")
# plt.ylabel("log(frequency)")
# plt.title("log(Frequency) depending on log(rank)")
# plt.show()
# print("process finished successfully !")
#
#
# ''' index '''
# '''     Done pour CACM en un seul bloc (en mémoire). Il faut trouver une solution pour CS276.
# '''
# print('Index : ')
inverted_index = create_inverted_index(path)
# print('inverted_index[\'was\'] : ', inverted_index['was'])
# print('inverted_index[\'police\'] : ', inverted_index['police'])

''' 2.2.1 Index booléen '''


def intersection(lst1, lst2):
    lst3 = [value for value in lst1 if value in lst2]
    return lst3

def boolean_research_V0(client_request):
    request = tokenize(client_request)
    documents = []
    forbidden_docs = []
    if(len(request) == 1):
        documents = inverted_index[request[0]]
    else :
        for i in range(len(request)):
            if(request[i] in ['AND', 'OR', 'NOT']):
                pass
            else:
                if(i==0):
                    documents += inverted_index[request[i]]
                else:
                    previous_term = request[i-1]
                    if previous_term == 'OR':
                        documents += inverted_index[request[i]]
                    elif previous_term == 'AND':
                        documents = intersection(documents, inverted_index[request[i]])
                    elif previous_term == 'NOT':
                        if request[i-2] == 'AND':
                            forbidden_docs += inverted_index[request[i]]
    if len(forbidden_docs)>0:
        for docId in documents:
            if docId in forbidden_docs:
                documents.remove(docId)
    return documents

def get_all_doc_Id(path):
    file_obj = open(path, 'r')
    lines = file_obj.readlines()
    listDocId=[]
    for (i,line) in enumerate(lines):
        if line[0] == '.':
            if line[1] == 'I':
                listDocId.append(int(line[3:]))
    return listDocId


import pdb
def boolean_research(client_request, path_client = path):
    all_doc_id = get_all_doc_Id(path_client)
    request = tokenize(client_request)
    #handling AND elements
    final_docs=[]
    while(next((operator for operator in request if operator == 'AND'), False)):
        index_treated = []
        forbidden_doc = []
        documents = []
        i = request.index('AND')
        if(request[i-2]=='NOT'):
            index_treated =[i-2,i-1,i]
            forbidden_doc+=inverted_index[request[i-1]]
        else:
            if type(request[i-1])==str: # mot AND ..
                doc_treated= inverted_index[request[i - 1]]
            else: # [ liste doc ] AND ..
                doc_treated = request[i-1]
            documents += doc_treated
            index_treated=[i-1,i]
        if(request[i+1]=='NOT'):
            index_treated.extend((i+1,i+2))
            forbidden_doc+=inverted_index[request[i+2]]
        else:
            index_treated.append(i+1)
            if type(request[i+1])==str:
                doc_treated= inverted_index[request[i + 1]]
            else:
                doc_treated = request[i+1]
            if(documents != []):
                documents=intersection(documents,doc_treated)
            else:
                documents+=doc_treated
        if len(forbidden_doc) > 0: # Removing forbidden docs from results
            if len(documents) == 0:
                documents = all_doc_id
            for docId in documents:
                if docId in forbidden_doc:
                    documents.remove(docId)
        request.insert(index_treated[0],documents)
        for j in range(len(index_treated)):
            request.pop(index_treated[1]) #
        final_docs=documents

    while(next((operator for operator in request if operator == 'OR'), False)):
        index_treated = []
        forbidden_doc = []
        documents = []
        i = request.index('OR')
        if(request[i-2]=='NOT'):
            index_treated =[i-2,i-1,i]
            documents += all_doc_id.remove(docId for docId in inverted_index[request[i-1]])
            #forbidden_doc+=inverted_index[request[i-1]]
        else:
            if type(request[i-1])==str:
                doc_treated= inverted_index[request[i - 1]]
            else:
                doc_treated = request[i-1]
            documents += doc_treated
            index_treated=[i-1,i]
        if(request[i+1]=='NOT'):
            index_treated.extend((i+1,i+2))
            #if forbidden_doc !=[]:
             #   forbidden_doc=intersection(forbidden_doc,inverted_index[request[i+2]])
            #else:
            documents += all_doc_id.remove(docId for docId in inverted_index[request[i + 2]])
            #forbidden_doc+=inverted_index[request[i+2]]
        else:
            index_treated.append(i+1)
            if type(request[i+1])==str:
                doc_treated= inverted_index[request[i + 1]]
            else:
                doc_treated = request[i+1]
            documents+=doc_treated
        '''
        if len(forbidden_doc) > 0:
            if len(documents) == 0:
                documents = all_doc_id
            for docId in documents:
                if docId in forbidden_doc:
                    documents.remove(docId)
                    '''
        request.insert(index_treated[0],documents)
        for j in range(len(index_treated)):
            request.pop(index_treated[1]) # ?? Je comprends pas trop
        final_docs=documents


    return final_docs


'''request1 = 'mechanical AND pragmatics'
request2 = 'translation AND mechanical'
request3 = 'mechanical AND translation OR NOT pragmatics'
print('mechanical : ',inverted_index['mechanical'])
print('pragmatics :', inverted_index['pragmatics'])
print('translation : ', inverted_index['translation'] )
print('list of documents', boolean_research_V0(request1))
print('list of documents', boolean_research_V0(request2))
print('list of docs', boolean_research_V0(request3))
print('query empty', boolean_research_V0('hjljk'))
'''
''' 
request1 = 'NOT pragmatics OR mechanical'
print(boolean_research(request1))
print('mechanical : ',inverted_index['mechanical'])
print('pragmatics :', inverted_index['pragmatics'])
print('translation : ', inverted_index['translation'] )
'''
request = 'mechanical AND NOT pragmatics'
print('mechanical : ',inverted_index['mechanical'])
print('pragmatics :', inverted_index['pragmatics'])
print(boolean_research(request))
