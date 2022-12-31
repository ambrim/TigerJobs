import flask
import os

#----------------------------------------------------------------------

app = flask.Flask(__name__, template_folder='.')

# Home page
@app.route('/', methods=['GET'])
def index():
    html = flask.render_template('templates/landing.html')
    response = flask.make_response(html)
    return response
