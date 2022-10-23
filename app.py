from asyncio import events
from dataclasses import field
from multiprocessing.dummy import active_children
from turtle import title
from flask import Flask, render_template, flash, redirect, url_for, session, request, logging, Response, Blueprint, jsonify
from flask import render_template
from datetime import timedelta, date, datetime
from flask_mysqldb import MySQL,MySQLdb
import json
import requests

import sender as sender

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
	#print(doctors)
	flash('Welcome',category="success")
	return render_template('index.html', doctors = doctors)

#book2 Page
@app.route('/make_booking/<seldate>', methods = ['POST', 'GET'])
def make_booking(seldate = date.today()):
	if request.method == "GET":
		cursor = mysql.connection.cursor()
		cursor.execute("select * from time_range where time not in(select time from appointments where date = '{seldate}')".format(seldate = seldate))
		print("select * from time_range where time not in(select time from appointments where date = '{seldate}')".format(seldate = seldate))
		times = cursor.fetchall()	

		cursor = mysql.connection.cursor()
		cursor.execute("SELECT concat(title, ' ', lastname, ' | ', field) `name` from doctors")
		doctors = cursor.fetchall()
		return render_template('makebooking.html', times = times, doctors = doctors, seldate = seldate)

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
		flash('Logged In',category="success")
		return render_template('login.html')

# Logout
@app.route('/logout')
def logout():
    session.pop("username", None)
    #flash('Loged Out!', category = 'error')
    return redirect(url_for('home'))


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

	cursor.execute("select count(*) from patients")
	patients = cursor.fetchall()

	cursor.execute("select count(*) from appointments where date >= CURDATE()")
	reminders = cursor.fetchall()

	for doctor in doctors:
		pass
	for appointment in appointments:
		pass
	for patient in patients:
		pass
	for reminder in reminders:
		pass

		return render_template('admin.html', var_apointments = appointment[0], var_patients = patient[0], var_doctors = doctor[0], var_reminders = reminder[0])

###################################################################################################################################

#calendar
@app.route('/calendar', methods = ['POST', 'GET'])
def calendar():
	if request.method == 'GET':
		#cur = mysql.connection.cursor()
		#cur.execute("SELECT concat(code, ' with doc.', dr, ' | ', notes), concat(date, ' ',STR_TO_DATE(time, '%l:%i %p')) FROM appointments where approve = 1")
		#appointments = cur.fetchall()
		return render_template('calendartest.html')

	else:
		code = request.form['session_code']
		cur = mysql.connection.cursor()
		cur.execute("SELECT concat(code, ' with doc.', dr, ' | ', notes), concat(date, ' ',STR_TO_DATE(time, '%l:%i %p')) FROM appointments where approve = 1 and code = '{code}'".format(code = code))
		appointments = cur.fetchall()
		print(code)
		return render_template('calendartest.html', appointments = appointments)


#calendar admin
@app.route('/calendar_admin', methods = ['POST', 'GET'])
def calendar_admin():
	if request.method == 'GET':
		cur = mysql.connection.cursor()
		cur.execute("SELECT concat(code, ' with doc.', dr, ' | ', notes), concat(date, ' ',STR_TO_DATE(time, '%l:%i %p')) FROM appointments where approve = 1")
		appointments = cur.fetchall()
		return render_template('calendartest.html', appointments = appointments)
##################################################################################################################################

#View Doctors
@app.route('/doctors', methods = ['POST','GET'])
def doctors():
	cur = mysql.connection.cursor()
	cur.execute("SELECT id, title ``, concat(lastname, ', ', firstname) `name`, field FROM doctors")
	doctors = cur.fetchall()
	#print(doctors)
	return render_template('doctorslist.html', doctors = doctors)

#Add Doctors
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
	return redirect(url_for('doctors'))

#Update Doctors
@app.route('/edit_doc/<id>', methods = ['POST', 'GET'])
def edit_doc(id):
	if request.method == 'POST':
		title = request.form['title']
		lastname = request.form['lastname']
		firstname = request.form['firstname']
		field = request.form['field']

		cursor = mysql.connection.cursor()
		cursor.execute("""update doctors set title = '{title}', lastname = '{lastname}', firstname = '{firstname}', field = '{field}' where id = '{id}'""".format(title = title, lastname = lastname, firstname = firstname, field = field, id = id))
		mysql.connection.commit()

		return redirect(url_for('doctors'))
	else:
		cur = mysql.connection.cursor()
		cur.execute("""select * from doctors where id = '{id}'""".format(id = id))
		isodocs = cur.fetchall()
		for isodoc in isodocs:
			#print(isodoc)
			pass
			return render_template('doctorsform.html', lastname = isodoc[2], firstname = isodoc[3], Fieldval = isodoc[4])

