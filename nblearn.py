import os
import string
import sys


def populate_stopwords(stopword_file):
    global stopwords_list
    with open(stopword_file, 'r') as stopword:
        stopwords = stopword.readlines(1)

    for word in stopwords:
        stopwords_list.append(word.strip("\n"))


def correct_words(word_list):
    global stopwords_list

    result = []
    # Remove digits
    word_list = [word for word in word_list if not isinstance(word, int)]
    # Remove digits within words
    for word in word_list:
        word_string = ""
        for i in word:
            if not i.isdigit():
                word_string += i
        if bool(word_string.strip()) and word_string.lower().strip() not in stopwords_list:
            result.append(word_string.lower().strip())
    return result


def parse_file(file_path, identifier):
    global all_vocabulary, stopwords_list

    with open(file_path, 'r') as input_file:
        for line in input_file:
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

            corrected_word_list = correct_words(word_list)

            for word in corrected_word_list:
                if all_vocabulary.get(word, None):
                    class_list = all_vocabulary.get(word)
                else:
                    class_list = [0, 0, 0, 0]

                if identifier == 'DN':
                    class_list[0] = class_list[0] + 1
                elif identifier == "DP":
                    class_list[1] = class_list[1] + 1
                elif identifier == "TN":
                    class_list[2] = class_list[2] + 1
                elif identifier == "TP":
                    class_list[3] = class_list[3] + 1

                all_vocabulary[word] = class_list

        update_dictionaries(corrected_word_list, identifier)


def update_dictionaries(word_list, identifier):
    global dn_count, dp_count, tn_count, tp_count
    global dn_dictionary, dp_dictionary, tn_dictionary, tp_dictionary

    if identifier == "DN":
        for word in word_list:
            if dn_dictionary.get(word):
                dn_dictionary[word] = dn_dictionary[word] + 1
            else:
                dn_dictionary[word] = 1
        dn_count += len(word_list)
    elif identifier == "DP":
        for word in word_list:
            if dp_dictionary.get(word):
                dp_dictionary[word] = dp_dictionary[word] + 1
            else:
                dp_dictionary[word] = 1
        dp_count += len(word_list)
    elif identifier == "TN":
        for word in word_list:
            if tn_dictionary.get(word):
                tn_dictionary[word] = tn_dictionary[word] + 1
            else:
                tn_dictionary[word] = 1
        tn_count += len(word_list)
    elif identifier == "TP":
        for word in word_list:
            if tp_dictionary.get(word):
                tp_dictionary[word] = tp_dictionary[word] + 1
            else:
                tp_dictionary[word] = 1
        tp_count += len(word_list)


def get_all_vocabulary(file_path):
    global all_vocabulary
    global files_count_dictionary

    files_counting = []
    for root, directory, files in os.walk(file_path):
        for file in files:
            files_counting.append(root + "/" + file)
            if file == "README.txt":
                continue
            if not file.endswith(".txt"):
                continue

            read_file_path = root + "/" + file

            if "deceptive" in read_file_path and "negative" in read_file_path:
                parse_file(read_file_path, "DN")
                files_count_dictionary["DN"] += 1
            elif "deceptive" in read_file_path and "positive" in read_file_path:
                parse_file(read_file_path, "DP")
                files_count_dictionary["DP"] += 1
            elif "truthful" in read_file_path and "negative" in read_file_path:
                parse_file(read_file_path, "TN")
                files_count_dictionary["TN"] += 1
            elif "truthful" in read_file_path and "positive" in read_file_path:
                parse_file(read_file_path, "TP")
                files_count_dictionary["TP"] += 1


def generate_all_probabilities():
    global dn_count, dp_count, tn_count, tp_count
    global dn_dictionary, dp_dictionary, tn_dictionary, tp_dictionary

    for key, value_list in all_vocabulary.items():
        dn_score = value_list[0] + 1
        dp_score = value_list[1] + 1
        tn_score = value_list[2] + 1
        tp_score = value_list[3] + 1

        number_of_words = len(all_vocabulary)
        dn_posterior = (dn_score) / float(number_of_words + dn_count)
        dp_posterior = (dp_score) / float(number_of_words + dp_count)
        tn_posterior = (tn_score) / float(number_of_words + tn_count)
        tp_posterior = (tp_score) / float(number_of_words + tp_count)

        all_vocabulary[key] = [dn_posterior, dp_posterior, tn_posterior, tp_posterior]


def write_model_file(prior_list):
    with open("nbmodel.txt", "w") as model_file:
        model_file.write("P( " + "CalcPrior" + " ) = " + str(prior_list[0]) + "\n")
        model_file.write("P( " + "CalcPrior" + " ) = " + str(prior_list[1]) + "\n")
        model_file.write("P( " + "CalcPrior" + " ) = " + str(prior_list[2]) + "\n")
        model_file.write("P( " + "CalcPrior" + " ) = " + str(prior_list[3]) + "\n")
        for key, value in all_vocabulary.items():
            result = value
            model_file.write("P( " + key + " | Deceptive Negative) = " + str(result[0]) + "\n")
            model_file.write("P( " + key + " | Deceptive Positive) = " + str(result[1]) + "\n")
            model_file.write("P( " + key + " | Truthful Negative) = " + str(result[2]) + "\n")
            model_file.write("P( " + key + " | Truthful Positive) = " + str(result[3]) + "\n")


if __name__ == "__main__":
    input_file_path = sys.argv[1]

    all_vocabulary = {}
    stopwords_list = []
    all_my_words = []
    files_count_dictionary = {'DN': 0, 'DP': 0, 'TN': 0, 'TP': 0}

    dn_dictionary = {}
    dp_dictionary = {}
    tn_dictionary = {}
    tp_dictionary = {}

    dn_count = 0
    dp_count = 0
    tn_count = 0
    tp_count = 0

    # populate_stopwords("stopwords.txt")

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

    count = 0
    get_all_vocabulary(input_file_path)

    generate_all_probabilities()

    total_files = sum(files_count_dictionary.values())

    dn_prior = float(files_count_dictionary['DN']) / total_files
    dp_prior = float(files_count_dictionary['DP']) / total_files
    tn_prior = float(files_count_dictionary['TN']) / total_files
    tp_prior = float(files_count_dictionary['TP']) / total_files

    write_model_file([dn_prior, dp_prior, tn_prior, tp_prior])