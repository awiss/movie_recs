from flask import request, session, url_for, redirect
from globals import get_db_conn

def logout():
    if request.method == 'GET':
        session.pop('user_id', None)
        session.pop('email', None)
        return redirect(url_for('landing'))