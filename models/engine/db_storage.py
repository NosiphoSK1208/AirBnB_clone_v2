#!/usr/bin/python3
"""Defines the DBStorage engine."""
from os import getenv
from models.base_model import Base
from models.base_model import BaseModel
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
from sqlalchemy import create_engine
from sqlalchemy.orm import relationship
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker


class DBStorage:
    """Represents a db  storage engine.

    Attributes:
        __engine: SQLAlchemy engine.
        __session: SQLAlchemy session.
    """

    __engine = None
    __session = None

    def __init__(self):
        """Init a new DBStorage instance."""
        self.__engine = create_engine("mysql+mysqldb://{}:{}@{}/{}".
                                      format(getenv("HBNB_MYSQL_USER"),
                                             getenv("HBNB_MYSQL_PWD"),
                                             getenv("HBNB_MYSQL_HOST"),
                                             getenv("HBNB_MYSQL_DB")),
                                      pool_pre_ping=True)
        if getenv("HBNB_ENV") == "test":
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """Query on the curret db session all objects of the given class.

        Return:
            Dict of queried classes in the format <class name>.<obj id> = obj.
        """
        if cls is None:
            my_objs = self.__session.query(State).all()
            my_objs.extend(self.__session.query(City).all())
            my_objs.extend(self.__session.query(User).all())
            my_objs.extend(self.__session.query(Place).all())
            my_objs.extend(self.__session.query(Review).all())
            my_objs.extend(self.__session.query(Amenity).all())
        else:
            if type(cls) == str:
                cls = eval(cls)
            my_objs = self.__session.query(cls)
        return {"{}.{}".format(type(o).__name__, o.id): o for o in my_objs}

    def new(self, obj):
        """Add object to current db session."""
        self.__session.add(obj)

    def save(self):
        """Save all changes to the current db session."""
        self.__session.commit()

    def delete(self, obj=None):
        """Delete object from the current db session."""
        if obj is not None:
            self.__session.delete(obj)

    def reload(self):
        """Reload all tables in the db  and init a new session."""
        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(bind=self.__engine,
                                       expire_on_commit=False)
        Session = scoped_session(session_factory)
        self.__session = Session()

    def close(self):
        """Close the working SQLAlchemy session."""
        self.__session.close()
