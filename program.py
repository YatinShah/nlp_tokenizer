import argparse

import re 
import pandas as pd


class TextProcessor:
    def __init__(self, file_path):
        self.file_path = file_path
        self.lines = self.load_data()
        self.is_narrated = False
        self.do_narrated = True
        self.words = []

    def load_data(self):
        lines = []
        with open(self.file_path, 'r') as file:
            for line in file:
                lines.append(line)
        return lines

    def check_opening_quotes(self, proto_word):
        if not self.do_narrated:
            return self.is_narrated
        if type(proto_word) != list:
            proto_word = [proto_word]
        for word in proto_word:
            if '“' in word:
                self.is_narrated = True
        return self.is_narrated

    def check_closing_quotes(self, proto_word):
        if not self.do_narrated:
            return self.is_narrated
        if type(proto_word) != list:
            proto_word = [proto_word]
        for word in proto_word:
            if '”' in word and self.is_narrated:
                self.is_narrated = False
        return self.is_narrated

    def split_punctuations_braces(self, proto_word):
        new_data = []
        if type(proto_word) != list:
            proto_word = [proto_word]
        for word in proto_word:
            if self.is_narrated:
                new_data.append(word)
            else:
                new_data.extend(re.split(r"([\-\?!_\:,;\(\[\{<>\}\]\)\"“”‘’'\.\n])", word))
        return new_data

    def replace_apostrophes(self, proto_word):
        new_data = []
        if type(proto_word) != list:
            proto_word = [proto_word]
        for word in proto_word:
            if self.is_narrated:
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
            if self.is_narrated:
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
            if self.is_narrated:
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
            if self.is_narrated:
                new_data.append(word)
            else:
                new_data.append(re.sub(r"^\s+|\s+$", "", word))
        return new_data

    def delete_empty_words(self, proto_word):
        new_data = []
        if type(proto_word) != list:
            proto_word = [proto_word]
        for word in proto_word:
            if self.is_narrated:
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
                formatted_text = f"{word:<20} {count:>6}"
                file.write(formatted_text + "\n")
                print(formatted_text)
        return ordered_histogram

    def process_lines(self):
        line_nr = 0
        for line in self.lines:
            words_in_line = line.split()
            temp_words = []
            for word in words_in_line:
                self.check_opening_quotes(word)
                temp_words = self.replace_abbr(word)
                temp_words = self.replace_apostrophes(temp_words)
                temp_words = self.split_punctuations_braces(temp_words)
                temp_words = self.reverse_characters(temp_words)
                temp_words = self.remove_spaces_tabs_newlines(temp_words)
                temp_words = self.delete_empty_words(temp_words)
                self.check_closing_quotes(word)
                self.words.extend(temp_words)
            # with open('./temp_words.txt', 'w') as file:
            #     for word in temp_words:
            #         file.write(f"{word}\n")
            line_nr += 1


    def save_results(self):
        total_words = len(self.words)
        print(f"Total number of words: {total_words}")
        with open('./tokenized_words.txt', 'w') as file:
            for word in self.words:
                formatted_text = f"{word}"
                file.write(formatted_text + "\n")
                print(formatted_text)
        ordered_histogram = self.create_ordered_histogram(self.words)
        with open('./top_10_words.txt', 'w') as file:
            count = 0
            for word, freq in ordered_histogram.items():
                if not re.match(r"^[\-\?!\:,;\"“”‘’'\.]$", word):  # Check if the word is not a punctuation mark
                    formatted_text = f"word: {word:<20}, count:{freq:>6}, freq:{freq/total_words:>10.5f}"
                    print(formatted_text)
                    file.write(formatted_text + "\n")
                    count += 1
                if count == 10:
                    break
        with open('./top_20_words.txt', 'w') as file:
            for word, count in list(ordered_histogram.items())[:20]:
                formatted_text = f"word:{word:<20}, count:{count:>6}, freq:{count*100/total_words:>10.5f}"
                print(formatted_text)
                file.write(formatted_text + "\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process a text file to generate tokens.')
    parser.add_argument('file_path', type=str, help='Path to the text file to processed')
    parser.add_argument('--no_narrate', action='store_true', help='Disable special handling of narration')
    args = parser.parse_args()

    processor = TextProcessor(args.file_path)
    if args.no_narrate:
        processor.do_narrated = False
    processor.process_lines()
    processor.save_results()
