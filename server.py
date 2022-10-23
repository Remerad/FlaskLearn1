import atexit
from flask import Flask, jsonify, request
from flask.views import MethodView
from sqlalchemy import create_engine, Column, Integer, String, DateTime, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError
from os import getenv

engine = create_engine(f"postgresql://postgres:{getenv('PG_pasw')}@127.0.0.1:5432/flask_netology", echo=True)#o12KinvJdE
Base = declarative_base()
Session = sessionmaker(bind=engine)
atexit.register(lambda: engine.dispose())

class HttpError(Exception):
    def __init__(self, status_code, error_message):
        self.status_code = status_code
        self.error_message = error_message

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    registration_time = Column(DateTime, server_default=func.now())


Base.metadata.create_all(engine)
app = Flask('server')


@app.route('/test/', methods=['POST'])
def test():
    json_data = request.json
    headers = request.headers
    qs = request.args

    return jsonify({'status': 'OK',
                    'json_data': json_data,
                    'headers': dict(headers),
                    'qs': dict(qs)})


@app.errorhandler(HttpError)
def http_error_handler(error):
    response = jsonify({
        'error': error.error_message
    })
    error.status_code = 400
    return response
    pass


class UserView(MethodView):

    def get(self):
        pass

    def post(self):
        json_data = request.json
        with Session() as session:
            user = User(email=json_data['email'], password=json_data['password'])
            session.add(user)
            try:
                session.commit()
                return jsonify({
                    'id': user.id,
                    'registration_time': user.registration_time.isoformat()
                }
                )
            except IntegrityError:
                raise HttpError(400, 'User already exists')


app.add_url_rule('/users/', view_func=UserView.as_view('create_user'), methods=['POST'])
app.run(
    host='0.0.0.0',
    port=5000
)
