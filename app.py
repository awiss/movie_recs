from flask import Flask, send_from_directory, g
from routes import rec, login, signup, index

app = Flask(__name__, static_folder='front_end')

app.config['DEBUG'] = True

app.add_url_rule('/recommendations', 'recommendations', rec.show_rec, methods=['GET'])
app.add_url_rule('/login', 'login', login.login, methods=['GET', 'POST'])
app.add_url_rule('/logout', 'logout', login.logout, methods=['GET'])
app.add_url_rule('/signup', 'signup', signup.signup, methods=['GET', 'POST'])
app.add_url_rule('/index', 'index', index.index, methods=['GET'])

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



