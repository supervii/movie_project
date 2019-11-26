import requests
from bs4 import BeautifulSoup
import json, csv
import os, re

## python파일의 위치
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

req = requests.get('http://ticket2.movie.daum.net/Movie/MovieRankList.aspx?')
html = req.text
soup = BeautifulSoup(html, 'html.parser')
my_titles = soup.select(
    'div > strong > a'
    )
my_poster = soup.select(
    'a > span.thumb_poster > img'
)

res = []
data = {}
for title in my_titles:
    res.append(title.get('href'))
    for i in res:
        
        i = i[-10:]
        txt = title.text
        txt = txt.replace('\r\n                                                ','')
        datum = {
            txt: {
                'np_title': txt,
                'code': i,
            }
        }
        data.update(datum)
print(data)


# with open(os.path.join(BASE_DIR, 'result.json'), 'w+') as json_file:
#     json.dump(data, json_file)

with open(os.path.join(BASE_DIR, 'result.csv'), 'w', encoding='UTF-8', newline='') as f:
    fieldnames = ['np_title','code']
    write = csv.DictWriter(f, fieldnames=fieldnames)
    write.writeheader()
    for dat in data.values():
        # print(dat)
        write.writerow(dat)
