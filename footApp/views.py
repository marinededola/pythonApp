import sqlite3
from datetime import datetime, timedelta

import requests
from flask import flash, redirect, render_template, request, url_for
from flask_login import current_user, login_user, logout_user

from . import app, db
from .forms import LoginForm, RegisterForm
from .models import User, Favoris

# Pick the current date
date = datetime.now()

date2 = datetime.now() - timedelta(6)
# Adjust the date's format to the API
if len(str(date.day)) < 2:
    dateDay = "0" + str(date.day)
else:
    dateDay = str(date.day)
jourUrl = str(date.year) + "-" + str(date.month) + "-" + dateDay

if len(str(date2.day)) < 2:
    dateDay2 = "0" + str(date2.day)
else:
    dateDay2 = str(date2.day)
jourUrl2 = str(date2.year) + "-" + str(date2.month) + "-" + dateDay2

# Initialize the football API's URL
url = (
    "https://stroccoli-futbol-science-v1.p.rapidapi.com/s1/calendar/"
    + jourUrl + "/" + jourUrl)

# Initialize query parameters
headers = {
    'x-rapidapi-host': "stroccoli-futbol-science-v1.p.rapidapi.com",
    'x-rapidapi-key': "3c3e50e2d3msh35e5bd40a835711p1680e1jsn6f0ff3f70e35"
}

url2 = "https://rapidapi.p.rapidapi.com/s2/live"

url3 = "https://stroccoli-futbol-science-v1.p.rapidapi.com/s1/tournaments"

url4 = (
    "https://stroccoli-futbol-science-v1.p.rapidapi.com/s1/results/"
    + jourUrl2 + "/" + jourUrl)


def get_db_connection():
    """Connect to the database."""
    conn = sqlite3.connect('footApp/database.db')
    conn.row_factory = sqlite3.Row
    return conn


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    loginForm = LoginForm()
    # check if form is valid
    if loginForm.validate_on_submit():
        # retrieve user data
        user = User.query.filter_by(username=loginForm.username.data).first()
        # check if user is on database and check password
        if user is None or not user.check_password(loginForm.password.data):
            flash('Pseudo ou mot de passe incorrecte !')
            return redirect(url_for('index'))
        login_user(user)
        return redirect(url_for('home'))
    return render_template('index.html', loginForm=loginForm)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['get', 'post'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    registerForm = RegisterForm()
    if registerForm.validate_on_submit():
        # create new object User with username and password generate by form
        user = User(username=registerForm.username.data)
        user.set_password(registerForm.password.data)
        # Add to database
        db.session.add(user)
        # Validate session
        db.session.commit()
        flash('Vous êtes bien inscrit !')
        return redirect(url_for('index'))
    return render_template('register.html', registerForm=registerForm)


@app.route('/home', methods=['get', 'post'])
def home():
    # Check if user is authenticated
    if current_user.is_authenticated:
        # Football API requests
        tournaments = requests.request("GET", url3, headers=headers).json()
        match = requests.request("GET", url, headers=headers).json()
        favorites = Favoris.query.filter_by(user_id=current_user.id)
        return render_template(
            'home.html', match=match, favorites=favorites,
            tournaments=tournaments)
    else:
        return redirect(url_for('index'))


@app.route('/tournaments')
def tournaments():
    tournaments = requests.request("GET", url3, headers=headers).json()
    # Football API request
    return render_template('tournaments.html', tournaments=tournaments)


@app.route('/tournament/')
def tournament():
    # Pick the tournament name
    tournament = request.args.get('name')
    querystring = {"tournament_name": tournament}
    tournaments = requests.request("GET", url3, headers=headers).json()
    tournament_result = requests.request(
        "GET", url4, headers=headers, params=querystring).json()
    return render_template(
        'tournament.html', tournament=tournament_result,
        tournament_name=tournament, tournaments=tournaments)


@app.route('/add_favorites')
def add_favorites():
    tournament_name = request.args.get('name')
    name = Favoris.query.filter_by(
        user_id=current_user.id, name=tournament_name).first()
    # Verify whether tournament_name already exists in db for current user
    if name is None:
        favorite = Favoris(user_id=current_user.id, name=tournament_name)
        # Add to database
        db.session.add(favorite)
        # Validate session
        db.session.commit()
    return redirect(url_for('home'))


@app.route('/live')
def live():
    tournaments = requests.request("GET", url3, headers=headers).json()
    live = requests.request("GET", url2, headers=headers).json()
    return render_template('live.html', live=live, tournaments=tournaments)
