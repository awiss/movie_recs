from flask import render_template, request, redirect, url_for, session
from globals import get_db_conn

# Route for signing up a new user
def signup():
    if request.method == 'GET':
        return render_template('signup.html')
    else:
        if request.form['password'] != request.form['password_conf']:
            return redirect(url_for('signup'))

        email = str(request.form['email'])
        conn = get_db_conn()
        cursor = conn.cursor()
        cursor.execute("SELECT id, pw_hash FROM users where email = %s LIMIT 1", (email,))
        result = cursor.fetchone()
        if result is not None:
            print "User exists"
            return redirect(url_for('login'))

        cursor.execute("INSERT into users (email, pw_hash) VALUES (%s, %s)", (email, request.form['password']))
        conn.commit()
        cursor.execute("SELECT id FROM users WHERE email = %s", (email,))
        res = cursor.fetchone()
        cursor.close()
        conn.close()

        session['user_id'] = res[0]
        session['email'] = email

        return redirect(url_for('index'))


