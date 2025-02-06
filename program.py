import re #import the regular expression module
import pandas as pd #import pandas module

# Load the data#

#write code to read a text file line by line and store in lines variable 
class TextProcessor:
    def __init__(self, file_path):
        self.file_path = file_path
        self.lines = self.load_data()
        self.in_direct_quotes = False
        self.words = []

    def load_data(self):
        lines = []
        with open(self.file_path, 'r') as file:
            for line in file:
                lines.append(line)
        return lines

    def check_direct_quotes(self, proto_word):
        if type(proto_word) != list:
            proto_word = [proto_word]
        for word in proto_word:
            if '“' in word:
                self.in_direct_quotes = True
            elif '”' in word:
                self.in_direct_quotes = False
        return self.in_direct_quotes

    def split_punctuations_braces(self, proto_word):
        new_data = []
        if type(proto_word) != list:
            proto_word = [proto_word]
        for word in proto_word:
            if self.in_direct_quotes:
                new_data.append(word)
            else:
                new_data.extend(re.split(r"([\-\?!_\:,;\(\[\{<>\}\]\)\"“”‘’'\.\n])", word))
        return new_data

    def replace_apostrophes(self, proto_word):
        new_data = []
        if type(proto_word) != list:
            proto_word = [proto_word]
        for word in proto_word:
            if self.in_direct_quotes:
                new_data.append(word)
            else:
                if "'" in word:
                    new_data.append(re.sub(r"\'", "\x05", word))
                elif "’" in word:
                    new_data.append(re.sub(r"’", "\x06", word))
                else:
                    new_data.append(word)
        return new_data

    def replace_abbr(self, proto_word):
        new_data = []
        if type(proto_word) != list:
            proto_word = [proto_word]
        for word in proto_word:
            if self.in_direct_quotes:
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

    def reverse_characters(self, proto_word):
        new_data = []
        if type(proto_word) != list:
            proto_word = [proto_word]
        for word in proto_word:
            if self.in_direct_quotes:
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

    def remove_spaces_tabs_newlines(self, proto_word):
        new_data = []
        if type(proto_word) != list:
            proto_word = [proto_word]
        for word in proto_word:
            if self.in_direct_quotes:
                new_data.append(word)
            else:
                new_data.append(re.sub(r"^\s+|\s+$", "", word))
        return new_data

    def delete_empty_words(self, proto_word):
        new_data = []
        if type(proto_word) != list:
            proto_word = [proto_word]
        for word in proto_word:
            if self.in_direct_quotes:
                new_data.append(word)
            else:
                if word != '':
                    new_data.append(word)
        return new_data

    def create_ordered_histogram(self, words):
        histogram = {}
        for word in words:
            word_lower = word.lower()
            if word_lower in histogram:
                histogram[word_lower] += 1
            else:
                histogram[word_lower] = 1
        ordered_histogram = dict(sorted(histogram.items(), key=lambda item: item[1], reverse=True))
        with open('data/ordered_histogram.txt', 'w') as file:
            for word, count in ordered_histogram.items():
                file.write(f"{word}: {count}\n")
        return ordered_histogram

    def process_lines(self):
        line_nr = 0
        for line in self.lines:
            words_in_line = line.split()
            for word in words_in_line:
                self.check_direct_quotes(word)
                temp_words = self.replace_abbr(word)
                temp_words = self.replace_apostrophes(temp_words)
                temp_words = self.split_punctuations_braces(temp_words)
                temp_words = self.reverse_characters(temp_words)
                temp_words = self.remove_spaces_tabs_newlines(temp_words)
                temp_words = self.delete_empty_words(temp_words)
                self.words.extend(temp_words)
            with open('data/temp_words.txt', 'w') as file:
                for word in temp_words:
                    file.write(f"{word}\n")
            line_nr += 1


    def save_results(self):
        total_words = len(self.words)
        print(f"Total number of words: {total_words}")
        with open('data/tokenized_words.txt', 'w') as file:
            for word in self.words:
                file.write(f"{word}\n")
        ordered_histogram = self.create_ordered_histogram(self.words)
        with open('data/top_10_words.txt', 'w') as file:
            count = 0
            for word, freq in ordered_histogram.items():
                if not re.match(r"^[\-\?!\:,;\"“”‘’'\.]$", word):  # Check if the word is not a punctuation mark
                    file.write(f"{word}: {freq} & freq {freq/total_words:.1f}\n")
                    count += 1
                if count == 10:
                    break
        with open('data/top_20_words.txt', 'w') as file:
            for word, count in list(ordered_histogram.items())[:20]:
                file.write(f"{word}: {count} & freq {count/total_words:.5f}\n")


if __name__ == "__main__":
    processor = TextProcessor('data/ti.txt')
    processor.process_lines()
    processor.save_results()
