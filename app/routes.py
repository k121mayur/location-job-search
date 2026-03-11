import os
import math
from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from models import db, Job, Employee
from datetime import datetime

main = Blueprint('main', __name__)

# Haversine formula for distance calculation
def haversine(lat1, lon1, lat2, lon2):
    R = 6371  # Earth radius in kilometers
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat/2) * math.sin(dlat/2) + math.cos(math.radians(lat1)) \
        * math.cos(math.radians(lat2)) * math.sin(dlon/2) * math.sin(dlon/2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    return R * c

@main.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        emp_email = os.environ.get('EMPLOYER_EMAIL')
        emp_pass = os.environ.get('EMPLOYER_PASSWORD')
        employee_email = os.environ.get('EMPLOYEE_EMAIL')
        employee_pass = os.environ.get('EMPLOYEE_PASSWORD')
        
        if email == emp_email and password == emp_pass:
            session['user_type'] = 'employer'
            return redirect(url_for('main.employer_dashboard'))
        elif email == employee_email and password == employee_pass:
            session['user_type'] = 'employee'
            # Initialize employee in DB if not exists
            employee = Employee.query.filter_by(email=email).first()
            if not employee:
                employee = Employee(email=email)
                db.session.add(employee)
                db.session.commit()
            return redirect(url_for('main.employee_dashboard'))
        else:
            flash('Invalid credentials')
            return redirect(url_for('main.login'))
            
    return render_template('login.html')

@main.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('main.login'))

@main.route('/employer')
def employer_dashboard():
    if session.get('user_type') != 'employer':
        return redirect(url_for('main.login'))
    return render_template('employer_dashboard.html')

@main.route('/create-job', methods=['GET', 'POST'])
def create_job():
    if session.get('user_type') != 'employer':
        return redirect(url_for('main.login'))
        
    if request.method == 'POST':
        title = request.form.get('title')
        short_description = request.form.get('short_description')
        description = request.form.get('description')
        lat = request.form.get('latitude')
        lng = request.form.get('longitude')
        
        if not title or not description or not lat or not lng:
            flash('Please fill in all required fields and select a location.')
            return redirect(url_for('main.create_job'))
            
        job = Job(
            title=title,
            short_description=short_description,
            description=description,
            latitude=float(lat),
            longitude=float(lng)
        )
        db.session.add(job)
        db.session.commit()
        flash('Job posted successfully!')
        return redirect(url_for('main.employer_dashboard'))
        
    return render_template('job_form.html')

@main.route('/employee')
def employee_dashboard():
    if session.get('user_type') != 'employee':
        return redirect(url_for('main.login'))
        
    employee_email = os.environ.get('EMPLOYEE_EMAIL')
    employee = Employee.query.filter_by(email=employee_email).first()
    
    if not employee.home_latitude or not employee.home_longitude:
        return redirect(url_for('main.set_home'))
        
    return render_template('employee_dashboard.html', employee=employee)

@main.route('/set-home', methods=['GET', 'POST'])
def set_home():
    if session.get('user_type') != 'employee':
        return redirect(url_for('main.login'))
        
    employee_email = os.environ.get('EMPLOYEE_EMAIL')
    employee = Employee.query.filter_by(email=employee_email).first()
        
    if request.method == 'POST':
        lat = request.form.get('latitude')
        lng = request.form.get('longitude')
        if lat and lng:
            employee.home_latitude = float(lat)
            employee.home_longitude = float(lng)
            db.session.commit()
            flash('Home location saved!')
            return redirect(url_for('main.employee_dashboard'))
        else:
            flash('Please select a location on the map.')
            return redirect(url_for('main.set_home'))
            
    return render_template('map_picker.html')

@main.route('/search-jobs', methods=['GET'])
def search_jobs():
    if session.get('user_type') != 'employee':
        return redirect(url_for('main.login'))
        
    employee_email = os.environ.get('EMPLOYEE_EMAIL')
    employee = Employee.query.filter_by(email=employee_email).first()
    
    if not employee.home_latitude or not employee.home_longitude:
        return redirect(url_for('main.set_home'))
        
    query = request.args.get('q', '').lower().strip()
    
    all_jobs = Job.query.all()
    nearby_jobs = []
    
    search_nearby_keyword = 'search jobs near me'
    
    for job in all_jobs:
        # If there's a search term and it's not the generic option 2 term, filter by title
        if query and query != search_nearby_keyword:
            if query not in job.title.lower():
                continue
                
        dist = haversine(employee.home_latitude, employee.home_longitude, job.latitude, job.longitude)
        if dist <= 3.0:
            job.distance = round(dist, 2)
            nearby_jobs.append(job)
            
    # Sort closest first
    nearby_jobs.sort(key=lambda x: x.distance)
            
    return render_template('job_list.html', jobs=nearby_jobs, query=query)
