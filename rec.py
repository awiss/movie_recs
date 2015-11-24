# All the Imports 
import psycopg2


# Returns recommended movies for a given user id
# Logic is that selects all critics who liked the movies that the user liked, and then returns the other movies that those critics liked too
# A critic's "Like" is based on value LIMIT_CONST
def make_rec(user_id):
	LIMIT_CONST = 0.7
	cur.execute("SELECT * FROM critic_review WHERE critic_id in (SELECT critic_id FROM critic_review WHERE movie_id in (SELECT movie_id FROM users_rate WHERE user_id = %s and rating = 1) and critic_review.score >= %s) and critic_review.score >= %s and critic_review.movie_id NOT IN (SELECT movie_id FROM users_rate WHERE user_id = %s and rating = 1)", (user_id, LIMIT_CONST, LIMIT_CONST, user_id))
	rows = cur.fetchall()
	return_dict = {}
	for row in rows:
		movie_id = row[0]
		cur.execute("SELECT name, synopsis FROM movies WHERE movies.id = %s", (movie_id))
		rows2 = cur.fetchall()
		return_dict[rows2[0]] = rows2[1]
	return return_dict




#### MAIN PROGRAM ####

conn = psycopg2.connect(host="movies.cfgdweprellz.us-east-1.rds.amazonaws.com", port=5432, database="project", user="cis450", password="450movies")
cur = conn.cursor()



