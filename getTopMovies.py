import requests
from bs4 import BeautifulSoup

for i in xrange(2000, 2016):
    r = requests.get('http://www.boxofficemojo.com/yearly/chart/?yr=%d&p=.htm' % i)

    soup = BeautifulSoup(r.text, 'html.parser')

    rows = soup.find_all('table')[6].find_all("tr")[2:102]
    for row in rows:
        print row.find("td").find_next_sibling().get_text()
