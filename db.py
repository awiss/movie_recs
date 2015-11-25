import psycopg2


conn = psycopg2.connect(host="movies.cfgdweprellz.us-east-1.rds.amazonaws.com", port=5432, database="project", user="cis450", password="450movies")
cursor = conn.cursor()
with open('reviews', 'r') as f:
    cursor.copy_from(f, 'reviews', null='NULL')
    cursor.close()
conn.commit()
conn.close()

