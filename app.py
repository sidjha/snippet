from flask import Flask, render_template, redirect, request, session
import os
import mixpanel

app = Flask(__name__)

DEBUG_MODE = os.environ['SNIPPET_DEBUG']

app.secret_key = os.environ['SNIPPET_APP_SECRET']


MONGO_DB_NAME = os.environ['MONGO_DB_NAME']
BUCKET_NAME = os.environ['S3_BUCKET_NAME']
MIXPANEL_TOKEN = os.environ['MIXPANEL_TOKEN']

@app.route('/')
def index():
	if active_session() == True:
		return render_template('logged_in.html')
		# ANALYTICS TODO: trigger reloaded dashboard
	else:
		return render_template('landing.html')
		# ANALYTICS TODO: trigger homepage visit

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
