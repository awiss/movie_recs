import psycopg2
import random
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
  outer_dict = []
  cur.execute("SELECT movie_id FROM users_rate WHERE user_id = %s and rating = 1", (user_id,))
  movies = cur.fetchall()
  for movie in movies:
    movie_id = movie[0]

    cur.execute("SELECT movie_id FROM reviews WHERE critic_name IN (SELECT critic_name FROM reviews WHERE movie_id = %s and reviews.score >=%s) AND reviews.score >= %s AND reviews.movie_id NOT IN (SELECT movie_id FROM users_rate WHERE user_id = %s and rating = 1) AND reviews.movie_id NOT IN (SELECT movie_id FROM users_rate WHERE user_id = %s and rating = 0)",  (movie_id, LIMIT_CONST, LIMIT_CONST, user_id,user_id))
    names = cur.fetchall()
    random.shuffle(names)
    cur.execute("SELECT title FROM movies WHERE id = %s", (movie_id,))
    indextuple = cur.fetchone()
    i = 0
    inner = []
    for row in names:
      if i == 10:
        break
      movie_id2 = row[0]
      cur.execute("SELECT title, year, poster_url,synopsis FROM movies WHERE movies.id = %s", (movie_id2,))
      rows2 = cur.fetchall()
      inner.append(rows2)
      i = i + 1
    outer_dict.append((indextuple,inner))
  cur.close()
  return outer_dict


def show_rec():
  user_id = session.get('user_id')
  if user_id is None:
    return redirect(url_for('login'))
  else:
    recs = get_recs(user_id)
    print recs
    return render_template("recommendations.html", recs=recs, email=user_id)
