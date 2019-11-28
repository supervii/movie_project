# :clapper: 영화 추천 웹 사이트 구축 프로젝트

> 팀명: 15G==90000
> 팀원 : 신정우, 이길현



## 1. 목표

* Django를 이용한 영화 추천 웹 사이트 구축한다.
* API를 사용하여 seed data 수집한다.
  * TMDB API, 네이버 영화 검색 API, The Movie DB API, 영화진흥위원회 API, OpenWeatherMap API
* **Django ORM을 사용**하여 Database에 접근 / data읽기 / filter



## 2. 사용 기술

* Python 3.7.x
* Django 2.1.x
* HTML5 + CSS3 + Javascript



## 3. 데이터 베이스 설계

![노트북 (5) 2](https://user-images.githubusercontent.com/52685245/69785859-7d4f4800-11fc-11ea-8190-d2cdf912404f.png)

## 4. 주요 기능

> Database에 있는 Data들을 사용하기 위하여 orm을 이용해 Database에 접근하고, 필요한 Data를 읽어와 다양한 영화 추천 서비스 기능을 개발

1. **회원가입 / 로그인 / 로그아웃**
   * 회원 가입 시 선호 장르를 선택 
   * 로그인 시 검색 , 좋아요 및 평점 남기기 가능 
   * 소셜 로그인 구축 (카카오,구글,네이버)



2. **User 회원가입(닉네임, 자기소개, 선호장르 선택)** 

   <img width="1432" alt="Screen Shot 2019-11-28 at 4 37 36 PM" src="https://user-images.githubusercontent.com/52685245/69786674-3eba8d00-11fe-11ea-88c0-7839b600ce25.png">



3. **소셜어카운트를 이용한 로그인도 가능 **

   <img width="1427" alt="Screen Shot 2019-11-28 at 4 38 18 PM" src="https://user-images.githubusercontent.com/52685245/69786781-690c4a80-11fe-11ea-95f2-ae8af27594b4.png">

4. **User의 프로필 페이지**

   1. 유저의 관련정보, 프로필 수정, 탭으로의 이동, 팔로잉, 팔로워의 현황을 볼 수 있다.
   2. 비동기식으로 팔로잉, 언팔로우를 구현했다.
   
   <img width="1434" alt="Screen Shot 2019-11-28 at 4 42 26 PM" src="https://user-images.githubusercontent.com/52685245/69786901-b25c9a00-11fe-11ea-9e1b-4e1ec7d66b13.png">
   <img width="1434" alt="Screen Shot 2019-11-28 at 4 42 38 PM" src="https://user-images.githubusercontent.com/52685245/69786908-b4bef400-11fe-11ea-8d90-f04ba32c7d4a.png">

5. **프로필 수정페이지**

   1. 기존의 정보를 가져와 수정해서 업데이트 가능

   <img width="1434" alt="Screen Shot 2019-11-28 at 5 14 38 PM" src="https://user-images.githubusercontent.com/52685245/69788796-965af780-1202-11ea-8986-f4dd763f1bc9.png">

6. **Movie main 페이지**

   1. 현재 상영 중인 20개의 영화의 이미지를 가져오고 가져온 데이터로 직접 해당 영화 예매 가능
   2. 최신 개봉 순으로 영화를 50개를 가져와 25개를 무작위로 선정 후 5개의 높은 평점 영화 추천
   3. 유튜브 채널을 랜더해와서 영화추천 채널의 동영상을 디비에 저장, 저장된 동영상을 무작위 재생
   4. 관리자 계정으로 로그인 시 영화정보 추가 및 수정이 가능하며, 유저의 리스트를 확인 가능

   <img width="1434" alt="Screen Shot 2019-11-28 at 4 50 49 PM" src="https://user-images.githubusercontent.com/52685245/69787203-59d9cc80-11ff-11ea-8008-bcb891d17c33.png">
   <img width="1434" alt="Screen Shot 2019-11-28 at 4 51 04 PM" src="https://user-images.githubusercontent.com/52685245/69787205-59d9cc80-11ff-11ea-96d4-aec268232112.png">
   <img width="1434" alt="Screen Shot 2019-11-28 at 4 51 12 PM" src="https://user-images.githubusercontent.com/52685245/69787206-59d9cc80-11ff-11ea-8f68-5f11186edebe.png">
   <img width="1434" alt="Screen Shot 2019-11-28 at 4 51 20 PM" src="https://user-images.githubusercontent.com/52685245/69787207-5a726300-11ff-11ea-9838-4fe956f0a9da.png">

   

7. **Movie Search**

   1. nav 바의 검색을 통해 영화의 정보를 검색하여 보여주는 페이지
   2. 장르 선택을 통해 장르 별 영화를 볼수 있다.

   <img width="1434" alt="Screen Shot 2019-11-28 at 5 07 54 PM" src="https://user-images.githubusercontent.com/52685245/69788370-b342fb00-1201-11ea-939c-6c0c9955c87e.png">

8. **Movie Detail 페이지**

   1. 영화의 모든 정보를 가져와서 보여준다.
   2. 비동기식 좋아요를 구현했다.
   3. 관련 유튜브 트레일러를 보여준다
   4. 작성된 리뷰와 평점 작성자를 볼 수 있다.
   5. 1~10 점까지 별을 통해 평점이 가능

   <img width="1434" alt="Screen Shot 2019-11-28 at 5 17 10 PM" src="https://user-images.githubusercontent.com/52685245/69789031-141f0300-1203-11ea-9ad6-28a570aba4bd.png">
   <img width="1434" alt="Screen Shot 2019-11-28 at 5 17 36 PM" src="https://user-images.githubusercontent.com/52685245/69789032-141f0300-1203-11ea-97b6-f91a3c9e74d5.png">
   <img width="1434" alt="Screen Shot 2019-11-28 at 5 17 51 PM" src="https://user-images.githubusercontent.com/52685245/69789034-14b79980-1203-11ea-8505-d3a8bf54ff01.png">

   