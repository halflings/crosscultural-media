from flask import Flask, render_template, request

import config
import crawler
import gavagai
import processor

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
    for result in processor.process(query):
        print result.title
        for score in result.scores:
            print "\t{}: score: {}, normalized score: {}".format(score.tone, score.score, score.normalizedScore)
    return ''

if __name__ == '__main__':
    app.run(host=config.flask_host, port=config.flask_port, debug=config.flask_debug)
