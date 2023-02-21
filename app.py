import flask
import os
import database
import models
import json
from datetime import datetime
import re

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
    query_words = re.split(r' |,|;', data['query'])
    filters = [
        query_words,
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
    query_words = re.split(r' |,|;', data['query'])
    print(query_words)
    filters = [
        query_words,
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
    major_codes = list(database.majors.keys())
    major_names = list(database.majors.values())
    res = database.get_all_companies()
    top = database.get_top_companies('')
    html = flask.render_template('templates/companieshome.html', 
            netid=netid,
            company_top_res=top,
            company_search_res=res,
            major_codes=major_codes,
            major_names=major_names)
    response = flask.make_response(html)
    return response
# Get top companies
@app.route('/companies/top', methods=['POST'])
def top_companies():
    _ = auth.authenticate()
    major = flask.request.args.get('major')
    top = database.get_top_companies(major)
    html = flask.render_template('templates/companies_top_results.html', 
            company_top_res=top)
    response = flask.make_response(html)
    return response
# Get companies by search
@app.route('/companies/search', methods=['POST'])
def search_companies():
    _ = auth.authenticate()
    query = flask.request.args.get('query')
    res = database.get_search_companies(query)
    html = flask.render_template('templates/companies_search_results.html', 
            company_search_res=res)
    response = flask.make_response(html)
    return response
# Companies specific page
@app.route('/companies/<id>', methods=['GET'])
def company_page(id):
    netid = auth.authenticate()
    comp = database.get_company(id)
    comp_interviews, comp_internships = database.get_reviews_by_company(id)
    # Sort locations, fields, and majors
    zip_locations = zip(comp.location_count, comp.locations)
    locations = [x for _, x in sorted(zip_locations, reverse=True)]
    zip_fields = zip(comp.field_count, comp.fields)
    fields = [x for _, x in sorted(zip_fields, reverse=True)]
    zip_majors = zip(comp.major_count, comp.majors)
    majors = [x for _, x in sorted(zip_majors, reverse=True)]
    html = flask.render_template('templates/company.html', 
            netid=netid,
            comp=comp,
            locations=locations,
            fields=fields,
            majors=majors,
            comp_interviews=comp_interviews,
            comp_internships=comp_internships)
    response = flask.make_response(html)
    return response
#----------------------------------------------------------------------
# About Routes
#----------------------------------------------------------------------
# About page
@app.route('/about', methods=['GET'])
def about():
    netid = auth.authenticate()
    comp = database.get_company_by_name('MITRE')
    res = database.get_all_companies() ######## PLACEHOLDER ########
    top = database.get_top_companies('') ######## PLACEHOLDER ########
    html = flask.render_template('templates/about.html', 
            netid=netid,
            comp=comp,
            company_top_res=top,
            company_search_res=res)
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
            location_count=[1],
            fields=current_fields,
            field_count=[1],
            majors=current_majors,
            major_count=[1],
            interview_grades = [0, 0, 0, 0, 0],
            internship_grades = current_grades,
            advanced = 0,
            enjoyed_interview = 0,
            enjoyed_internship = current_enjoyment,
            difficult_interview = 0,
            difficult_internship = current_difficulty,
            reported = False
        )
        database.add_company(new_company)
    else:
        current_locations = company.locations
        current_location_count = company.location_count
        # Update locations and location count
        if data['location'].upper() not in (location.upper() for location in current_locations):
            current_locations.append(data['location'])
            current_location_count.append(1)
        else:
            new_locations = [location.upper() for location in current_locations]
            location_index = new_locations.index(data['location'].upper())
            current_location_count[location_index] += 1
        current_fields = company.fields
        current_field_count = company.field_count
        # Update fields and fields count
        if data['companyType'] not in current_fields:
            current_fields.append(data['companyType'])
            current_field_count.append(1)
        else:
            field_index = current_fields.index(data['companyType'])
            current_field_count[field_index] += 1
        current_majors = company.majors
        current_major_count = company.major_count
        # Update majors and major count
        if user.major not in current_majors:
            current_majors.append(user.major)
            current_major_count.append(1)
        else:
            major_index = current_majors.index(user.major)
            current_major_count[major_index] += 1
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
            location_count=current_location_count,
            fields=current_fields,
            field_count=current_field_count,
            majors=current_majors,
            major_count=current_major_count,
            interview_grades = company.interview_grades,
            internship_grades = current_grades,
            advanced = company.advanced,
            enjoyed_interview = company.enjoyed_interview,
            enjoyed_internship = company.enjoyed_internship + current_enjoyment,
            difficult_interview = company.difficult_interview,
            difficult_internship = company.difficult_internship + current_difficulty,
            reported = company.reported
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
            date_created = today,
            reported = False
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
            date_created = today,
            reported = False
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
        current_fields = [data['companyType']]
        current_majors = [user.major]
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
            location_count=[],
            fields=current_fields,
            field_count=[1],
            majors=current_majors,
            major_count=[1],
            interview_grades = current_grades,
            internship_grades = [0, 0, 0, 0, 0],
            advanced = current_advanced,
            enjoyed_interview = current_enjoyment,
            enjoyed_internship = 0,
            difficult_interview = current_difficulty,
            difficult_internship = 0,
            reported = False
        )
        database.add_company(new_company)
    else:
        # Update fields and fields count
        current_fields = company.fields
        current_field_count = company.field_count
        if data['job_type'] not in current_fields:
            current_fields.append(data['job_type'])
            current_field_count.append(1)
        else:
            field_index = current_fields.index(data['job_type'])
            current_field_count[field_index] += 1
        # Update majors and major count
        current_majors = company.majors
        current_major_count = company.major_count
        if user.major not in current_majors:
            current_majors.append(user.major)
            current_major_count.append(1)
        else:
            major_index = current_majors.index(user.major)
            current_major_count[major_index] += 1
        # Update grades
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
            location_count = company.location_count,
            fields=current_fields,
            field_count=current_field_count,
            majors=current_majors,
            major_count=current_major_count,
            interview_grades = current_grades,
            internship_grades = company.internship_grades,
            advanced = current_advanced,
            enjoyed_interview = company.enjoyed_interview + current_enjoyment,
            enjoyed_internship = company.enjoyed_internship,
            difficult_interview = company.difficult_interview + current_difficulty,
            difficult_internship = company.difficult_internship,
            reported = company.reported
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
        date_created = today,
        reported = False
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
    # Delete location if present
    new_location_count = company.location_count
    updated_locations = company.locations
    new_locations = [location.lower() for location in company.locations]
    location_index = new_locations.index(internship.location.lower())
    new_location_count[location_index] = company.location_count[location_index] - 1
    # Remove location if less than or equal to 0
    if new_location_count[location_index] <= 0:
        updated_locations.pop(location_index)
        new_location_count.pop(location_index)
    # Delete field if present
    new_field_count = company.field_count
    updated_fields = company.fields
    field_index = company.fields.index(internship.company_type)
    new_field_count[field_index] = company.field_count[field_index] - 1
    # Remove field if less than or equal to 0
    if new_field_count[field_index] <= 0:
        updated_fields.pop(field_index)
        new_field_count.pop(field_index)
    # Delete major if present
    new_major_count = company.major_count
    updated_majors = company.majors
    major_index = company.majors.index(internship.major)
    new_major_count[major_index] = max(company.major_count[major_index] - 1, 0)
    # Remove major if less than or equal to 0
    if new_major_count[major_index] <= 0:
        updated_majors.pop(major_index)
        new_major_count.pop(major_index)
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
        locations = updated_locations,
        location_count = new_location_count,
        fields = updated_fields,
        field_count = new_field_count,
        majors = updated_majors,
        major_count=new_major_count,
        interview_grades = company.interview_grades,
        internship_grades = new_internship_grades,
        advanced = company.advanced,
        enjoyed_interview = company.enjoyed_interview,
        enjoyed_internship = max(company.enjoyed_internship - new_enjoyment, 0),
        difficult_interview = company.difficult_interview,
        difficult_internship = max(company.difficult_internship - new_difficulty, 0),
        reported = company.reported
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
    # Delete field if present
    new_field_count = company.field_count
    updated_fields = company.fields
    field_index = company.fields.index(interview.job_field)
    new_field_count[field_index] = company.field_count[field_index] - 1
    # Remove field if less than or equal to 0
    if new_field_count[field_index] <= 0:
        updated_fields.pop(field_index)
        new_field_count.pop(field_index)
    # Delete major if present
    new_major_count = company.major_count
    updated_majors = company.majors
    major_index = company.majors.index(interview.major)
    new_major_count[major_index] = max(company.major_count[major_index] - 1, 0)
    # Remove major if less than or equal to 0
    if new_major_count[major_index] <= 0:
        updated_majors.pop(major_index)
        new_major_count.pop(major_index)
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
        location_count = company.location_count,
        fields = updated_fields,
        field_count = new_field_count,
        majors = updated_majors,
        major_count=new_major_count,
        interview_grades = new_interview_grades,
        internship_grades = company.internship_grades,
        advanced = advanced_count,
        enjoyed_interview = max(company.enjoyed_interview - new_enjoyment, 0),
        enjoyed_internship = company.enjoyed_internship,
        difficult_interview = max(company.difficult_interview - new_difficulty, 0),
        difficult_internship = company.difficult_internship,
        reported = company.reported
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

