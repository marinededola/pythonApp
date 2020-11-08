import sqlite3
import requests
import datetime
import itertools
from config import Config
from footApp import app, db
from footApp.forms import LoginForm, RegisterForm
from footApp.models import User
from flask import Flask, render_template, request, flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse
from operator import itemgetter

#Pick the current date
date = datetime.datetime.now()
#Adjust the date's format to the API
if len(str(date.day)) < 2:
    dateDay = "0" + str(date.day)
else:
    dateDay= str(date.day)
jourUrl = str(date.year) + "-" + str(date.month) + "-" + dateDay

#Initialize the football API's URL
url = "https://stroccoli-futbol-science-v1.p.rapidapi.com/s1/calendar/" + jourUrl + "/" + jourUrl

#Initialize query parameters
headers = {
'x-rapidapi-host': "stroccoli-futbol-science-v1.p.rapidapi.com",
'x-rapidapi-key': "3c3e50e2d3msh35e5bd40a835711p1680e1jsn6f0ff3f70e35"
}

url2 = "https://rapidapi.p.rapidapi.com/s2/live"

headers2 = {
'x-rapidapi-key': "3c3e50e2d3msh35e5bd40a835711p1680e1jsn6f0ff3f70e35",
'x-rapidapi-host': "stroccoli-futbol-science-v1.p.rapidapi.com"
}

#Connexion to the database
def get_db_connection():
    conn = sqlite3.connect('footApp/database.db')
    conn.row_factory = sqlite3.Row
    return conn


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    loginForm = LoginForm()
    registerForm = RegisterForm()
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    if loginForm.validate_on_submit():
        user = User.query.filter_by(username=loginForm.username.data).first()
        if user is None or not user.check_password(loginForm.password.data):
            flash('Invalid username or password')
            return redirect(url_for('index'))
        return redirect(url_for('home'))
    return render_template('index.html', loginForm=loginForm, registerForm=registerForm)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

    
@app.route('/register', methods=['get', 'post'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    registerForm = RegisterForm()
    loginForm = LoginForm()
    if registerForm.validate_on_submit():
        user = User(username=registerForm.username.data)
        user.set_password(registerForm.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('index'))
    return render_template('index.html', loginForm=loginForm, registerForm=registerForm)

@app.route('/home', methods=['get', 'post'])
def home():
    conn = get_db_connection()
    teams = conn.execute('SELECT * FROM team').fetchall()
    favoris = conn.execute('SELECT * FROM favoris').fetchall()
    conn.close()
    #Football API request
    match = requests.request("GET", url, headers=headers).json()
    return render_template('home.html', teams=teams, favoris=favoris, match=match)

@app.route('/team')
def team():
    conn = get_db_connection()
    teams = conn.execute('SELECT * FROM team').fetchall()
    favoris = conn.execute('SELECT * FROM favoris').fetchall()
    conn.close()
    #Football API request
    match = requests.request("GET", url, headers=headers).json()
    return render_template('team.html', teams=teams, favoris=favoris, match=match)

@app.route('/live')
def live():
    live = requests.request("GET", url2, headers=headers2).json()
    return render_template('live.html', live=live)

app.config.from_object('config')

if __name__ == "__main__":
    app.run()



