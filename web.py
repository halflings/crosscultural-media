from flask import Flask, render_template, request, jsonify

import config
import json
import mongoengine
import pca_transformer
from crawler import processing_routine, enqueue_query
from model import QueryJob

# Initializing the web app
app = Flask(__name__)
mongoengine.connect(config.db_name)

# Views
@app.route('/')
def index():
    return render_template('index.html', queries = QueryJob.objects(language='en', processed=True))

# Returns the processed jobs for the given query
def get_processed_jobs(query, language):
	return QueryJob.objects(text=query, language=language, processed=True)

# Actions
@app.route('/search', methods=['GET'])
def search():
	query = request.args.get('query') or ''
	lang = 'en'
	jobs = get_processed_jobs(query, lang)
	query_job = None

	# Check if any jobs exists
	if len(jobs) == 0:
		# Else process it
		enqueue_query(query, lang)
		processing_routine()
		query_job = get_processed_jobs(query, lang)[0]
	else:
		query_job = jobs[0]

	return json.dumps(dict(query=query, results=pca_transformer.project(query_job)))

@app.route('/results', methods=['GET'])
def result():
	return render_template('result.html', query=request.args.get('query', ''))

if __name__ == '__main__':
    app.run(host=config.flask_host, port=config.flask_port, debug=config.flask_debug)