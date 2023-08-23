#!/usr/bin/python3
"""This is the base model class for AirBnB"""
import uuid
import models
from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, DateTime

Base = declarative_base()


class BaseModel:
    """On this class will defines all common attributes/methods
    for other classes
    """
    # init of columns database
    id = Column(String(60), primary_key=True, nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow())
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow())

    def __init__(self, *args, **kwargs):
        """Int of base model class
        Args:
            args: never used
            kwargs: constructor of the BaseModel arguments 
        Attributes:
            id: generated unique id 
            created_at: date creation
            updated_at: date updated
        """
        if kwargs:
            if 'id' not in kwargs:
                self.id = str(uuid.uuid4())

            for key, value in kwargs.items():
                if key == "created_at" or key == "updated_at":
                    value = datetime.strptime(value, "%Y-%m-%dT%H:%M:%S.%f")
                if key != "__class__":
                    setattr(self, key, value)

            if 'created_at' not in kwargs:
                self.created_at = self.updated_at = datetime.now()
        else:
            self.id = str(uuid.uuid4())
            self.created_at = self.updated_at = datetime.now()

    def __str__(self):
        """returns the string
        Return:
            returns the string of class dictionary, name & id 
        """
        return "[{}] ({}) {}".format(
            type(self).__name__, self.id, self.__dict__)

    def __repr__(self):
        """return a string representaion
        """
        return self.__str__()

    def save(self):
        """the public instance attribute updated_at to current
        """
        self.updated_at = datetime.now()
        models.storage.new(self)
        models.storage.save()

    def delete(self):
        """methond to delete current instance from storage
        """
        models.storage.delete(self)

    def to_dict(self):
        """methond creates dictionary of the class  and returns
        Return:
            returns a dictionary of all the key values in __dict__
        """
        the_dictionary = dict(self.__dict__)

        if '_sa_instance_state' in the_dictionary:
            del the_dictionary['_sa_instance_state']

        the_dictionary["__class__"] = str(type(self).__name__)

        the_dictionary["created_at"] = self.created_at.isoformat()
        the_dictionary["updated_at"] = self.updated_at.isoformat()

        return the_dictionary
