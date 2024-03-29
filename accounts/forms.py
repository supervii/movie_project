from django import forms
from django.contrib.auth import get_user_model

from django.contrib.auth.forms import UserCreationForm, UserChangeForm



class UserCustomCreationForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = ('username', 'email', 'password1', 'password2', 'nickname', 'introduction', 'genre',)
    def __init__(self, *args, **kwargs):
        super(UserCustomCreationForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'placeholder': '사용자 이름'})
        self.fields['email'].widget.attrs.update({'placeholder': '이메일 주소'})
        self.fields['password1'].widget.attrs.update({'placeholder': '비밀번호'})
        self.fields['password2'].widget.attrs.update({'placeholder': '비밀번호 확인'})
        self.fields['nickname'].widget.attrs.update({'placeholder': '닉네임'})
        self.fields['introduction'].widget.attrs.update({'placeholder': '자기소개', 'class': 'input-field'})
        self.fields['genre'].widget.attrs.update({'placeholder': '선호 장르', 'class': 'input-field'})

class CustomProfileForm(UserChangeForm):
    password = None
    class Meta:
        model = get_user_model()
        fields = ('nickname', 'introduction', 'genre',)        
