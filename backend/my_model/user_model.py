# coding: utf-8
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import generate_password_hash, check_password_hash

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    username = db.Column(db.String(20), primary_key=True, nullable=False)
    useremail = db.Column(db.String(100))
    userpwd = db.Column(db.String(100), nullable=False)
    bio = db.Column(db.Text)
    created_at = db.Column(db.DateTime, server_default=db.FetchedValue())
    updated_at = db.Column(db.DateTime, server_default=db.FetchedValue())

    def has_password(self):
        """
        userpwd 를 암호화 해준다.
        """
        self.userpwd = generate_password_hash(self.userpwd).decode('utf8')

    def check_password(self, password):
        """
        check_password 함수에서 암호화 된 비밀번호와 입력받은 비밀번호를 비교
        """
        return check_password_hash(self.userpwd, password)
