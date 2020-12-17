from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, RadioField, SelectField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo
from webapp.models import User


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Login')


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Create Account')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Username is taken. Please choose another.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Email is already used. Please use another')


class AddSongForm(FlaskForm):
    query = StringField('Search', validators=[DataRequired()])
    submit = SubmitField('Search')


class SongSelectionForm(FlaskForm):
    song_radio_buttons = RadioField('Song 1')
    submit = SubmitField('Add')


class JoinPlaylistForm(FlaskForm):
    playlist_code = StringField('Playlist Code')
    submit = SubmitField('Join')

    def validate_playlist_code(self, code):
        pass
