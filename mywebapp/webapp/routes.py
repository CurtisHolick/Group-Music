from flask import render_template, flash, redirect, url_for, request
from webapp import app, db, sp, group_playlist_id
from webapp.forms import LoginForm
from flask_login import current_user, login_user, logout_user, login_required
from webapp.models import User, Song, Playlist
from werkzeug.urls import url_parse
from webapp.forms import RegistrationForm, AddSongForm, SongSelectionForm


# TODOm: add admin abilities(create playlist)
# TODOm: add more account restrictions? (email verification?, i have to confirm?)
# TODO: add password reset


@app.route('/')
@app.route('/index')
@login_required
def index():
    return render_template('index.html', title='Home', header_title='Home', playlist_code=group_playlist_id)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data.lower()).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Login', header_title='Login', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data.lower(), email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been successfully created')
        return redirect(url_for('login'))
    return render_template('register.html', title='New Account', header_title='Create New Account', form=form)


@app.route('/user/<username>', methods=['GET', 'POST'])
@login_required
def user(username):
    db_user = User.query.filter_by(username=username).first_or_404()
    # user = current_user
    # songs = current_user.songs.all()
    songs = db_user.songs.all()
    # print('Method= ', request.method)

    if request.method == 'POST' and db_user == current_user:
        for i in range(len(songs)):
            if request.form.get('name'+str(i+1)):
                remove_song_from_playlist(db_user.songs[i].spotify_id)
                db.session.delete(db_user.songs[i])

                db.session.commit()
                flash('Song successfully deleted!')
                songs = db_user.songs.all()
                redirect(url_for('user', username=username))
        # if request.form.get('name3') == 'delete':
        #     print("delete 3")
        # elif request.form.get('name2') == 'delete':
        #     print("delete 2")
    return render_template('user.html', title='My Songs', header_title='My Songs', user=db_user, songs=songs)


@app.route('/add_song', methods=['GET', 'POST'])
@login_required
def add_song():
    if len(current_user.songs.all()) >= 5:
        flash('You already have the maximum amount of songs. Delete some before adding more.')
        return redirect(url_for('user', username=current_user.username))
    form = AddSongForm()
    if form.validate_on_submit():
        query = form.query.data
        q = query
        search_results = sp.search(q=q, type='track', limit=5)
        simplified_results = []
        for result in search_results['tracks']['items']:
            simplified_results.append(result['id'])
        return redirect(url_for('search', query=q, results=simplified_results))
    return render_template('add_song.html', title='Add song', header_title='Find a Song', form=form)


# TODO: make url only have query
@app.route('/search/<query>/<results>', methods=['GET', 'POST'])
@login_required
def search(query, results):
    parsed_results = results.replace('[', '').replace(']', '').replace("'", '').split(', ')
    selection_form = SongSelectionForm()
    selection_form.song_radio_buttons.choices = [('1', 'song1'), ('2', 'song2'), ('3', 'song3'), ('4', 'song4'), ('5', 'song5')]

    # if selection_form.validate_on_submit() and len(current_user.songs.all()) < 5:
    #     print('submit')
    #     selected_song = request.form['song_radio_buttons']
    #     print('selected_song: ', selected_song)
    #     selected_id = parsed_results[int(selected_song)-1]
    #     s = Song(spotify_id=selected_id, user_id=current_user.id, playlist_id=1)
    #     db.session.add(s)
    #     db.session.commit()
    #     # flash('Song successfully added to database!')
    #     add_song_to_playlist(selected_id)
    #     flash('Song successfully added!')
    #     return redirect(url_for('user', username=current_user.username))

    if request.method == 'POST' and len(current_user.songs.all()) < 5:
        for i in range(len(parsed_results)):
            if request.form.get('name' + str(i + 1)):
                print('====BUTTON====: ', 'name' + str(i + 1))
                print('SONGS: ', parsed_results)
                print("====Song====: ", parsed_results[i])
                selected_id = parsed_results[i]
                s = Song(spotify_id=selected_id, user_id=current_user.id, playlist_id=1)
                db.session.add(s)
                db.session.commit()
                add_song_to_playlist(selected_id)
                flash('Song successfully added!')
                return redirect(url_for('user', username=current_user.username))

    form = AddSongForm()
    if form.validate_on_submit():
        # search form submit
        query = form.query.data
        q = query
        search_results = sp.search(q=q, type='track', limit=5)
        simplified_results = []
        for result in search_results['tracks']['items']:
            simplified_results.append(result['id'])
        return redirect(url_for('search', query=q, results=simplified_results))
    return render_template('inline_search_results.html', title='Search results', header_title='Search Results', query=query, results=parsed_results, selection_form=selection_form, form=form)


def add_song_to_playlist(song_spotify_id):
    """Add song to spotify playlist"""
    sp.user_playlist_add_tracks('legosail2424', group_playlist_id, [song_spotify_id])
    # flash('Song successfully added to spotify playlist!')


def remove_song_from_playlist(song_spotify_id):
    sp.user_playlist_remove_all_occurrences_of_tracks('legosail2424', group_playlist_id, [song_spotify_id])


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html', title='404 page not found', header_title='404')


@app.route('/info')
def info():
    return render_template('info.html', title='Information', header_title='About')


@app.route('/mission')
def mission():
    return render_template('mission.html', title='Mission', header_title='Our Mission')


@app.route('/testimonials')
def testimonials():
    return render_template('testimonials.html', title='Testimonials', header_title='Testimonials')


# TODO: REMOVE BEFORE COMPLETED - TO MAKE SURE CSS IS REFRESHED
import os
@app.context_processor
def override_url_for():
    return dict(url_for=dated_url_for)

def dated_url_for(endpoint, **values):
    if endpoint == 'static':
        filename = values.get('filename', None)
        if filename:
            file_path = os.path.join(app.root_path,
                                     endpoint, filename)
            values['q'] = int(os.stat(file_path).st_mtime)
    return url_for(endpoint, **values)

