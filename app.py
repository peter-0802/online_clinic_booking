from multiprocessing.dummy import active_children
from flask import Flask, render_template, flash, redirect, url_for, session, request, logging, Response, Blueprint, jsonify
from flask import render_template
from datetime import timedelta
#from flask_mysqldb import MySQL

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
	if 'username' in session:
		return render_template('index.html')
	else:
		return redirect(url_for('login'))

# Login for Admin
@app.route('/login', methods = ['POST', 'GET'])
def login():
	if request.method == "POST":
		username = request.form['username']
		password = request.form['pass']

		#cursor = mysql.connection.cursor()
		#cursor.execute("select * from accounts where username = '{username}' and password = '{password}'".format(username = username, password = password))
		
		if username == 'admin' and password == 'admin':
			session['username'] = username
			return redirect(url_for('admin'))
		else:
			return redirect(url_for('login'))

	else:
		return render_template('login.html')

#Admin View
@app.route('/admin')
def admin():
	return render_template('admin.html', active = '')


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
