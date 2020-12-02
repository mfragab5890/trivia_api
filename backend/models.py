import os
from flask_migrate import Migrate
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy

# Declare database name
database_name = "trivia"

#intiate db with no assigment
db = SQLAlchemy()

def setup_db(app,database_name):
    app.config.from_pyfile('config.py')
    app.config['SQLALCHEMY_DATABASE_URI'] += database_name
    moment = Moment(app)
    db.init_app(app)
    # create instance migrate for data migration
    migrate = Migrate(app, db, compare_type=True)


'''
Question

'''


class Question(db.Model):
    __tablename__ = 'questions'

    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String)
    answer = db.Column(db.String)
    category = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)
    difficulty = db.Column(db.Integer)

    def __init__(self, question, answer, category, difficulty):
        self.question = question
        self.answer = answer
        self.category = category
        self.difficulty = difficulty

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'question': self.question,
            'answer': self.answer,
            'category': self.category,
            'difficulty': self.difficulty
        }


'''
Category

'''


class Category(db.Model):
    __tablename__ = 'categories'

    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String)
    questions = db.relationship('Question', backref='Q', lazy=True)
    def __init__(self, type):
        self.type = type

    def format(self):
        return {
            'id': self.id,
            'type': self.type
        }
