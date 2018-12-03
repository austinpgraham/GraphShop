#!/usr/bin/env python3
import json
import random
import logging
import operator
import numpy as np

from sqlalchemy import Float
from sqlalchemy import Column
from sqlalchemy import String
from sqlalchemy import Integer
from sqlalchemy import ForeignKey

from gs.dataserver.model import Base
from gs.dataserver.model import _batch
from gs.dataserver.model import ModelDB

from gs.dataserver.model.product import Product
from gs.dataserver.model.product import PRODUCT_ID_LENGTH

from gs.dataserver.model.user import ReviewUser
from gs.dataserver.model.user import get_user_set
from gs.dataserver.model.user import USER_ID_LENGTH

from gs.dataserver.algorithms import GraphSVD


class Review(Base):
    """
    ORM object representing a Review Entity
    """

    __tablename__ = 'review'

    reviewerID = Column(String(USER_ID_LENGTH), ForeignKey("reviewuser.id"), primary_key=True)
    asin = Column(String(PRODUCT_ID_LENGTH), ForeignKey("product.asin"), primary_key=True)
    helpful = Column(String)
    text = Column(String)
    overall = Column(Float)
    summary = Column(String)
    time = Column(Integer)

    _JSON_ATTS = [
        "helpful"
    ]

    def __init__(self, *args, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
    
    def convert_json(self):
        """
        Convert the object to JSON
        """
        for att in self._JSON_ATTS:
            val = getattr(self, att, "[]") or "[]"
            setattr(self, att, json.loads(val))


class Recommendation(Base):
    """
    ORM object for a Recommendation entity
    """

    __tablename__ = "recommendation"

    userID = Column(String(USER_ID_LENGTH), ForeignKey("reviewuser.id"), primary_key=True)
    asin = Column(String(PRODUCT_ID_LENGTH), ForeignKey("product.asin"), primary_key=True)
    estimated_rating = Column(Float)

    def __init__(self, *args, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)


def reviewfunc(func, *args, **kwargs):
    """
    Check for the review table, create if
    not present
    """
    def wrapper(*args, **kwargs):
        with ModelDB() as db:
            if "review" not in db.inspector.get_table_names():
                Base.metadata.create_all(db._engine)
        return func(*args, **kwargs)
    return wrapper


def recommendationfunc(func, *args, **kwargs):
    """
    Check for recommendation table, create if not present
    """
    def wrapper(*args, **kwargs):
        with ModelDB() as db:
            if "recommendation" not in db.inspector.get_table_names(): # pragma: no cover
                Base.metadata.create_all(db._engine)
        return func(*args, **kwargs)
    return wrapper

@reviewfunc
def add_reviews(objs, batch_size=50):
    """
    Add a set of reviews
    """
    with ModelDB() as db:
        for b in _batch(objs, batch_size):
            db.session.bulk_save_objects(b)


@reviewfunc
def get_reviews(rids=None, pids=None):
    """
    Get all reveiws for the given pids and rids.
    """
    with ModelDB() as db:
        query = db.session.query(Review)
        if rids is not None:
            query = query.filter(Review.reviewerID.in_(rids))
        if pids is not None:
            query = query.filter(Review.asin.in_(pids))
        result = query.all()
    for r in result:
        r.convert_json()
    return result


@reviewfunc
def review_exists(rid, pid):
    """
    Check if a review exists.
    """
    with ModelDB() as db:
        query = db.session.query(Review).filter(Review.reviewerID == rid).filter(Review.asin == pid)
        ans = db.session.query(query.exists()).all().pop()[0]
    return ans


@recommendationfunc
def add_recommendations(objs, batch_size=50):
    """
    Add a set of recommendations.
    """
    with ModelDB() as db:
        for b in _batch(objs, batch_size):
            db.session.bulk_save_objects(b)


@recommendationfunc
def get_recommendations(uids=None):
    """
    Get recommendations for a given set of users.
    """
    with ModelDB() as db:
        query = db.session.query(Recommendation)
        if uids is not None:
            query = query.filter(Recommendation.userID.in_(uids))
        result = query.all()
    return result


REC_LIMIT = 10000


def compute_recommendations(components=3):
    """
    Compute the new recommendations.
    """
    logging.info('Collecting data...')
    # Get the users and corresponding and reviews
    users = get_user_set(REC_LIMIT)
    reviews = get_reviews(rids=users)
    pids = list(set([r.asin for r in reviews]))
    logging.info("A total of {} users and {} products are being used.".format(len(users), len(pids)))
    mat = []
    holdout = []
    logging.info('Building matrix...')
    for u in users:
        mat.append([0 for _ in range(len(pids))])
        # Get all relevant reviews
        user_reviews = [r for r in reviews if r.reviewerID == u]
        for r in user_reviews:
            # Flip a coin, if heads save for testing
            if len(holdout) < 200 and random.randint(1, 2) == 1:
                holdout.append((r.reviewerID, r.asin, r.overall / 5.0))
            # insert values into matrix
            idx = pids.index(r.asin)
            mat[-1][idx] = r.overall / 5.0
    logging.info('Computing SVD...')
    # Compute the SVD object
    recommender = GraphSVD(np.array(mat), components=components, epsilon=1e-6)
    logging.info('Getting test results...')
    correct = 0
    # for every item held out, test against
    # the predictions
    for _id, asin, score in holdout:
        idx = users.index(_id)
        pidx = pids.index(asin)
        predicted = recommender.predictions[idx][pidx]
        if abs(predicted - score) <= 0.2:
                correct += 1
    # Log success rate
    logging.info('Success rate: {}%.'.format((correct / 200)*100))
    logging.info('Uploading recommendations...')
    # Upload all the recommendatinos
    for idx, u in enumerate(users):
        # Sort based on likliehood
        recommended = sorted(zip(pids, recommender.predictions[idx]), key=operator.itemgetter(1), reverse=True)
        recommended = recommended[:5]
        items = [Recommendation(userID=u, asin=r[0], estimated_rating=r[1]) for r in recommended]
        logging.info('Uploading recommendations for user {}...'.format(u))
        add_recommendations(items)
