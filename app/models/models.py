from app.models import db
from datetime import datetime


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(64), unique=True)
    mobile = db.Column(db.String(16), unique=True)
    # md5 hash
    password = db.Column(db.String(32), nullable=False)
    # 1为root，2为admin，3为用户
    user_type = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.user_name


class UltrasonicImage(db.Model):
    __tablename__ = 'ultrasonic_images'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    body_part = db.Column(db.String(64))
    image_path = db.Column(db.String(256), nullable=False)
    annotations = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return '<UltrasonicImage %r>' % self.image_path


class ExamResult(db.Model):
    __tablename__ = "exam_results"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    score = db.Column(db.Float, default=0)
    exam_date = db.Column(db.DateTime, default=datetime.now)
    user_id = db.Column(db.Integer, db.ForeignKey('Users.id'), nullable=False)

    def __repr__(self):
        return '<ExamResults (%d, %f)>'.format(self.user_id, self.score)
