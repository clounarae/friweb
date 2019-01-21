from math import log, exp
import numpy as np
import matplotlib.pyplot as plt
from text_processing import create_lowercase_text, tokenize, vocabulary, select_text_from_doc_part

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

def compute_linear_reg(lowercase_string_of_interesting_data):
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

def plot_frequecy_distribution(tokenized_text):
    vocab = vocabulary(tokenized_text)
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
