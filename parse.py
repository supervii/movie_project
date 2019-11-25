import requests
from bs4 import BeautifulSoup
import json
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

data = []
res = []

for title in my_titles:
    res.append(title.get('href'))
for i in res:
    i = i[-10:]
    data.append(i)
# print(data)
res = []
for poster in my_poster:
    res.append(poster.get('src'))
# print(res)

N = len(data)
codes = {}
for x in range(N):
    codes[data[x]] = res[x]

# print(codes)


with open(os.path.join(BASE_DIR, 'result.json'), 'w+') as json_file:
    json.dump(codes, json_file)
