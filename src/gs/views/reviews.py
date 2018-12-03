#!/usr/bin/env python3
import json

from flask import Response
from flask import Blueprint

from pandas import DataFrame

from gs.dataserver.model.review import get_reviews
from gs.dataserver.model.review import get_recommendations

from gs.dataserver.algorithms import KMeans
from gs.dataserver.algorithms import document_points

REVIEWS_ROUTE = Blueprint("reviews", __name__)

@REVIEWS_ROUTE.route('/<pid>', methods=['GET'])
def reviews_for_product(pid):
    """
    Get reviews for a product
    """
    reviews = [r.__dict__ for r in get_reviews(pids=[pid])]
    for r in reviews:
        r.pop('_sa_instance_state')
    return Response(json.dumps(reviews, skipkeys=True), mimetype='application/json')


@REVIEWS_ROUTE.route('/recommendations/<uid>', methods=['GET'])
def recs_for_user(uid):
    """
    Get the recommendations for a user
    """
    recs = [r.__dict__ for r in get_recommendations(uids=[uid])]
    for r in recs:
        r.pop('_sa_instance_state')
    return Response(json.dumps(recs, skipkeys=True), mimetype='application/json')


def _get_cluster_string_labels(clustering):
    """
    Get the labels for online clustering
    """
    diffs = [c[0] - c[1] for c in clustering._centers]
    max_dif = max(diffs)
    positive_label = diffs.index(max_dif)
    return ["bad", "good"] if positive_label == 0 else ["good", "bad"]


@REVIEWS_ROUTE.route('/vis/<pid>', methods=['GET'])
def get_vis(pid):
    """
    Return the clusters for the visualization
    """
    # Get the reviews
    reviews = get_reviews(pids=[pid])
    if len(reviews) <= 0:
        return Response(json.dumps([], skipkeys=True), mimetype='application/json')
    # Turn the documents to points
    points = document_points(reviews)
    # Cluster the points
    cluster = KMeans(DataFrame(points), 2)
    reviews = [r.__dict__ for r in reviews]
    # Label and return the objects.
    str_labels = _get_cluster_string_labels(cluster)
    for idx, r in enumerate(reviews):
        r.pop('_sa_instance_state')
        label = cluster._clabels[idx]
        if label > len(str_labels) - 1:
            label = len(str_labels) - 1
        r['cluster'] = str_labels[label]
    return Response(json.dumps(reviews, skipkeys=True), mimetype='application/json')


def register_reviews(app):
    app.register_blueprint(REVIEWS_ROUTE, url_prefix="/reviews")
