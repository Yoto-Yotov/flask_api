from flask import Flask
from flask_restful import Api, Resource, marshal_with, reqparse, abort, fields
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

class VideoModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    views = db.Column(db.Integer, nullable=False)
    likes = db.Column(db.Integer, nullable=False)

    def __repr__(self) -> str:
        return f'Video(name = {self.name}, views = {self.views}, likes = {self.likes})'

video_put_args = reqparse.RequestParser()
video_put_args.add_argument('name', type=str, help="Name of the video", required=True)
video_put_args.add_argument('views', type=int, help="Views of the video", required=True)
video_put_args.add_argument('likes', type=int, help="Likes of the video", required=True)

video_update_args = reqparse.RequestParser()
video_update_args.add_argument('name', type=str, help="Name of the video")
video_update_args.add_argument('views', type=int, help="Views of the video")
video_update_args.add_argument('likes', type=int, help="Likes of the video")

resource_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'views': fields.Integer,
    'likes': fields.Integer,
}


class Video(Resource):
    @marshal_with(resource_fields)
    def get(self, video_id: int):
        result = VideoModel.query.filter_by(id=video_id).first()
        if not result:
            abort(404, message="Could not find video")

        return result

    @marshal_with(resource_fields)
    def put(self, video_id: int):
        args = video_put_args.parse_args()
        result = VideoModel.query.filter_by(id=video_id).first()
        if result:
            abort(409, message="Video already exists")

        video = VideoModel(id=video_id, name=args['name'], views=args['views'], likes=args['likes'])
        db.session.add(video)
        db.session.commit()
        return video, 201

    @marshal_with(resource_fields)
    def patch(self, video_id):
        args = video_update_args.parse_args()
        result = VideoModel.query.filter_by(id=video_id).first()
        if not result:
            abort(404, message="Could not find video")

        for arg, value in args.items():
            if value:
                setattr(result, arg, value)

        db.session.commit()

        return result, 202

    def delete(self, video_id: int):
        return '', 204


api.add_resource(Video, '/video/<int:video_id>')

@app.route("/")
def home_page():
    return {'home': 1}

if __name__ == "__main__":
    app.run(debug=True)
