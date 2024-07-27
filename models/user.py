#!/usr/bin/python3
""" holds class User"""
import models
from models.base_model import BaseModel, Base, hash_password
from os import getenv
import sqlalchemy
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
import hashlib


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
        if 'password' in kwargs:
            pwd = kwargs.pop('password')
            self.__hash_password(pwd)
        super().__init__(*args, **kwargs)

    @property
    def password(self):
        """Getter for password"""
        return self.__password

    @password.setter
    def password(self, value):
        """Setter for password, hashes it before saving"""
        self.__hash_password(value)

    def __hash_password(self, pwd):
        """Custom setter: encrypts password to MD5"""
        md5 = hashlib.md5()
        md5.update(pwd.encode("utf-8"))
        self.__password = md5.hexdigest()
