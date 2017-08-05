import os

from flask import Flask, render_template, redirect, url_for, request, session, flash
from functools import wraps

app = Flask(__name__)

app.secret_key = 'qwertylkjhgzxcvb'

# login required decorator
def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('You need to login first.')
            return redirect(url_for('login'))
    return wrap

#Home Page
@app.route('/')
@login_required
def home():
    return render_template("index.html")
    
@app.route('/welcome')
def welcome():
    return render_template("welcome.html")
    
#Login Page
@app.route('/login',methods=['GET','POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'admin' or request.form['password'] != 'admin':
            error = 'Invalid Credentials - Please try again'
        else:
            session['logged_in'] = True
            flash('You were just logged in')
            return redirect(url_for('home'))
    
    return render_template("login.html", error=error)

#Logout Page
@app.route('/logout')
@login_required
def logout():
    session.pop('logged_in', None)
    flash('You were just logged out')
    return redirect(url_for('welcome'))
    
#Signin Page
@app.route('/signin')
def signin():
    return render_template("signin.html")
    
@app.route('/jumbotron')
def jumbotron():
    return render_template("jumbotron.html")

if __name__ == '__main__':
    host = os.getenv('IP','0.0.0.0')
    port = int(os.getenv('PORT',5000))
    app.debug = True
    app.run(host=host,port=port)
    
