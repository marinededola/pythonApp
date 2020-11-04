import sqlite3
from flask import Flask, render_template, request
from footApp.forms import LoginForm, RegisterForm

def get_db_connection():
    conn = sqlite3.connect('footApp/database.db')

    return conn

app = Flask(__name__)
app.config['SECRET_KEY'] = 'Thesecretkey'


@app.route('/')
@app.route('/index')
def index():
    loginForm = LoginForm()
    registerForm = RegisterForm()
    return render_template('index.html', loginForm=loginForm, registerForm=registerForm)

@app.route('/home', methods=['get', 'post'])
def home():
    conn = get_db_connection()
    teams = conn.execute('SELECT * FROM team').fetchall()
    favoris = conn.execute('SELECT * FROM favoris').fetchall()
    user = {'username': 'Test'}
    return render_template('home.html', teams=teams, favoris=favoris, user=user)
    

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



