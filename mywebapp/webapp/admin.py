from flask_admin.contrib.sqla import ModelView
from flask import session, redirect, url_for, request, flash
from flask_login import current_user

admins = ['curtis']


class AdminView(ModelView):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.static_folder = 'static'

    def is_accessible(self):
        return current_user.username in admins

    def inaccessible_callback(self, name, **kwargs):
        if not self.is_accessible():
            flash('Bad admin page request')
            print(admins, session.get('user'))
            return redirect(url_for('index', next=request.url))
