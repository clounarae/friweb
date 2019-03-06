from math import log, log10, exp
import numpy as np
import matplotlib.pyplot as plt
<<<<<<< HEAD
import operator
from text_processing import create_lowercase_text, tokenize, vocabulary, select_text_from_doc_part, get_number_of_documents
=======
from text_processing import create_lowercase_text, tokenize, vocabulary, select_text_from_doc_part, \
    get_number_of_documents

>>>>>>> 963ec6c1b69cd0923eddf61d94d0e638944bcfaf

def create_inverted_index(path):
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
    return inverted_index


def split_documents(path):
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
    term_freq = 0
    try:
        term_freq = doc_dict[docID].count(term)
    except:
        term_freq = 0  # doc n'existe pas
    if term_freq > 0:
        return 1 + log10(term_freq)
    else:
        return 0

<<<<<<< HEAD
def inverted_document_freq(term, inverted_index, n_documents):
=======

def inverted_document_freq(term, inverted_index, path):
>>>>>>> 963ec6c1b69cd0923eddf61d94d0e638944bcfaf
    n_docs_with_term = 0
    try:
        n_docs_with_term = len(inverted_index[term])
    except:
<<<<<<< HEAD
        return 0      #terme n'existe pas dans la collection
    return log10(n_documents / n_docs_with_term)

def tf_idf_weight(docID, term, doc_dict, inverted_index, n_documents):
    return inverted_document_freq(term, inverted_index, n_documents) * log_term_freq_in_doc(term, docID, doc_dict)

def compute_docs_coordinates(vocabulary, inverted_index, path):
    docs_coordinates = {}
    doc_dict = split_documents(path)
    n_documents = get_number_of_documents(path)
    for docID in doc_dict.keys():
        docs_coordinates[docID] = np.asarray([tf_idf_weight(docID, term, doc_dict, inverted_index, n_documents) for term in vocabulary])
    return docs_coordinates

def compute_cos_distance(doc1, doc2, docs_coordinates):
    return (np.dot(docs_coordinates[doc1], docs_coordinates[doc2]) /
           (np.linalg.norm(docs_coordinates[doc1]) * np.linalg.norm(docs_coordinates[doc2])))

def input_query_vectorial_model(docs_coordinates, vocabulary, inverted_index, path, n_results=10):
    doc_dict = split_documents(path)
    n_documents = get_number_of_documents(path)
    doc_dict[0] = tokenize(input('Rechercher un document... : ').lower())  #On demande une requête et on fait comme si elle était le document n°0
    docs_coordinates[0] = np.asarray([tf_idf_weight(0, term, doc_dict, inverted_index, n_documents) for term in vocabulary])
    distance_dict = {docID : compute_cos_distance(0, docID, docs_coordinates) for docID in doc_dict.keys()}
    distance_from_query = sorted(distance_dict.items(), key=operator.itemgetter(1), reverse=True)
    return [result[0] for result in distance_from_query[1:n_results+1]]

def print_query_result(result):
    print('Les documents les plus pertinents pour votre recherche sont :')
    for (i,x) in enumerate(result):
        print(str(i+1) +'. '+ str(x))
=======
        return 0  # terme n'existe pas dans la collection
    return log10(get_number_of_documents(path) / n_docs_with_term)


def tf_idf_weight(docID, term, doc_dict, inverted_index, path):
    return inverted_document_freq(term, inverted_index, path) * log_term_freq_in_doc(term, docID, doc_dict)
>>>>>>> 963ec6c1b69cd0923eddf61d94d0e638944bcfaf


def compute_linear_reg(lowercase_string_of_interesting_data):
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
