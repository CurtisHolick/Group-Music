from webapp import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    songs = db.relationship('Song', backref='owner', lazy='dynamic')

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Song(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    spotify_id = db.Column(db.String(60))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    playlist_id = db.Column(db.Integer, db.ForeignKey('playlist.id'))

    def __repr__(self):
        return '<Song {}>'.format(self.spotify_id)


class Playlist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    playlist_name = db.Column(db.String(100))
    playlist_code = db.Column(db.String(20), unique=True)
    songs = db.relationship('Song', backref='playlist', lazy='dynamic')
    spotify_playlist_id = db.Column(db.String(20))
    # todo: add way to generate join code?

    def __repr__(self):
        return '<Playlist {}>'.format(self.playlist_name)

    def generate_playlist_code(self):
        """Generate a unique code for the playlist"""
        code = []
        code.append(self.playlist_name[:3])
        code.append(str(self.id))
        print(''.join(code))
        self.playlist_code = ''.join(code)


@login.user_loader
def load_user(id):
    return User.query.get(int(id))