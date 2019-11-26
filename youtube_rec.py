import requests
from bs4 import BeautifulSoup
import json, csv
import os, re


import sys; sys.stdin = open('Youtube_code.txt', 'r')
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
res = sys.stdin.readlines()
print(type(res))
lst = set()

for e in res:
    e = e.strip(',\n')
    lst.add(e.strip("'"))

lst= list(lst)
you_li = {}

for i in lst:
    codes = {
            i: {
                'you_code': i,
                
            }
        }
    you_li.update(codes)


# with open(os.path.join(BASE_DIR, 'youtube.json'), 'w+') as json_file:
#     json.dump(lst, json_file)


with open(os.path.join(BASE_DIR, 'youtube.csv'), 'w', encoding='UTF-8', newline='') as f:
    fieldnames = ['you_code']
    write = csv.DictWriter(f, fieldnames=fieldnames)
    write.writeheader()
    for you in you_li.values():
        # print(dat)
        write.writerow(you)
