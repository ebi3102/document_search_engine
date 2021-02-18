import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.stem import WordNetLemmatizer
import math

en_stops = set(stopwords.words('english'))
porter = PorterStemmer()
wordnet_lemmatizer = WordNetLemmatizer()


"""
return Query tf_idf and Query Score
parameters @query is a string variable
           @idf_dic is a dic object that store idf of each term
"""


def query_processor(query, idf_dic):
    query = query.lower()
    query_tokens = nltk.word_tokenize(query)
    query_tokens = [word for word in query_tokens if word.isalnum()]

    # Create query_tf_idf_table
    frq_table = {}
    for query_token in query_tokens:
        if query_token not in en_stops:
            word = porter.stem(query_token)
            word = wordnet_lemmatizer.lemmatize(word)
            if word in frq_table:
                frq_table[word] += 1
            else:
                frq_table[word] = 1

    total_query_terms = len(frq_table)
    query_tf_table = {}
    for word, count in frq_table.items():
        query_tf_table[word] = count / total_query_terms

    query_tf_idf_table = {}
    for word, tf in query_tf_table.items():
        if word in idf_dic:
            tf_idf = (math.log(1 + tf)) * idf_dic[word]
        else:
            tf_idf = 0
        query_tf_idf_table[word] = tf_idf

    query_score = 0
    for word, tf_idf in query_tf_idf_table.items():
        query_score += tf_idf

    query_score = query_score / total_query_terms
    return query_tf_idf_table, query_score


"""
it returns cosine similarity between query and each document as a sorted dictionary
params @query: is a string variable
       @inverted_index : is inverted index table as a dictionary
       idf_dic is a dic object that store idf of each term
"""
def search_engine(query, inverted_index, idf_dic):
    query_tf_idf, query_score = query_processor(query, idf_dic)
    total_query_terms = len(query_tf_idf)
    scores = {}
    for word, tf_idf in query_tf_idf.items():
        if tf_idf > 0:
            for doc, doc_tf_idf in inverted_index[word]:
                score = doc_tf_idf * tf_idf
                if doc in scores:
                    scores[doc] += score
                else:
                    scores[doc] = score

    cosine_table = {}
    for doc, score in scores.items():
        cosine = score / total_query_terms

        cosine_table[doc] = cosine

    cosine_table = sorted(cosine_table.items(), key=lambda x: x[1], reverse=True)

    return cosine_table