#Delete Doctors
@app.route('/archive_doc/<id>', methods = ['GET'])
def archive_doc(id):
	cursor = mysql.connection.cursor()
	cursor.execute("""delete from doctors where id = '{id}'""".format(id = id))
	mysql.connection.commit()
	return redirect(url_for('doctors'))

######################################################################################################

#View Patients
@app.route('/patients', methods = ['POST','GET'])
def patients():
	cur = mysql.connection.cursor()
	cur.execute("SELECT id, concat(lastname, ', ', firstname) `name`, email, mobile FROM patients")
	patients = cur.fetchall()
	#print(doctors)
	return render_template('patientslist.html', patients = patients)

#Add Patients
@app.route('/add_patient', methods = ['POST'])
def add_pat():
	lastname = request.form['lastname']
	firstname = request.form['firstname']
	email = request.form['email']
	mobile = request.form['mobile']

	cursor = mysql.connection.cursor()
	cursor.execute("""insert into patients
					  (lastname, firstname, email, mobile)
					  values
					  ('{lastname}', '{firstname}', '{email}', '{mobile}')""".format(lastname = lastname, firstname = firstname, email = email, mobile = mobile))
	mysql.connection.commit()

	return redirect(url_for('patients'))

#Update Patients
@app.route('/edit_pat/<id>', methods = ['POST', 'GET'])
def edit_pat(id):
	if request.method == 'POST':
		lastname = request.form['lastname']
		firstname = request.form['firstname']
		email = request.form['email']
		mobile = request.form['mobile']

		cursor = mysql.connection.cursor()
		cursor.execute("""update patients set email = '{email}', lastname = '{lastname}', firstname = '{firstname}', mobile = '{mobile}' where id = '{id}'""".format(email = email, lastname = lastname, firstname = firstname, mobile = mobile, id = id))
		mysql.connection.commit()

		return redirect(url_for('patients'))
	else:
		cur = mysql.connection.cursor()
		cur.execute("""select * from patients where id = '{id}'""".format(id = id))
		patients = cur.fetchall()
		for patient in patients:
			#print(isodoc)
			pass
			return render_template('patientform.html', lastname = patient[1], firstname = patient[2], email = patient[3], mobile = patient[4])

#Delete Patients
@app.route('/archive_pat/<id>', methods = ['GET'])
def archive_pat(id):
	cursor = mysql.connection.cursor()
	cursor.execute("""delete from patients where id = '{id}'""".format(id = id))
	mysql.connection.commit()
	return redirect(url_for('patients'))

######################################################################################################

#pending bookings list
@app.route('/bookings', methods = ['POST','GET'])
def bookings():
	cur = mysql.connection.cursor()
	cur.execute("SELECT id, date, concat(lastname, ', ', firstname) `name`, email, number, notes, dr, IF(approve = '0', 'Pending', 'Approved') as status FROM appointments order by date desc")
	appointments = cur.fetchall()
	return render_template('appointmentslist.html', appointments = appointments)

#approved bookings list
@app.route('/approved_bookings', methods = ['POST','GET'])
def approved_bookings():
	cur = mysql.connection.cursor()
	cur.execute("SELECT id, date, concat(lastname, ', ', firstname) `name`, email, number, notes, dr FROM appointments where approve = 1 order by date desc")
	appointments = cur.fetchall()
	return render_template('appointmentsapproved.html', appointments = appointments)

#pending bookings list
@app.route('/pending_bookings', methods = ['POST','GET'])
def pending_bookings():
	cur = mysql.connection.cursor()
	cur.execute("SELECT id, date, concat(lastname, ', ', firstname) `name`, email, number, notes, dr FROM appointments where approve = 0 order by date desc")
	appointments = cur.fetchall()
	return render_template('appointmentlistpending.html', appointments = appointments)

