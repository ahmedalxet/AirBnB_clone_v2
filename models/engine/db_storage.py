#!/usr/bin/python3
"""Module to define the DBStorage class"""
from os import getenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from models.base_model import Base


class DBStorage:
    """Class to store objects in a MySQL database"""
    __engine = None
    __session = None

    def __init__(self):
        """Instantiates a new DBStorage object"""
        user = getenv('HBNB_MYSQL_USER')
        pwd = getenv('HBNB_MYSQL_PWD')
        host = getenv('HBNB_MYSQL_HOST')
        db = getenv('HBNB_MYSQL_DB')
        env = getenv('HBNB_ENV')
        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'.
                                      format(user, pwd, host, db),
                                      pool_pre_ping=True)
        if env == 'test':
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """Returns a dictionary of all objects in storage"""
        if cls:
            objects = self.__session.query(cls).all()
        else:
            from models.base_model import BaseModel
            from models.user import User
            from models.state import State
            from models.city import City
            from models.amenity import Amenity
            from models.place import Place
            from models.review import Review
            objects = []
            classes = [BaseModel, User, State, City, Amenity, Place, Review]
            for cls in classes:
                objects += self.__session.query(cls).all()
        return {obj.__class__.__name__ + '.' + obj.id: obj for obj in objects}

    def new(self, obj):
        """Adds a new object to the database session"""
        self.__session.add(obj)

    def save(self):
        """Commits all changes to the database"""
        self.__session.commit()

    def delete(self, obj=None):
        """Deletes an object from the database"""
        if obj:
            self.__session.delete(obj)

    def reload(self):
        """Creates all tables in the database and initializes a new session"""
        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(session_factory)
        self.__session = Session()

    def close(self):
        """Calls remove() method on the private session attribute"""
        self.__session.close()
