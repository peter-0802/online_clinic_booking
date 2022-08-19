from dataclasses import field
from multiprocessing.dummy import active_children
from turtle import title
from flask import Flask, render_template, flash, redirect, url_for, session, request, logging, Response, Blueprint, jsonify
from flask import render_template
from datetime import timedelta
from flask_mysqldb import MySQL

app = Flask(__name__)
app.config['SECRET_KEY'] = 'nothingtoseehere'
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'clinic_apointment'
app.permanent_session_lifetime = timedelta(hours = 1)

mysql = MySQL(app)


#Landing Page
@app.route('/')
def home():
	cursor = mysql.connection.cursor()
	cursor.execute("SELECT concat(title, ' ', lastname) `name` from doctors")
	doctors = cursor.fetchall()
	print(doctors)
	return render_template('index.html', doctors = doctors)
	#else:
	#	return redirect(url_for('login'))

# Login for Admin
@app.route('/login', methods = ['POST', 'GET'])
def login():
	if request.method == "POST":
		username = request.form['username']
		password = request.form['pass']

		cursor = mysql.connection.cursor()
		cursor.execute("select * from accounts where username = '{username}' and password = '{password}'".format(username = username, password = password))
		account = cursor.fetchall()
		for row in account:
			if len(account) == 1:
				#print(len(account))
				session['username'] = username
				return redirect(url_for('admin'))
			else:
				return redirect(url_for('login'))

		return redirect(url_for('login'))
	else:
		return render_template('login.html')

#Admin View
@app.route('/admin')
def admin():
	cursor = mysql.connection.cursor()
	cursor.execute("select count(*) from doctors")
	doctors = cursor.fetchall()

	cursor.execute("select count(*) from appointments")
	appointments = cursor.fetchall()

	cursor.execute("select count(*) from patients")
	patients = cursor.fetchall()

	for doctor in doctors:
		print(doctor[0])
	for appointment in appointments:
		print(appointment[0])
	for patient in patients:
		print(patient[0])

		return render_template('admin.html', var_apointments = appointment[0], var_patients = patient[0], var_doctors = doctor[0])

#Admin View
@app.route('/add_doc', methods = ['POST'])
def add_doc():
	title = request.form['title']
	lastname = request.form['lastname']
	firstname = request.form['firstname']
	field = request.form['field']
	cursor = mysql.connection.cursor()
	cursor.execute("""insert into doctors
					  (title, lastname, firstname, field)
					  values
					  ('{title}', '{lastname}', '{firstname}', '{field}')""".format(title = title, lastname = lastname, firstname = firstname, field = field))
	mysql.connection.commit()
	return redirect(url_for('admin'))

#booking
@app.route('/book', methods = ['POST','GET'])
def book():
	return render_template('book.html')

#Add booking
@app.route('/add_booking', methods = ['POST','GET'])
def add_booking():
	if request.method == "POST":
		date = request.form['date']
		lastname = request.form['lastname']
		firstname = request.form['firstname']
		email = request.form['email']
		notes = request.form['notes']
		doctor = request.form['doctor']

		cursor = mysql.connection.cursor()
		cursor.execute("""insert into appointments
					  (date, lastname, firstname, email, notes, dr)
					  values
					  ('{date}', '{lastname}', '{firstname}', '{email}', '{notes}', '{doctor}')""".format(date = date, lastname = lastname, firstname = firstname, email = email, notes = notes, doctor = doctor))

		cursor.execute("""replace into patients
					  (lastname, firstname, email)
					  values
					  ('{lastname}', '{firstname}', '{email}')""".format(lastname = lastname, firstname = firstname, email = email))
		mysql.connection.commit()

		return redirect(url_for('home'))

		



@app.route('/add_pat', methods = ['POST'])
def add_pat():
	pusername = request.form['patient1']
	ppassword = request.form['patient2']
	print(pusername + ' ' + ppassword)
	return redirect(url_for('admin'))


'''
@app.route('/login', methods = ['POST', 'GET'])
def login():
	if request.method == "POST":
		username = request.form['username']
		password = request.form['pass']

		cursor = mysql.connection.cursor()
		cursor.execute("select * from accounts where username = '{username}' and password = '{password}'".format(username = username, password = password))
		account = cursor.fetchall()
		for row in account:
			if len(account) == 1:
				#print(len(account))
				session['username'] = username
				return redirect(url_for('admin'))
			else:
				return redirect(url_for('login'))

		return redirect(url_for('login'))
	else:
		return render_template('login.html')

@app.route('/tab')
def tab():
	return render_template('main.html')

@app.route('/land')
def land():
	return render_template('landing.html')
'''

if __name__ == '__main__':
	app.run(debug=True, host = '0.0.0.0')
