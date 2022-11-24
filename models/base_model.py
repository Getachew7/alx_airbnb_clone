#!/usr/bin/python3
"""Module contains superclass for mananging all Airbnb objects"""
import uuid
import datetime
import models


class BaseModel:
    """Handles initialization, serialization and deserialization of your future instances
       Args:
            *args: arguments(unused)
            **kwargs(dict): attrubute values   
    """
    def __init__(self, *args, **kwargs):
        """Initialization of class instances"""
        DATE_TIME_FORMAT = '%Y-%m-%dT%H:%M:%S.%f'
        if not kwargs:
            user_id = uuid.uuid4()
            self.id = str(user_id)
            self.created_at = datetime.datetime.now()
            self.updated_at = datetime.datetime.now()
            models.storage.new(self)
        else:
            for key, value in kwargs.items():
                if key in ("updated_at", "created_at"):
                    self.__dict__[key] = datetime.datetime.strptime(
                        value, DATE_TIME_FORMAT)
                elif key[0] == "id":
                    self.__dict__[key] = str(value)
                else:
                    self.__dict__[key] = value

    def __str__(self):
        """Override string representation of class instance"""
        return f"[{__class__.__name__}] {self.id} {self.__dict__}"

    def save(self):
        """updates the public instance attribute updated_at with the current datetime"""
        self.updated_at = datetime.datetime.now()
        models.storage.save()

    def to_dict(self):
        """returns a dictionary containing all keys/values of __dict__"""
        my_dict = {"__class__": __class__.__name__}

        for key in self.__dict__:
            if key in ("created_at", "updated_at"):
                my_dict.update({key: getattr(self, key).isoformat()})
            else:
                my_dict.update({key: getattr(self, key)})

        return my_dict