# Edit Job Review
@app.route('/profile/edit/job', methods=['POST'])
def edit_job():
    ## Load in data to update company
    netid = auth.authenticate()
    # Get job id for review to update
    id = flask.request.args.get('id')
    # Get job review
    internship = database.get_internship(id)
    # Keep track of reported status
    reported = internship.reported
    # Make sure current user is one deleting internship
    if internship.netid != netid:
        return "YOU ARE NOT THE WRITER OF THIS REVIEW!"
    # Get company for job
    company = database.get_company_by_name(internship.company)
    # Get current user data
    user = database.get_user(netid)
    # Check if user has put in info yet
    if user.grade == "" or user.major == "":
        return "ERROR"
    # Get form data
    data = json.loads(flask.request.form.to_dict()['event_data'])
    # Get current date
    today = datetime.today().strftime('%Y-%m-%d')

    ## Update internship grade list
    # First remove internship grade from before
    new_internship_grades = company.internship_grades
    new_internship_grades[grades_global.index(internship.grade)] -= 1
    # Then update grades to new grades
    new_internship_grades[grades_global.index(data['year'])] += 1

    ## Update locations of company
    # Delete location if present
    new_location_count = company.location_count
    updated_locations = company.locations
    new_locations = [location.lower() for location in company.locations]
    location_index = new_locations.index(internship.location.lower())
    new_location_count[location_index] = company.location_count[location_index] - 1
    if new_location_count[location_index] <= 0:
        updated_locations.pop(location_index)
        new_location_count.pop(location_index)
    # Now update location list
    if data['location'].upper() not in (location.upper() for location in updated_locations):
        updated_locations.append(data['location'])
        new_location_count.append(1)
    else:
        updated_locations = [location.upper() for location in updated_locations]
        location_index = updated_locations.index(data['location'].upper())
        new_location_count[location_index] += 1
    
    ## Update fields of company
    # Delete field if present
    new_field_count = company.field_count
    updated_fields = company.fields
    field_index = company.fields.index(internship.company_type)
    new_field_count[field_index] = company.field_count[field_index] - 1
    # Remove field if less than or equal to 0
    if new_field_count[field_index] <= 0:
        updated_fields.pop(field_index)
        new_field_count.pop(field_index)
    # Update fields and fields count
    if data['companyType'] not in updated_fields:
        updated_fields.append(data['companyType'])
        new_field_count.append(1)
    else:
        field_index = updated_fields.index(data['companyType'])
        new_field_count[field_index] += 1
    
    ## Update majors of company
    # Delete major if present
    new_major_count = company.major_count
    updated_majors = company.majors
    major_index = company.majors.index(internship.major)
    new_major_count[major_index] = max(company.major_count[major_index] - 1, 0)
    # Remove major if less than or equal to 0
    if new_major_count[major_index] <= 0:
        updated_majors.pop(major_index)
        new_major_count.pop(major_index)
    # Update majors and major count
    if user.major not in updated_majors:
        updated_majors.append(user.major)
        new_major_count.append(1)
    else:
        major_index = updated_majors.index(user.major)
        new_major_count[major_index] += 1

    ## Update enjoyment and difficulty
    new_enjoyment = 0
    if internship.enjoyment >= 3:
        new_enjoyment = 1
    new_difficulty = 0
    if internship.difficulty >= 3:
        new_difficulty = 1
    current_enjoyment = 0
    if int(data['enjoyment']) >= 3:
        current_enjoyment = 1
    current_difficulty = 0
    if int(data['difficulty']) >= 3:
        current_difficulty = 1

    ## Update company
    new_company = models.Companies(
        id = company.id,
        name = company.name,
        num_interviews = company.num_interviews,
        num_internships = company.num_internships,
        interview_difficulty = company.interview_difficulty,
        interview_enjoyment = company.interview_enjoyment,
        internship_supervisor = max(company.internship_supervisor - internship.supervisor + int(data['supervisor']) , 0),
        internship_pay = max(company.internship_pay - internship.pay + int(data['pay']), 0),
        internship_balance = max(company.internship_balance - internship.balance + int(data['balance']), 0),
        internship_culture = max(company.internship_culture - internship.culture + int(data['culture']), 0),
        internship_career = max(company.internship_career - internship.career_impact + int(data['career']), 0),
        internship_difficulty = max(company.internship_difficulty - internship.difficulty + int(data['difficulty']), 0),
        internship_enjoyment = max(company.internship_enjoyment - internship.enjoyment + int(data['enjoyment']), 0),
        locations = updated_locations,
        location_count = new_location_count,
        fields = updated_fields,
        field_count = new_field_count,
        majors = updated_majors,
        major_count=new_major_count,
        interview_grades = company.interview_grades,
        internship_grades = new_internship_grades,
        advanced = company.advanced,
        enjoyed_interview = company.enjoyed_interview,
        enjoyed_internship = max(company.enjoyed_internship - new_enjoyment + current_enjoyment, 0),
        difficult_interview = company.difficult_interview,
        difficult_internship = max(company.difficult_internship - new_difficulty + current_difficulty, 0),
        reported = company.reported
    )
    database.update_company(new_company)
    ## Edit internship
    # Check data['salary'] to be nonempty
    if data['salary'] == '':
        # Create new internship review to add
        internship = models.Internships(
            id = id,
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
            date_created = today,
            reported = reported
        )
    # Check data['salary'] to be nonempty
    else:
        # Create new internship review to add
        internship = models.Internships(
            id = id,
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
            date_created = today,
            reported = reported
        )
    database.update_internship(internship)
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

