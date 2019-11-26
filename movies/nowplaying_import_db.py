import csv, io
from django.shortcuts import render
from .models import NowPlaying20, Movie

# Create your views here.
# CSV 로 받은 영화 정보를 django DB 로 import 하기 위한 별도 view 페이지 구성
def nowplaying(request):
    nowplays = NowPlaying20.objects.all()
    template = 'movie_upload.html'
    prompt = {
        'order': '겨울왕국 2,블랙머니,신의 한 수: 귀수편,82년생 김지영,터미네이터: 다크 페이트,윤희에게,엔젤 해즈 폴른,아이리시맨,날씨의 아이,대통령의 7시간,나를 찾아줘,어제 일은 모두 괜찮아,좀비랜드: 더블 탭,헤로니모,얼굴없는 보스,삽질,조커 ,아담스 패밀리,프란치스코 교황 : 맨 오브 히스 워드,벌새',
        'movies': nowplays,
    }
    if request.method == 'GET':
        return render(request, template, prompt)
    
    csv_file = request.FILES['file']

    data_set = csv_file.read().decode('UTF-8')

    io_string = io.StringIO(data_set)
    next(io_string)
    # print(data_set)
    for col in csv.reader(io_string):
        print(col)
        _, created = NowPlaying20.objects.update_or_create(
            title=col[0],
            code=col[1],
        )
    
    context = {}
    return render(request, template, context)