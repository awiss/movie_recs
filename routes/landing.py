import psycopg2
from flask import render_template, request, session, url_for, redirect
from globals import get_db_conn

# Routes for login and logout
def landing():
    if request.method == 'GET':
        user_id = session.get('user_id')
        if user_id is None:
            return render_template('landing.html')
        else :
            return redirect(url_for('index'))
    else:
        conn = get_db_conn()
        cursor = conn.cursor()
        print request.form
        cursor.execute("SELECT id, pw_hash FROM users where email = %s LIMIT 1", (str(request.form['email']),))
        result = cursor.fetchone()
        cursor.close()
        if result is None:
            print "No user"
            return redirect(url_for('landing'))

        if request.form['password'] == result[1]:
            session['user_id'] = result[0]
            session['email'] = str(request.form['email'])
            return redirect(url_for('index'))
        else:
            print "Wrong PW"
            return redirect(url_for('landing'))



