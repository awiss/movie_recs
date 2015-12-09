import psycopg2
from flask import request, session, redirect, url_for, render_template
from globals import get_db_conn

# Returns recommended movies for a given user id
# Logic is that it for each "rated" movie, it selects movies with the same genre has the "rated movie" and which were liked by at least one critic who also enjoyed the "rated" movie
# A critic's "Like" is based on value LIMIT_CONST
def get_recs(user_id):
    conn = get_db_conn()
    cur = conn.cursor()
    LIMIT_CONST = 0.7
    print user_id
    print LIMIT_CONST

    #Start new code
    outer_dict = {}
    cur.execute("SELECT movie_id FROM users_rate WHERE user_id = %s and rating = 1", (user_id))
    movies = cur.fetchall()
    for movie in movies:
      movie_id = movie[0]
      cur.execute("SELECT genre FROM movies_genres WHERE movie_id = %s", (movie_id))
      genre = cur.fetchone()[0]
      cur.execute("WITH critics as (SELECT critic_name FROM reviews WHERE movie_id = %s and reviews.score >=LIMIT_CONST), SELECT * FROM reviews INNER JOIN movies_genres ON movies_genres.movie_id = reviews.movie_id WHERE critic_name in critics AND reviews.score >= %s AND genre = %s", (movie_id, LIMIT_CONST, LIMIT_CONST, genre)
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

    cur.close()
    return outer_dict


def show_rec():
    user_id = session.get('user_id')
    if user_id is None:
        return redirect(url_for('login'))
    else:
        recs = get_recs(user_id)
        return render_template("recommendations.html", recs=recs, email=user_id)
