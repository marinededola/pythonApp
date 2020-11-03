import sqlite3
from flask import Flask, render_template, request
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Length, DataRequired, EqualTo
from werkzeug.security import generate_password_hash, check_password_hash

def get_db_connection():
    conn = sqlite3.connect('footApp/database.db')
    conn.row_factory = sqlite3.Row
    return conn

app = Flask(__name__)
app.config['SECRET_KEY'] = 'Thesecretkey'

class LoginForm(FlaskForm):
    username = StringField('Pseudo', validators=[InputRequired('Un pseudo est requis'), Length(min=4, max=25, message='Le pseudo doit êtr entre 4 et 25 caractères.')])
    password = PasswordField('Mot de passe', validators=[InputRequired('Un mot de passe est requis'), Length(min=6, max=32, message='Le mot de passe doit être entre 6 et 32 caractères.')])

class RegisterForm(FlaskForm):
    username = StringField('Pseudo', validators=[InputRequired(), Length(min=4, max=25)])
    password = PasswordField('Mot de passe', validators=[InputRequired(), Length(min=6, max=32)])
    confirm_password = PasswordField('Confirmation de votre mot de passe', validators=[DataRequired(), EqualTo('password')])

@app.route('/')
def index():
    loginForm = LoginForm()
    registerForm = RegisterForm()
    conn = get_db_connection()
    users = conn.execute('SELECT * FROM user').fetchall()
    for user in users:
        print(user[1])
    conn.close
    return render_template('index.html', users=users, loginForm=loginForm, registerForm=registerForm)

@app.route('/home', methods=['get', 'post'])
def home():
    loginForm = LoginForm()
    registerForm = RegisterForm()
    conn = get_db_connection()
    teams = conn.execute('SELECT * FROM team').fetchall()
    favoris = conn.execute('SELECT * FROM favoris').fetchall()
    if request.method == 'POST':
        username_field = request.form.get('username')
        password_field = request.form.get('password')
        password_hash = generate_password_hash(password_field)
        if loginForm.validate_on_submit():
            print(password_field, username_field, password_hash)
            return render_template('home.html', teams=teams, favoris=favoris, loginForm=loginForm)
    return render_template('index.html', loginForm=loginForm, registerForm=registerForm)

@app.route('/team')
def team():
    conn = get_db_connection()
    teams = conn.execute('SELECT * FROM team').fetchall()
    favoris = conn.execute('SELECT * FROM favoris').fetchall()
    conn.close()
    return render_template('team.html', teams=teams, favoris=favoris)

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
                password_hash = generate_password_hash(password_field)
                msg = "Inscription réussie !"
                conn.execute('INSERT INTO user (username, password) VALUES (?, ?)',
                (username_field, password_hash))
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



