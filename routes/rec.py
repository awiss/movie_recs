import psycopg2
from flask import request, session, redirect, url_for, render_template
from globals import get_db_conn

# Returns recommended movies for a given user id
# Logic is that it selects all critics who liked the movies that the user liked, and then returns the other movies
# that those critics liked too.
# A critic's "Like" is based on value LIMIT_CONST
def get_recs(user_id):
    conn = get_db_conn()
    cursor = conn.cursor()
    LIMIT_CONST = 0.7
    print user_id
    print LIMIT_CONST
    cursor.execute("SELECT title, year, poster_url, synopsis FROM movies WHERE id IN "
                       "(SELECT movie_id FROM (SELECT DISTINCT movie_id, score FROM reviews WHERE " +
                           "critic_name in " +
                               "(SELECT critic_name FROM reviews WHERE movie_id in " +
                                   "(SELECT movie_id FROM users_rate WHERE user_id = %s and rating = 1) " +
                               "and reviews.score >= %s) " +
                           "and reviews.score >= %s " +
                           "and reviews.movie_id NOT IN " +
                               "(SELECT movie_id FROM users_rate WHERE user_id = %s) " +
                            "ORDER BY score LIMIT 30) recommendations)",

                   (user_id, LIMIT_CONST, LIMIT_CONST, user_id))
    rows = cursor.fetchall()
    cursor.close()
    return rows


def show_rec():
    user_id = session.get('user_id')
    if user_id is None:
        return redirect(url_for('login'))
    else:
        recs = get_recs(user_id)
        return render_template("recommendations.html", recs=recs, email=user_id)
