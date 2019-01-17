import re
import os
from math import log, exp
import nltk
import numpy as np
import matplotlib.pyplot as plt

path = os.getcwd()+'\\Data\\CACM\\cacm.all'
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

word_freq = sorted([tokenized_text.count(w) for w in vocab], reverse=True)    #frequency
x = [i+1 for i in range(len(word_freq))]  #rank
print("Drawing graph")
plt.plot(x,word_freq, color='r')
plt.xlabel("rank")
plt.ylabel("frequency")
plt.title("Frequency depending on rank")
plt.show()
print("Drawing log graph")
plt.plot(np.log(x),np.log(word_freq), color='b')
plt.xlabel("log(rank)")
plt.ylabel("log(frequency)")
plt.title("log(Frequency) depending on log(rank)")
plt.show()
print("process finished successfully !")


''' index '''
'''     Done pour CACM en un seul bloc (en mémoire). Il faut trouver une solution pour CS276.
'''
print('Index : ')
inverted_index = create_inverted_index(path)
print('inverted_index[\'was\'] : ', inverted_index['was'])
print('inverted_index[\'police\'] : ', inverted_index['police'])

''' 2.2.1 Index booléen '''

reg_op = 'AND|OR|\(|\)'
