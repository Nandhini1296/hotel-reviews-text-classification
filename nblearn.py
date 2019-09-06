import os
import math
import sys
import string
from itertools import islice

def populate_stopwords(stopword_file):
    global stopwords_list
    with open(stopword_file, 'r') as stopword:
        stopwords = stopword.readlines(1)

    for word in stopwords:
        stopwords_list.append(word.strip("\n"))


def correct_words(word_list):
    global stopwords_list
    result = []
    for word in word_list:
        word_string = ""
        for i in word:
            if not i.isdigit():
                word_string += i
        if bool(word_string.strip()) and word_string.lower().strip() not in stopwords_list:
            result.append(word_string.lower().strip())
    return result


def read_model_file():

    with open("nbmodel.txt", 'r') as model_file:
        for n_lines in iter(lambda: tuple(islice(model_file, 4)), ()):
            dn = n_lines[0].split(" ")[-1]
            dp = n_lines[1].split(" ")[-1]
            tn = n_lines[2].split(" ")[-1]
            tp = n_lines[3].split(" ")[-1]
            key = n_lines[1].split(" ")[1]

            all_vocabulary[key] = [float(dn), float(dp), float(tn), float(tp)]


def get_counts_dictionary(file_path):
    count_dict = {}

    with open(file_path, 'r') as my_file:
        for line in my_file:
            # Remove punctuation
            line = line.replace(".", " ")
            # Remove empty lines and empty spaces
            words = line.split()

            word_list = []
            for word in words:
                word = word.strip('1234567890`~!@#$%^&*()_+{}:"<>?-=[];\',.\n/')
                word = word.lower()
                if word not in stopwords_list and word != "":
                    word_list.append(word)
            
            corrected_word_list = word_list
            
            for word in corrected_word_list:
                if count_dict.get(word):
                    value = count_dict.get(word) + 1
                    count_dict[word] = value
                else:
                    count_dict[word] = 1

    return count_dict

def get_word_scores(word, count_dict, identifier):
    global all_vocabulary

    calculated_probability = 0

    if all_vocabulary.get(word):
        count = float(count_dict[word])
        if identifier == "DN":
            calculated_probability = all_vocabulary[word][0]
        elif identifier == "DP":
            calculated_probability = all_vocabulary[word][1]
        elif identifier == "TN":
            calculated_probability = all_vocabulary[word][2]
        elif identifier == "TP":
            calculated_probability = all_vocabulary[word][3]

        calculated_probability = math.log(calculated_probability, 10)
        return calculated_probability * count

    return calculated_probability

if __name__ == "__main__":
    all_vocabulary = {}
    read_model_file()

    input_file_path = sys.argv[1]

    stopwords_list = []

    #populate_stopwords('stopwords.txt')
    stopwords_list = ["ourselves", "hers", "between", "yourself", "but", "again", "there", "about",
                      "once", "during", "out", "very", "having", "with", "they", "own", "an", "be",
                      "some", "for", "do", "its", "yours", "such", "into", "of", "most", "itself",
                      "other", "off", "is", "s", "am", "or", "who", "as", "from", "him", "each",
                      "the", "themselves", "until", "below", "are", "we", "these", "your", "his",
                      "through", "don", "nor", "me", "were", "her", "more", "himself", "this", "down",
                      "should", "our", "their", "while", "above", "both", "up", "to", "ours", "had",
                      "she", "all", "no", "when", "at", "any", "before", "them", "same", "and", "been",
                      "have", "in", "will", "on", "does", "yourselves", "then", "that", "because", "what",
                      "over", "why", "so", "can", "did", "not", "now", "under", "he", "you", "herself",
                      "has", "just", "where", "too", "only", "myself", "which", "those", "i", "after",
                      "few", "whom", "t", "being", "if", "theirs", "my", "against", "a", "by", "doing",
                      "it", "how", "further", "was", "here", "than"]

    nb_output = open("nboutput.txt", 'w')

    for root, directories, files in os.walk(input_file_path):
        for file in files:
            if file.endswith(".txt") and file != 'README.txt':
                new_file_path = str(root)+'/'+file
                counts_dictionary = get_counts_dictionary(new_file_path)
                dp_score = math.log(all_vocabulary['CalcPrior'][0])
                dn_score = math.log(all_vocabulary['CalcPrior'][1])
                tn_score = math.log(all_vocabulary['CalcPrior'][2])
                tp_score = math.log(all_vocabulary['CalcPrior'][3])

                for key,value in counts_dictionary.items():
                    dn_score += get_word_scores(key, counts_dictionary, "DN")
                    dp_score += get_word_scores(key, counts_dictionary, "DP")
                    tn_score += get_word_scores(key, counts_dictionary, "TN")
                    tp_score += get_word_scores(key, counts_dictionary, "TP")

                scores_list = [dn_score, dp_score, tn_score, tp_score]

                max_score = max(scores_list)
                max_index = scores_list.index(max_score)

                if max_index == 0:
                    nb_output.write('deceptive negative '+str(new_file_path) + "\n")
                elif max_index == 1:
                    nb_output.write('deceptive positive '+str(new_file_path) + "\n")
                elif max_index == 2:
                    nb_output.write('truthful negative '+str(new_file_path) + "\n")
                elif max_index == 3:
                    nb_output.write('truthful positive '+str(new_file_path) + "\n")
    nb_output.close()



