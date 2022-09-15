from dataclasses import field
from multiprocessing.dummy import active_children
from turtle import title
from flask import Flask, render_template, flash, redirect, url_for, session, request, logging, Response, Blueprint, jsonify
from flask import render_template
from datetime import timedelta
from flask_mysqldb import MySQL,MySQLdb
import json


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

	for doctor in doctors:
		#print(doctor[0])
		pass
	for appointment in appointments:
		#print(appointment[0])
		pass
	for patient in patients:
		#print(patient[0])
		pass

		return render_template('admin.html', var_apointments = appointment[0], var_patients = patient[0], var_doctors = doctor[0])

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
		mobile = request.form['number']
		notes = request.form['notes']
		doctor = request.form['doctor']

		cursor = mysql.connection.cursor()
		cursor.execute("""insert into appointments
					  (date, lastname, firstname, email, number, notes, dr)
					  values
					  ('{date}', '{lastname}', '{firstname}', '{email}', '{mobile}', '{notes}', '{doctor}')""".format(date = date, lastname = lastname, firstname = firstname, email = email, mobile = mobile, notes = notes, doctor = doctor))

		cursor.execute("""replace into patients
					  (lastname, firstname, email, mobile)
					  values
					  ('{lastname}', '{firstname}', '{email}', '{mobile}')""".format(lastname = lastname, firstname = firstname, email = email, mobile = mobile))
		mysql.connection.commit()

		return redirect(url_for('home'))


		






#booking
@app.route('/test')
def test():
	mycursor = mydb.cursor()
	mycursor.execute("SELECT title, concat(lastname, ', ', firstname) ,`field` FROM doctors")
	myresult = mycursor.fetchall()
	return render_template('test.html', doctors = myresult)

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
