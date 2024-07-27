#!/usr/bin/python3
""" holds class User"""
import hashlib
import models
from models.base_model import BaseModel, Base
from os import getenv
import sqlalchemy
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship


class User(BaseModel, Base):
    """Representation of a user """
    if models.storage_t == 'db':
        __tablename__ = 'users'
        email = Column(String(128), nullable=False)
        password = Column(String(128), nullable=False)
        first_name = Column(String(128), nullable=True)
        last_name = Column(String(128), nullable=True)
        places = relationship("Place", backref="user")
        reviews = relationship("Review", backref="user")
    else:
        email = ""
        password = ""
        first_name = ""
        last_name = ""

    def __init__(self, *args, **kwargs):
        """initializes user"""
        if kwargs:
            pwd = kwargs.pop('password', None)
            if pwd:
                User.__hash_password(self, pwd)
        super().__init__(*args, **kwargs)

    def __hash_password(self, pwd):
        """Hash a password using MD5"""
        md5 = hashlib.md5()
        md5.update(pwd.encode('utf-8'))
        secure_password = md5.hexdigest()
        setattr(self, "password", secure_password)
