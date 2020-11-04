import sqlite3
import requests
import datetime
from flask import Flask, render_template
import itertools
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

app = Flask(__name__)

#Initialization of application routes
@app.route('/')
def index():
    conn = get_db_connection()
    users = conn.execute('SELECT * FROM user').fetchall()
    favoris = conn.execute('SELECT * FROM favoris').fetchall()
    conn.close()
    return render_template('index.html', users=users, favoris=favoris)

@app.route('/home')
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



