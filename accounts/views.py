from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import get_user_model
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm

from django.http import HttpResponse, JsonResponse, HttpResponseBadRequest
from django.views.decorators.http import require_POST

from movies.models import Movie
from .models import User
from .forms import UserCustomCreationForm, CustomProfileForm


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
    if request.user.is_authenticated:
        return redirect('movies:main')
    if request.method == 'POST':
        form = UserCustomCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('movies:main')
    else:
        form = UserCustomCreationForm()
    context = {'form': form,}
    return render(request, 'accounts/auth_form.html', context)


# 2-2. 로그인
def login(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            login_form = AuthenticationForm(request, request.POST)
            if login_form.is_valid():
                auth_login(request, login_form.get_user())
                return redirect('movies:main')
        else:
            login_form = AuthenticationForm()
        context = {'login_form': login_form}
        return render(request, 'accounts/login.html', context)
    else:
        return redirect('movies:main')


# 2-3. 로그아웃
def logout(request):
    auth_logout(request)
    return redirect('accounts:login')


# 2-4. 유저 업데이트
@login_required
def update(request):
    if request.method == 'POST':
        form = CustomProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('movies:main')
    else:
        form = CustomProfileForm(instance=request.user)
    context = {'form': form}
    return render(request, 'accounts/auth_form.html', context)


# 2-5. 유저 상세페이지
# 찜한 영화 추가하기
def detail(request, user_pk):
    userDetail = get_object_or_404(get_user_model(), pk=user_pk)
    context = {'userDetail': userDetail}
    return render(request, 'accounts/detail.html', context)

    
# 2-6. 팔로우
@login_required
def follow(request, user_pk):
    if request.is_ajax():
        userDetail = get_object_or_404(User, pk=user_pk)
        # if request.user in userDetail.follower.all():
        if userDetail.follower.filter(pk=request.user.pk).exists():
            userDetail.follower.remove(request.user)
            followed = False
        else:
            userDetail.follower.add(request.user)
            followed = True
        context = {'followed': followed, 'count': userDetail.follower.count(),}
        return JsonResponse(context)
    else:
        return HttpResponseBadRequest()
        # return redirect('accounts:detail', user_pk)
