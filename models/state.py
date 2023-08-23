#!/usr/bin/python3
""" State Module for HBNB project """
from os import environ
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from models.base_model import BaseModel, Base



class State(BaseModel):
    """ State class """
    __tablename__ = "states"

    if environ['HBNB_TYPE_STORAGE'] == 'db':
        name = Column(String(128), nullable=False)
        cities = relationship('City', cascade='all, delete', backref='state')
    else:
        @property
        def cities(self):
            """
            Getter attribute that returns a list of City instances with a state_id
            equal to the current State's id. This leverages the FileStorage relationship
            between State and City.
            """
            from models import storage
            from models.city import City
            """returns City objs list in __objects"""
            the_cities_dict = storage.all(City)
            the_cities_list = []

            """get values from dict to list"""
            for city in the_cities_dict.values():
                if city.state.id == self.id:
                    the_cities_list.append(city)

            return the_cities_list
