import os
from math import log, exp
import nltk
from text_processing import create_lowercase_text,\
                            tokenize,\
                            vocabulary,\
                            get_number_of_documents
from utils import create_inverted_index,\
                  compute_linear_reg,\
                  plot_frequecy_distribution,\
                  intersection,\
                  tf_idf_weight,\
                  normalized_freq_weight
from search_methods import boolean_search,\
                           input_query_vectorial_model,\
                           print_query_result
from import_export import read_object

collection_path = os.getcwd()+'/Data/CACM/cacm.all'
file_path = os.getcwd()+'/Data/CACM/computed'

'''
To execute this file, please run the import_export file once so that all the pickle objects are computed
and saved in the "computed" folder.
'''

'''Q1'''
# Read the pickle dump that contains the vocabulary for CACM
vocab = read_object(file_path+'/vocabulary.pickle')

'''Q2'''

print("Le vocabulaire de l'ensemble a %i éléments distincts." %(len(vocab)))

'''Q3'''

# Read the pickle dump that contains the full text in lowercase for CACM
lowercase_text = read_object(file_path+'/lowercase_text.pickle')

# Compute the linear regression for CACM
beta_reg, K_reg = compute_linear_reg(lowercase_text)

print("La loi de Heap : b = %f,  K = %f" %(beta_reg, K_reg))

'''Q4'''

print("Pour un million : %f " % (K_reg * ((10 ** 6) ** beta_reg)))

'''Q5'''

# Read the pickle dump that contains the tokenized text for CACM
tokenized_text = read_object(file_path+'/tokenized_text.pickle')

plot = None
while plot not in ['y','n']:
    plot = input('Voulez-vous voir le diagramme de fréquence de la collection ? y/n\n')
    if plot == 'y':
        plot_frequecy_distribution(tokenized_text)

'''2.2 Index inversé'''

# Read the pickle dump that contains the inverted index for CACM
inverted_index = read_object(file_path+'/inverted_index.pickle')


docs_coordinates_tf_idf = read_object(file_path+'/docs_coordinates_tf_idf.pickle')
doc_dict = read_object(file_path+'/doc_dict.pickle')

choice = None
while choice != 'q':
    # Choose a search method
    print(': = = = = = = = = = = = = = = = = = = = = = = = = = = :')
    choice = input('Choisissez une méthode pour votre recherche :\nb - Booléen\nv - Vectoriel\nq - Quitter\n')

    ''' 2.2.1 Méthode booléenne '''

    if choice == 'b':
        print_query_result(boolean_search(input('Faites une recherche booléenne : '), inverted_index, collection_path, n_results=15), doc_dict)

    ''' 2.2.2 Méthode vectorielle '''

    if choice == 'v':
        print_query_result(input_query_vectorial_model(docs_coordinates_tf_idf, vocab, inverted_index, collection_path, tf_idf_weight, n_results=15))