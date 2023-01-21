import flask
import os
import database
import models
import json
from datetime import datetime

#----------------------------------------------------------------------

app = flask.Flask(__name__, template_folder='.')

import auth
app.secret_key = os.getenv('SECRET_KEY')

grades_global = ['fr', 'so', 'jr', 'sr', 'grad']
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
    res = database.get_all_internships()
    major_codes = list(database.majors.keys())
    major_names = list(database.majors.values())
    certificates = list(database.certificates)
    locations = database.get_all_internship_locations()
    html = flask.render_template('templates/jobs.html', 
                netid=netid,
                job_search_res = res,
                major_codes=major_codes,
                major_names=major_names,
                certificates=certificates,
                locations=locations
            )
    response = flask.make_response(html)
    return response

# Jobs main page
@app.route('/jobs/filter', methods=['POST'])
def job_filtered():
    netid = auth.authenticate()
    # Get form data
    data = json.loads(flask.request.form.to_dict()['event_data'])
    filters = [
        data['query'],
        data['difficulty'],
        data['enjoyment'],
        data['classes'],
        data['locationstyle'],
        data['jobtype'],
        data['locations'],
        data['majors'],
        data['certificates'],
        data['fields'],
        data['sortType'],
        data['sortDirection']
    ]
    res = database.get_filtered_internships(filters)
    html = flask.render_template('templates/job_search_results.html', 
                netid = netid,
                job_search_res = res,
            )
    response = flask.make_response(html)
    return response

# Jobs main page
@app.route('/jobs/upvote', methods=['POST'])
def upvote_job():
    netid = auth.authenticate()
    # Get form data
    id = flask.request.args.get('id')
    # Variable to say whether adding or removing
    adding = True
    old_review = database.get_internship(id)
    old_upvotes = old_review.upvotes
    if netid in old_upvotes:
        old_upvotes.remove(netid)
        adding = False
    else:
        old_upvotes.append(netid)
    database.upvote_internship(id, old_upvotes)
    return [str(adding), str(len(old_upvotes))]
#----------------------------------------------------------------------
# Interviews Routes
#----------------------------------------------------------------------
# Interviews main page
@app.route('/interviews', methods=['GET'])
def interviews():
    netid = auth.authenticate()
    res = database.get_all_interviews()
    major_codes = list(database.majors.keys())
    major_names = list(database.majors.values())
    certificates = list(database.certificates)
    html = flask.render_template('templates/interviews.html', 
                netid=netid,
                interview_search_res = res,
                major_codes=major_codes,
                major_names=major_names,
                certificates=certificates
            )
    response = flask.make_response(html)
    return response

@app.route('/interviews/filter', methods=['POST'])
def interview_filtered():
    _ = auth.authenticate()
    # Get form data
    data = json.loads(flask.request.form.to_dict()['event_data'])
    filters = [
        data['query'],
        data['difficulty'],
        data['enjoyment'],
        data['classes'],
        data['locationtypes'],
        data['interviewtypes'],
        data['interviewoutcomes'],
        data['interviewfinals'],
        data['interviewdurations'],
        data['howinterviews'],
        data['majors'],
        data['certificates'],
        data['fields'],
        data['sortType'],
        data['sortDirection']
    ]
    res = database.get_filtered_interviews(filters)
    html = flask.render_template('templates/interview_search_results.html', 
                interview_search_res = res,
            )
    response = flask.make_response(html)
    return response

@app.route('/interviews/upvote', methods=['POST'])
def upvote_interview():
    netid = auth.authenticate()
    # Get form data
    id = flask.request.args.get('id')
    # Variable to say whether adding or removing
    adding = True
    old_review = database.get_interview(id)
    old_upvotes = old_review.upvotes
    if netid in old_upvotes:
        old_upvotes.remove(netid)
        adding = False
    else:
        old_upvotes.append(netid)
    database.upvote_interview(id, old_upvotes)
    return [str(adding), str(len(old_upvotes))]
#----------------------------------------------------------------------
# Companies Routes
#----------------------------------------------------------------------
# Companies main page
@app.route('/companies', methods=['GET'])
def companies():
    netid = auth.authenticate()
    comp = database.get_company_by_name('MITRE')
    html = flask.render_template('templates/companies.html', 
            netid=netid,
            comp=comp)
    response = flask.make_response(html)
    return response
