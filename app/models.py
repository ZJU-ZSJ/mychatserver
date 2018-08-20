# -*- coding=utf-8 -*-
from . import db, login_manager
from werkzeug.security import generate_password_hash, check_password_hash  # 引入密码加密 验证方法
from flask_login import LoginManager
from datetime import datetime
from flask_login import UserMixin
import hashlib
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from sqlalchemy import Float


class User(UserMixin,db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True)
    password_hash = db.Column(db.String(128))
    email = db.Column(db.String(64))
    phone = db.Column(db.String(32))

    @property
    def password(self):
        raise AttributeError(u'密码属性不正确')

    def is_active(self):
        return True

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)
        # 增加password会通过generate_password_hash方法来加密储存

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)
        # 在登入时,我们需要验证明文密码是否和加密密码所吻合

class Message(db.Model):
    __tablename__ = 'message'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64))
    content = db.Column(db.String(64))


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))