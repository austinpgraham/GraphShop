#!/usr/bin/env python3
import string

from nltk.corpus import stopwords


FILLERS = set(stopwords.words('english'))


def _filter(documents):
    words = []
    for d in documents:
        translated = d.translate(str.maketrans("", "", string.punctuation)).lower()
        words.extend(translated.split())
    words = list(set(words))
    words = [w for w in words if w not in FILLERS]
    return words


def word_weights(documents):
    word_list = _filter(documents)
    
