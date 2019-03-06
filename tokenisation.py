import os
import nltk
import pdb
from text_processing import create_lowercase_text, tokenize, vocabulary
from utils import create_inverted_index, compute_linear_reg, plot_frequecy_distribution

# path = os.getcwd()+'\\Data\\CACM\\cacm.all'
path = "./Data/CACM/cacm.all"a
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

# word_freq = sorted([tokenized_text.count(w) for w in vocab], reverse=True)    #frequency
# x = [i+1 for i in range(len(word_freq))]  #rank
# print("Drawing graph")
# plt.plot(x,word_freq, color='r')
# plt.xlabel("rank")
# plt.ylabel("frequency")
# plt.title("Frequency depending on rank")
# plt.show()
# print("Drawing log graph")
# plt.plot(np.log(x),np.log(word_freq), color='b')
# plt.xlabel("log(rank)")
# plt.ylabel("log(frequency)")
# plt.title("log(Frequency) depending on log(rank)")
# plt.show()
# print("process finished successfully !")
#
#
# ''' index '''
# '''     Done pour CACM en un seul bloc (en mémoire). Il faut trouver une solution pour CS276.
# '''
# print('Index : ')
inverted_index = create_inverted_index(path)
# print('inverted_index[\'was\'] : ', inverted_index['was'])
# print('inverted_index[\'police\'] : ', inverted_index['police'])
#plot_frequecy_distribution(tokenized_text)

''' index '''
'''     Done pour CACM en un seul bloc (en mémoire). Il faut trouver une solution pour CS276.
'''
print('Index : ')
inverted_index = create_inverted_index(path)
print('inverted_index[\'complex\'] : ', inverted_index['complex'])
print('inverted_index[\'effective\'] : ', inverted_index['effective'])


''' 2.2.1 Index booléen '''


def intersection(lst1, lst2):
    lst3 = [value for value in lst1 if value in lst2]
    return lst3

def get_all_doc_Id(path):
    file_obj = open(path, 'r')
    lines = file_obj.readlines()
    listDocId=[]
    for (i,line) in enumerate(lines):
        if line[0] == '.':
            if line[1] == 'I':
                listDocId.append(int(line[3:]))
    return listDocId

def boolean_research(client_request, path_client = path):
    all_doc_id = get_all_doc_Id(path_client)
    request = tokenize(client_request)
    final_docs=[]
    documents = []
    #forbidden_doc = []
    #handling AND elements first
    while(next((operator for operator in request if operator == 'AND'), False)):
        index_treated = []
        forbidden_doc = list(set())
        i = request.index('AND')
        print('AND loop, i:', i, ' request : ', request)
        if(request[i-2]=='NOT'):
            index_treated =[i-2,i-1,i]
            forbidden_doc+=inverted_index[request[i-1]]
        elif(request[i-2]!='NOT'):
            if type(request[i-1])==str: # mot AND ..
                doc_treated= inverted_index[request[i - 1]]
            else: # [ liste doc ] AND ..
                doc_treated = request[i-1]
            documents += doc_treated
            index_treated=[i-1,i]
        if(request[i+1]=='NOT'):
            index_treated.extend((i+1,i+2))
            forbidden_doc+=inverted_index[request[i+2]]
        elif(request[i+1]!='NOT'):
            index_treated.append(i+1)
            if type(request[i+1])==str:
                doc_treated= inverted_index[request[i + 1]]
            else:
                doc_treated = request[i+1]
            if(documents != []):
                documents=intersection(documents,doc_treated)
            else:
                documents+=doc_treated
        if len(forbidden_doc) > 0: # Removing forbidden docs from results
            print('forbidden docs',forbidden_doc)
            print('documents before removal', documents)
            if len(documents) == 0:
                documents = all_doc_id.copy()

            for docId in documents:
                if docId in forbidden_doc:
                    print('docID', docId)
                    documents.remove(docId)
        request.insert(index_treated[0],documents)
        for j in range(len(index_treated)):
            request.pop(index_treated[1]) #
        print('documents after removal', documents, ' and request is now :', request)
        final_docs=documents
    #Handling OR elements
    while(next((operator for operator in request if operator == 'OR'), False)):
        index_treated = []
        forbidden_doc = []
        i = request.index('OR')
        if(request[i-2]=='NOT'):
            index_treated =[i-2,i-1,i]
            all_docs = all_doc_id.copy()
            for docId in inverted_index[request[i - 1]]:
                all_docs.remove(docId)
            documents+= all_docs
        else:
            if type(request[i-1])==str:
                doc_treated= inverted_index[request[i - 1]]
            else:
                doc_treated = request[i-1]
            documents += doc_treated
            index_treated=[i-1,i]
        if(request[i+1]=='NOT'):
            index_treated.extend((i+1,i+2))
            all_doc = all_doc_id.copy()
            for docId in inverted_index[request[i + 2]]:
                all_doc.remove(docId)
            documents+= all_doc
        else:
            index_treated.append(i+1)
            if type(request[i+1])==str:
                doc_treated= inverted_index[request[i + 1]]
            else:
                doc_treated = request[i+1]
            documents+=doc_treated
        request.insert(index_treated[0],documents)
        for j in range(len(index_treated)):
            request.pop(index_treated[1])
        final_docs=documents
    return list(set(final_docs))

'''example of request'''

print('mechanical : ',inverted_index['mechanical'])
print('pragmatics :', inverted_index['pragmatics'])
print('police : ', inverted_index['police'])
request_andNot = 'pragmatics AND NOT pragmatics AND police'
print(request_andNot)
print(boolean_research(request_andNot))