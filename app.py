from flask import Flask, render_template, redirect, request, session, json, url_for
import os, re, base64, binascii
import mixpanel, boto
from db import connection

app = Flask(__name__)

DEBUG_MODE = os.environ['SNIPPET_DEBUG']

app.secret_key = os.environ['SNIPPET_APP_SECRET']


MONGO_DB_NAME = os.environ['MONGO_DB_NAME']
BUCKET_NAME = os.environ['S3_BUCKET_NAME']
MIXPANEL_TOKEN = os.environ['MIXPANEL_TOKEN']

@app.route('/')
def index():
	if active_session() == True:
		return render_template('logged_in.html', user=session['email'])
		# ANALYTICS TODO: trigger reloaded dashboard
	else:
		return render_template('landing.html')
		# ANALYTICS TODO: trigger homepage visit

@app.route('/loggedin')
def logged_in():
	return render_template('logged_in.html')

@app.route('/signup')
def signup():
	if active_session() == True:
		return render_template('logged_in.html')
		# ANALYTICS TODO: trigger reloaded dashboard
	else:
		return render_template('signup.html')
		# ANALYTICS TODO: trigger homepage visit

@app.route('/signup_submit', methods=['POST'])
def signup_submit():
	if request.method == 'POST':
		email = request.form['email']
		password = request.form['password']

		# TODO: check email, password validity

		print email, password

		user_coll = None
		try:
			user_coll = connection[MONGO_DB_NAME].users

		except Exception as err:
			print err
			print('ERROR could not connect to DB')

		user = user_coll.User.find_one({'email': email})

		if user is None:
			user = user_coll.User()
			user['email'] = email
			user['password'] = password
			try:
				user.save()
				output = 'New user: %s' % (email)
				session['email'] = email

				user_data = {}
				user_data['email'] = email
				return json.dumps({'success': 1, 'user': user_data}), 200
			except Exception as err:
				print err
				print('ERROR in saving new user to db')
		else:
			print 'User with that email already exists'
			return json.dumps({'success': 0, 
							   'errorMsg': 'User with that email already exists'
							 }), 400
	else:
		return 'Bad call'


@app.route('/post_media', methods=['POST'])
def post_media():
	if request.method == 'POST':
		base64_img_url = request.form['media']
		m = re.search('base64,(.*)', base64_img_url)
		decoded_img = m.group(1)

		# generate unique random filename
		NUM_SUFFIX_CHARS = 10
		FILE_EXTENSION = '.png'

		filename = binascii.b2a_hex(os.urandom(NUM_SUFFIX_CHARS)) + FILE_EXTENSION

		try:
			f = open(filename, 'wb')
			f.write(decoded_img.decode('base64'))
			f.close()
		except Exception as err:
			return json.dumps({'url': 'Failed'}), 400

		from boto.s3.key import Key
		conn = boto.connect_s3(os.environ['AWS_ACCESS_KEY_ID'], os.environ['AWS_SECRET_ACCESS_KEY'])
		bucket = conn.get_bucket(BUCKET_NAME)
		key = filename
		k = Key(bucket)
		k.key = key
		k.set_contents_from_filename(key)
		k.set_acl('public-read')

		os.remove(filename)

		return json.dumps({'url': 'yoyoyo'}), 200
	else:
		return json.dumps({"error": "Bad call"}), 400



def active_session():
	if 'email' in session:
		return True
	else:
		return False
	

if __name__ == '__main__':
	port = int(os.environ.get('PORT', '5000'))
	if DEBUG_MODE == 'true':
		app.run(host='0.0.0.0', port=port, debug=True)
	else:
		app.run(host='0.0.0.0', port=port)
