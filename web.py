from flask import Flask, render_template, request, jsonify

import config
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
    resEnglish = dict(query='coffe', language='en', results=[[-0.5, 0.2], [-0.15, -0.1], [0.25, -0.35], [0.6 ,-0.05], [0.7, 0], [0.9, 0.4]])
    resFrench = dict(query='cafe', language='fr', results=[[-0.5, 0.2], [-0.41, 0.05], [-0.25, -0.25], [-0.05, 0.1], [0.01, -0.4], [0.07, -0.02], [0.25, -0.3], [0.35, 0.3]])
    return json.dumps([resEnglish, resFrench])

@app.route('/results', methods=['GET'])
def result():
    return render_template('result.html')

if __name__ == '__main__':
    app.run(host=config.flask_host, port=config.flask_port, debug=config.flask_debug)
