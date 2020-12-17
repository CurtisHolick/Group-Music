from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
import spotipy
import spotipy.util as util
from flask_admin import Admin
from webapp.admin import AdminView
from flask_admin.contrib.sqla import ModelView


app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)
login.login_view = 'login'

with open('api_info.txt', mode='r') as file:
    data = file.readlines()
    spotifyUsername = data[0].rstrip()
    spotifyClientId = data[1].rstrip()
    spotifyClientSecret = data[2].rstrip()

token = util.prompt_for_user_token(spotifyUsername, scope='playlist-modify-public',
                                   client_id=spotifyClientId,
                                   client_secret=spotifyClientSecret, redirect_uri='http://localhost/')
sp = spotipy.Spotify(token)
sp.trace = False


def get_playlist_id():
    playlists = sp.current_user_playlists()
    for i in playlists['items']:
        if i['name'] == 'Group Playlist':
            return i['id']


group_playlist_id = get_playlist_id()
from webapp import models

admin = Admin(app, name='Dashboard', index_view=AdminView(models.User, db.session, url='/admin', endpoint='admin'))
admin.add_view(ModelView(models.Song, db.session))
admin.add_view(ModelView(models.Playlist, db.session))

from webapp import routes
