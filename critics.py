import requests
import time


def writeCriticInfo(id, reviews):
    done = False
    page = 1
    movie = None
    parsed = 0
    while True:
        time.sleep(.2)
        r = requests.get("http://api.rottentomatoes.com/api/public/v1.0/movies/%s/reviews.json?apikey=kd3eptsp45wtmkgpsw5zywu2&page_limit=30&page=%d" % (id, page))

        page += 1
        data = r.json()
        if len(data['reviews']) > 0:

            for review in data['reviews']:
                parsed += 1
                critic = review['critic']
                score = None
                if 'original_score' in review:
                    try:
                        spl = review['original_score'].split('/')
                        score = float(spl[0])/float(spl[1])
                    except:
                        pass
                if score is None:
                    if review['freshness'] == 'fresh':
                        score = .75
                    else:
                        score = .25

                reviews.write("%s\t%0.4f\t%s\n" % (id, score, critic))
        if parsed >= data['total']:
            break



with open('movies','r') as f:
    with open('reviews', 'w') as reviews:
        i = 0
        for line in f:
            print i
            id = line.split('\t')[0]
            writeCriticInfo(id, reviews)
            i+=1

