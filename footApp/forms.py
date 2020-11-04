from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Length, DataRequired, EqualTo, ValidationError
from werkzeug.security import generate_password_hash, check_password_hash
from footApp.models import User

class LoginForm(FlaskForm):
    username = StringField('Pseudo', validators=[InputRequired('Un pseudo est requis'), Length(min=4, max=25, message='Le pseudo doit être entre 4 et 25 caractères.')])
    password = PasswordField('Mot de passe', validators=[InputRequired('Un mot de passe est requis'), Length(min=6, max=32, message='Le mot de passe doit être entre 6 et 32 caractères.')])

class RegisterForm(FlaskForm):
    username = StringField('Pseudo', validators=[InputRequired(), Length(min=4, max=25)])
    password = PasswordField('Mot de passe', validators=[InputRequired(), Length(min=6, max=32)])
    confirm_password = PasswordField('Confirmation de votre mot de passe', validators=[DataRequired(), EqualTo('password')])

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Pseudo déja utilisé !')