# Companies specific page
@app.route('/companies/<id>', methods=['GET'])
def company_page(id):
    netid = auth.authenticate()
    comp = database.get_company(id)
    comp_interviews, comp_internships = database.get_reviews_by_company(id)
    html = flask.render_template('templates/companies.html', 
            netid=netid,
            comp=comp,
            comp_interviews=comp_interviews,
            comp_internships=comp_internships)
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
    my_interview_upvotes = 0
    my_internship_upvotes = 0
    for interview in interviews:
        my_interview_upvotes += len(interview.upvotes)
    for internship in internships:
        my_internship_upvotes += len(internship.upvotes)
    upvote_interviews, upvote_internships = database.get_upvoted_reviews_by_user(netid)
    major_codes = list(database.majors.keys())
    major_names = list(database.majors.values())
    user_certificates = user.certificates.split(", ")
    company_names = database.get_all_company_names()
    html = flask.render_template('templates/profile.html', 
                netid=netid,
                user=user,
                interviews=interviews,
                internships=internships,
                upvote_interviews=upvote_interviews,
                upvote_internships=upvote_internships,
                major_codes=major_codes,
                major_names=major_names,
                user_certificates=user_certificates,
                company_names=company_names,
                my_internship_upvotes=my_internship_upvotes,
                my_interview_upvotes=my_interview_upvotes
            )
    response = flask.make_response(html)
    return response

# Update profile route
@app.route('/profile/update', methods=['POST'])
def profile_update():
    netid = auth.authenticate()
    # Get form data
    data = json.loads(flask.request.form.to_dict()['event_data'])
    # Update user data
    user = models.Users(
        netid=netid,
        major=data['major'],
        certificates = data['certificates'],
        grade = data['grade']
    )
    database.update_user(user)
    major_codes = list(database.majors.keys())
    major_names = list(database.majors.values())
    user_certificates = user.certificates.split(", ")
    html = flask.render_template('templates/profileform.html', 
                netid=netid,
                user=user,
                major_codes=major_codes,
                major_names=major_names,
                user_certificates=user_certificates
            )
    response = flask.make_response(html)
    return response

