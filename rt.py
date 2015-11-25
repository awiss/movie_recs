import requests
import time


def getMovieInfo(title, movies, actors, actors_movies):
    found = False
    page = 1
    movie = None
    print "Title:" + title
    while not found:
        time.sleep(.2)
        r = requests.get("http://api.rottentomatoes.com/api/public/v1.0/movies.json?apikey=kd3eptsp45wtmkgpsw5zywu2&q=%s&page_limit=1&page=%d" % (title, page))
        page += 1
        if page > 5:
            print "done"
            return 0
        if len(r.json()['movies']) > 0:
            movie = r.json()['movies'][0]
            print movie['title']
            if str(movie['title']).strip() == str(title).strip() and movie['year'] > 1999:
                found = True
        else:
            print "no movies: " + title
            return 0
    if 'ratings' not in movie or movie['ratings']['critics_score'] is None or movie['ratings']['critics_score'] < 0:
        print "no ratings"
        return 0

    try:
        if (int(movie['ratings']['critics_score']) < 0):
            print "negative critic score"
            return 0
    except:
        print "not int for critics_score"
        return 0

    movies.write("\t".join([str(movie['id']), str(movie.get('runtime', 'NULL')), str(movie.get('year','NULL')), movie['title'], movie['synopsis'], movie.get('critics_consensus', 'NULL'), str(movie['ratings']['critics_score']), str(movie['ratings']['audience_score'])]) + "\n")
    for member in movie['abridged_cast']:
        actors.write("%s\t%s\n" % (member['id'], member['name']))
        actors_movies.write("%s\t%s\n" % (member['id'], movie['id']))
    return 1

with open('movie_list.txt','r') as f:
    titles = f.readlines()
    with open('movies', 'w') as movies:
        with open('actors', 'w') as actors:
            with open('actors_movies', 'w') as actors_movies:
                total = 0
                for title in titles:
                    total += getMovieInfo(title, movies, actors, actors_movies)
                    print total

                print "%d written" % total

