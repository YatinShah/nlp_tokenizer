import re #import the regular expression module
import pandas as pd #import pandas module

# Load the data#

#write code to read a text file line by line and store in lines variable 
lines = []
with open('data/ti.txt', 'r') as file:
    for line in file:
        lines.append(line)

#create a static variable, called in_direct_qotes, and set it when encountering a '“' and unset it when encountering a '”'
in_direct_quotes = False

#write function that checks if beginning of a word is a quote, then set in_direct_quotes to True and if end of word containers a quote, then set in_direct_quotes to False
def check_direct_quotes(proto_word):
    global in_direct_quotes
    if type(proto_word) != list:
        proto_word = [proto_word]
    for word in proto_word:
        if '“' in word:
            in_direct_quotes = True
        elif '”' in word:
            in_direct_quotes = False
    return in_direct_quotes


#write a function to observe each word and it contains a comma split into two words and add to the list
def split_punctuations_braces(proto_word):
    global in_direct_quotes
    new_data = []
    if type(proto_word) != list:
        proto_word = [proto_word]
    for word in proto_word:
        if in_direct_quotes:
            new_data.append(word)
        else:
            new_data.extend(re.split(r"[\-\?!_\:,;\(\[\{<>\}\]\)\"“”‘’'\.\n]", word))
            # for char in [',', '-', '?', '!', '_', ':', ';', '(', '[', '{', '<', '>', '}', ']', \
            #              ')', '"', '“', '”', '‘', '’', '\'', '.', '\n']:
            #     if char in word:
            #         new_data.extend(word.split(char))
            #         break
            # else:
            #     new_data.append(word)
    return new_data

# #create a function to change multie character words like "don't" to "do\x5t" and Mr. to Mr\x6
# def replace_multi_character_words(proto_word):
#     new_data = []
#     global in_direct_quotes
#    for word in proto_word:
#     if in_direct_quotes:
#         new_data.append(word)
#     else:
#         if len(word) > 1:
#             if word[1] in ['.', ',']:
#                 new_data.append(word[0] + chr(ord(word[1]) + 2) + word[2:])
#             else:
#                 new_data.append(word)
#         else:
#             new_data.append(word)
#     return new_data

#create a regex that identifies words that contains an apostrophe within the word, then replace the apostrophe with a \x5 character
def replace_apostrophes(proto_word):
    global in_direct_quotes
    new_data = []
    if type(proto_word) != list:
        proto_word = [proto_word]
    for word in proto_word:
        if in_direct_quotes:
            new_data.append(word)
        else:
            if "'" in word:
                new_data.append(re.sub(r"\'", "\x05", word))
            elif "’" in word:
                new_data.append(re.sub(r"’", "\x06", word))
            else:
                new_data.append(word)
    return new_data

#create function with a dictionary of words like Mr. and Mrs. and replace them with Mr\x6 and Mrs\x6
def replace_abbr(proto_word):
    global in_direct_quotes
    new_data = []
    if type(proto_word) != list:
        proto_word = [proto_word]
    for word in proto_word:
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
                new_data.append(re.sub(r"\.", "\x07", word))
            else:
                new_data.append(word)
    return new_data

#write a function revers all the \x5, \x6 and \x7 characters to their original characters
def reverse_characters(proto_word):
    global in_direct_quotes
    new_data = []
    if type(proto_word) != list:
        proto_word = [proto_word]
    for word in proto_word:
        if in_direct_quotes:
            new_data.append(word)
        else:
            if "\x05" in word:
                new_data.append(re.sub(r"\x05", "'", word))
            elif "\x06" in word:
                new_data.append(re.sub(r"\x06", "’", word))
            elif "\x07" in word:
                new_data.append(re.sub(r"\x07", ".", word))
            else:
                new_data.append(word)
    return new_data

#write a function to eat awau all spaces, tabs and newlines from the beginning and end of each word and return the word
def remove_spaces_tabs_newlines(proto_word):
    global in_direct_quotes
    new_data = []
    if type(proto_word) != list:
        proto_word = [proto_word]
    for word in proto_word:
        if in_direct_quotes:
            new_data.append(word)
        else:
            new_data.append(re.sub(r"^\s+|\s+$", "", word))
    return new_data

#write a function to delete all empty words from the list
def delete_empty_words(proto_word):        
    global in_direct_quotes
    new_data = []
    if type(proto_word) != list:
        proto_word = [proto_word]
    for word in proto_word:
        if in_direct_quotes:
            new_data.append(word)
        else:
            if word != '':
                new_data.append(word)
    return new_data

#write code to split each line into words and store in words variable
def print_line_nr(line_nr, line):
    line_nr += 1
    print(f"Line {line_nr}: {line}")


#create a variable words to store words from each line split by space
words = []
line_nr = 0

for line in lines:
#write code to print line with line numbers
    words_in_line = []
#    print_line_nr(line_nr, line)
    words_in_line =line.split()
    for word in words_in_line:
        in_quotes = check_direct_quotes(word)
        temp_words = replace_abbr(word)
        temp_words = replace_apostrophes(temp_words)
        temp_words = split_punctuations_braces(temp_words)
        temp_words = reverse_characters(temp_words)
        temp_words = remove_spaces_tabs_newlines(temp_words)
        temp_words = delete_empty_words(temp_words)
        words.extend(temp_words)
#write temp_words to a file called temp_words.txt
    with open('data/temp_words.txt', 'w') as file:
        for word in temp_words:
            file.write(f"{word}\n")
        # print(f"Words: {temp_words}")
    line_nr += 1
# print(f"Words: {words}")

# write the words to a file name tokenized_words.txt
with open('data/tokenized_words.txt', 'w') as file:
    for word in words:
        file.write(f"{word}\n")


#write to create histogram of words, then store in histogram variable
histogram = {}
for word in words:
    if word in histogram:
        histogram[word] += 1
    else:
        histogram[word] = 1
# print(f"Histogram: {histogram}")

#order the historgram in descending order and store in ordered_histogram variable
ordered_histogram = dict(sorted(histogram.items(), key=lambda item: item[1], reverse=True))
#write ordered_histogram to a file called ordered_histogram.txt 
with open('data/ordered_histogram.txt', 'w') as file:
    for word, count in ordered_histogram.items():
        file.write(f"{word}: {count}\n")


#print top 10 words from the ordered_histogram
# print(f"Top 10 words: {list(ordered_histogram.items())[:10]}")
#write top 10 words to a file called top_10_words.txt
with open('data/top_10_words.txt', 'w') as file:
    for word, count in list(ordered_histogram.items())[:10]:
        file.write(f"{word}: {count}\n")

#close all file handles at the end
