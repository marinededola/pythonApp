import sqlite3
import requests
import datetime
from datetime import datetime, timedelta
import itertools
from config import Config
from footApp import app, db
from footApp.forms import LoginForm, RegisterForm
from footApp.models import User, Favoris
from flask import Flask, render_template, request, flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse
from operator import itemgetter

#Pick the current date
date = datetime.now()

date2 = (datetime.now() -  timedelta(6))
#Adjust the date's format to the API
if len(str(date.day)) < 2:
    dateDay = "0" + str(date.day)
else:
    dateDay= str(date.day)
jourUrl = str(date.year) + "-" + str(date.month) + "-" + dateDay

if len(str(date2.day)) < 2:
    dateDay2 = "0" + str(date2.day)
else:
    dateDay2= str(date2.day)
jourUrl2 = str(date2.year) + "-" + str(date2.month) + "-" + dateDay2

#Initialize the football API's URL
url = "https://stroccoli-futbol-science-v1.p.rapidapi.com/s1/calendar/" + jourUrl + "/" + jourUrl

#Initialize query parameters
headers = {
'x-rapidapi-host': "stroccoli-futbol-science-v1.p.rapidapi.com",
'x-rapidapi-key': "3c3e50e2d3msh35e5bd40a835711p1680e1jsn6f0ff3f70e35"
}

url2 = "https://rapidapi.p.rapidapi.com/s2/live"

url3 = "https://stroccoli-futbol-science-v1.p.rapidapi.com/s1/tournaments"

url4 = "https://stroccoli-futbol-science-v1.p.rapidapi.com/s1/results/" + jourUrl2 + "/" + jourUrl


#Connexion to the database
def get_db_connection():
    conn = sqlite3.connect('footApp/database.db')
    conn.row_factory = sqlite3.Row
    return conn

#Route for index
@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    loginForm = LoginForm()
    #check if form is valid
    if loginForm.validate_on_submit():
        #retrieve user data
        user = User.query.filter_by(username=loginForm.username.data).first()
        #check if user is on database and check password
        if user is None or not user.check_password(loginForm.password.data):
            flash('Invalid username or password')
            return redirect(url_for('index'))
        login_user(user)
        return redirect(url_for('home'))
    return render_template('index.html', loginForm=loginForm)

#route for deconnexion user 
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

#route for registration 
@app.route('/register', methods=['get', 'post'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    registerForm = RegisterForm()
    if registerForm.validate_on_submit():
        #create new object User with username and password generate by form
        user = User(username=registerForm.username.data)
        user.set_password(registerForm.password.data)
        #Add to database
        db.session.add(user)
        #Validate session
        db.session.commit()
        flash('Vous êtes bien inscrit !')
        return redirect(url_for('index'))
    return render_template('register.html', registerForm=registerForm)

#route for user homepage
@app.route('/home', methods=['get', 'post'])
def home():
    #Check if user is authenticated
    if current_user.is_authenticated:
        #Football API requests
        tournaments = requests.request("GET", url3, headers=headers).json()
        match = requests.request("GET", url, headers=headers).json()
        favorites = Favoris.query.filter_by(user_id = current_user.id)
        return render_template('home.html', match=match, favorites=favorites, tournaments=tournaments)
    else: 
        return redirect(url_for('index'))

@app.route('/tournaments')
def tournaments():
    tournaments = requests.request("GET", url3, headers=headers).json()
    #Football API request
    return render_template('tournaments.html', tournaments=tournaments)

@app.route('/tournament/')
def tournament():
    tournament = request.args.get('name')
    querystring = {"tournament_name":tournament}
    tournaments = requests.request("GET", url3, headers=headers).json()
    tournament_result = requests.request("GET", url4, headers=headers, params=querystring).json()
    return render_template('tournament.html', tournament=tournament_result, tournament_name=tournament, tournaments=tournaments)

@app.route('/add_favorites')
def add_favorites():
    tournament_name = request.args.get('name')
    name = Favoris.query.filter_by(name = tournament_name).first()
    #verify if tournament_name exist in db
    if name is None:
        favorite = Favoris(user_id=current_user.id, name=tournament_name)
        #Add to database
        db.session.add(favorite)
        #Validate session
        db.session.commit()
    return redirect('home')

#route for live
@app.route('/live')
def live():
    tournaments = requests.request("GET", url3, headers=headers).json()
    live = requests.request("GET", url2, headers=headers).json()
    return render_template('live.html', live=live, tournaments=tournaments)

app.config.from_object('config')

if __name__ == "__main__":
    app.run()