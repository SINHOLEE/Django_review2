from django.shortcuts import render, redirect

# UserCreationForm : 유저계정 생성, AuthenticationForm : 세션 생성(로그인 하기!)
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm  # django가 제공하는 로그인 관련 기능
from django.contrib.auth import login as auth_login # 로그인을 하기위한 로직을 임포트 한다.
from django.contrib.auth import logout as auth_logout # 로그아웃을 하기위한 로직을 임포트 한다.
from django.views.decorators.http import require_POST
from IPython import embed
# Create your views here.
#


def signup(request):
    if request.user.is_authenticated:
        return redirect('articles:index')


    if request.method == "POST":  # 포스트 요청을 받으면 회원가입 해주세요
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()  # form.save() 가 반환하는 정보는 사용자의 정보이다. ==  get_user()
            auth_login(request, user)
            return redirect('articles:index')
        
    else: # get요청을 받으면 회원가입 가능한 창을 반환해 주세요
        form = UserCreationForm()
    context = {
        'form' : form,
    }
    return render(request, 'accounts/signup.html', context)


def login(request):  # 로그인은 세션 데이터를 만드는 것
    if request.user.is_authenticated:
        return redirect('articles:index')

    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())  # get_user(): 사용자의 정보를 주는 함수, AuthenticationForm메소드 안에만 있는 함수
            next_page = request.GET.get('next') # next라는 parametor를 달아로그인 페이지로 보낸다. ex) http://127.0.0.1:8000/accounts/login/?next=/articles/create/
            if next_page: # url정보에 next페이지라는 애가 있으면! 넥스트페이지로 보내고, 아니면 인덱스로 보내줘
                return redirect(next_page)
            else:
                return redirect('articles:index')

            # return redirect(next_page or 'articles:index')  # 위 로직과 동일한 코드
    else:
        form = AuthenticationForm()
    context = {
        'form' : form
    }
    return render(request, 'accounts/login.html', context)


def logout(request):
    auth_logout(request)
    return redirect('articles:index')


@require_POST
def delete(request):
    if request.user.is_authenticated:
        request.user.delete()
    return redirect('articles:index')