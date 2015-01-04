
import re
import string
from collections import defaultdict


import nltk
from nltk.corpus import stopwords
from nltk.tokenize import TreebankWordTokenizer
from nltk.stem import SnowballStemmer
import nltk.data

nltk.data.path.append('.')

def calculate_keywords_similarity(keyword1, keyword2):
    """
        Naive keywords Similarity
    """
    result = 0
    for key in keyword1:
        if key  in keyword2:
            result = result + 1
    return result/len(keyword1)



# source https://github.com/wnksd2/plagiarism/blob/master/plagiarism.py

def get_words(text):
    punct = re.compile('[%s0-9\–]' % re.escape(string.punctuation))
    words = TreebankWordTokenizer().tokenize(str(text));
    words[:] = [word for word in words if len(word)>2]
    words[:] = [word for word in words if punct.sub("", word) == word]
    words[:] = [word.lower() for word in words]
    stops = stopwords.words('polish')
    for stop in stops:
        words[:] = [word for word in words if word not in stop]

    # stemmer = SnowballStemmer('polish')
    # words[:] = [stemmer.stem(word) for word in words]
    return words

def get_keywords(text, num = 10):

    words = get_words(text)

    wordsCount = defaultdict(int)
    for word in words:
        wordsCount[word] += 1

    words = sorted(wordsCount.items(), key=lambda x: x[1], reverse=True)[:num]
    words[:] = [word for (word, cnt) in words]

    return words
