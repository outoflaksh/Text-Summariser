from nltk.corpus import stopwords
from nltk.cluster.util import cosine_distance
import re
import numpy as np
import networkx as nx
import heapq

stopwords = stopwords.words("english")


def get_sentences(filename):
    txt_file = open(filename, "r", encoding="utf8")
    og_text = txt_file.read()
    og_sents = []
    txt_file.close()

    og_text = re.sub(r'\[[0-9]*\]', ' ', og_text)
    og_text = re.sub(r'\s+', ' ', og_text)

    processed_txt = re.sub(r'[^a-zA-z]', ' ', og_text)
    processed_txt = re.sub(r'\s+', ' ', processed_txt)

    for sentence in og_text.split("\n"):
        if sentence != "\n":
            og_sents.extend(sentence.split(". "))
    
    return og_sents


def sent_simliarity(sentence1, sentence2):
    sentence1, sentence2 = sentence1.lower(), sentence2.lower()

    all_words = list(set(sentence1 + sentence2))
    total_words = len(all_words)

    # initializing the vectors with zeros
    vector1 = [0]*total_words
    vector2 = [0]*total_words

    # now to fill the vectors, we will fill the freq acc to the index at which the
    # word is located in the all_words list

    for word in sentence1:
        if word not in stopwords:
            vector1[all_words.index(word)] += 1

    for word in sentence2:
        if word not in stopwords:
            vector2[all_words.index(word)] += 1
    
    similarity = 1 - cosine_distance(vector1, vector2)

    return similarity


def get_similarity_matrix(sentences):
    total_sents = len(sentences)
    # initializing a sq matrix of zeroes to calculate, row_i's similarity to column_j
    similarity_matrix = np.zeros((total_sents, total_sents))
    
    for i in range(total_sents):
        for j in range(total_sents):
            if i != j:
                similarity_matrix[i][j] = sent_simliarity(sentences[i], sentences[j])
    
    return similarity_matrix


def summarise(filename, n = 4):
    sentences = get_sentences(filename)

    similarity_matrix = get_similarity_matrix(sentences)

    similarity_graph = nx.from_numpy_array(similarity_matrix)

    scores = nx.pagerank(similarity_graph)

    summ_sents = heapq.nlargest(n, scores, key=scores.get)
    summ_sents = [sentences[i] for i in summ_sents]

    return '. '.join(summ_sents)