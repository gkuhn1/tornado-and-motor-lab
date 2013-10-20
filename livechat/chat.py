# encoding: utf-8
import pymongo

import tornado.ioloop
import tornado.web
from tornado import websocket

from db import connection
from models import Message

clients = []

def create_message(message):
    """
    Creates a new message and sent it to all connected clients
    """
    msg = Message.create(message=message)
    for c in clients:
        c.write_message(msg.to_json)

class AddMessageHandler(tornado.web.RequestHandler):

    @tornado.web.asynchronous
    def post(self):
        self.redirect("/")
        create_message(self.get_argument("message"))

class SocketHandler(websocket.WebSocketHandler):

    def open(self):
        if self not in clients:
            clients.append(self)

    def on_message(self, message):
        create_message(message)

    def on_close(self):
        if self in clients:
            clients.remove(self)

class IndexHandler(tornado.web.RequestHandler):

    @tornado.web.asynchronous
    def get(self):
        cursor = Message.collection.find()
        cursor.sort([('created_at', pymongo.DESCENDING)]).limit(10)
        cursor.to_list(callback=self.after_find)

    def after_find(self, results, error):
        results.reverse()
        messages = [Message(r) for r in results]
        self.render("templates/index.html", messages=messages)


application = tornado.web.Application([
    (r"/add$", AddMessageHandler),
    (r"/ws$", SocketHandler),
    (r"/$", IndexHandler),
])

if __name__ == "__main__":
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()