# -*- coding: utf-8 -*-
"""MyEng - Телеграм бот для узучения английского языка"""

from flask import jsonify
from flask import Flask
from flask_ngrok import run_with_ngrok
from flask_restful import Resource, Api, reqparse
import sqlalchemy as sa
from sqlalchemy.orm import Session
import sqlalchemy.ext.declarative as dec

SqlAlchemyBase = dec.declarative_base()

__factory = None


def global_init(db_file):
    global __factory

    if __factory:
        return

    if not db_file or not db_file.strip():
        raise Exception("Необходимо указать файл базы данных.")

    conn_str = f"sqlite:///{db_file}?check_same_thread=False"
    print(f"Подключение к базе данных по адресу {conn_str}")

    engine = sa.create_engine(conn_str, echo=False)
    __factory = orm.sessionmaker(bind=engine)
    SqlAlchemyBase.metadata.create_all(engine)


def create_session() -> Session:
    global __factory
    return __factory()


import datetime
import sqlalchemy
from flask_login import UserMixin
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin


class User(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = 'users'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, index=True)
    surname = sqlalchemy.Column(sqlalchemy.String)
    name = sqlalchemy.Column(sqlalchemy.String)
    age = sqlalchemy.Column(sqlalchemy.Integer)
    address = sqlalchemy.Column(sqlalchemy.String)
    email = sqlalchemy.Column(sqlalchemy.String)
    telegram_name = sqlalchemy.Column(sqlalchemy.String)
    aim = sqlalchemy.Column(sqlalchemy.String)
    password = sqlalchemy.Column(sqlalchemy.String)


class Test(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = 'tests'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    theme = sqlalchemy.Column(sqlalchemy.String)  # тема теста
    questions = sqlalchemy.Column(sqlalchemy.String)
    passed_users = sqlalchemy.Column(sqlalchemy.String)


class Question(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = 'questions'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    theme = sqlalchemy.Column(sqlalchemy.String)  # тема вопроса
    text = sqlalchemy.Column(sqlalchemy.String)  # на русском
    ans = sqlalchemy.Column(sqlalchemy.String)  # на английском


app = Flask(__name__)
run_with_ngrok(app)
app.config['PERMANENT_SESSION_LIFETIME'] = datetime.timedelta(days=365)
app.config['SECRET_KEY'] = 'my_secret'

api = Api(app)


def log_user(user_id, given_password):
    ses = create_session()
    user = ses.query(User).filter(User.id == user_id).first()
    if user and user.check_password(given_password):
        return jsonify({"message": 'ok'})
    else:
        return jsonify({"message": "something wrong"})


class UsersResource(Resource):
    def get(self, user_id):
        session = create_session()
        user = session.query(User).filter(User.id == user_id).first()
        if not user:
            return jsonify({"message": "such user does not exist"})
        return jsonify({'user_data': user.to_dict(), "message": "ok"})

    def delete(self, user_id):
        session = create_session()
        user = session.query(User).filter(User.id == user_id).first()
        if not user:
            return jsonify({"message": "such user does not exist"})
        session.delete(user)
        session.commit()
        return jsonify({'message': 'ok, user successfully deleted'})


class UsersListResource(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('id', type=int, required=True)
    parser.add_argument('surname')
    parser.add_argument('name')
    parser.add_argument('age', type=int)
    parser.add_argument('address')
    parser.add_argument('email')
    parser.add_argument('password')
    parser.add_argument('telegram_name')
    parser.add_argument('aim')

    def get(self):
        session = create_session()
        users = session.query(User).all()
        return jsonify({'users': [item.to_dict() for item in users]})

    def post(self):
        args = UsersListResource.parser.parse_args()
        attributes = ['surname', 'name', 'age', 'address', 'email', 'telegram_name', 'aim']
        session = create_session()
        exist = session.query(User).filter(User.id == args['id']).first()
        if exist:
            return jsonify({"message": "such user already exists"})
        user = User(
            id=args['id'],
            surname=args['surname'],
            name=args['name'],
            age=args['age'],
            address=args['address'],
            password=args['password'],
            email=args['email'],
            aim=args['aim'],
            telegram_name=args['telegram_name'],
        )
        session.add(user)
        session.commit()
        return jsonify({'success': 'OK - the user has been added'})


class QuestionListResource(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('id', type=int)
    parser.add_argument('theme')
    parser.add_argument('text')
    parser.add_argument('ans')

    def post(self):
        args = QuestionListResource.parser.parse_args()
        session = create_session()
        ques = Question(
            id=args['id'],
            theme=args['theme'],
            text=args['text'],
            ans=args['ans']
        )
        session.add(ques)
        session.commit()
        return jsonify({"message": 'ok - question added'})


class QuestionResource(Resource):
    def get(self, ques_id):
        session = create_session()
        ques = session.query(Question).filter(Question.id == ques_id).first()
        if not ques:
            return jsonify({"error": "such question does not exist"})
        return jsonify({'question': ques.to_dict()})


class TestsListResource(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('id', type=int)
    parser.add_argument('theme')
    parser.add_argument('questions')
    parser.add_argument('passed_users')

    def post(self):
        session = create_session()
        args = TestsListResource.parser.parse_args()
        test = Test(
            id=args['id'],
            theme=args['theme'],
            questions=args['questions'],
            passed_users=args['passed_users']
        )
        session.add(test)
        session.commit()
        return jsonify({"message": "ok - test added"})


class TestsResource(Resource):
    def get(self, theme, user_id):
        session = create_session()
        tests = session.query(Test).filter(Test.theme == theme).all()
        if len(tests) == 0:
            return jsonify({"error": "no such test"})
        for i in range(len(tests)):
            if str(user_id) not in tests[i].passed_users.split(','):
                tests[i].passed_users += str(user_id) + ','
                return jsonify({'test': tests[i].to_dict(), "message": "ok"})
        return jsonify({"error": "all existing test are passed"})


if __name__ == "__main__":
    global_init('baza.db')
    api.add_resource(UsersListResource, '/api/users')
    api.add_resource(UsersResource, '/api/users/<int:user_id>')

    api.add_resource(TestsResource, '/api/tests/<string:theme>/<int:user_id>')
    api.add_resource(TestsListResource, '/api/tests')
    api.add_resource(QuestionListResource, '/api/questions')
    api.add_resource(QuestionResource, '/api/questions/<int:ques_id>')
    app.run()
