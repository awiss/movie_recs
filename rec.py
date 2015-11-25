# All the Imports 
import psycopg2
from flask import Flask
from flask import request
from flask import jsonify

app = Flask(__name__)

# Returns recommended movies for a given user id
# Logic is that selects all critics who liked the movies that the user liked, and then returns the other movies that those critics liked too
# A critic's "Like" is based on value LIMIT_CONST
@app.route('/rec', methods=['GET'])
def make_rec():
	user_id = int(request.args.get('id', ''))
	conn = psycopg2.connect(host="movies.cfgdweprellz.us-east-1.rds.amazonaws.com", port=5432, database="project", user="cis450", password="450movies")
	cur = conn.cursor()
	LIMIT_CONST = 0.7
	cur.execute("SELECT * FROM reviews WHERE critic_name in (SELECT critic_name FROM reviews WHERE movie_id in (SELECT movie_id FROM users_rate WHERE user_id = %s and rating = 1) and reviews.score >= %s) and reviews.score >= %s and reviews.movie_id NOT IN (SELECT movie_id FROM users_rate WHERE user_id = %s and rating = 1)", (user_id, LIMIT_CONST, LIMIT_CONST, user_id))
	rows = cur.fetchall()
	return_dict = {}
	for row in rows:
		movie_id = row[0]
		cur.execute("SELECT title, synopsis FROM movies WHERE movies.id = %s", (movie_id))
		rows2 = cur.fetchall()
		return_dict[rows2[0]] = rows2[1]
	return flask.jsonify(**return_dict)

if __name__ == "__main__":
    app.run()





