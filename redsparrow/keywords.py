
import re
import string
from collections import defaultdict


import nltk
from nltk.corpus import stopwords
from nltk.tokenize import TreebankWordTokenizer
from nltk.stem import SnowballStemmer
import nltk.data

nltk.data.path.append('.')

# http://www.catalysoft.com/articles/StrikeAMatch.html

def get_bigrams(string):

    s = string.lower()
    return {s[i:i+2] for i in range(len(s) - 1)}

def calculate_keywords_similarity(keywords1, keywords2):
    """
        Naive keywords Similarity
    """
    result = 0
    for key in keywords1:
        if key  in keywords2:
            result = result + 1
    return result/len(keywords1)
    # TODO: trzebo to nizej przerobic tak zeby dalo rade przyjmowac liste i potem odkomentowac
    # pairs1 = get_bigrams(keywords1)
    # pairs2 = get_bigrams(keywords2)
    #
    # intersection = pairs1 & pairs2
    #
    # return (2.0 * len(intersection)) / (len(pairs1) + len(pairs2))

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
