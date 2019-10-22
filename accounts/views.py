from django.shortcuts import render, redirect
from .forms import CustomUserChangeForm
# UserCreationForm : 유저계정 생성, AuthenticationForm : 세션 생성(로그인 하기!)
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm, PasswordChangeForm # django가 제공하는 로그인 관련 기능
from django.contrib.auth import login as auth_login # 로그인을 하기위한 로직을 임포트 한다.
from django.contrib.auth import logout as auth_logout # 로그아웃을 하기위한 로직을 임포트 한다.
from django.contrib.auth import update_session_auth_hash  # 세션 정보가 바뀔 때 자동으로 해쉬값을 업데이트 해주는 기능
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required

from IPython import embed
# Create your views here.
#


def signup(request):
    if request.user.is_authenticated:
        return redirect('articles:index')


    if request.method == "POST":  # 포스트 요청을 받으면 회원가입 해주세요
        # embed()
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
    return render(request, 'accounts/form.html', context)


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
    return render(request, 'accounts/form.html', context)


def logout(request):
    auth_logout(request)
    return redirect('articles:index')


@require_POST
def delete(request):
    if request.user.is_authenticated:
        request.user.delete()
    return redirect('articles:index')


@login_required
def update(request):
    if request.method == 'POST':  # 포스트 요청을 받는다면 수정해주세요
        form = CustomUserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('articles:index')
    else:  # GET 요청을 받는다면 수정할 수 있는 페이지를 보여주세요
        # form = UserChangeForm(instance=request.user)  # request.user에  회원정보가 담겨져 있으므로 이를 인스턴스에 담아 논 상태로 반환해야 한다.

        form = CustomUserChangeForm(instance=request.user)  # 우리가 커스텀한 form 내용만 노출해서 사용자에게 제공한다.

    context = { 'form' : form }
    return render(request, 'accounts/form.html', context)        


@login_required
def password(request):
    if request.method =='POST':  # 실제 비밀번호 변경
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()  # 이렇게까지 하면 비밀번호는 변경이 되지만, 변경되고 나서 로그인이 풀린다. 왜? 비밀번호가 변경되면 세션에 저장되어 있던 데이터가 바뀌면서, 기존에 가지고 있던 세션값과 변경 후 세션이 달라지기 때문에 로그인 상태가 풀린다.
            update_session_auth_hash(request, user)  # (1, 2) 첫번째 인자 : request, 두번째인자 : user는 form.save()가 반환하는 값을 인자로 한다.
            return redirect('accounts:update')
    else:  # 사용자가 
        form = PasswordChangeForm(request.user)
    context = { 'form' : form }
    return render(request, 'accounts/form.html', context)