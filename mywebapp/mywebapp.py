from webapp import app, db
from webapp.models import User, Song, Playlist


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Song': Song, 'Playlist': Playlist}
