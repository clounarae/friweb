
file_obj = open('/data/Documents/ECP/3A/FRI/Data/CACM/cacm.all', 'r')
lines = file_obj.readlines()
dict = {}


I = None
for (i, line) in enumerate(lines):
    if line[0] == '.':
        if line[1] == "I":
            I = line[3:]
        elif line[1] == "T":
            j = i + 1
            title = ""
            while (lines[j][0] != "."):
                title = title + lines[j]
                j = j + 1
            dict.update({I:title})
        elif line[1] == "W":
            j = i + 1
            summary = ""
            while (lines[j][0] != "."):
                summary = summary + lines[j]
                j = j + 1
            dict[I] = dict[I] + summary
        elif line[1] == "K":
            j = i + 1
            key_word = ""
            while (lines[j][0] != "."):
                key_word = key_word + lines[j]
                j = j + 1
            dict[I] = dict[I] + key_word

print(dict)