#Add booking
@app.route('/add_booking', methods = ['POST','GET'])
def add_booking():
	if request.method == "POST":
		date = request.form['date']
		time = request.form['slottime']
		lastname = request.form['lastname']
		firstname = request.form['firstname']
		email = request.form['email']
		mobile = request.form['number']
		notes = request.form['notes']
		doctor = request.form['doctor']

		cursor = mysql.connection.cursor()
		cursor.execute("""insert into appointments
					  (date, time, code, lastname, firstname, email, number, notes, dr)
					  values
					  ('{date}', '{time}',(select if (count(id) <= 0, 'SES1', concat('SES', max(id) + 1)) code from appointments as code), '{lastname}', '{firstname}', '{email}', '{mobile}', '{notes}', '{doctor}')""".format(date = date, time = time, lastname = lastname, firstname = firstname, email = email, mobile = mobile, notes = notes, doctor = doctor))

		cursor.execute("""replace into patients
					  (lastname, firstname, email, mobile)
					  values
					  ('{lastname}', '{firstname}', '{email}', '{mobile}')""".format(lastname = lastname, firstname = firstname, email = email, mobile = mobile))
					  
		mysql.connection.commit()

		cur = mysql.connection.cursor()
		cur.execute("SELECT code, concat(date, ' ', time), concat(lastname, ' ', firstname), number FROM appointments order by id desc limit 1")
		appointments = cur.fetchall()
		for appointment in appointments:
			pass
		message = f"Hello {appointment[2]} Your session with code {appointment[0]} on {appointment[1]} is now booked, please wait for our confirmation."
		print(message)
		#sender.semaphore(appointment[3]', message)
		return redirect(url_for('home'))
	


#Update Patients
@app.route('/edit_booking/<id>', methods = ['POST', 'GET'])
def edit_booking(id):
	if request.method == 'POST':
		date = request.form['date']
		lastname = request.form['lastname']
		firstname = request.form['firstname']
		email = request.form['email']
		mobile = request.form['mobile']
		notes = request.form['notes']
		doctor = request.form['doctor']

		cursor = mysql.connection.cursor()
		cursor.execute("""update appointments set date = '{date}', lastname = '{lastname}', firstname = '{firstname}', email = '{email}', number = '{mobile}', notes = '{notes}' , dr = '{doctor}' where id = '{id}'""".format(date = date, email = email, lastname = lastname, firstname = firstname, mobile = mobile, notes = notes, doctor = doctor, id = id))
		mysql.connection.commit()

		return redirect(url_for('bookings'))
	else:
		cur = mysql.connection.cursor()
		cur.execute("""select * from appointments where id = '{id}'""".format(id = id))
		appointments = cur.fetchall()
		for appointment in appointments:
			#print(isodoc)
			pass
		cur = mysql.connection.cursor()
		cur.execute("""select concat(title, ' ', lastname) from doctors""")
		doctors = cur.fetchall()
		
		return render_template('appointmentform.html', date = appointment[1], time = appointment[2], lastname = appointment[4], firstname = appointment[5], email = appointment[6], mobile = appointment[7], notes = appointment[8], doctor = appointment[9], doctors = doctors)

#approve booking
@app.route('/approve/<id>', methods = ['GET'])
def approve(id):
	cursor = mysql.connection.cursor()
	cursor.execute("""update appointments set approve = 1 where id = '{id}'""".format(id = id))
	mysql.connection.commit()

	cur = mysql.connection.cursor()
	cur.execute("SELECT code, concat(date, ' ', time), concat(lastname, ' ', firstname), number FROM appointments where id = '{id}' order by id desc limit 1".format(id = id))
	appointments = cur.fetchall()
	for appointment in appointments:
		pass
	message = f"Hello {appointment[2]} Your session with code {appointment[0]}, has been confirmed by our Admin / Doctor. Please do come in time."
	print(message)
	#sender.semaphore(appointment[3]', message)
	return redirect(url_for('bookings'))

#Delete Patients
@app.route('/cancel/<id>', methods = ['GET'])
def cancel(id):
	cursor = mysql.connection.cursor()
	cursor.execute("""update appointments set approve = 0 where id = '{id}'""".format(id = id))
	mysql.connection.commit()

	cur = mysql.connection.cursor()
	cur.execute("SELECT code, concat(date, ' ', time), concat(lastname, ' ', firstname), number FROM appointments where id = '{id}' order by id desc limit 1".format(id = id))
	appointments = cur.fetchall()
	for appointment in appointments:
		pass
	message = f"Hello {appointment[2]} Your session with code {appointment[0]}, has been cancelled by our Admin / Doctor."
	print(message)
	#sender.semaphore(appointment[3]', message)
	return redirect(url_for('bookings'))

#Delete Patients
@app.route('/archive_booking/<id>', methods = ['GET'])
def archive_booking(id):
	cursor = mysql.connection.cursor()
	cursor.execute("""delete from appointments where id = '{id}'""".format(id = id))
	mysql.connection.commit()
	return redirect(url_for('bookings'))
		



if __name__ == '__main__':
	app.run(debug=True, host = '0.0.0.0')
