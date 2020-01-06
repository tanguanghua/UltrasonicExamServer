from . import db
from datetime import datetime


class User(db.Model):
    __tablename__ = 'Users'

    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(64), unique=True)
    mobile = db.Column(db.String(16), unique=True)
    # md5 hash
    password = db.Column(db.String(32), nullable=False)

    def __repr__(self):
        return '<User %r>' % self.user_name


class UltrasonicImage(db.Model):
    __tablename__ = 'UltrasonicImages'

    id = db.Column(db.Integer, primary_key=True)
    body_part = db.Column(db.String(64))
    image_path = db.Column(db.String(256), nullable=False)
    annotations = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return '<UltrasonicImage %r>' % self.image_path


class ExamResult(db.Model):
    __tablename__ = "ExamResults"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('Users.id'), nullable=False)
    score = db.Column(db.Float, default=0)
    exam_date = db.Column(db.DateTime, default=datetime.now)

    def __repr__(self):
        return '<ExamResults (%d, %f)>'.format(self.user_id, self.score)
