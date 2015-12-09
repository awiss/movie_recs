import psycopg2
from flask import request
from flask import jsonify

# Returns recommended movies for a given user id
# Logic is that selects all critics who liked the movies that the user liked, and then returns the other movies that those critics liked too
# A critic's "Like" is based on value LIMIT_CONST
def make_rec():
	user_id = int(request.args.get('id', ''))
	conn = psycopg2.connect(host="movies.cfgdweprellz.us-east-1.rds.amazonaws.com", port=5432, database="project", user="cis450", password="450movies")
	cur = conn.cursor()
	LIMIT_CONST = 0.7
	cur.execute("SELECT * FROM reviews WHERE critic_name in (SELECT critic_name FROM reviews WHERE movie_id in (SELECT movie_id FROM users_rate WHERE user_id = %s and rating = 1) and reviews.score >= %s) and reviews.score >= %s and reviews.movie_id NOT IN (SELECT movie_id FROM users_rate WHERE user_id = %s and rating = 1)", (user_id, LIMIT_CONST, LIMIT_CONST, user_id))
	rows = cur.fetchall()

	#Start new code
	outer_dict = {}
	cur.execute("SELECT movie_id FROM users_rate WHERE user_id = %s and rating = 1", (user_id))
	movies = cur.fetchall()
	for movie in movies:
		movie_id = movie[0]
		cur.execute("SELECT genre FROM movies_genres WHERE movie_id = %s", (movie_id))
		genre = cur.fetchone()[0]
		cur.execute("WITH critics as (SELECT critic_name FROM reviews WHERE movie_id = %s), SELECT * FROM reviews INNER JOIN movies_genres ON movies_genres.movie_id = reviews.movie_id WHERE critic_name in critics AND reviews.score >= %s AND genre = %s", (movie_id, LIMIT_CONST, genre)
		ids = cur.fetchall()
		cur.execute("SELECT title, poster_url FROM movies WHERE movie.id = %s", movie_id)
		indextuple = cur.fetchone()
		inner_dict = {}
		for row in ids:
			movie_id2 = row[0]
			cur.execute("SELECT title, synopsis FROM movies WHERE movies.id = %s", (movie_id2))
			rows2 = cur.fetchall()
			inner_dict[rows2[0]] = rows2[1]
		outer_dict[indextuple] = innder_dict
	return jsonify(**outer_dict)