# Add Job Review
@app.route('/profile/add/job', methods=['POST'])
def add_job():
    netid = auth.authenticate()
    # Get current user data
    user = database.get_user(netid)
    # Check if user has put in info yet
    if user.grade == "" or user.major == "":
        return "ERROR"
    # Get form data
    data = json.loads(flask.request.form.to_dict()['event_data'])
    # Get current date
    today = datetime.today().strftime('%Y-%m-%d')
    # Calculate whether users enjoyed or found job difficult
    current_enjoyment = 0
    if int(data['enjoyment']) >= 3:
        current_enjoyment = 1
    current_difficulty = 0
    if int(data['difficulty']) >= 3:
        current_difficulty = 1
    # Either update company or add company to database
    company = database.get_company_by_name(data['company'])
    if company is None:
        current_locations = [data['location']]
        current_fields = [data['companyType']]
        current_majors = [user.major]
        current_grades = [0, 0, 0, 0, 0]
        current_grades[grades_global.index(data['year'])] += 1
        new_company = models.Companies(
            name = data['company'],
            num_interviews = 0,
            num_internships = 1,
            interview_difficulty = 0,
            interview_enjoyment = 0,
            internship_supervisor = int(data['supervisor']),
            internship_pay = int(data['pay']),
            internship_balance = int(data['balance']),
            internship_culture = int(data['culture']),
            internship_career = int(data['career']),
            internship_difficulty = int(data['difficulty']),
            internship_enjoyment = int(data['enjoyment']),
            locations=current_locations,
            fields=current_fields,
            majors=current_majors,
            interview_grades = [0, 0, 0, 0, 0],
            internship_grades = current_grades,
            advanced = 0,
            enjoyed_interview = 0,
            enjoyed_internship = current_enjoyment,
            difficult_interview = 0,
            difficult_internship = current_difficulty
        )
        database.add_company(new_company)
    else:
        current_locations = company.locations
        # Update locations
        if data['location'] not in current_locations:
            current_locations.append(data['location'])
        current_fields = company.fields
        # Update fields
        if data['companyType'] not in current_fields:
            current_fields.append(data['companyType'])
        current_majors = company.majors
        # Update majors
        if user.major not in current_majors:
            current_majors.append(user.major)
        current_grades = company.internship_grades
        # Update grades
        current_grades[grades_global.index(data['year'])] += 1
        new_company = models.Companies(
            id = company.id,
            name = data['company'],
            num_interviews = company.num_interviews,
            num_internships = 1 + company.num_internships,
            interview_difficulty = company.interview_difficulty,
            interview_enjoyment = company.interview_enjoyment,
            internship_supervisor = int(data['supervisor']) + company.internship_supervisor,
            internship_pay = int(data['pay']) + company.internship_pay,
            internship_balance = int(data['balance']) + company.internship_balance,
            internship_culture = int(data['culture']) + company.internship_culture,
            internship_career = int(data['career']) + company.internship_career,
            internship_difficulty = int(data['difficulty']) + company.internship_difficulty,
            internship_enjoyment = int(data['enjoyment']) + company.internship_enjoyment,
            locations=current_locations,
            fields=current_fields,
            majors=current_majors,
            interview_grades = company.interview_grades,
            internship_grades = current_grades,
            advanced = company.advanced,
            enjoyed_interview = company.enjoyed_interview,
            enjoyed_internship = company.enjoyed_internship + current_enjoyment,
            difficult_interview = company.difficult_interview,
            difficult_internship = company.difficult_internship + current_difficulty
        )
        database.update_company(new_company)
    # Get company to get company ID
    company = database.get_company_by_name(data['company'])
    # Add new internship review
    # Check data['salary'] to be nonempty
    if data['salary'] == '':
        # Create new internship review to add
        internship = models.Internships(
            netid = netid,
            title = data['title'],
            location = data['location'],
            virtual = data['locationstyle'],
            description = data['description'],
            technologies = data['technologies'],
            type = data['type'],
            length = int(data['length']),
            company = data['company'],
            company_id = company.id,
            company_type = data['companyType'],
            supervisor = int(data['supervisor']),
            pay = int(data['pay']),
            balance = int(data['balance']),
            culture = int(data['culture']),
            career_impact = int(data['career']),
            difficulty = int(data['difficulty']),
            enjoyment = int(data['enjoyment']),
            upvotes = [],
            major = user.major,
            certificates = user.certificates,
            grade = data['year'],
            date_created = today
        )
    # Check data['salary'] to be nonempty
    else:
        # Create new internship review to add
        internship = models.Internships(
            netid = netid,
            title = data['title'],
            location = data['location'],
            virtual = data['locationstyle'],
            description = data['description'],
            technologies = data['technologies'],
            type = data['type'],
            length = int(data['length']),
            company = data['company'],
            company_id = company.id,
            company_type = data['companyType'],
            salary = int(data['salary']),
            supervisor = int(data['supervisor']),
            pay = int(data['pay']),
            balance = int(data['balance']),
            culture = int(data['culture']),
            career_impact = int(data['career']),
            difficulty = int(data['difficulty']),
            enjoyment = int(data['enjoyment']),
            upvotes = [],
            major = user.major,
            certificates = user.certificates,
            grade = data['year'],
            date_created = today
        )
    database.add_internship(internship)
    # Rerender profile reviews template
    interviews, internships = database.get_reviews_by_user(netid)
    html = flask.render_template('templates/profilereviews.html', 
                netid=netid,
                user=user,
                interviews=interviews,
                internships=internships
            )
    response = flask.make_response(html)
    return response

