import psycopg2
from flask import render_template, request, session, url_for, redirect
from globals import get_db_conn

# Routes for login and logout
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        conn = get_db_conn()
        cursor = conn.cursor()
        print request.form
        cursor.execute("SELECT id, pw_hash FROM users where email = %s LIMIT 1", (str(request.form['email']),))
        result = cursor.fetchone()
        cursor.close()
        if result is None:
            print "No user"
            return redirect(url_for('login'))

        if request.form['password'] == result[1]:
            session['user_id'] = result[0]
            session['email'] = str(request.form['email'])
            return redirect(url_for('index'))
        else:
            print "Wrong PW"
            return redirect(url_for('login'))


def logout():
    if request.method == 'GET':
        session.pop('user_id', None)
        session.pop('email', None)
        return redirect(url_for('login'))


