# Text Summarisation using TextRank

<p align = "center">
<a href = "https://www.python.org">
<img src = "http://ForTheBadge.com/images/badges/made-with-python.svg">
</a>
</p>


Text summarisation is a challenging problem in Natural Language Processing (NLP) tasks. The task at hand involves taking a large text file and summarise it in a way that the core meaning and important points can be represented in a much smaller text. There have been different approaches devised to achieve the same.

### Approaches:

Two kinds of approaches are employed for summarising texts:
1. **Extractive summary**: This approach involves finding out the most important few sentences of the full text and compiling them to present as a summary.

2. **Abstractive summary**: This involves generating new texts to represent the meaning of the full text. The sentences produced in this approach are not necessarily present in the original text unlike extractive summarisation techniques.

### More about this repo:
This repository has two different files that are capable of summarising texts. Both use extractive approaches, in that, they both aim to find out the most important sentences from the full original text by some metrics. 

The more successful one was the second file "text_summ2.py" that implements the TextRank algorithm. It's an unsupervised machine learning technique in NLP based on the *PageRank* algorithm used by search engines like Google to rank webpages in search results.

Example of a summary created based on [this link](https://www.investopedia.com/terms/c/cloud-computing.asp):
> *Companies that provide cloud services enable users to store files and applications on remote servers and then access all the data via the Internet. Cloud computing services also make it possible for users to back up their music, files, and photos, ensuring those files are immediately available in the event of a hard drive crash. Cloud-based software offers companies from all sectors a number of benefits, including the ability to use software from any device either via a native app or a browser. For example, Adobe customers can access applications in its Creative Cloud through an Internet-based subscription.*

### TextRank:
The algorithm involves extracting all individual sentences from the full original text and then doing some standard preprocessing like making all letters lowercase, removing digits and punctuation, removing stopwords, and stemming+lemmatizing individual words.

The sentences are then converted into vectors, and cosine similarity between them is calculated which is then entered into a similarity matrix where each element represents sentence i's similarity with sentence j.

This matrix is translated into a graph where each node is a sentence connected by weighted edges as the similarity between them.

PageRank algorithm is then applied on this graph and the most important 4 sentences are combined and displayed.
