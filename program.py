import re #import the regular expression module
import pandas as pd #import pandas module

# Load the data#
#load text file into an array of words, split line at space characters and remove empty strings from the list
data = pd.read_csv('data/ti.txt', sep=" ", header=None)
data = data.values.flatten()
data = list(filter(None, data))

#create a static variable, called in_direct_qotes, and set it when encountering a '“' and unset it when encountering a '”'
in_direct_quotes = False

#write function that checks if beginning of a word is a quote, then set in_direct_quotes to True and if end of word containers a quote, then set in_direct_quotes to False
def check_direct_quotes(data):
    global in_direct_quotes
    for word in data:
        if '“' in word:
            in_direct_quotes = True
        elif '”' in word:
            in_direct_quotes = False
    return data


#write a function to observe each word and it contains a comma split into two words and add to the list
def split_punctuations_braces(data):
    new_data = []
    global in_direct_quotes
    for word in data:
        if in_direct_quotes:
            new_data.append(word)
        else:
            for char in [',', '-', '?', '!', '_', ':', ';', '(', '[', '{', '<', '>', '}', ']', ')', '"', '“', '”', '‘', '’', '\'', '.', '\n']:
                if char in word:
                    new_data.extend(word.split(char))
                    break
            else:
                new_data.append(word)
    return new_data

#create a function to change multie character words like "don't" to "do\x5t" and Mr. to Mr\x6
def replace_multi_character_words(data):
    new_data = []
    global in_direct_quotes
    for word in data:
        if in_direct_quotes:
            new_data.append(word)
        else:
            if len(word) > 1:
                if word[1] in ['.', ',']:
                    new_data.append(word[0] + chr(ord(word[1]) + 2) + word[2:])
                else:
                    new_data.append(word)
            else:
                new_data.append(word)
    return new_data

#create a regex that identifies words that contains an apostrophe within the word, then replace the apostrophe with a \x5 character
def replace_apostrophes(data):
    new_data = []
    global in_direct_quotes
    for word in data:
        if in_direct_quotes:
            new_data.append(word)
        else:
            if "'" in word:
                new_data.append(re.sub(r"\'", "\x5", word))
            elif "’" in word:
                new_data.append(re.sub(r"’", "\x6", word))
            else:
                new_data.append(word)
    return new_data

#create function with a dictionary of words like Mr. and Mrs. and replace them with Mr\x6 and Mrs\x6
def replace_abbr(data):
    new_data = []
    global in_direct_quotes
    for word in data:
        if in_direct_quotes:
            new_data.append(word)
        else:
            if word in ['Mr.', 'Mrs.', 'Dr.', 'Ms.', 'Jr.', 'St.', 'Co.', 'Inc.', 'Ltd.', 'Prof.', 'Sr.', 'Gen.', 'Rep.', 'Sen.', \
                        'Rev.', 'Col.', 'Sgt.', 'Gov.', 'Lt.', 'Maj.', 'Capt.', 'Cpl.', 'Pvt.', 'Spc.', 'Cmdr.', 'Adm.', 'Ens.', \
                        'Atty.', 'Hon.', 'Pres.', 'V.P.', 'Sec.', 'Treas.', 'Asst.', 'Mngr.', 'Mgr.', 'Dir.', 'Asso.', 'Assn.', \
                        'Prof.', 'Ph.D.', 'M.D.', 'D.D.', 'D.V.M.', 'O.D.', 'D.D.S.', 'D.M.D.', 'D.O.', 'D.C.', 'D.P.M.', 'D.C.M.', \
                        'D.C.L.', 'D.C.N.', 'D.C.P.', 'D.C.S.', 'D.C.T', 'N.A.', 'N.','E.','S.','W.',\
                        'N.N.E.', 'N.N.W.', 'N.W.', 'S.E.', 'S.S.E.', 'S.S.W.', 'S.W.', 'W.S.W.', 'N.N.W.', \
                        'N.E.', 'E.N.E.','E.S.E.', 'S.E.', 'S.S.E.', 'S.S.W.', 'S.W.', 'W.N.W.', 'P.P.S.','P.S.']:
                new_data.append(word[:-1] + "\x7")
            else:
                new_data.append(word)
    return new_data
