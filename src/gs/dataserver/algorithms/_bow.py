#!/usr/bin/env python3
import string

from nltk.corpus import stopwords

# Define constant for stop words
FILLERS = set(stopwords.words('english'))
MAX_RATING = 5


def _filter_single(document):
    """
    Filter a single document from punctuation
    and stop words
    """
    translated = document.translate(str.maketrans("", "", string.punctuation)).lower()
    return [t for t in translated.split() if t not in FILLERS]


def _make_weight_vector(documents):
    """
    Create the discrete word vector
    from a series of documents
    """
    words = []
    for d in documents:
        words.extend(d)
    words = list(set(words))
    return {w:0 for w in words}


def word_weights(documents):
    """
    Get a dictionary of positive and negative
    weights for each word, including the vectorized
    document series.
    """
    doc_vectors = [_filter_single(d.summary) for d in documents]
    word_list = _make_weight_vector(doc_vectors)
    for idx, d in enumerate(documents):
        rating = d.overall
        for word in doc_vectors[idx]:
                word_list[word] += 1 if MAX_RATING - rating > 0 else -1
    return word_list, doc_vectors


def document_points(documents):
    """
    Convert each document into a 2D point
    with structure [positive, negative] 
    """
    weights, vectors = word_weights(documents)
    points = []
    for idx, d in enumerate(documents):
        weight = (len([_ for _ in vectors[idx] if weights[_] > 0]), len([_ for _ in vectors[idx] if weights[_] <= 0]))
        points.append(weight)
    return points
