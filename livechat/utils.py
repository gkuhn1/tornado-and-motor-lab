# encoding: utf-8

import datetime
import settings
from tornado.locale import get


FORMATTERS = {
    datetime.datetime: lambda x: x.strftime(settings.DATETIME_FORMAT),
    datetime.date: lambda x: x.strftime(settings.DATE_FORMAT)
}

def format(value):
    if type(value) not in FORMATTERS:
        return value

    return FORMATTERS[type(value)](value)