# Edit Interview Review
@app.route('/profile/edit/interview', methods=['POST'])
def edit_interview():
    # Get all data from form and other
    netid = auth.authenticate()
    # Get interview id for review to delete
    id = flask.request.args.get('id')
    # Get interview review
    interview = database.get_interview(id)
    # Keep track of reported status
    reported = interview.reported
    # Make sure current user is one deleting internship
    if interview.netid != netid:
        return "YOU ARE NOT THE WRITER OF THIS REVIEW!"
    # Get company for interview
    company = database.get_company_by_name(interview.company)
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

    # Interview Grades 
    new_interview_grades = company.interview_grades
    new_interview_grades[grades_global.index(interview.grade)] -= 1
    new_interview_grades[grades_global.index(data['year'])] += 1

    ## Update fields of company
    # Delete field if present
    new_field_count = company.field_count
    updated_fields = company.fields
    field_index = company.fields.index(interview.job_field)
    new_field_count[field_index] = company.field_count[field_index] - 1
    # Remove field if less than or equal to 0
    if new_field_count[field_index] <= 0:
        updated_fields.pop(field_index)
        new_field_count.pop(field_index)
    # Update fields and fields count
    if data['job_type'] not in updated_fields:
        updated_fields.append(data['job_type'])
        new_field_count.append(1)
    else:
        field_index = updated_fields.index(data['job_type'])
        new_field_count[field_index] += 1
    
    ## Update majors of company
    # Delete major if present
    new_major_count = company.major_count
    updated_majors = company.majors
    major_index = company.majors.index(interview.major)
    new_major_count[major_index] = max(company.major_count[major_index] - 1, 0)
    # Remove major if less than or equal to 0
    if new_major_count[major_index] <= 0:
        updated_majors.pop(major_index)
        new_major_count.pop(major_index)
    # Update majors and major count
    if user.major not in updated_majors:
        updated_majors.append(user.major)
        new_major_count.append(1)
    else:
        major_index = updated_majors.index(user.major)
        new_major_count[major_index] += 1

    # Interview advanced count
    advanced_count = company.advanced
    if interview.advanced:
        advanced_count -= 1
    if data['advanced']:
        advanced_count += 1

    # Interview enjoyment
    new_enjoyment = 0
    if interview.enjoyment >= 3:
        new_enjoyment = 1
    current_enjoyment = 0
    if int(data['enjoyment']) >= 3:
        current_enjoyment = 1
    
    # Interview difficulty
    new_difficulty = 0
    if interview.difficulty >= 3:
        new_difficulty = 1
    current_difficulty = 0
    if int(data['difficulty']) >= 3:
        current_difficulty = 1
    
    # Update company
    new_company = models.Companies(
        id = company.id,
        name = company.name,
        num_interviews = company.num_interviews,
        num_internships = company.num_internships,
        interview_difficulty = max(company.interview_difficulty - interview.difficulty + int(data['difficulty']), 0),
        interview_enjoyment = max(company.interview_enjoyment - interview.enjoyment + int(data['enjoyment']), 0),
        internship_supervisor = company.internship_supervisor,
        internship_pay = company.internship_pay,
        internship_balance = company.internship_balance,
        internship_culture = company.internship_culture,
        internship_career = company.internship_career,
        internship_difficulty = company.internship_difficulty,
        internship_enjoyment = company.internship_enjoyment,
        locations = company.locations,
        location_count = company.location_count,
        fields = updated_fields,
        field_count = new_field_count,
        majors = updated_majors,
        major_count=new_major_count,
        interview_grades = new_interview_grades,
        internship_grades = company.internship_grades,
        advanced = advanced_count,
        enjoyed_interview = max(company.enjoyed_interview - new_enjoyment + current_enjoyment, 0),
        enjoyed_internship = company.enjoyed_internship,
        difficult_interview = max(company.difficult_interview - new_difficulty + current_difficulty, 0),
        difficult_internship = company.difficult_internship,
        reported = company.reported
    )
    database.update_company(new_company)
    company = database.get_company_by_name(data['company'])

    # Update interview review
    interview = models.Interviews(
        id = id,
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
        date_created = today,
        reported = reported
    )
    database.update_interview(interview)
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

