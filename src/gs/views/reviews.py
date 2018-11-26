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
    reviews = [r.__dict__ for r in get_reviews(pids=[pid])]
    for r in reviews:
        r.pop('_sa_instance_state')
    return Response(json.dumps(reviews, skipkeys=True), mimetype='application/json')


@REVIEWS_ROUTE.route('/recommendations/<uid>', methods=['GET'])
def recs_for_user(uid):
    recs = [r.__dict__ for r in get_recommendations(uids=[uid])]
    for r in recs:
        r.pop('_sa_instance_state')
    return Response(json.dumps(recs, skipkeys=True), mimetype='application/json')


@REVIEWS_ROUTE.route('/vis/<pid>', methods=['GET'])
def get_vis(pid):
    reviews = get_reviews(pids=[pid])
    points = document_points(reviews)
    cluster = KMeans(DataFrame(points), 2)
    reviews = [r.__dict__ for r in reviews]
    for idx, r in enumerate(reviews):
        r.pop('_sa_instance_state')
        r['cluster'] = cluster._clabels[idx]
    return Response(json.dumps(reviews, skipkeys=True), mimetype='application/json')


def register_reviews(app):
    app.register_blueprint(REVIEWS_ROUTE, url_prefix="/reviews")
