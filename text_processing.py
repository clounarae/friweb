import re
from nltk.stem import PorterStemmer

reg='\. |\.\n|,| - |\n| |: |\(|\)|\/|\{|\}|=|\"|<|>|,...,|,...;|\+|\||\[|\]|\;|\?|\!|\'|\t'
ps = PorterStemmer() # Word stemmer, permits to transform a word into its root

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
            elif line[1] in ["T","W","B","A","N","X","K"]:
                string_of_interesting_data += select_text_from_doc_part(i, lines)
    return string_of_interesting_data

def select_text_from_doc_part(i, lines):
    j = i + 1
    text_block = ""
    while (j < len(lines)) and (lines[j][0] != ".") :
        text_block = text_block + lines[j]
        j = j + 1
    return text_block.lower()

def tokenize(text):
    '''
    Creates tokens in the format of stemmed words from the text given, after removing all punctuation
    :param text: text to tokenize
    :return: list of stemmed words
    '''
    splitting = re.split(reg, text)
    splitting[:] = [ps.stem(x) for x in splitting if x != '']
    return splitting

def vocabulary(tokens):
    '''
    vocabulary of the stemmed text => We show only the root words
    :param tokens: tokens of the text
    :return: set of all the root words
    '''
    return sorted(set(tokens))

def get_number_of_documents(path):
    file_obj = open(path, 'r')
    lines = file_obj.readlines()
    N = 0
    for line in lines:
        if line[:2] == '.I':
            N += 1
    return N

def get_all_doc_id(path):
    file_obj = open(path, 'r')
    lines = file_obj.readlines()
    listDocId = []
    for (i, line) in enumerate(lines):
        if line[0] == '.':
            if line[1] == 'I':
                listDocId.append(int(line[3:]))
    return listDocId