# Edit jobs main page
@app.route('/profile/jobs/get', methods=['GET'])
def get_job():
    netid = auth.authenticate()
    # Get form data
    id = flask.request.args.get('id')
    job = database.get_internship(id)
    html = flask.render_template('templates/profileeditjobform.html', 
                netid=netid,
                job=job
            )
    response = flask.make_response(html)
    return response

# Edit interview page
@app.route('/profile/interviews/get', methods=['GET'])
def get_interviews():
    netid = auth.authenticate()
    # Get form data
    id = flask.request.args.get('id')
    interview = database.get_interview(id)
    html = flask.render_template('templates/profileeditinterviewform.html', 
                netid=netid,
                interview=interview
            )
    response = flask.make_response(html)
    return response
#----------------------------------------------------------------------
# Admin Routes
#----------------------------------------------------------------------
# Admin main page
@app.route('/admin', methods=['GET'])
def admin():
    netid = auth.authenticate()
    internships, interviews, companies = database.get_reported()
    html = flask.render_template('templates/admin.html', 
                netid=netid,
                internships=internships,
                interviews=interviews,
                companies=companies
            )
    response = flask.make_response(html)
    return response
# Report routes
# Report interview page
@app.route('/report/interviews', methods=['POST'])
def report_interview():
    _ = auth.authenticate()
    # Get form data
    id = flask.request.args.get('id')
    database.report_interview(id, True)
    return "SUCCESS"

