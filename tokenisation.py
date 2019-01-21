import os
import nltk
from text_processing import create_lowercase_text, tokenize, vocabulary
from utils import create_inverted_index, compute_linear_reg, plot_frequecy_distribution

path = os.getcwd()+'\\Data\\CACM\\cacm.all'

''' Q1'''

lowercase_text = create_lowercase_text(path)
tokenized_text = tokenize(lowercase_text)

'''Q2'''

vocab=vocabulary(tokenized_text)
print("Le vocabulaire de l'ensemble a %i éléments distincts." %(len(vocab)))

'''Q3'''

beta_reg = None
K_reg = None
beta_reg, K_reg = compute_linear_reg(lowercase_text)
print("La loi de Heap : b = %f,  K = %f" %(beta_reg, K_reg))

'''Q4'''

print("Pour un million : %f " %(K_reg*((10**6)**beta_reg)))

'''Q5'''

#plot_frequecy_distribution(tokenized_text)

''' index '''
'''     Done pour CACM en un seul bloc (en mémoire). Il faut trouver une solution pour CS276.
'''
print('Index : ')
inverted_index = create_inverted_index(path)
print('inverted_index[\'complex\'] : ', inverted_index['complex'])
print('inverted_index[\'effective\'] : ', inverted_index['effective'])

''' 2.2.1 Index booléen '''

reg_op = 'AND|OR|\(|\)'
