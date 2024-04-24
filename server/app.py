from flask import Flask, make_response, jsonify, request, session
from flask_migrate import Migrate
from flask_restful import Api, Resource
from models import db, Article, User

app = Flask(__name__)
app.secret_key = b'Y\xf1Xz\x00\xad|eQ\x80t \xca\x1a\x10K'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)
api = Api(app)

# Resource for user login
class Login(Resource):
    def post(self):
        username = request.json.get('username')
        user = User.query.filter_by(username=username).first()
        if user:
            session['user_id'] = user.id
            return jsonify(id=user.id, username=user.username), 200
        return {'message': 'User not found'}, 404

# Resource for user logout
class Logout(Resource):
    def delete(self):
        if 'user_id' in session:
            session.pop('user_id', None)
        return '', 204

# Resource to check session
class CheckSession(Resource):
    def get(self):
        user_id = session.get('user_id')
        if user_id:
            user = User.query.get(user_id)
            if user:
                return jsonify(id=user.id, username=user.username), 200
        return {}, 401

# Existing resources and new ones added to the API
api.add_resource(ClearSession, '/clear')
api.add_resource(IndexArticle, '/articles')
api.add_resource(ShowArticle, '/articles/<int:id>')
api.add_resource(Login, '/login')
api.add_resource(Logout, '/logout')
api.add_resource(CheckSession, '/check_session')

if __name__ == '__main__':
    app.run(port=5555, debug=True)
