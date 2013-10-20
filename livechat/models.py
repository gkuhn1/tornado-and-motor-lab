# encoding: utf-8

import json
import settings

from datetime import datetime

import utils
from db import connection


class BaseModel(dict):
    connection = connection
    collection = None

    @classmethod
    def build(cls, **kwargs):
        if "created_at" not in kwargs: kwargs["created_at"] = datetime.now()
        return cls(result=kwargs)

    @classmethod
    def create(cls, **kwargs):
        _object = cls.build(**kwargs)
        _object.save()
        return _object

    def __getattr__(self, attr):
        return self.get(attr, '')

    def get(self, attr, default=""):
        return utils.format(super(BaseModel, self).get(attr, default))

    def __init__(self, result=None, **kwargs):
        super(BaseModel, self).__init__()
        self.create_from_result(result or kwargs)

    def save(self, callback=None):
        if callback is None: callback=self.after_save

        self.collection.insert(self, callback=callback)

    def after_save(self, result, error):
        pass

    def create_from_result(self, result):
        self.update(result or {})

    @property
    def to_dict(self):
        dict_obj = {}
        for field in self._JSON_FIELDS:
             dict_obj[field] = self.get(field)
        return dict_obj

    @property
    def to_json(self):
        return json.dumps(self.to_dict)


class Message(BaseModel):
    _JSON_FIELDS = ["message", "created_at"]
    collection = connection.messaging.messages

