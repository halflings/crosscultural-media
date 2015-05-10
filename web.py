from flask import Flask, render_template, request, jsonify

import config
import json
import mongoengine
import pca_transformer
from crawler import processing_routine, enqueue_query
from model import QueryJob

# Initializing the web app
app = Flask(__name__)

# Views
@app.route('/')
def index():
    return render_template('index.html')

# Actions
@app.route('/search', methods=['GET'])
def search():
	query = request.args.get('query') or ''
	#resEnglish = dict(query='coffee', language='en', results=[[-0.61748019,  0.10154602], [-0.61748019,  0.10154602], [ 0.51323593, -0.03923523], [ 0.60949273,  0.14345396], [-0.61748019,  0.10154602], [-0.47234277, -0.00079441], [-0.61748019,  0.10154602], [ 0.2137013, -0.44803087], [ 0.76519622,  0.38417246], [ 0.76519622,  0.38417246]])
	#resSwedish = dict(query='kaffe', language='sv', results=[[ 0.1815497,  -0.21035415], [ 0.3043041,   0.28996368], [-0.61748019,  0.10154602], [ 0.13368673, -0.00892597], [ 0.6372332,   0.16000524], [ 0.2137013,  -0.44803087], [-0.61748019,  0.10154602], [ 0.2137013,  -0.44803087], [ 0.2137013,  -0.44803087], [-0.58747614,  0.08038933]])
	#return json.dumps(dict(query='coffee', results=[resEnglish, resSwedish]))
	lang = "en"
	mongoengine.connect(config.db_name)
	jobs = QueryJob.objects(text=query, language=lang, processed=True)
	query_job = None

	# Check if any jobs exists
	if len(jobs) == 0:
		# Else process it
		enqueue_query(query, lang)
		processing_routine()
		query_job = QueryJob.objects(text=query, language=lang, processed=True)[0]
	else:
		query_job = jobs[0]

	return json.dumps(dict(query=query, results=pca_transformer.project(query_job)))

@app.route('/results', methods=['GET'])
def result():
	return render_template('result.html', query=request.args.get('query', ''))

if __name__ == '__main__':
    app.run(host=config.flask_host, port=config.flask_port, debug=config.flask_debug)