from decouple import config
from pprint import pprint
from datetime import datetime, timedelta
import requests
import csv

key = config('KOBIS_KEY')
tmdb_key = config('TMDB_KEY')
CLIENT_ID = config('NAVER_CLIENT_ID')
CLIENT_SECRET = config('NAVER_CLIENT_SECRET')
HEADERS = {
    'X-Naver-Client-Id': CLIENT_ID,
    'X-Naver-Client-Secret': CLIENT_SECRET
    }

kobis_base_url = 'http://www.kobis.or.kr/kobisopenapi/webservice/rest/boxoffice/searchWeeklyBoxOfficeList.json?weekGb=0&'
kobis_movie_url = 'http://www.kobis.or.kr/kobisopenapi/webservice/rest/movie/searchMovieInfo.json'
naver_url = 'https://openapi.naver.com/v1/search/movie.json'
tmdb_url = 'https://api.themoviedb.org/3/search/movie'


# result = {}			
# for i in range(50):
#     daytime = datetime(2019, 11, 26) - timedelta(weeks=i)
#     targetDt = daytime.strftime('%Y%m%d')

#     kobis_boxoffice_api_url = f'{kobis_base_url}key={key}&targetDt={targetDt}'

#     api_data = requests.get(kobis_boxoffice_api_url).json()
#     weekly_boxoffice_list = api_data.get('boxOfficeResult').get('weeklyBoxOfficeList')

#     for movie in weekly_boxoffice_list:
#         code = movie.get('movieCd')
#         if code not in result:
#             result[code] = {
#                 'movieCd': movie.get('movieCd'),
#                 'movieNm': movie.get('movieNm'),
#                 'openDt': movie.get('openDt'),
#                 'audiAcc': movie.get('audiAcc'),
#                 'targetDt': targetDt
#             }

# with open('boxoffice.csv', 'w', newline='', encoding='UTF-8') as f:
#     fieldnames = ('movieCd', 'movieNm', 'openDt', 'audiAcc', 'targetDt')
#     writer = csv.DictWriter(f, fieldnames=fieldnames)

#     writer.writeheader()

#     for value in result.values():
#        writer.writerow(value)



# 개별 영화 정보 정리하기
movies = {}
movieCodes = []
movieNames = []
genres = {'가족': 1, '공포(호러)': 2, '드라마': 3, '멜로/로맨스': 4,
            '미스터리': 5, '사극': 6, '스릴러': 7, '액션': 8, '어드벤처': 9, '판타지': 10, '코미디': 11,
            '애니메이션': 12, '범죄': 13, '다큐멘터리': 14, 'SF': 15, '전쟁':16, '공연': 17, '기타': 18}
with open('boxoffice.csv', 'r', encoding='UTF-8', newline='') as f:
    reader = csv.DictReader(f)
    for row in reader:
        movieCodes.append(row['movieCd'])
        movieNames.append(row['movieNm'])

for i in range(len(movieCodes)):
    kobis_full_url = f'{kobis_movie_url}?key={key}&movieCd={movieCodes[i]}'
    naver = requests.get(f'{naver_url}?query={movieNames[i]}', headers=HEADERS).json()
    tmdb = requests.get(f'{tmdb_url}?api_key={tmdb_key}&language=ko-kr&query={movieNames[i]}').json()
    # kobis: 영진위
    kobis = requests.get(kobis_full_url).json()
    info = kobis['movieInfoResult']['movieInfo']
    #naverData: 네이버 영화 데이터
    # pprint(naver)
    naverData = naver['items'][0]
    # pprint(naverData)
    movieCode = info['movieCd']
    title = info['movieNm']

    if tmdb['results'] == []:
        description = None
    else:
        description = tmdb['results'][0]['overview']

    year = info['prdtYear']
    genre = info['genres'][0]['genreNm']
    for genre_key, genre_value in genres.items():
        if genre == genre_key:
            genre = genre_value

    grade = info['audits'][0]['watchGradeNm']
    if tmdb['results'] == []:
        poster_path = None
    else:
        poster_key = tmdb['results'][0]['poster_path']
        poster_path = f'https://image.tmdb.org/t/p/w780/{poster_key}'
    
    if tmdb['results'] == []:
        youtube_url = None
    else:
        movieId = tmdb['results'][0]['id'] 
        mdb = requests.get(f'https://api.themoviedb.org/3/movie/{movieId}/videos?api_key={tmdb_key}&language=ko-kr').json()
        
        if mdb['results'] == []:
            youtube_url = None
        else:
            # pprint(mdb['results'][0]['key'])
            movieKey = mdb['results'][0]['key']
            youtube_url = f'https://www.youtube.com/embed/{movieKey}'

    rate = naverData['userRating']

    if tmdb['results'] == []:
        backdrop_path = None
        release_date = None
    else:
        backdrop_key = tmdb['results'][0]['backdrop_path']
        backdrop_path = f'https://image.tmdb.org/t/p/original/{backdrop_key}'
        release_date = tmdb['results'][0]['release_date']

    
    if len(info['directors']) != 0:
        director = info['directors'][0]['peopleNm']
    else:
        director = None
    if len(info['actors']) != 0:
        actors = []
        for i in range(len(info['actors'])):
            actors.append(info['actors'][i]['peopleNm'])
    else:
        actors = None
    
    movieInfo = { 
        title: 
                {
                    'movieCode': movieCode,
                    'title': title,
                    'year': year,
                    'release_date': release_date,
                    'description': description,
                    'genre': genre,
                    'director': director,
                    'grade': grade,
                    'actors': actors,
                    'poster_path': poster_path,
                    'backdrop_path': backdrop_path,
                    'youtube_url': youtube_url,
                    'rate': rate
        }
    }
    movies.update(movieInfo)
    print(title)

with open('movieDetail.csv', 'w', encoding='UTF-8', newline='') as f:
    fieldnames = ['movieCode', 'title', 'year', 'release_date', 'description', 'genre', 'director', 'grade', 'actors', 'poster_path', 'backdrop_path', 'youtube_url', 'rate']
    write = csv.DictWriter(f, fieldnames=fieldnames)
    write.writeheader()
    for mov in movies.values():
        write.writerow(mov)