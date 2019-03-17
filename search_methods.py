import numpy as np
import operator
from utils import split_documents,\
                  get_number_of_documents,\
                  tf_idf_weight,\
                  compute_cos_similarity,\
                  intersection
from text_processing import tokenize,\
                            get_all_doc_id
import time


def print_query_result(list_of_docs, doc_dict):
    '''
    Print the result of a querry in well shaped format
    :param: list_of_docs: list of document IDs 
    '''
    if len(list_of_docs)==0:
        print('No documents found')
    else:
        print('Les documents les plus pertinents pour votre recherche sont :')
        for (i,x) in enumerate(list_of_docs):
            words = ''
            for w in doc_dict[x][:7]:
                words+= ' '+ w
            print(str(i+1) +'. '+ str(x)+ ': ' + words +'...')

def input_query_vectorial_model(docs_coordinates, vocabulary, inverted_index, path, weight_function, n_results=10):
    '''
    Give the n_results closest document IDs to the user's querry based on the vectorial search model
    '''
    doc_dict = split_documents(path)
    n_documents = get_number_of_documents(path)
    request_id = 0
    user_input = input('Faites une recherche vectorielle : ')
    start_time = time.clock()
    doc_dict[request_id] = tokenize(user_input.lower())  #On demande une requête et on fait comme si elle était le document n°0
    docs_coordinates[request_id] = np.asarray([weight_function(request_id, term, doc_dict, inverted_index, n_documents) for term in vocabulary])
    similarity_dict = {docID : compute_cos_similarity(request_id, docID, docs_coordinates) for docID in doc_dict.keys()}
    similarity_to_query = sorted(similarity_dict.items(), key=operator.itemgetter(1), reverse=True)
    results = [result[0] for result in similarity_to_query[1:n_results+1] if result[1] > 0]
    elapsed_time = time.clock() - start_time
    print('vectorial search took {:.2f} s to run the query'.format(elapsed_time))
    return results


def boolean_search(client_request, inverted_index, collection_path, n_results=10):
    '''
    Give n_results document IDs corresponding to the user's querry based on the boolean search model
    '''
    time_start = time.clock()
    all_doc_id = get_all_doc_id(collection_path)
    request = tokenize(client_request)
    final_docs = []
    documents = []
    if(len(request)==1):
        final_docs=inverted_index[request[0]]
    # handling and elements first
    while (next((operator for operator in request if operator == 'and'), False)):
        index_treated = []
        forbidden_doc = list(set())
        i = request.index('and')
        if (request[i - 2] == 'not'):
            index_treated = [i - 2, i - 1, i]
            forbidden_doc.extend(element for element in inverted_index[request[i - 1]] if element not in forbidden_doc)
        elif (request[i - 2] != 'not'):
            if type(request[i - 1]) == str:  # mot and ..
                doc_treated = inverted_index[request[i - 1]]
            else:  # [ liste doc ] and ..
                doc_treated = request[i - 1]
            documents.extend(element for element in doc_treated if element not in documents)
            index_treated = [i - 1, i]
        if (request[i + 1] == 'not'):
            index_treated.extend((i + 1, i + 2))
            forbidden_doc.extend(element for element in inverted_index[request[i + 2]] if element not in forbidden_doc)
        elif (request[i + 1] != 'not'):
            index_treated.append(i + 1)
            if type(request[i + 1]) == str:
                doc_treated = inverted_index[request[i + 1]]
            else:
                doc_treated = request[i + 1]
            if (documents != []):
                documents = intersection(documents, doc_treated)
            else:
                documents.extend(element for element in doc_treated if element not in documents)
        if len(forbidden_doc) > 0:  # Removing forbidden docs from results
            for docId in documents.copy():
                if docId in forbidden_doc:
                    documents.remove(docId)
        request.insert(index_treated[0], documents)
        for j in range(len(index_treated)):
            request.pop(index_treated[1])  #
        final_docs = documents
    # Handling or elements
    while (next((operator for operator in request if operator == 'or'), False)):
        index_treated = []
        i = request.index('or')
        if (request[i - 2] == 'not'):
            index_treated = [i - 2, i - 1, i]
            all_docs = all_doc_id.copy()
            for docId in inverted_index[request[i - 1]]:
                all_docs.remove(docId)
            documents.extend(element for element in all_docs if element not in documents)
        else:
            if type(request[i - 1]) == str:
                doc_treated = inverted_index[request[i - 1]]
            else:
                doc_treated = request[i - 1]
            documents.extend(element for element in doc_treated if element not in documents)
            index_treated = [i - 1, i]
        if (request[i + 1] == 'not'):
            index_treated.extend((i + 1, i + 2))
            all_doc = all_doc_id.copy()
            for docId in inverted_index[request[i + 2]]:
                all_doc.remove(docId)
            documents.extend(element for element in all_doc if element not in documents)
        else:
            index_treated.append(i + 1)
            if type(request[i + 1]) == str:
                doc_treated = inverted_index[request[i + 1]]
            else:
                doc_treated = request[i + 1]
            documents.extend(element for element in doc_treated if element not in documents)
        request.insert(index_treated[0], documents)
        for j in range(len(index_treated)):
            request.pop(index_treated[1])
        final_docs = documents
        time_elapsed =  time.clock()-time_start
        print('boolean search took {:.2f} s to run the query'.format(time_elapsed))
    return final_docs[:n_results]
