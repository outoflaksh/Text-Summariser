#THIS WAS A FUCKING FAILURE

import nltk
import re
import heapq


txt_file = open("og_text.txt", "r", encoding="utf8")
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

stopwords = nltk.corpus.stopwords.words("english")
word_freq = {}

for word in processed_txt.split(' '):
    if word not in stopwords:
        if word in word_freq:
            word_freq[word] += 1
        else:
            word_freq[word] = 1

max_freq = max(word_freq.values())

for word in word_freq:
    word_freq[word] = word_freq[word]/max_freq

sentence_scores = {}

for sentence in og_sents:
    for word in sentence.split(' '):
        if len(sentence.split(' ')) < 25:
            if word in word_freq:
                if sentence in sentence_scores:
                    sentence_scores[sentence] += word_freq[word]
                else:
                    sentence_scores[sentence] = word_freq[word]

summ_sents = heapq.nlargest(6, sentence_scores, key=sentence_scores.get)
print('. '.join(summ_sents))