"""
Flask Documentation:     http://flask.pocoo.org/docs/
Jinja2 Documentation:    http://jinja.pocoo.org/2/documentation/
Werkzeug Documentation:  http://werkzeug.pocoo.org/documentation/

This file creates your application.
"""

import os
from flask import Flask, render_template, request, Response, json
import requests

app = Flask(__name__)

app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'this_should_be_configured')


###
# Routing for your application.
###

@app.route('/')
def home():
    """Render website's home page."""
    return render_template('home.html')


@app.route('/about/')
def about():
    """Render the website's about page."""
    return render_template('about.html')


@app.route('/test_output')
def test_output():
    return 'this is my test output'


@app.route('/v1/defineWord', methods=['GET'])
def defineWordGet():
    return 'this should return something useful'


@app.route('/v1/defineWord/', methods=['POST'])
def defineWord():
    params = request.get_json()
    try:
        word = params['result']['parameters']['any']
    except Exception as e:
        response = 'I\'m having some trouble with that word'
        rtn = {
            'speech': response,
            'displayText': response,
            'data': {},
            'contextOut': [],
            'source': 'PeterKnowsBest'
        }
        contents = json.dumps(rtn)

        return Response(contents, 200, mimetype='application/json')

    if word:
        url = 'https://od-api.oxforddictionaries.com/api/v1/entries/en/' + word
        headers = {
            'app_id': '4a5a193d',
            'app_key': 'e6ce29c1c11fd02c4aa3877956b61b2f'
        }

        response = requests.get(url, headers=headers)
        response_json = r.json()
        results = response_json['results']

    if results and len(results) > 0:
        lexicalEntries = results[0]['lexicalEntries']

    if lexicalEntries and len(lexicalEntries) > 0:
        entries = lexicalEntries[0]['entries']

    if entries and len(entries) > 0:
        senses = entries[0]['senses']

    if senses and len(senses) > 0:
        definitions = senses[0]['definitions']

    if definitions and len(definitions) > 0:
        definition = ['definitions'][0]

    response = 'I don\'t know the definition of ' + word
    if definition:
        response = definition

    rtn = {
        'speech': response,
        'displayText': response,
        'data': {},
        'contextOut': [],
        'source': 'PeterKnowsBest'
    }
    contents = json.dumps(rtn)

    return Response(contents, 200, mimetype='application/json')

###
# The functions below should be applicable to all Flask apps.
###

@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=600'
    return response


@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(debug=True)
