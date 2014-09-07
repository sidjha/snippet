from flask import Flask, render_template, redirect, request, session
import os
import mixpanel

app = Flask(__name__)

app.secret_key = os.environ['SNIPPET_APP_SECRET']
debug_mode = os.environ['SNIPPET_DEBUG']

MONGO_DB_NAME = os.environ['MONGO_DB_NAME']
BUCKET_NAME = os.environ['S3_BUCKET_NAME']

@app.route('/')
def index():
	return "Yo!"

if __name__ == '__main__':
	port = int(os.environ.get('PORT', '5000'))
	if debug_mode == 'true':
		app.run(host='0.0.0.0', port=port, debug=True)
	else:
		app.run(host='0.0.0.0', port=port)
