import os
import urllib

from flask import Flask, request,  url_for, send_from_directory
from flask_restful import Api, Resource, reqparse, fields, marshal_with
from flask_cors import CORS
from PIL import Image
from werkzeug.utils import secure_filename

from models import db, Episodes, Locations, Coordinates

DB_NAME = os.getenv('POSTGRES_DB')
DB_USER = os.getenv('POSTGRES_USER')
DB_PASSWORD = os.getenv('POSTGRES_PASSWORD')
UPLOAD_FOLDER = '/code/data/uploads'
THUMBNAIL_FOLDER = '/code/data/thumbnails'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://{DB_USER}:{DB_PASSWORD}@postgres_backend:5432/{DB_NAME}"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['THUMBNAIL_FOLDER'] = THUMBNAIL_FOLDER
app.config['SECRET_KEY'] = 'the random string'

api = Api(app)
CORS(app)

db.init_app(app)

episode_put_args = reqparse.RequestParser()
episode_put_args.add_argument("title", type=str, help="Name of the episode")
episode_put_args.add_argument(
    "location_name", type=str, help="Name of the location")

episode_basic_fields = {
    'id': fields.String,
    'title': fields.String,
}

coordinate_fields = {
    'longitude': fields.String,
    'latitude': fields.String,
    'active': fields.Boolean
}

location_basic_fields = {
    'name': fields.String,
    'context': fields.String,
    'coordinates': fields.List(fields.Nested(coordinate_fields)),
}
location_fields = {
    'name': fields.String,
    'coordinates': fields.List(fields.Nested(coordinate_fields)),
    'episodes': fields.List(fields.Nested(episode_basic_fields))
}
topic_basic_fields = {
    'name': fields.String,
    'context': fields.String
}


episode_fields = {
    'id': fields.String,
    'title': fields.String,
    'summary': fields.String,
    'link': fields.String,
    'image': fields.String,
    'thumbnail': fields.String,
    'published': fields.String,
    'story_time_start': fields.String,
    'story_time_end': fields.String,
    'locations': fields.List(fields.Nested(location_basic_fields)),
    'topics': fields.List(fields.Nested(topic_basic_fields))
}


class EpisodeListResource(Resource):
    @ marshal_with(episode_fields)
    def get(self):
        result = Episodes.query.order_by(
            Episodes.published.desc()).all()
        return result


class EpisodeResource(Resource):
    @ marshal_with(episode_fields)
    def get(self, episode_id):
        # result = Episode.query.get(episode_id)
        result = Episodes.query.filter(Episodes.id == episode_id).first()
        return result


class LocationListResource(Resource):
    @ marshal_with(location_fields)
    def get(self):
        result = Locations.query.join(Coordinates).filter(
            Coordinates.active == True and (Coordinates.longitude.isnot(None)
                                            or Coordinates.latitude.isnot(None))).all()
        return result


@ app.route('/get-episode-image-from-link', methods=['POST'])
def upload_episode_image_from_url():
    url = request.form.get('url')
    episode_id = request.form.get('episode_id')

    filename = secure_filename(episode_id + '.jpeg')
    thumbnail_filename = secure_filename(episode_id + '_thumbnail.jpeg')

    if os.path.exists(os.path.join(app.config['THUMBNAIL_FOLDER'], thumbnail_filename)):
        return url_for('thumbnail', filename=thumbnail_filename)

    with urllib.request.urlopen(url) as image_stream:
        with Image.open(image_stream) as im:
            im.save(os.path.join(
                app.config['UPLOAD_FOLDER'], filename), 'JPEG')
            im.thumbnail((128, 128))
            im.save(os.path.join(
                app.config['THUMBNAIL_FOLDER'], thumbnail_filename), 'JPEG')

            return url_for('thumbnail', filename=thumbnail_filename)


@ app.route('/uploads/images/<filename>')
def uploaded_image(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)


@ app.route('/uploads/thumbnails/<filename>')
def thumbnail(filename):
    return send_from_directory(app.config['THUMBNAIL_FOLDER'],
                               filename)


api.add_resource(EpisodeListResource, "/episodes/")
api.add_resource(EpisodeResource, "/episodes/<string:episode_id>")
api.add_resource(LocationListResource, "/locations/")

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
