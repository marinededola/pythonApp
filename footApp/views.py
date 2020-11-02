import sqlite3
from flask import Flask, render_template, request
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Length
from werkzeug.security import generate_password_hash, check_password_hash

def get_db_connection():
    conn = sqlite3.connect('footApp/database.db')
    conn.row_factory = sqlite3.Row
    return conn

app = Flask(__name__)
app.config['SECRET_KEY'] = 'Thesecretkey'

class LoginForm(FlaskForm):
    pseudo = StringField('pseudo', validators=[InputRequired('Un pseudo est requis'), Length(min=4, max=25, message='Le pseudo doit êtr entre 4 et 25 caractères.')])
    password = PasswordField('password', validators=[InputRequired('Un mot de passe est requis'), Length(min=6, max=32, message='Le mot de passe doit être entre 6 et 32 caractères.')])

class RegisterForm(FlaskForm):
    pseudo = StringField('pseudo', validators=[InputRequired(), Length(min=4, max=25)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=6, max=32)])

@app.route('/')
def index():
    form = LoginForm()
    conn = get_db_connection()
    users = conn.execute('SELECT * FROM user').fetchall()
    favoris = conn.execute('SELECT * FROM favoris').fetchall()
    conn.close()
    return render_template('index.html', users=users, favoris=favoris, form=form)

@app.route('/home', methods=['get', 'post'])
def home():
    form = LoginForm()
    conn = get_db_connection()
    teams = conn.execute('SELECT * FROM team').fetchall()
    favoris = conn.execute('SELECT * FROM favoris').fetchall()
    conn.close()
    if form.validate_on_submit():
        return render_template('home.html', teams=teams, favoris=favoris, form=form)
    return render_template('index.html', form=form)

@app.route('/team')
def team():
    conn = get_db_connection()
    teams = conn.execute('SELECT * FROM team').fetchall()
    favoris = conn.execute('SELECT * FROM favoris').fetchall()
    conn.close()
    return render_template('team.html', teams=teams, favoris=favoris)

@app.route('/register', methods=['get', 'post'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        return render_template('index.html', form=form)
    else:
        return "error"
    

app.config.from_object('config')

if __name__ == "__main__":
    app.run()



