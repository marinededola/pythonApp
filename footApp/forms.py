from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField
from wtforms.validators import (
    InputRequired, Length, DataRequired, EqualTo, ValidationError)

from .models import User


class LoginForm(FlaskForm):
    username = StringField(
        'Pseudo', validators=[
            InputRequired('Un pseudo est requis'),
            Length(min=4, max=25, message=(
                'Le pseudo doit être entre 4 et 25 caractères.'))])
    password = PasswordField(
        'Mot de passe', validators=[
            InputRequired('Un mot de passe est requis'),
            Length(min=6, max=32, message=(
                'Le mot de passe doit être entre 6 et 32 caractères.'))])


class RegisterForm(FlaskForm):
    username = StringField(
        'Pseudo', validators=[
            InputRequired(), Length(min=4, max=25, message=(
                'Le pseudo doit être entre 4 et 25 caractères.'))])
    password = PasswordField(
        'Mot de passe', validators=[
            InputRequired(), Length(min=6, max=32, message=(
                'Le mot de passe doit être entre 6 et 32 caractères.'))])
    confirm_password = PasswordField(
        'Confirmation mot de passe', validators=[
            DataRequired(),
            EqualTo('password', message='Le mot de passe est différent.')])

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Pseudo déja utilisé !')
