#!/usr/bin/python3
"""This module defines a class User"""
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship


class User(BaseModel, Base):
    """This class defines a user model by various attributes"""
    __tablename__ = 'users'

    first_name = Column(String(128), nullable=False)
    last_name = Column(String(128), nullable=True)
    email = Column(String(128), nullable=False)
    password = Column(String(128), nullable=False)

    # relationship
    reviews = relationship('Review', cascade='all, delete', backref='user')
    places = relationship('Place', cascade='all, delete', backref='user')
