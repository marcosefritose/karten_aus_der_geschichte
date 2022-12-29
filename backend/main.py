import csv
import json

from flask import Flask
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
api = Api(app)
CORS(app)


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


print(type(db))


class Episode(db.Model):
    id = db.Column(db.String(10), primary_key=True)
    title = db.Column(db.String(100))
    summary = db.Column(db.String(10000))
    link = db.Column(db.String(164))
    image = db.Column(db.String(1000))
    published = db.Column(db.DateTime())
    locations = db.relationship('Location', backref='episode', lazy=False)
    
    def __repr__(self):
        return f"Episode {self.id}: {self.title}, Locations: {', '.join([l.name for l in self.locations])}"

class Location(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    episode_id = db.Column(db.String(10), db.ForeignKey('episode.id'))
    name = db.Column(db.String(164))
    longitude = db.Column(db.String(164))
    latitude = db.Column(db.String(164))

# Only run first start
# db.drop_all()
# db.create_all()
# print('done')


# def import_locations_from_csv(db):
#     with open('ep_loc.csv', mode='r') as file:
#         csv_file = csv.reader(file)
#         next(csv_file, None)
#         for entry in csv_file:
#             ep = Episode(id=entry[0])
#             db.session.add(ep)
#             #for (name, long, lat) in (entry[1].):
#             #     db.sessio.add(Location(name=name, longitute=long, latitude=lat))
#             db.session.commit()

# import_locations_from_csv(db)
# print(Episode.query.all())
episode_put_args = reqparse.RequestParser()
episode_put_args.add_argument("title", type=str, help="Name of the episode")
episode_put_args.add_argument("location_name", type=str, help="Name of the location")

# episodes = {
#     1: {'title': 'GAG123 Schöne Gschite ausm Paulaner', 'location_name': 'Paris', 'location_long': 23.34345, 'location_lang': 12.2112, },
#     2: {'title': 'GAG312 qwedqwd', 'location_name': 'Timbukdu', 'location_long': 23.12313, 'location_lang': 12.2112, }}

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
        result = Episode.query.all()
        return result
    
class EpisodeResource(Resource):
    @marshal_with(resource_fields)
    def get(self, episode_id):
        #result = Episode.query.get(episode_id)
        result = Episode.query.filter(Episode.id == episode_id).first()
        return result
    
    # def put(self, episode_id):
    #     args = episode_put_args.parse_args()
    #     episodes[episode_id] = args 
    #     return episodes[episode_id], 201
    
class Importer(Resource):
    def get(self):
        return True, 200


api.add_resource(EpisodeListResource, "/episodes/")
api.add_resource(EpisodeResource, "/episode/<string:episode_id>")

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
