import functools
from typing import Callable
from flask import session, flash, redirect, url_for

def requires_login(f: Callable) -> Callable:
    @functools.wraps(f)
    def decorated(*args, **kwargs):
        if not session.get('email'):
            flash('You need to be logged in to view this page.', 'danger')
            return redirect(url_for('users.login'))
        return f(*args, **kwargs)
    return decorated

def redirect_if_login(f: Callable) -> Callable:
    @functools.wraps(f)
    def decorated(*args, **kwargs):
        if session.get('email'):
            flash('You cannot access this page while logged in.', 'danger')
            return redirect(url_for('users.profile'))
        return f(*args, **kwargs)
    return decorated
