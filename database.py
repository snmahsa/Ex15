from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), nullable=False, unique=True)
    password = db.Column(db.String(150), nullable=False)

class TrackerInput(db.Model):
    __tablename__ = 'tracker_input'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    result_code = db.Column(db.Integer)
    result = db.Column(db.String(100))
    sepal_length = db.Column(db.Float)
    sepal_width = db.Column(db.Float)
    petal_length = db.Column(db.Float)
    petal_width = db.Column(db.Float)
