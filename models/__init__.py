#!/usr/bin/python3
"""This module instantiates an object of class FileStorage or DBStorage"""
from os import environ
from models.engine.db_storage import DBStorage
from models.engine.file_storage import FileStorage

if environ['HBNB_TYPE_STORAGE'] == 'db':
    # Use DBStorage as the storage method
    storage = DBStorage()
else:
    # Use FileStorage as the storage method
    storage = FileStorage()

# Load data into the storage
storage.reload()
