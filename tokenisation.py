import re
import os
from math import log, exp
import nltk
import numpy as np
import matplotlib.pyplot as plt

path = os.getcwd()+'\\Data/CACM/cacm.all'
reg='\. |\.\n|,| - |\n| |: |\(|\)|\/|\{|\}|=|\"|<|>|,...,|,...;|\+|\||\[|\]\;'

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
            elif line[1] == "T":
                j = i + 1
                title = ""
                while (lines[j][0] != "."):
                    title = title + lines[j]
                    j = j + 1
                string_of_interesting_data += title
            elif line[1] == "W":
                j = i + 1
                summary = ""
                while (lines[j][0] != "."):
                    summary = summary + lines[j]
                    j = j + 1
                string_of_interesting_data += summary
            elif line[1] == "K":
                j = i + 1
                key_word = ""
                while (lines[j][0] != "."):
                    key_word = key_word + lines[j]
                    j = j + 1
                string_of_interesting_data += key_word
    return string_of_interesting_data.lower()

def tokenize(text):
    splitting = re.split(reg, text)
    splitting[:] = [x for x in splitting if x != '']
    return splitting

def vocabulary(tokens):
    return sorted(set(tokens))


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

