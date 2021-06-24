#TextRank implementation

from nltk.corpus import stopwords
from nltk.cluster.util import cosine_distance
from nltk import word_tokenize
import re
import numpy as np
import networkx as nx
import heapq
import requests
from bs4 import BeautifulSoup
from nltk.stem import WordNetLemmatizer, PorterStemmer
stemmer = PorterStemmer()
lemmatizer = WordNetLemmatizer() 

stopwords = stopwords.words("english")

def process_sentence(sentence):
    #remove numbers
    sentence = re.sub(r'\d+', '', sentence.lower().strip())

    #remove punctuation
    sentence = re.sub(r'[^a-zA-z]+', ' ', sentence)

    #tokenize the sentences
    sentence = word_tokenize(sentence)

    #removing stopwords
    sentence = [lemmatizer.lemmatize(stemmer.stem(word)) for word in sentence if word not in stopwords]

    return ' '.join(sentence)


def get_src_text(url):
    response = requests.get(url = url)
    soup = BeautifulSoup(response.content, 'html.parser')
    paras = soup.find_all('p')
    content = ""
    for para in paras:
        content += ' ' + para.text
    
    return content


def get_sentences(og_text):
    og_sents = og_text.split('.')
    return og_sents


def sent_simliarity(sentence1, sentence2):
    sentence1, sentence2 = process_sentence(sentence1), process_sentence(sentence2)

    all_words = list(set(sentence1 + sentence2))
    total_words = len(all_words)

    # initializing the vectors with zeros
    vector1 = [0]*total_words
    vector2 = [0]*total_words

    # now to fill the vectors, we will fill the freq acc to the index at which the
    # word is located in the all_words list

    for word in sentence1:
        vector1[all_words.index(word)] += 1

    for word in sentence2:
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


def summarise(url, n = 4):
    content = get_src_text(url)
    sentences = get_sentences(content)

    similarity_matrix = get_similarity_matrix(sentences)

    similarity_graph = nx.from_numpy_array(similarity_matrix)

    scores = nx.pagerank(similarity_graph)

    summ_sents = heapq.nlargest(n, scores, key=scores.get)
    summ_sents = [sentences[i].strip() for i in summ_sents]

    return '. '.join(summ_sents).strip()+'.'
