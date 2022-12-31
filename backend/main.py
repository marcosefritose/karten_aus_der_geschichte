import csv
import json

from flask import Flask
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
api = Api(app)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://gag:gag@postgres_backend:5432/gag"

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
        'Locations', secondary=EpisodeLocation, backref='Episodes')

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
        'Episodes', secondary=EpisodeLocation, backref='Locations')

episode_put_args = reqparse.RequestParser()
episode_put_args.add_argument("title", type=str, help="Name of the episode")
episode_put_args.add_argument("location_name", type=str, help="Name of the location")

location_fields = {
    'name': fields.String,
    'longitude': fields.String,
    'latitude': fields.String,
}
resource_fields = {
    'id': fields.String,
    'title': fields.String,
    'summary': fields.String,
    'link': fields.String,
    'image': fields.String,
    'published': fields.String,
    'locations': fields.List(fields.Nested(location_fields))
}
        
class EpisodeListResource(Resource):
    @marshal_with(resource_fields)
    def get(self):
        result = Episodes.query.all()
        return result
    
class EpisodeResource(Resource):
    @marshal_with(resource_fields)
    def get(self, episode_id):
        #result = Episode.query.get(episode_id)
        result = Episodes.query.filter(Episodes.id == episode_id).first()
        return result


api.add_resource(EpisodeListResource, "/episodes/")
api.add_resource(EpisodeResource, "/episode/<string:episode_id>")

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
