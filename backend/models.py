import os
import urllib

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.associationproxy import association_proxy

db = SQLAlchemy()


class Episodes(db.Model):
    __tablename__ = 'episodes_target'

    id = db.Column(db.String(10), primary_key=True)
    title = db.Column(db.String(100))
    subtitle = db.Column(db.String(1000))
    summary = db.Column(db.String(10000))
    link = db.Column(db.String(1000))
    image = db.Column(db.String(1000))
    thumbnail = db.Column(db.String(1000))
    published = db.Column(db.DateTime())
    story_time_start = db.Column(db.Integer())
    story_time_end = db.Column(db.Integer())
    locations_association = db.relationship(
        'EpisodesLocation', backref='episodes')
    topicss_association = db.relationship(
        'EpisodesTopic', backref='episodes')


class Locations(db.Model):
    __tablename__ = 'locations'
    name = db.Column(db.String(164), primary_key=True)
    episodes = db.relationship(
        'Episodes', secondary='episodes_locations', backref='locations')
    context = association_proxy('episodes_locations', 'context')
    coordinates = db.relationship('Coordinates', backref='Locations')


class Coordinates(db.Model):
    __tablename__ = 'coordinates'
    location_name = db.Column(db.String(164), db.ForeignKey('locations.name'))
    longitude = db.Column(db.String(164), primary_key=True)
    latitude = db.Column(db.String(164))
    active = db.Column(db.Boolean())
    locations = db.relationship('Locations', backref='Coordinates')


class EpisodesLocation(db.Model):
    __tablename__ = 'episodes_locations'
    id = db.Column(db.Integer, primary_key=True)
    episode_id = db.Column(
        db.String(1000), db.ForeignKey('episodes_target.id'))
    location_name = db.Column(
        db.String(1000), db.ForeignKey('locations.name'))
    context = db.Column(db.String(1000))

    episode = db.relationship(Episodes, backref='episodes_locations')
    location = db.relationship(Locations, backref='episodes_locations')


class Topics(db.Model):
    __tablename__ = 'topics'
    name = db.Column(db.String(164), primary_key=True)
    episodes = db.relationship(
        'Episodes', secondary='episodes_topics', backref='topics')
    context = association_proxy('episodes_topics', 'context')


class EpisodesTopic(db.Model):
    __tablename__ = 'episodes_topics'
    id = db.Column(db.Integer, primary_key=True)
    episode_id = db.Column(
        db.String(1000), db.ForeignKey('episodes_target.id'))
    topic_name = db.Column(
        db.String(1000), db.ForeignKey('topics.name'))
    context = db.Column(db.String(1000))

    episode = db.relationship(Episodes, backref='episodes_topics')
    topic = db.relationship(Topics, backref='episodes_topics')