# Add Interview Review
@app.route('/profile/add/interview', methods=['POST'])
def add_interview():
    netid = auth.authenticate()
    # Get current user data
    user = database.get_user(netid)
    # Check if user has put in info yet
    if user.grade == "" or user.major == "":
        return "ERROR"
    # Get form data
    data = json.loads(flask.request.form.to_dict()['event_data'])
    # Change final to boolean
    if data['final'] == 'True':
        data['final'] = True
    else:
        data['final'] = False
    # Change advanced to boolean
    if data['advanced'] == 'True':
        data['advanced'] = True
    else:
        data['advanced'] = False
    # Get current date
    today = datetime.today().strftime('%Y-%m-%d')
    # Calculate whether users enjoyed or found job difficult
    current_enjoyment = 0
    if int(data['enjoyment']) >= 3:
        current_enjoyment = 1
    current_difficulty = 0
    if int(data['difficulty']) >= 3:
        current_difficulty = 1
    # Either update company or add company to database
    company = database.get_company_by_name(data['company'])
    if company is None:
        current_grades = [0, 0, 0, 0, 0]
        current_grades[grades_global.index(data['year'])] += 1
        current_advanced = 0
        if data['advanced']:
            current_advanced = 1
        new_company = models.Companies(
            name = data['company'],
            num_interviews = 1,
            num_internships = 0,
            interview_difficulty = int(data['difficulty']),
            interview_enjoyment = int(data['enjoyment']),
            internship_supervisor = 0,
            internship_pay = 0,
            internship_balance = 0,
            internship_culture = 0,
            internship_career = 0,
            internship_difficulty = 0,
            internship_enjoyment = 0,
            locations=[],
            fields=[],
            majors=[],
            interview_grades = current_grades,
            internship_grades = [0, 0, 0, 0, 0],
            advanced = current_advanced,
            enjoyed_interview = current_enjoyment,
            enjoyed_internship = 0,
            difficult_interview = current_difficulty,
            difficult_internship = 0
        )
        database.add_company(new_company)
    else:
        current_grades = company.interview_grades
        current_grades[grades_global.index(data['year'])] += 1
        current_advanced = company.advanced
        if data['advanced']:
            current_advanced += 1
        new_company = models.Companies(
            id = company.id,
            name = data['company'],
            num_interviews = 1 + company.num_interviews,
            num_internships = company.num_internships,
            interview_difficulty = int(data['difficulty']) + company.interview_difficulty,
            interview_enjoyment = int(data['enjoyment']) + company.interview_enjoyment,
            internship_supervisor = company.internship_supervisor,
            internship_pay = company.internship_pay,
            internship_balance = company.internship_balance,
            internship_culture = company.internship_culture,
            internship_career = company.internship_career,
            internship_difficulty = company.internship_difficulty,
            internship_enjoyment = company.internship_enjoyment,
            locations = company.locations,
            fields = company.fields,
            majors= company.majors,
            interview_grades = current_grades,
            internship_grades = company.internship_grades,
            advanced = current_advanced,
            enjoyed_interview = company.enjoyed_interview + current_enjoyment,
            enjoyed_internship = company.enjoyed_internship,
            difficult_interview = company.difficult_interview + current_difficulty,
            difficult_internship = company.difficult_internship
        )
        database.update_company(new_company)
    # Get company to get company ID
    company = database.get_company_by_name(data['company'])
    # Create new interview review to add
    interview = models.Interviews(
        netid = netid,
        round = int(data['round']),
        final_round = data['final'],
        job_position = data['job_position'],
        job_field = data['job_type'],
        type=data['type'],
        location_type=data['location'],
        duration = data['duration'],
        company = data['company'],
        company_id = company.id,
        num_interviewers = data['num'],
        question_description = data['questions'],
        technologies = data['technologies'],
        how_interview = data['how'],
        tips = data['tips'],
        difficulty = int(data['difficulty']),
        enjoyment = int(data['enjoyment']),
        advanced = data['advanced'],
        upvotes = [],
        major = user.major,
        certificates = user.certificates,
        grade = data['year'],
        date_created = today
    )
    database.add_interview(interview)
    # Rerender profile reviews template
    interviews, internships = database.get_reviews_by_user(netid)
    html = flask.render_template('templates/profilereviews.html', 
                netid=netid,
                interviews=interviews,
                internships=internships
            )
    response = flask.make_response(html)
    return response

# Delete job review
@app.route('/profile/delete/job', methods=['POST'])
def delete_job():
    netid = auth.authenticate()
    # Get job id for review to delete
    id = flask.request.args.get('id')
    # Get job review
    internship = database.get_internship(id)
    # Make sure current user is one deleting internship
    if internship.netid != netid:
        return "YOU ARE NOT THE WRITER OF THIS REVIEW!"
    # Get company for job
    company = database.get_company_by_name(internship.company)
    new_internship_grades = company.internship_grades
    new_internship_grades[grades_global.index(internship.grade)] -= 1
    new_enjoyment = 0
    if internship.enjoyment >= 3:
        new_enjoyment = 1
    new_difficulty = 0
    if internship.difficulty >= 3:
        new_difficulty = 1
    # Update company
    new_company = models.Companies(
        id = company.id,
        name = company.name,
        num_interviews = company.num_interviews,
        num_internships = max(company.num_internships - 1, 0),
        interview_difficulty = company.interview_difficulty,
        interview_enjoyment = company.interview_enjoyment,
        internship_supervisor = max(company.internship_supervisor - internship.supervisor, 0),
        internship_pay = max(company.internship_pay - internship.pay, 0),
        internship_balance = max(company.internship_balance - internship.balance, 0),
        internship_culture = max(company.internship_culture - internship.culture, 0),
        internship_career = max(company.internship_career - internship.career_impact, 0),
        internship_difficulty = max(company.internship_difficulty - internship.difficulty, 0),
        internship_enjoyment = max(company.internship_enjoyment - internship.enjoyment, 0),
        locations = company.locations,
        fields = company.fields,
        majors = company.majors,
        interview_grades = company.interview_grades,
        internship_grades = new_internship_grades,
        advanced = company.advanced,
        enjoyed_interview = company.enjoyed_interview,
        enjoyed_internship = max(company.enjoyed_internship - new_enjoyment, 0),
        difficult_interview = company.difficult_interview,
        difficult_internship = max(company.difficult_internship - new_difficulty, 0)
    )
    database.update_company(new_company)
    # Delete job review
    database.delete_internship(id)
    # Rerender profile reviews template
    interviews, internships = database.get_reviews_by_user(netid)
    html = flask.render_template('templates/profilereviews.html', 
                netid=netid,
                interviews=interviews,
                internships=internships
            )
    response = flask.make_response(html)
    return response

