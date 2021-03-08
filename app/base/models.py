# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from flask_login import UserMixin
from sqlalchemy import Binary, Column, Integer, String
from pytz import timezone

from app import db, login_manager

from app.base.util import hash_pass

from datetime import datetime

class ApiaryModel(db.Model):
    __tablename__ = 'Apiary'
    apiary_id = Column(String(80), primary_key=True)
    user_id = Column(String(80), primary_key=True)
    location = Column(String(80))

class HiveModel(db.Model):
    __tablename__ = 'Hive'
    hive_id = Column(Integer, primary_key=True)
    apiary_id = Column(String(80), nullable=False)
    user_id = Column(String(80))
    hive_description = Column(String(80))
    association_code = Column(String(80), nullable=False)

class SensorFeed(db.Model):
    __tablename__ = 'SensorFeed'
    hive_id = db.Column(db.String(80), primary_key=True)
    temperature = db.Column(db.Integer)
    humidity = db.Column(db.Integer)
    weight = db.Column(db.Integer)
    timestamp = db.Column(db.DateTime(timezone=True), primary_key=True, default=datetime.now)

class User(db.Model, UserMixin):
    __tablename__ = 'User'
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    email = Column(String, unique=True)
    password = Column(Binary)

    def __init__(self, **kwargs):
        for property, value in kwargs.items():
            # depending on whether value is an iterable or not, we must
            # unpack it's value (when **kwargs is request.form, some values
            # will be a 1-element list)
            if hasattr(value, '__iter__') and not isinstance(value, str):
                # the ,= unpack of a singleton fails PEP8 (travis flake8 test)
                value = value[0]

            if property == 'password':
                value = hash_pass( value ) # we need bytes here (not plain str)
                
            setattr(self, property, value)

    def __repr__(self):
        return str(self.username)


@login_manager.user_loader
def user_loader(id):
    return User.query.filter_by(id=id).first()

@login_manager.request_loader
def request_loader(request):
    username = request.form.get('username')
    user = User.query.filter_by(username=username).first()
    return user if user else None
