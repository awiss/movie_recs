import requests
import time
import os
from globals import connect_to_database


conn = connect_to_database()
cursor = conn.cursor()

cursor.execute("SELECT id, title, year FROM movies WHERE poster_url ISNULL")

for result in cursor.fetchall():
    time.sleep(.2)
    id, title, year = result

    r = requests.get("http://api.themoviedb.org/3/search/movie?api_key=3aa487434ba1c3a4b38d0694bbfa3345&query=%s&year=%d"
                     % (title, year))
    search_results = r.json()
    if search_results is not None:
        if 'results' in search_results and len(search_results['results']) > 0:
            poster_path = search_results['results'][0].get('poster_path')
            if poster_path is not None:
                poster_url = os.path.join("image.tmdb.org/t/p/w500", poster_path[1:])
                cursor.execute("UPDATE movies SET poster_url = %s WHERE id = %s", (poster_url, id))
                print title, year
            else:
                print title, year, "poster_path none"
        else:
            print title, year, "no results"
    else:
        print title, year, "no json"

conn.commit()
cursor.close()
conn.close()