# Delete interview review
@app.route('/profile/delete/interview', methods=['POST'])
def delete_interview():
    netid = auth.authenticate()
    # Get interview id for review to delete
    id = flask.request.args.get('id')
    # Get interview review
    interview = database.get_interview(id)
    # Make sure current user is one deleting internship
    if interview.netid != netid:
        return "YOU ARE NOT THE WRITER OF THIS REVIEW!"
    # Get company for job
    company = database.get_company_by_name(interview.company)
    new_interview_grades = company.interview_grades
    new_interview_grades[grades_global.index(interview.grade)] -= 1
    advanced_count = company.advanced
    if interview.advanced:
        advanced_count -= 1
    new_enjoyment = 0
    if interview.enjoyment >= 3:
        new_enjoyment = 1
    new_difficulty = 0
    if interview.difficulty >= 3:
        new_difficulty = 1
    # Update company
    new_company = models.Companies(
        id = company.id,
        name = company.name,
        num_interviews = max(company.num_interviews - 1, 0),
        num_internships = company.num_internships,
        interview_difficulty = max(company.interview_difficulty - interview.difficulty, 0),
        interview_enjoyment = max(company.interview_enjoyment - interview.enjoyment, 0),
        internship_supervisor = company.internship_supervisor,
        internship_pay = company.internship_pay,
        internship_balance = company.internship_balance,
        internship_culture = company.internship_culture,
        internship_career = company.internship_career,
        internship_difficulty = company.internship_difficulty,
        internship_enjoyment = company.internship_enjoyment,
        locations = company.locations,
        fields = company.fields,
        majors = company.majors,
        interview_grades = new_interview_grades,
        internship_grades = company.internship_grades,
        advanced = advanced_count,
        enjoyed_interview = max(company.enjoyed_interview - new_enjoyment, 0),
        enjoyed_internship = company.enjoyed_internship,
        difficult_interview = max(company.difficult_interview - new_difficulty, 0),
        difficult_internship = company.difficult_internship
    )
    database.update_company(new_company)
    # Delete interview review
    database.delete_interview(id)
    # Rerender profile reviews template
    interviews, internships = database.get_reviews_by_user(netid)
    html = flask.render_template('templates/profilereviews.html', 
                netid=netid,
                interviews=interviews,
                internships=internships
            )
    response = flask.make_response(html)
    return response

# Remove job upvote on profile page
# Jobs main page
@app.route('/profile/jobs/upvote', methods=['POST'])
def upvote_job_profile():
    netid = auth.authenticate()
    # Get form data
    id = flask.request.args.get('id')
    old_review = database.get_internship(id)
    old_upvotes = old_review.upvotes
    if netid in old_upvotes:
        old_upvotes.remove(netid)
    database.upvote_internship(id, old_upvotes)
    upvote_interviews, upvote_internships = database.get_upvoted_reviews_by_user(netid)
    html = flask.render_template('templates/profileupvoted.html', 
                netid=netid,
                upvote_interviews=upvote_interviews,
                upvote_internships=upvote_internships,
            )
    response = flask.make_response(html)
    return response

# Remove interview upvote on profile page
# Jobs main page
@app.route('/profile/interviews/upvote', methods=['POST'])
def upvote_interview_profile():
    netid = auth.authenticate()
    # Get form data
    id = flask.request.args.get('id')
    old_review = database.get_interview(id)
    old_upvotes = old_review.upvotes
    if netid in old_upvotes:
        old_upvotes.remove(netid)
    database.upvote_interview(id, old_upvotes)
    upvote_interviews, upvote_internships = database.get_upvoted_reviews_by_user(netid)
    html = flask.render_template('templates/profileupvoted.html', 
                netid=netid,
                upvote_interviews=upvote_interviews,
                upvote_internships=upvote_internships,
            )
    response = flask.make_response(html)
    return response