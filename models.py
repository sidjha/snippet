from flask.ext.mongokit import Document
import datetime
from bson.objectid import ObjectId

class User(Document):

	__collection__ = 'users'
	structure = {
		'email': basestring,
		'password': basestring,
		'username': basestring,
		'following': [ObjectId],
		'followers': [ObjectId],
		'friends': [ObjectId]
	}

	use_dot_notation = True


class Post(Document):
	__collection__ = 'posts'
	structure = {
		'media_url': basestring,
		'file_extension': basestring,
		's3_bucket': basestring,
		'text': basestring,
		'poster': ObjectId,
		'faves': [ObjectId],
		'posted_at': datetime.datetime,
		'opens': [ObjectId]
	}

	use_dot_notation = True


class Fav(Document):
	__collection__ = 'faves'
	structure = {
		'post': ObjectId,
		'faver': ObjectId,
		'favee': ObjectId,
		'timestamp': datetime.datetime,
	}

	use_dot_notation = True

class Open(Document):
	__collection__ = 'opens'
	structure = {
		'post': ObjectId,
		'opener': ObjectId,
		'timestamp': datetime.datetime
	}

	use_dot_notation = True
