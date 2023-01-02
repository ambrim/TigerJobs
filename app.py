import flask
import os
import database
import models

#----------------------------------------------------------------------

app = flask.Flask(__name__, template_folder='.')

import auth
app.secret_key = os.getenv('SECRET_KEY')

#----------------------------------------------------------------------

# Landing page
@app.route('/', methods=['GET'])
@app.route('/index', methods=['GET'])
def index():
    html = flask.render_template('templates/landing.html')
    response = flask.make_response(html)
    return response

# CAS Login
@app.route('/login', methods=['GET'])
def netID():
    _ = auth.authenticate()
    # if netid is None:
    #     return flask.redirect('/error')
    # coop = flask.session.get('coop')
    return flask.redirect("/internships")

# Internships Page
@app.route('/internships', methods=['GET'])
def internships():
    netid = auth.authenticate()
    html = flask.render_template('templates/test.html', netid=netid)
    response = flask.make_response(html)
    return response
