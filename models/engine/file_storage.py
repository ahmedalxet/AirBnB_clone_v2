#!/usr/bin/python3
"""Module to define the FileStorage class"""
import json


class FileStorage:
    """Class to store objects in a JSON file"""
    __file_path = 'file.json'
    __objects = {}

    def all(self):
        """Returns a dictionary of all objects in storage"""
        return FileStorage.__objects

    def new(self, obj):
        """Adds a new object to the storage dictionary"""
        key = obj.__class__.__name__ + '.' + obj.id
        FileStorage.__objects[key] = obj

    def save(self):
        """Serializes the storage dictionary to JSON and saves to file"""
        json_dict = {}
        for key, value in FileStorage.__objects.items():
            json_dict[key] = value.to_dict()
        with open(FileStorage.__file_path, mode='w', encoding='utf-8') as file:
            json.dump(json_dict, file)

    def reload(self):
        """Deserializes the JSON file to objects"""
        try:
            with open(FileStorage.__file_path, mode='r', encoding='utf-8') as file:
                json_dict = json.load(file)
            for key, value in json_dict.items():
                module_name, class_name = key.split('.')
                module = __import__('models.' + module_name, fromlist=[class_name])
                cls = getattr(module, class_name)
                obj = cls(**value)
                FileStorage.__objects[key] = obj
        except FileNotFoundError:
            pass

    def close(self):
        """Calls reload() method for deserializing the JSON file to objects"""
        self.reload()
