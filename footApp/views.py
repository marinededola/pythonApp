import sqlite3
import requests
import datetime
import itertools
from footApp import app
from config import Config
from flask import Flask, render_template, request, flash, redirect
from footApp.forms import LoginForm, RegisterForm
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
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

    if loginForm.validate_on_submit():
        flash('Bonjour user{}'.format(loginForm.username.data))
        return redirect('/home')
    return render_template('index.html', loginForm=loginForm, registerForm=registerForm)

@app.route('/home', methods=['get', 'post'])
def home():
    conn = get_db_connection()
    teams = conn.execute('SELECT * FROM team').fetchall()
    favoris = conn.execute('SELECT * FROM favoris').fetchall()
    conn.close()
    #Football API request
    match = requests.request("GET", url, headers=headers).json()
    user = {'username': 'Test'}
    return render_template('home.html', teams=teams, favoris=favoris, match=match, user=user)

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

@app.route('/register', methods=['get', 'post'])
def register():
    loginForm = LoginForm()
    registerForm = RegisterForm()
    conn = get_db_connection()
    if request.method == 'POST':
        try:
            if registerForm.validate_on_submit():
                username_field = request.form['username']
                password_field = request.form['password']
                msg = "Inscription réussie !"
                conn.execute('INSERT INTO user (username, password) VALUES (?, ?)',
                (username_field, password_field))
                conn.commit()
                conn.close()
                return render_template('index.html', loginForm=loginForm, registerForm=registerForm, msg=msg)
            else:
                msg = "Une erreur est survenue !"
                return render_template('index.html', loginForm=loginForm, registerForm=registerForm, msg=msg)
        except:
            msg = "Identifiant déja utilisé !"
            return render_template('index.html', loginForm=loginForm, registerForm=registerForm, msg=msg)
    return render_template('index.html', loginForm=loginForm, registerForm=registerForm)
    

app.config.from_object('config')

if __name__ == "__main__":
    app.run()



