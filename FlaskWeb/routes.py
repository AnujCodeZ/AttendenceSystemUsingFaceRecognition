from flask import render_template, url_for, request, redirect, flash
from FlaskWeb import app
from wtforms.validators import ValidationError
from FlaskWeb.models import User
from FlaskWeb import face
from FlaskWeb import pd
from FlaskWeb import df
from FlaskWeb import db
import os
import cv2
import secrets

@app.route("/")
@app.route("/index")
def index():
	return render_template("index.html",df = df)

@app.route("/Dashboard")
def Dashboard():
	df = pd.read_excel(r'Attendence.xlsx')
	return render_template("Dashboard.html",df = df,title = 'Dashboard')

@app.route("/program")
def program():
	face.Detect()
	df = pd.read_excel(r'Attendence.xlsx')
	return render_template("Dashboard.html",df = df,title = 'Dashboard')

def upload_file(file,name):
    if request.method == 'POST':
        if file.filename == '':
            # flash('No selected file')
            return redirect(request.url)
        if file:
        	f_ext = os.path.splitext(file.filename)
        	f_name = name + f_ext[1]
        	file.save(os.path.join(app.root_path, '../Images', f_name))
        	return f_name

@app.route("/register", methods=['GET','POST'])
def register():
	first_name = request.form.get('first_name')
	last_name = request.form.get('last_name')
	birthday = request.form.get('birthday')
	email = request.form.get('email')
	rollno = request.form.get('rollno')
	department = request.form.get('department')
	imagefile = request.files.get('file','')
	img = upload_file(imagefile,first_name)
	def validate_rollno(this,rollno):
		temp = User.query.filter_by(rollno=rollno)
		if temp:
			raise ValidationError("rollno is already registered")
	db.create_all()
	user = User(first_name=first_name,last_name=last_name,email=email,imagefile=img,rollno=rollno,birthday=birthday,department=department)
	db.session.add(user)
	db.session.commit()
	return render_template("register.html",title='Register',first_name=first_name,last_name=last_name,
		birthday=birthday,email=email,rollno=rollno,department=department,imagefile=imagefile)

@app.route("/comingsoon")
def comingsoon():
	return render_template("ComingSoon.html")