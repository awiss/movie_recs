from flask import Flask, send_from_directory, g, session, make_response
from routes import rec, landing, signup, index, logout
from flask import render_template, request, session, url_for, redirect
from authomatic.adapters import WerkzeugAdapter
from authomatic import Authomatic
from config import CONFIG
from globals import get_db_conn
from pprint import pprint


app = Flask(__name__, static_folder='front_end')

app.config['DEBUG'] = True
app.add_url_rule('/', 'landing', landing.landing, methods=['GET', 'POST'])
app.add_url_rule('/recommendations', 'recommendations', rec.show_rec, methods=['GET'])
app.add_url_rule('/landing', 'landing', landing.landing, methods=['GET', 'POST'])
app.add_url_rule('/logout', 'logout', logout.logout, methods=['GET'])
app.add_url_rule('/signup', 'signup', signup.signup, methods=['GET', 'POST'])
app.add_url_rule('/index', 'index', index.index, methods=['GET'])


authomatic = Authomatic(config=CONFIG, secret='some random secret string')
@app.route('/login/fb', methods=['GET', 'POST'])
def fb():
    # We need response object for the WerkzeugAdapter.
    response = make_response()
    
    # print authomatic
    # Log the user in, pass it the adapter and the provider name.
    result = authomatic.login(WerkzeugAdapter(request, response), 'fb')
    print result
    
    # If there is no LoginResult object, the login procedure is still pending.
    if result:
        if result.user:
            # We need to update the user to get more info.
            result.user.update()
            conn = get_db_conn()
            cursor = conn.cursor()
            cursor.execute("SELECT id, pw_hash FROM users where email = %s LIMIT 1", (result.user.name,))
            user = cursor.fetchone()
            print user
            if user is None:
                cursor.execute("INSERT into users (email, pw_hash) VALUES (%s, %s)", (result.user.name, result.user.id))
                conn.commit()
                cursor.execute("SELECT id FROM users WHERE email = %s", (result.user.name,))
                user = cursor.fetchone()
            session['user_id'] = user[0]
            session['email'] = result.user.name
            cursor.close()
            conn.close()
        # The rest happens inside the template.
            return redirect(url_for('index'))
        else :
            return redirect(url_for('landing'))
    return response

@app.route('/<path:path>')
def send_js(path):
	return send_from_directory('front_end', path)

@app.teardown_appcontext
def teardown_db(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

if __name__ == "__main__":
    app.run()



