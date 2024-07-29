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
        """Initializes user"""
        password = kwargs.pop('password', None)
        super().__init__(*args, **kwargs)
        if password:
            self.password = self.__hash_password(password)
        elif not hasattr(self, 'password'):
            self.password = ""

    def __hash_password(self, pwd):
        """Hash a password using MD5"""
        md5 = hashlib.md5()
        md5.update(pwd.encode('utf-8'))
        return md5.hexdigest()
