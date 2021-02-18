"""
 Indexer read each text file in documents directory and create Inverted Index and save it in a Json file
 Also it calculate idf for each terms and save it in a file that named terms_idf
"""

import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.stem import WordNetLemmatizer
import os
import math
import json


en_stops = set(stopwords.words('english'))
porter = PorterStemmer()

# calculate total number of documents
docs_list = os.listdir('documents')
total_documents = len(docs_list)
wordnet_lemmatizer = WordNetLemmatizer()

# Creating dictionary of terms frequencies
en_stops = set(stopwords.words('english'))
frequency_matrix = {}
for doc_name in docs_list:
    path = 'documents\\'
    path += doc_name
    file = open(path)
    data = file.read()
    data = data.lower()
    doc_tokens = nltk.word_tokenize(data)
    doc_tokens = [word for word in doc_tokens if word.isalnum()]
    freq_table = {}
    for doc_token in doc_tokens:
        if doc_token not in en_stops:
            word = porter.stem(doc_token)
            word = wordnet_lemmatizer.lemmatize(word)
            if word in freq_table:
                freq_table[word] += 1
            else:
                freq_table[word] = 1

    frequency_matrix[doc_name] = freq_table

# Create tf_matrix

tf_matrix = {}
for doc, f_table in frequency_matrix.items():
    tf_table = {}
    count_words_in_document = len(f_table)
    for word, count in f_table.items():
        tf_table[word] = count / count_words_in_document

    tf_matrix[doc] = tf_table

# Calculate idf for each word as a dictionary
idf_dic = {}
for doc, f_table in frequency_matrix.items():
    for word, count in f_table.items():
        if word in idf_dic:
            idf_dic[word] += 1
        else:
            idf_dic[word] = 1

for word, freq in idf_dic.items():
    idf_dic[word] = math.log(10, total_documents / freq)

# inverted index
inverted_index = {}
for doc, tf_table in tf_matrix.items():
    for word, tf in tf_table.items():
        # for tf we calculate natural logarithm
        tf_idf = (math.log(1 + tf)) * idf_dic[word]
        if word in inverted_index:
            posting_list = inverted_index[word]
            posting_list[doc] = tf_idf / count_words_in_document
        else:
            inverted_index[word] = {doc: tf_idf}

for word, posting_list in inverted_index.items():
    inverted_index[word] = sorted(posting_list.items(), key=lambda x: x[1], reverse=True)

with open('inverted-index.json', 'w') as json_file:
    json.dump(inverted_index, json_file)

with open('terms-idf.json', 'w') as handler:
    json.dump(idf_dic, handler)