# Report internship page
@app.route('/report/internships', methods=['POST'])
def report_internship():
    _ = auth.authenticate()
    # Get form data
    id = flask.request.args.get('id')
    database.report_internship(id, True)
    return "SUCCESS"

# Report internship page
@app.route('/report/companies', methods=['POST'])
def report_company():
    _ = auth.authenticate()
    # Get form data
    id = flask.request.args.get('id')
    database.report_company(id, True)
    return "SUCCESS"

# Dismiss report routes
# Report interview page
@app.route('/dismiss/interviews', methods=['POST'])
def dismiss_interview():
    netid = auth.authenticate()
    # Get form data
    id = flask.request.args.get('id')
    database.report_interview(id, False)
    _, interviews, _ = database.get_reported()
    html = flask.render_template('templates/admin_interviews.html', 
                netid=netid,            
                interviews=interviews
            )
    response = flask.make_response(html)
    return response

# Report internship page
@app.route('/dismiss/internships', methods=['POST'])
def dismiss_internship():
    netid = auth.authenticate()
    # Get form data
    id = flask.request.args.get('id')
    database.report_internship(id, False)
    internships, _, _ = database.get_reported()
    html = flask.render_template('templates/admin_jobs.html', 
                netid=netid,
                internships=internships
            )
    response = flask.make_response(html)
    return response

# Report internship page
@app.route('/dismiss/companies', methods=['POST'])
def dismiss_company():
    netid = auth.authenticate()
    # Get form data
    id = flask.request.args.get('id')
    database.report_company(id, False)
    _, _, companies = database.get_reported()
    html = flask.render_template('templates/admin_companies.html', 
                netid=netid,
                companies=companies
            )
    response = flask.make_response(html)
    return response
