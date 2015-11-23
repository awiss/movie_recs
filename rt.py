import requests


r = requests.get("http://api.rottentomatoes.com/api/public/v1.0/lists/movies.json?apikey=kd3eptsp45wtmkgpsw5zywu2")
print r.json()
