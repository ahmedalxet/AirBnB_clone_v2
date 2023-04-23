#!/usr/bin/python3
"""Package initializer"""
from os import getenv
from models.engine.file_storage import FileStorage

if getenv('HBNB_TYPE_STORAGE') == 'db':
    from models.engine.db_storage import DBStorage
    storage = DBStorage()
else:
    storage = FileStorage()

storage.reload()
