#!/usr/bin/env python3
import string

from nltk.corpus import stopwords


FILLERS = set(stopwords.words('english'))
MAX_RATING = 5


def _filter_single(document):
    translated = document.translate(str.maketrans("", "", string.punctuation)).lower()
    return [t for t in translated.split() if t not in FILLERS]


def _make_weight_vector(documents):
    words = []
    for d in documents:
        words.extend(d)
    words = list(set(words))
    return {w:0 for w in words}


def word_weights(documents):
    doc_vectors = [_filter_single(d.summary) for d in documents]
    word_list = _make_weight_vector(doc_vectors)
    for idx, d in enumerate(documents):
        rating = d.overall
        for word in doc_vectors[idx]:
                word_list[word] += 1 if MAX_RATING - rating > 0 else -1
    return word_list, doc_vectors


def document_points(documents):
    weights, vectors = word_weights(documents)
    points = []
    for idx, d in enumerate(documents):
        weight = (len([_ for _ in vectors[idx] if weights[_] > 0]), len([_ for _ in vectors[idx] if weights[_] <= 0]))
        points.append(weight)
    return points
