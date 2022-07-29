from flask import Flask, render_template, flash, redirect, url_for, session, request, logging, Response, Blueprint, jsonify
from flask import render_template
from datetime import timedelta

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret123'
app.permanent_session_lifetime = timedelta(hours = 1)

@app.route('/')
def home():
	return render_template('index.html')

@app.route('/tab')
def tab():
	return render_template('main.html')

# Login
@app.route('/login', methods = ['POST', 'GET'])
def login():
	if request.method == "POST":
		username = request.form['username']
		password = request.form['pass']
		if username == 'admin' and password == '123':
			return redirect(url_for('home'))
		else:
			return render_template('login.html')
	else:
		return render_template('login.html')

if __name__ == '__main__':
	app.run(debug=True, host = '0.0.0.0')
