import csv
import json
import os

from dotenv import load_dotenv
from pathlib import Path
from flask import Flask
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

# env_path = Path('../.env')
load_dotenv()

db_name = os.getenv('POSTGRES_DB')
db_username = os.getenv('POSTGRES_USER')
db_password = os.getenv('POSTGRES_PASSWORD')

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://{db_username}:{db_password}@postgres_backend:5432/{db_name}"

api = Api(app)
CORS(app)


db = SQLAlchemy(app)


EpisodeLocation = db.Table('episodes_locations',
                   db.Column('episode_id', db.String(1000), db.ForeignKey('episodes_target.id')),
                   db.Column('location_name', db.String(1000), db.ForeignKey('locations.name'))
)

class Episodes(db.Model):
    __tablename__ = 'episodes_target'
    id = db.Column(db.String(10), primary_key=True)
    title = db.Column(db.String(100))
    subtitle = db.Column(db.String(1000))
    summary = db.Column(db.String(10000))
    link = db.Column(db.String(1000))
    image = db.Column(db.String(1000))
    published = db.Column(db.DateTime())
    locations = db.relationship(
        'Locations', secondary=EpisodeLocation, backref='Episodes', lazy='dynamic')

    def __repr__(self):
        return f"Episode {self.id}: {self.title}, Locations: {', '.join([l.name for l in self.locations])}"

class Locations(db.Model):
    __tablename__ = 'locations'
    name = db.Column(db.String(164), primary_key=True)
    longitude = db.Column(db.String(164))
    latitude = db.Column(db.String(164))
    requested = db.Column(db.Boolean())
    valid = db.Column(db.Boolean())
    episodes = db.relationship(
        'Episodes', secondary=EpisodeLocation, backref='Locations', lazy='dynamic')

episode_put_args = reqparse.RequestParser()
episode_put_args.add_argument("title", type=str, help="Name of the episode")
episode_put_args.add_argument("location_name", type=str, help="Name of the location")

episode_basic_fields = {
    'id': fields.String,
    'title': fields.String,
}

location_basic_fields = {
    'name': fields.String,
    'longitude': fields.String,
    'latitude': fields.String,
}

location_fields = {
    'name': fields.String,
    'longitude': fields.String,
    'latitude': fields.String,
    'episodes': fields.List(fields.Nested(episode_basic_fields))
}
episode_fields = {
    'id': fields.String,
    'title': fields.String,
    'summary': fields.String,
    'link': fields.String,
    'image': fields.String,
    'published': fields.String,
    'locations': fields.List(fields.Nested(location_basic_fields))
}
        
class EpisodeListResource(Resource):
    @marshal_with(episode_fields)
    def get(self):
        result = Episodes.query.order_by(Episodes.published.desc()).all()
        return result
    
class EpisodeResource(Resource):
    @marshal_with(episode_fields)
    def get(self, episode_id):
        #result = Episode.query.get(episode_id)
        result = Episodes.query.filter(Episodes.id == episode_id).first()
        return result
    
class LocationListResource(Resource):
    @marshal_with(location_fields)
    def get(self):
        result = Locations.query.filter(Locations.latitude != "NaN").all()
        return result


api.add_resource(EpisodeListResource, "/episodes/")
api.add_resource(EpisodeResource, "/episodes/<string:episode_id>")
api.add_resource(LocationListResource, "/locations/")

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
