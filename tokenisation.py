import os
import nltk
from text_processing import create_lowercase_text, tokenize, vocabulary, get_number_of_documents
from utils import create_inverted_index, compute_linear_reg, plot_frequecy_distribution, \
                  input_query_vectorial_model, print_query_result
from import_export import read_object

collection_path = os.getcwd()+'\\Data\\CACM\\cacm.all'
file_path = os.getcwd()+'\\Data\\CACM\\computed'

''' Q1'''

vocab = read_object(file_path+'\\vocabulary.pickle')

'''Q2'''

print("Le vocabulaire de l'ensemble a %i éléments distincts." %(len(vocab)))

'''Q3'''

beta_reg = None
K_reg = None
beta_reg, K_reg = compute_linear_reg(create_lowercase_text(collection_path))
print("La loi de Heap : b = %f,  K = %f" %(beta_reg, K_reg))

'''Q4'''

print("Pour un million : %f " %(K_reg*((10**6)**beta_reg)))

'''Q5'''

#plot_frequecy_distribution(tokenized_text)

''' index '''
'''     Done pour CACM en un seul bloc (en mémoire). Il faut trouver une solution pour CS276.
'''

inverted_index = read_object(file_path+'\\inverted_index.pickle')
#print('inverted_index[\'complex\'] : ', inverted_index['complex'])
#print('inverted_index[\'effective\'] : ', inverted_index['effective'])

''' 2.2.1 Index booléen '''



''' 2.2.2 Méthode vectorielle '''

docs_coordinates = read_object(file_path+'\\docs_coordinates.pickle')
print(': = = = = = = = = = = = = = = = = = = = = = = = = = = :')
while True:
    print_query_result(input_query_vectorial_model(docs_coordinates, vocab, inverted_index, collection_path))