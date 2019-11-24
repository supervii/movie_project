from django.shortcuts import render, redirect, get_object_or_404

from django.contrib.auth import get_user_model
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponse

from django.views.decorators.http import require_POST

from movies.models import Movie
from .models import Profile
from .forms import UserCustomCreationForm, ProfileForm


# 0. 메인 페이지
def main(request):
    return render(request, 'accounts.html')

# 1. 관리자만 접근할 수 있는 User관리 CRUD
# 1-1. User 리스트 조회
def list(request):
    if request.user.is_superuser:
        User = get_user_model()
        users = User.objects.all()
        context = {'users': users}
        return render(request, 'accounts/user_list.html', context)
    else:
        return HttpResponse('관리자 계정으로 로그인 하세요.')


# 2. User들이 접근할 수 있는 CRUD
# 2-1. 회원가입
def signup(request):
    user = get_user_model()
    profile = Profile()
    # print(request.user)
    # print(profile.genre)
    if request.method == 'POST':
        signup_form = UserCustomCreationForm(request.POST)
        profile_form = ProfileForm(request.POST)
        if signup_form.is_valid() and profile_form.is_valid():
            user = signup_form.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            auth_login(request, user)
            return redirect('movies:index')
    else:
        signup_form = UserCustomCreationForm()
        profile_form = ProfileForm()
    context = {'signup_form': signup_form, 'profile_form': profile_form}
    return render(request, 'accounts/signup.html', context)

# 2-2. 로그인
def login(request):
    if request.method == 'POST':
        login_form = AuthenticationForm(request, request.POST)
        if login_form.is_valid():
            auth_login(request, login_form.get_user())
            return redirect('movies:index')
    else:
        login_form = AuthenticationForm()
    context = {'login_form': login_form}
    return render(request, 'accounts/login.html', context)

# 2-3. 로그아웃
def logout(request):
    auth_logout(request)
    return redirect('accounts:login')

# 2-4. 유저 상세페이지
# 찜한 영화 추가하기
def detail(request, user_pk):
    User = get_user_model()
    userDetail = get_object_or_404(User, pk=user_pk)
    context = {'userDetail': userDetail}
    return render(request, 'accounts/detail.html', context)

# 2-5. 팔로우
def follow(request, user_pk):
    User = get_user_model()
    userDetail = get_object_or_404(User, pk=user_pk)

    if request.user not in userDetail.follower.all():
        userDetail.follower.add(request.user)
    else:
        userDetail.follower.remove(request.user)
    return redirect('accounts:detail', user_pk)

