import pickle
import os
from utils import compute_docs_coordinates,\
                  create_inverted_index,\
                  tf_idf_weight
from text_processing import vocabulary,\
                            create_lowercase_text,\
                            tokenize

def write_docs_coordinates(vocab, inverted_index, collection_path, weight_function, file_path):
    print('Exporting document vectorial representation for vectorial model...')
    docs_coordinates = compute_docs_coordinates(vocab, inverted_index, collection_path, weight_function)
    file = open(file_path, 'w+b')
    pickle.dump(docs_coordinates, file, protocol=pickle.HIGHEST_PROTOCOL)
    file.close()

def write_inverted_index(collection_path, file_path):
    print('Exporting inverted index...')
    inverted_index = create_inverted_index(collection_path)
    file = open(file_path, 'w+b')
    pickle.dump(inverted_index, file, protocol=pickle.HIGHEST_PROTOCOL)
    file.close()

def write_vocabulary(collection_path, file_path):
    print('Exporting vocabulary...')
    vocab = vocabulary(tokenize(create_lowercase_text(collection_path)))
    file = open(file_path, 'w+b')
    pickle.dump(vocab, file, protocol=pickle.HIGHEST_PROTOCOL)
    file.close()

def write_tokenized_text(collection_path, file_path):
    print('Exporting tokenized text...')
    tokenized_text = tokenize(create_lowercase_text(collection_path))
    file = open(file_path, 'w+b')
    pickle.dump(tokenized_text, file, protocol=pickle.HIGHEST_PROTOCOL)
    file.close()

def write_lowercase_text(collection_path, file_path):
    print('Exporting lowercase text...')
    lowercase_text = create_lowercase_text(collection_path)
    file = open(file_path, 'w+b')
    pickle.dump(lowercase_text, file, protocol=pickle.HIGHEST_PROTOCOL)
    file.close()

def read_object(file_path):
    file = open(file_path, 'rb')
    result = pickle.load(file)
    file.close()
    return result

if __name__ == '__main__':
    collection_path = os.getcwd()+'/Data/CACM/cacm.all'
    file_path = os.getcwd()+'/Data/CACM/computed'
    write_lowercase_text(collection_path, file_path+'/lowercase_text.pickle')
    write_tokenized_text(collection_path, file_path+'/tokenized_text.pickle')
    write_vocabulary(collection_path, file_path+'/vocabulary.pickle')
    write_inverted_index(collection_path, file_path+'/inverted_index.pickle')
    vocab = read_object(file_path + '/vocabulary.pickle')
    inverted_index = read_object(file_path + '/inverted_index.pickle')
    write_docs_coordinates(vocab, inverted_index, collection_path, tf_idf_weight, file_path+'/docs_coordinates_tf_idf.pickle')
    print('All writing done!')