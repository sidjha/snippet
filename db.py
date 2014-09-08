from flask.ext.mongokit import Connection
from models import User, Post, Fav, Open
import os

# initialize a connection to the MongoDB instance
connection = Connection(os.environ['MONGOHQ_URL'])

# register models with the connection
connection.register([User])
connection.register([Post])
connection.register([Fav])
connection.register([Open])

