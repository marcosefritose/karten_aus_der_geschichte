import os
import urllib

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.associationproxy import association_proxy

db = SQLAlchemy()


class Episodes(db.Model):
    __tablename__ = 'episodes_target'

    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(100))
    status = db.Column(db.String(100))
    title = db.Column(db.String(256))
    subtitle = db.Column(db.String(1000))
    summary = db.Column(db.String(10000))
    link = db.Column(db.String(1000))
    image = db.Column(db.String(1000))
    thumbnail = db.Column(db.String(1000))
    published = db.Column(db.DateTime())
    story_time_start = db.Column(db.Integer())
    story_time_end = db.Column(db.Integer())
    story_time_description = db.Column(db.String(1000))
    created_at = db.Column(db.DateTime())

    locations_association = db.relationship(
        'EpisodesLocation', backref='episodes')
    topics_association = db.relationship(
        'EpisodesTopic', backref='episodes')


class Locations(db.Model):
    __tablename__ = 'locations'
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String(164))
    name = db.Column(db.String(164))
    continent = db.Column(db.String(164))
    country = db.Column(db.String(164))
    origin = db.Column(db.String(164))
    created_at = db.Column(db.DateTime())

    episodes = db.relationship(
        'Episodes', secondary='episodes_locations', backref='locations')
    coordinates = db.relationship('Coordinates', backref='Locations')
    context = association_proxy('episodes_locations', 'context')


class EpisodesLocation(db.Model):
    __tablename__ = 'episodes_locations'
    id = db.Column(db.Integer, primary_key=True)
    context = db.Column(db.String(1000))
    created_at = db.Column(db.DateTime())

    episode_id = db.Column(
        db.Integer, db.ForeignKey('episodes_target.id'))
    location_id = db.Column(
        db.Integer, db.ForeignKey('locations.id'))

    episode = db.relationship(Episodes, backref='episodes_locations')
    location = db.relationship(Locations, backref='episodes_locations')


class Coordinates(db.Model):
    __tablename__ = 'coordinates'
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String(164))
    longitude = db.Column(db.String(164), primary_key=True)
    latitude = db.Column(db.String(164))
    created_at = db.Column(db.DateTime())

    location_id = db.Column(db.Integer, db.ForeignKey('locations.id'))
    locations = db.relationship('Locations', backref='Coordinates')


class Topics(db.Model):
    __tablename__ = 'topics'
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String(164))
    name = db.Column(db.String(164), primary_key=True)
    origin = db.Column(db.String(164))
    created_at = db.Column(db.DateTime())

    episodes = db.relationship(
        'Episodes', secondary='episodes_topics', backref='topics')


class EpisodesTopic(db.Model):
    __tablename__ = 'episodes_topics'
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String(164))
    context = db.Column(db.String(1000))

    episode_id = db.Column(db.Integer, db.ForeignKey('episodes_target.id'))
    topic_id = db.Column(db.Integer, db.ForeignKey('topics.name'))

    episode = db.relationship(Episodes, backref='episodes_topics')
    topic = db.relationship(Topics, backref='episodes_topics')
