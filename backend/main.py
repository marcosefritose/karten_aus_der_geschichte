import os
import urllib

from flask import Flask, request,  url_for, send_from_directory
from flask_restful import Api, Resource, fields, marshal_with
from flask_cors import CORS
from PIL import Image
from werkzeug.utils import secure_filename

from models import db, Episodes, Locations, Coordinates, Topics

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

episode_basic_fields = {
    'id': fields.Integer,
    'key': fields.String,
    'title': fields.String,
}

coordinate_fields = {
    'id': fields.Integer,
    'longitude': fields.String,
    'latitude': fields.String,
    'status': fields.String
}

location_basic_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'status': fields.String,
    'coordinates': fields.List(fields.Nested(coordinate_fields)),
}

location_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'coordinates': fields.List(fields.Nested(coordinate_fields)),
    'episodes': fields.List(fields.Nested(episode_basic_fields)),
    'status': fields.String,
}
topic_basic_fields = {
    'id': fields.Integer,
    'name': fields.String
}

topic_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'status': fields.String,
    'episodes': fields.List(fields.Nested(episode_basic_fields)),
}

episode_location_fields = {
    'location': fields.Nested(location_basic_fields),
    'status': fields.String,
    'context': fields.String
}

episode_topic_fields = {
    'topic_name': fields.String,
    'status': fields.String,
    'context': fields.String
}


episode_fields = {
    'id': fields.Integer,
    'key': fields.String,
    'title': fields.String,
    'summary': fields.String,
    'link': fields.String,
    'image': fields.String,
    'thumbnail': fields.String,
    'published': fields.String,
    'status': fields.String,
    'story_time_start': fields.String,
    'story_time_end': fields.String,
    'story_time_description': fields.String,
    'locations_association': fields.Nested(episode_location_fields),
    'locations': fields.List(fields.Nested(location_basic_fields)),
    'topics_association': fields.List(fields.Nested(episode_topic_fields))
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
        result = Episodes.query.get(episode_id)
        return result


class LocationListResource(Resource):
    @ marshal_with(location_fields)
    def get(self):
        if request.args.get('hasCoordinate') == 'true':
            result = Locations.query.join(Coordinates).filter(
                Coordinates.status == 'active' and (Coordinates.longitude.isnot(None)
                                                    or Coordinates.latitude.isnot(None))).all()
        else:
            result = Locations.query.order_by(
                Locations.name.asc()).all()
        return result


class LocationResource(Resource):
    @ marshal_with(location_fields)
    def get(self, location_id):
        result = Locations.query.get(location_id)
        return result


class TopicListResource(Resource):
    @ marshal_with(topic_fields)
    def get(self):
        result = Topics.query.all()
        return result


class TopicResource(Resource):
    @ marshal_with(topic_fields)
    def get(self, topic_id):
        result = Topics.query.get(topic_id)
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


@ app.route('/episodes/<episode_id>/status', methods=['PATCH'])
def update_episode_status(episode_id):
    episode = Episodes.query.filter(Episodes.id == episode_id).first()
    episode.status = request.form.get('status')
    db.session.commit()
    return 'OK'


@ app.route('/locations/<location_id>/status', methods=['PATCH'])
def update_location_status(location_id):
    location = Locations.query.filter(Locations.id == location_id).first()
    location.status = request.form.get('status')
    db.session.commit()
    return 'OK'


@ app.route('/topics/<topic_id>/status', methods=['PATCH'])
def update_topic_status(topic_id):
    topic = Topics.query.filter(Topics.id == topic_id).first()
    topic.status = request.form.get('status')
    db.session.commit()
    return 'OK'


api.add_resource(EpisodeListResource, "/episodes/")
api.add_resource(EpisodeResource, "/episodes/<string:episode_id>")
api.add_resource(LocationListResource, "/locations/")
api.add_resource(LocationResource, "/locations/<string:location_id>")
api.add_resource(TopicListResource, "/topics/")
api.add_resource(TopicResource, "/topics/<string:topic_id>")

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
