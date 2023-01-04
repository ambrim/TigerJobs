import flask
import os
import database
import models
import json

#----------------------------------------------------------------------

app = flask.Flask(__name__, template_folder='.')

import auth
app.secret_key = os.getenv('SECRET_KEY')

#----------------------------------------------------------------------
# General Routes
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
    return flask.redirect("/jobs")
#----------------------------------------------------------------------
# Jobs Routes
#----------------------------------------------------------------------
# Jobs main page
@app.route('/jobs', methods=['GET'])
def jobs():
    netid = auth.authenticate()
    html = flask.render_template('templates/jobs.html', netid=netid)
    response = flask.make_response(html)
    return response
#----------------------------------------------------------------------
# Interviews Routes
#----------------------------------------------------------------------
# Interviews main page
@app.route('/interviews', methods=['GET'])
def interviews():
    netid = auth.authenticate()
    html = flask.render_template('templates/interviews.html', netid=netid)
    response = flask.make_response(html)
    return response
#----------------------------------------------------------------------
# Companies Routes
#----------------------------------------------------------------------
# Companies main page
@app.route('/companies', methods=['GET'])
def companies():
    netid = auth.authenticate()
    html = flask.render_template('templates/companies.html', netid=netid)
    response = flask.make_response(html)
    return response
#----------------------------------------------------------------------
# Profile Routes
#----------------------------------------------------------------------
# Profile main page
@app.route('/profile', methods=['GET'])
def profile():
    netid = auth.authenticate()
    user = database.get_user(netid)
    interviews, internships = database.get_reviews_by_user(netid)
    html = flask.render_template('templates/profile.html', 
                netid=netid,
                user=user,
                interviews=interviews,
                internships=internships
            )
    response = flask.make_response(html)
    return response

# Update profile route
@app.route('/profile/update', methods=['POST'])
def profile_update():
    netid = auth.authenticate()
    # Get form data
    data = json.loads(flask.request.form.to_dict()['event_data'])
    # Get old user data
    old_user = database.get_user(netid)
    user = models.Users(
        netid=netid,
        major=data['major'],
        certificates = data['certificates'],
        grade = data['grade'],
        interview_upvotes = old_user.interview_upvotes,
        internship_upvotes = old_user.internship_upvotes
    )
    database.update_user(user)
    html = flask.render_template('templates/profileform.html', 
                netid=netid,
                user=user
            )
    response = flask.make_response(html)
    return response


