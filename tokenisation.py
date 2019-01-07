file_obj = open('/data/Documents/ECP/3A/FRI/Data/CACM/cacm.all', 'r')
lines = file_obj.readlines()
string_of_interesting_data = ""
import re

I = None
for (i, line) in enumerate(lines):
    if line[0] == '.':
        if line[1] == "I":
            I = line[3:]
            string_of_interesting_data += I
        elif line[1] == "T":
            j = i + 1
            title = ""
            while (lines[j][0] != "."):
                title = title + lines[j]
                j = j + 1
            string_of_interesting_data += title
        elif line[1] == "W":
            j = i + 1
            summary = ""
            while (lines[j][0] != "."):
                summary = summary + lines[j]
                j = j + 1
            string_of_interesting_data += summary
        elif line[1] == "K":
            j = i + 1
            key_word = ""
            while (lines[j][0] != "."):
                key_word = key_word + lines[j]
                j = j + 1
            string_of_interesting_data += key_word
lowercase_string_of_interesting_data=string_of_interesting_data.lower()
reg='\. |\.\n|,| - |\n| |: |\(|\)|\/|\{|\}|=|\"|<|>|,...,|,...;|\+|\||\[|\]'
splitting=re.split(reg, lowercase_string_of_interesting_data)
token=open('token.txt','w+')
splitting[:]=[x for x in splitting if x!='']


''' Q1'''
#print(len(splitting))


vocab=sorted(set(splitting))

'''Q2'''

print(len(vocab))