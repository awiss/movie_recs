from flask import render_template, request, session, redirect, url_for
from globals import get_db_conn

def index():
    if request.method == 'GET':
        user_id = session.get('user_id')
        if user_id is not None:
            conn = get_db_conn()
            cursor = conn.cursor()
            cursor.execute("SELECT id, title, year, poster_url FROM movies WHERE id NOT IN " +
                               "(SELECT movie_id FROM users_rate WHERE user_id = %s) " +
                           "ORDER BY random() LIMIT 1", (user_id,))
            result = cursor.fetchone()
            if result is None:
                return "Error, could not find movie. Please try again later", 500

            if 'rating' in request.args and 'movie_id' in request.args:
                movie_id = int(request.args['movie_id'])
                rating = int(request.args['rating'])
                cursor.execute("SELECT 1 FROM users_rate WHERE user_id = %s and movie_id = %s", (user_id, movie_id))
                if cursor.fetchone() is None:
                    cursor.execute("INSERT INTO users_rate VALUES (%s, %s, %s)", (user_id, movie_id, rating))
                else:
                    cursor.execute("UPDATE users_rate SET rating = %s WHERE user_id = %s and movie_id = %s",
                                   (rating, user_id, movie_id))
                conn.commit()
            cursor.close()

            return render_template('index.html', movie_id=result[0], title=result[1], year=result[2], poster_url=result[3])
        else:
            return redirect(url_for('login'))
