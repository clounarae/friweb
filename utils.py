from math import log, log10, exp
import numpy as np
import matplotlib.pyplot as plt
import operator
import os
import tracemalloc
import linecache
import time
from text_processing import create_lowercase_text, tokenize, vocabulary, select_text_from_doc_part, \
    get_number_of_documents


def create_inverted_index(path):
    '''
    Create the inverted index of the collection along the path
    '''
    tracemalloc.start()
    start_time = time.clock()
    file_obj = open(path, 'r')
    lines = file_obj.readlines()
    inverted_index = {}
    docID = None
    for (i, line) in enumerate(lines):
        if line[0] == '.':
            if line[1] == 'I':
                docID = int(line[3:])
            elif (line[1] in ["T", "W", "B", "A", "N", "X", "K"]) and (docID != None):
                for word in vocabulary(tokenize(select_text_from_doc_part(i, lines))):
                    try:
                        inverted_index[word].append(docID)
                    except:
                        inverted_index[word] = [docID]
    for word in inverted_index.keys():
        inverted_index[word] = sorted(list(set(inverted_index[word])))
    snapshot = tracemalloc.take_snapshot()
    print('inverted index took {} s to be created'.format(time.clock()-start_time))
    print("memory stats for inverted index")
    display_top(snapshot)
    return inverted_index


def split_documents(path):
    '''
    Create a dictionnary with doc IDs for keys and lists of tokens contained in the said document
    '''
    file_obj = open(path, 'r')
    lines = file_obj.readlines()
    documents_splitted = {}
    docID = None
    for (i, line) in enumerate(lines):
        if line[0] == '.':
            if line[1] == 'I':
                docID = int(line[3:])
            elif (line[1] in ["T", "W", "B", "A", "N", "X", "K"]) and (docID != None):
                try:
                    documents_splitted[docID] += tokenize(select_text_from_doc_part(i, lines))
                except:
                    documents_splitted[docID] = tokenize(select_text_from_doc_part(i, lines))
    return documents_splitted


def log_term_freq_in_doc(term, docID, doc_dict):
    '''
    Compute the logarithm of the term frequecy in a given document
    '''
    term_freq = 0
    try:
        term_freq = doc_dict[docID].count(term)
    except:
        term_freq = 0  # doc n'existe pas
    if term_freq > 0:
        return 1 + log10(term_freq)
    else:
        return 0


def inverted_document_freq(term, inverted_index, n_documents):
    '''
    Compute the inverse of the term frequency in the entire collection
    '''
    n_docs_with_term = 0
    try:
        n_docs_with_term = len(inverted_index[term])
    except:
        return 0      #terme n'existe pas dans la collection
    return log10(n_documents / n_docs_with_term)


def tf_idf_weight(docID, term, doc_dict, inverted_index, n_documents):
    '''
    Compute the tf-idf weight for a term and a document ID
    '''
    return inverted_document_freq(term, inverted_index, n_documents) * log_term_freq_in_doc(term, docID, doc_dict)


def normalized_freq_weight(term, docID, doc_dict, inverted_index, n_documents):
    '''
    Compute the normalized frequency weight
    '''
    max_term_freq = max([log_term_freq_in_doc(t, docID, doc_dict) for t in tokenize(doc_dict[docID])])
    return log_term_freq_in_doc(term, docID, doc_dict) / max_term_freq


def compute_cos_similarity(doc1, doc2, docs_coordinates):
    '''
    Compute the cosine of the angle between the two vectors representing two documents
    '''
    if np.linalg.norm(docs_coordinates[doc1]) == 0 or np.linalg.norm(docs_coordinates[doc2]) == 0:
        return 0
    else: 
        return (np.dot(docs_coordinates[doc1], docs_coordinates[doc2]) /
               (np.linalg.norm(docs_coordinates[doc1]) * np.linalg.norm(docs_coordinates[doc2])))


def compute_docs_coordinates(vocabulary, inverted_index, path, weight_function):
    '''
    Compute the components for all the documents along the axes (one axis for each term of the collection) using the weight function
    '''
    start_time = time.clock()
    docs_coordinates = {}
    doc_dict = split_documents(path)
    n_documents = get_number_of_documents(path)
    for docID in doc_dict.keys():
        docs_coordinates[docID] = np.asarray([weight_function(docID, term, doc_dict, inverted_index, n_documents) for term in vocabulary])
    print('creating docs coordinates for vectorial model took {} s'.format(time.clock()-start_time))
    return docs_coordinates


def compute_linear_reg(lowercase_string_of_interesting_data):
    '''
    Compute the coefs for the linear regression
    '''
    half_doc_of_interest = lowercase_string_of_interesting_data[:len(lowercase_string_of_interesting_data) // 2]
    linear_reg = []
    T1 = len(tokenize(lowercase_string_of_interesting_data))
    M1 = len(vocabulary(tokenize(lowercase_string_of_interesting_data)))
    linear_reg.append([log(T1), log(M1)])
    T2 = len(tokenize(half_doc_of_interest))
    M2 = len(vocabulary(tokenize(half_doc_of_interest)))
    linear_reg.append([log(T2), log(M2)])

    beta = (linear_reg[1][1] - linear_reg[0][1]) / (linear_reg[1][0] - linear_reg[0][0])
    K = exp(1 / 2 * (linear_reg[1][1] + linear_reg[0][1] - beta * (linear_reg[1][0] + linear_reg[0][0])))
    return beta, K


def plot_frequecy_distribution(tokenized_text):
    '''
    Plot the frequecy distribution and frequency distribution log
    '''
    vocab = vocabulary(tokenized_text)
    word_freq = sorted([tokenized_text.count(w) for w in vocab], reverse=True)  # frequency
    x = [i + 1 for i in range(len(word_freq))]  # rank
    print("Drawing graph")
    plt.plot(x, word_freq, color='r')
    plt.xlabel("rank")
    plt.ylabel("frequency")
    plt.title("Frequency depending on rank")
    plt.show()
    print("Drawing log graph")
    plt.plot(np.log(x), np.log(word_freq), color='b')
    plt.xlabel("log(rank)")
    plt.ylabel("log(frequency)")
    plt.title("log(Frequency) depending on log(rank)")
    plt.show()
    print("process finished successfully !")

def intersection(lst1, lst2):
    '''
    returns the intersection of two lists
    '''
    lst3 = [value for value in lst1 if value in lst2]
    return lst3

def display_top(snapshot, key_type='lineno'):
    '''
    display total of memory resources used by a program
    :param snapshot: tracemalloc at the time t
    :param key_type:
    :return:
    '''
    snapshot = snapshot.filter_traces((
        tracemalloc.Filter(False, "<frozen importlib._bootstrap>"),
        tracemalloc.Filter(False, "<unknown>"),
    ))
    top_stats = snapshot.statistics(key_type)
    total = sum(stat.size for stat in top_stats)
    print("Total allocated size: %.1f KiB" % (total / 1024))