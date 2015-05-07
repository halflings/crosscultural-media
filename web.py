from flask import Flask, render_template, request, jsonify

import config
import crawler
import gavagai
import processor
from processor import Result, Sentence, Score, ResultEncoder
import json

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
    results = processor.process(query)
    for result in results:
        print result.title
        for sentence in result.sentences:
            print "sentence #{}".format(sentence.num)
            for score in sentence.scores:
                print "\t{}: score: {}, normalized score: {}".format(score.tone, score.score, score.normalizedScore)
    #return json.dumps(results, cls=ResultEncoder, sort_keys=True, indent=4, separators=(',', ': '))
    return ''

if __name__ == '__main__':
    app.run(host=config.flask_host, port=config.flask_port, debug=config.flask_debug)
