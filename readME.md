 # review2

1. git bash

```bash
venv
python -m venv venv
```

2. shift + ctrl + p 해서 인터프리터 설정

3. django download

```bash
pip ilstall django
```



4. 어떤 모듈이 설치되어 있는지에 대한 정보를 저장하려면

```
pip freeze > requirements.txt
```

그 안에 있는 pip 모듈들..

```
Django==2.2.6
pytz==2019.3
sqlparse==0.3.0
```



4. -1 ) 모듈 다 지우기

```
pip freeze | xargs pip uninstall -y
```



4. -2) reqirements.txt에 있는 모듈 설치하기

```
pip install -r requirements.txt
```





### 1. Django project 생성

```bash
django-admin startproject review .
```

### 2. settings.py 설정

```python
LANGUAGE_CODE = 'ko-kr'

TIME_ZONE = 'Asia/Seoul'



# USE_I18N = False 라면, 랭귀지 코드를 바꾸더라도 번역하지 않겠다라는 의미.

```



### 3. app 생성

```python
python manage.py startapp articles
```



### 4. app 등록

settings.py / installed_apps에 등록하기

```python
INSTALLED_APPS = [

    # Local apps
    'articles',

    # Django apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

```



### 5. model 생성

```python
# Create your models here.
class Article(models.Model):
    title = models.CharField(max_length=20) # max_length는 필수 속성
    # content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True) # 데이터가 새로 추가되었을 때만.
    updated_at = models.DateTimeField(auto_now=True)

```



bash 

```bash
python manage.py makemigrations  # 신고하기 not 생성
python manage.py migrate  # 생성
```

- 현재 `content`  filed를 추가하지 않은 채 생성했다.



### 6. model Filed 추가

이미 반영되어 있는 데이터 베이스에 새로운 필드를 추가하는 방법

```bash
# 하기 전에 다음 모듈을 다운받아본다.
pip install django-extensions ipython
```

- `django-extensions`는 `settings.py`에 등록해야 쓸 수 있다.

```python
INSTALLED_APPS = [

    # Third party apps
    'django_extensions',
    
    ''''''
```

- 상황설명 : 기존 필드들로 DB가 생성되어 있는데, 새로운 필드를 추가할 경우, 어떻게 처리할까?를 해결해야한다.

```
python manage.py shell_plus
```

- `from articles.models import Article` 이문구가 뜨면 정상(?)이다... 이 말뜻은 우리가 생성한 DB모델이 정상적으로 생성? 적용? 되었다는 뜻

```shell
# shell_plus 안
In [2]: Article
Out[2]: articles.models.Article

In [3]: article = Article()

In [4]: article.title = '첫번째 타이틀'

In [10]: aritlcle.save()

In [8]: article2 = Article()

In [9]: article2.title = '두번째 타이틀'

In [12]: article2.save(
    ...: )
    
```

- 현재 디비에 어떤 데이터가 저장되어 있다는 상황을 표현함.



models.py

```python
class Article(models.Model):
    title = models.CharField(max_length=20) # max_length는 필수 속성
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True) # 데이터가 새로 추가되었을 때만.
    updated_at = models.DateTimeField(auto_now=True)

```



re-migrations 

```
python manage.py makemigrations
```

하면 다음과 같은 옵션을 선택하라고 나온다.

```bash
You are trying to add a non-nullable field 'content' to article without a default; we can't do that (the database needs something to populate existing rows).
Please select a fix:
 1) Provide a one-off default now (will be set on all existing rows with a null value for this column)  # 이전에 있는 데이터에 어떤값을 저장할 지 수동으로 제어한다.
 2) Quit, and let me add a default in models.py # 뒤로가서 default값을 주는 옵션을 부여하고 다시온다.
```

- 1번옵션을 선택한다. 왜?  : content의 경우 textfield이기 때문에 ~~~~
- 이전에 있는 모든 값에는 `''` 빈스트링 값을 부여한다.
- 현재 데이터 베이스에 반영되어있지 않는다. -> `migrate` 해야함

```bash
python manage.py migrate
```

### 7. CRUD using model form

`django`를 만지기 전에 환경세팅을 해보자. 

/.vscode/ settings.json

```json
{
    "python.pythonPath": "venv\\Scripts\\python.exe",

    "files.associations": {
        "**/templates/*.html": "django-html",
        "**/templates/*": "django-txt",
        "**/requirements{/**,*}.{txt,in}": "pip-requirements"
    },

    "emmet.includeLanguages": {"django-html": "html"},

    "[django-html]" : {
        "editor.tabSize": 2
    },

}
```

#### 1) 길을 열어주기

review라는 프로젝트에서 ->어떤 경로로 이동할 수 있도록 길을 틀어주기 위해 urlpath를 설정해야한다.

```python
from django.urls import path, include

urlpatterns = [
    path('articles/', include('articles.urls')),  # 새로 생성
    path('admin/', admin.site.urls),
]

```

- review라는 애에서 articles/로 접근하면  articles라는 어플의 `urls`로 보낸다.

#### 2) app에 urls.py 생성

1. create 기능 만들어보자.

```python
from django.urls import path
from . import views

app_name = 'articles'  # 이름 지정하기
urlpatterns = [
    path('create/', views.create, name='create' ),
]

```



#### 3) view 함수 생성

views.py

```
def create(request):
    if request.method == 'POST':
        # Article 생성 요청
        pass
    else:  # GET 요청
        # Article 을 생성하기 위한 페이지를 달라는 요청
        return render(request, 'articles/create.html')

```

#### 4) create.html 생성

- articles/templates/article/create.html 생성한다.



#### 5) base.html 템플레이트 생성하기

review/templates 생성 후 base.html 생성한다.

```html
<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta http-equiv="X-UA-Compatible" content="ie=edge">
  <title>{% block title %}{% endblock title %}</title>
</head>
<body>
  <header>
    <h1>저희 페이지에 오신걸 환영합니다.</h1>
  </header>
  {% block container %}{% endblock container %}
</body>
</html>
```



#### 6) create.html 생성(base.html 이용하여)

이렇게만 하면 오류뜬다 왜? review라는 project폴더의 templates도  templates 탐색공간에 추가해줘야 함.

-> settings.py / templates를 설정해야한다.

```python
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'review', 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]


```

- `        'DIRS': [os.path.join(BASE_DIR, 'review', 'templates')],` 의  뜻 :  base dir에서부터 조인한다. review라는 프로젝트의 templates라는 공간까지 확장해서 templates의 탐색범위로 인식하겠다.

#### 7) model forms.py

forms.py를 한번만 정의하면, views.py에서 일일히 form에 대한 정의를 하지 않아도 된다.

```python
from django import forms
from .models import Article

class ArticleForm(forms.ModelForm):

    class Meta:
        model = Article
        fields ='__all__'
```

#### 8) forms.py 적용

views.py에 forms.py를 적용하기 위해 import하고, 다음과 같이 작성한다.

```python
from django.shortcuts import render, redirect
from .forms import ArticleForm


def create(request):
    if request.method == 'POST':
        # Article 생성 요청
        form = ArticleForm(request.POST)  #사용자의 데이터를 가져오겠다ㅓ.
        if form.is_valid():
            form.save()  # 저장하겠다라는 코드
            return redirect('articles:index')
        pass
    else:  # GET 요청
        # Article 을 생성하기 위한 페이지를 달라는 요청

        form = ArticleForm()
        context = {'form' : form}
        return render(request, 'articles/create.html', context)

```

#### 9) detail 페이지 작성

1. urls.py

```
path('<int:article_pk>/', views.detail, name='detail'),

```

2. views.py

```python
def detail(request, article_pk):
    # 사용자가 적어보낸 article_pk를 통해 detail page를 보여준다.
    # 특정 한개의 article을 꺼내는 방법
    article = get_object_or_404(Article, pk=article_pk)
    context = {'article' : article}
    
    return render(request, 'articles/detail.html', context)


```

3. detail.html

```django
{% extends 'base.html' %}

{% block title %}Article::Detail{% endblock title %}

{% block container %}


<h2>{{ article.title }}</h2>
<p>{{ article.created_at }}</p>
<p>{{ article.content }}</p>
{% endblock container %}
```



#### 10) update logic 구현

1. urls.py

```
    path('<int:article_pk>/update/', views.update, name='update'),

```

2. views.py

```python
def update(request, article_pk):
    article = get_object_or_404(Article, pk=article_pk)
    if request.method == 'POST':
        form = ArticleForm(request.POST, instance=article)  # 기존에 존재하는 인스턴스 안에 새롭게 받은 데이터로 바꾸겠다.
        if form.is_valid():
            form.save()
            return redirect('articles:detail', article_pk)
        
    else: # GET으로 들ㅇ옴
        form = ArticleForm(instance=article)  # 특정 인스턴스를 form안에 넣은채로 form을 생성하겠다.
    context = {'form':form}
    return render(request,'articles/update.html',context )
```

3. update.html

```django
{% extends 'base.html' %}

{% block title %} Article::Update
{% endblock title %}

{% block container %}

{% comment %}  form이 필요함 왜? 입력할 창이 필요하니까 {% endcomment %}

<form method="post">
    {% csrf_token %}
    {{ form.as_p }}
  <button type="submit">수정하기</button>
</form>
{% endblock container %}
```



#### 11) delete logic 구현

views.py 에 `from django.views.decorators.http import require_POST, require_GET`를 임포트 한 뒤 

```python
@require_GET
def index(request):
    articles = Article.objects.all()
    
    return render(request, 'articles/index.html', {'articles': articles})


```

- `@require_GET` 혹은 `@require_POST`으로 view 함수들을 관리하면, 명시해놓은 `method`형태의 요청만 받아들이기 때문에 보안 측면에서 유리하다.



# 사용자 권한 승인 기능 구현

- 쿠키 : 웹 서비스 상에서 데이터 처리의 효율성을 높이기 위해 잃어버려도 괜찮은 데이터를 `사용자의 브라우저에` 임시저장하는 것

  **간단하게 브라우저에  key : value 형태로 저장되는 공간**

  

- 세션 : 사용자와 클라이언트의 상호작용한 데이터 중 변화가 있어서는 안되는 정보들(결제내역, 로그인 등)을 클라이언트의 서버상에서(`DB`, `file` 등) 관리하는 정보들

  **간단하게 서버에서 사용자의 정보를 관리하는 공간**

  

- 캐시 : 

- 전반적인 정리

유저 관련 form을 이용하기 때문에, 우리가 model을 작성할 필요가 없다.

로그인 : 서버에서 세션데이터를 생성

로그인한 상태 :  브라우저에 세션 키를 보유하고 있는 상태

로그인 상태 확인 : 브라우저가 가지고 있는 세션키를  매 요청마다 확인한다. 어떻게? 미들웨어를 통해

미들웨어 : 간단하게 django가 제공하는 확인 절차

로그인되어잇는 상태는 request에 저장되어 있다. 그렇기 때문에, templates에 보내지는 모든 request(return render (request, '<특정html>.html') )에 로그인 상태를 확인할 수 있는 정보가 들어있다. 

ex) `request.user.is_authenticated` TRUE면 로그인 되어있는 상태, FALSE면 로그인 되어있지 않는 상태.

views.py 와 html파일 안에서 로그인과 비로그인 상태를 관리하도록 한다.

## 1. 인증구현을 위한 초기 세팅



1. 새로운 app 생성(장고앱 안에는 이미 로그인 기능이 구현되어있기 때문에 불러서 쓰면 된다. 그 이름이 `accounts`이다. ) 

   > 중요!!! app 이름을 `accounts`로 관리해야 좋다.(꼭 그래야 하는 것은 아니지만 하는 것이 좋다.)

   ```bash
   python manage.py startapp accounts
   ```

2.  settings.py에 등록하기

   ```python
   INSTALLED_APPS = [
   
       # Local apps
       'articles',
       'accounts',
       # # Third party apps
       # 'django_extensions',
   
       # Django apps
       'django.contrib.admin',
       'django.contrib.auth',
       'django.contrib.contenttypes',
       'django.contrib.sessions',
       'django.contrib.messages',
       'django.contrib.staticfiles',
   ]
   ```

3.  review/urls.py에 accounts를 연결하는 작업

   ```python
   from django.contrib import admin
   from django.urls import path, include
   
   urlpatterns = [
       path('articles/', include('articles.urls')),
       path('accounts/', include('accounts.urls')),  # include의 의미가 accounts 앱에 있는 urls.py의 urlpatterns를 찾으라는 뜻이므로 accounts urls.py에 해당 변수가 있어야 한다.
       path('admin/', admin.site.urls),
   ]
   
   ```

4. accounts/urls.py 생성

# 2. 회원가입 구현

1. urls.py

   ```python
   from django.urls import path
   from . import views
   
   app_name = 'accounts'
   urlpatterns = [
       path('signup/', views.signup, name='signup' ),
   ]
   
   ```

2. views.py

   ```python
   from django.shortcuts import render, redirect
   from django.contrib.auth.forms import UserCreationForm  # django가 제공하는 로그인 관련 기능
   # Create your views here.
   
   
   
   def signup(request):
       if request.method == "POST":  # 포스트 요청을 받으면
           # 회원가입 해주세요
           form = UserCreationForm(request.POST)
           if form.is_valid():
               form.save()
               return redirect('articles:index')
           
       else: # get요청을 받으면 
           # 회원가입 가능한 창을 반환해 주세요
           form = UserCreationForm()
       context = {
           'form' : form,
       }
       return render(request, 'accounts/signup.html', context)
   ```

3. tempates/accounts 생성 후 signup.html 생성

   ```django
   {% extends 'base.html' %}
   
   {% block title %}Accounts::Signup
   {% endblock title %}
   
   {% block container %}
   <H2>회원가입</H2>
   {% comment %} view.signup에서  get 요청으로 이 페이지에 와있ㅎ기 때문에, 다시  form요청으로 보낼때는 action 이 필요없다.  {% endcomment %}
   <form  method="POST"> 
     {{ form.as_p }}
     {% csrf_token %}
     <input type="submit" value='회원가입'>
   </form>
   
   
   {% endblock container %}
   ```

4. 결과화면![1](C:\Users\student\Django\django_review2\images\1.JPG)

5. 잘 등록 되었는지 확인하기

   ```
   python manage.py createsuperuser
   ```

   ![캡처](C:\Users\student\Django\django_review2\images\캡처.JPG)

   - 파란색 동그라미가 새로 등록한 계정

# 3. 로그인 구현

1. urls.py

   ```python
   from django.urls import path
   from . import views
   
   app_name = 'accounts'
   urlpatterns = [
       path('signup/', views.signup, name='signup' ),
       path('login/', views.login, name='login'),
   ]
   ```

   

2. views.py 

   - 시나리오 : 로그인 창에서 로그인을 시도하는

   ```python
   def login(request):  # 로그인은 세션 데이터를 만드는 것
       if request.method == 'POST':
           form = AuthenticationForm(request, request.POST)
           if form.is_valid():
               auth_login(request, form.get_user())  # get_user(): 사용자의 정보를 주는 함수, AuthenticationForm메소드 안에만 있는 함수
               return redirect('articles:index')
       else:
           form = AuthenticationForm()
       context = {
           'form' : form
       }
       return render(request, 'accounts/login.html', context)
   ```

   - `AuthenticationForm` 만의 특이한 점 

   - `form = AuthenticationForm(request, request.POST)` 두개의 인자가 필요함.

   -         if form.is_valid():
                 auth_login(request, form.get_user())

   - `get_user()`: 사용자의 정보를 주는 함수, AuthenticationForm메소드 안에만 있는 함수

3. login.html

   ```django
   {% extends 'base.html' %}
   
   {% block title %}Accounts::Login
   {% endblock title %}
   
   {% block container %}
   <h2>로그인하기</h2>
   
     <form method="POST">
       {% csrf_token %}
       {{ form.as_p }}
       <button type="submit">로그인하기</button>
     </form>
     <form action=""></form>
   {% endblock container %}
   ```

4. 문제없이 로그인 했는지 확인하기![캡처2](C:\Users\student\Django\django_review2\images\캡처2.JPG)

- `sessionid`가 생성되어 있다면 정상적으로 로그인 성공했다는 뜻. `SQL EXPLORER` -> `django_seesion`을 확인해보면 다음과 같이 저장되어 있다.![캡처3](C:\Users\student\Django\django_review2\images\캡처3.JPG)

5. 로그인 되어있는 상태를 사용자에게 확인해주기 위해 `base.html` 수정

   ```python
   <!DOCTYPE html>
   <html lang="ko">
   <head>
     <meta charset="UTF-8">
     <meta name="viewport" content="width=device-width, initial-scale=1.0">
     <meta http-equiv="X-UA-Compatible" content="ie=edge">
     <title>{% block title %}{% endblock title %}</title>
   </head>
   <body>
     <header>
       <h1>저희 페이지에 오신걸 환영합니다.</h1>
       <p>Hello, {{ user.username }}</p>
     </header>
     <a href="{% url 'articles:index' %}">[목록]</a>
   <hr>
   
     {% block container %}{% endblock container %}
   </body>
   </html>
   ```

6. 결과창1.![캡처4](C:\Users\student\Django\django_review2\images\캡처4.JPG)

## 4. 로그아웃

1. urls.py

   ```python
   path('logout/', views.logout, name='logout'),
   ```

   

1. views.py

   ```python
   from django.contrib.auth import logout as auth_logout # 로그아웃을 하기위한 로직을 임포트 한다.
   
   def logout(request):
       auth_logout(request)
       return redirect('articles:index')
   
   ```

   ## 5. middleware(개념 정리 다시하기)

   - ```python
     # request안에 저장되어 있는 정보 확인하기
     form Ipython import embed
     
     def index(request):
         embed()
         articles = Article.objects.all()
         
         return render(request, 'articles/index.html', {'articles': articles})
     
     ```
```
     
   - ```shell
     In [6]: dir(request.user)
     Out[6]:
     ['DoesNotExist',
      'EMAIL_FIELD',
      'Meta',
      'MultipleObjectsReturned',
      'REQUIRED_FIELDS',
      'USERNAME_FIELD',
     	......
      'is_active',
      'is_anonymous',
      'is_authenticated',
      
     In [8]: request.user.is_anonymous
     Out[8]: False
     
     In [9]: request.user.is_authenticated
     Out[9]: True
     
     In [10]: request.user.username
     Out[10]: 'dltlsgh5'
      
```

  - 위 정보를 이용해 각 views.py 에서 랜더하는 함수들에 각 각 조건을 부여하여 다른 화면을 보여주면 로그인 유뮤에 따라 기능이 다른 웹서비스를 제공할 수 있다.
   
- 즉, 로그인과 로그인 하기 전의 기능을 분리하기 위해 `base.html`과 `views.py`를 수정한다.
  
     ```django
     # base.html
         {% if  user.is_authenticated  %}
           <p>
             <span>Hello, {{ user.username }}</span>
             <a href="{% url 'accounts:logout' %}">[로그아웃]</a>
           </p>
         {% else %}
             <a href="{% url 'accounts:login' %}">[로그인]</a>
             <a href="{% url 'accounts:signup' %}">[회원가입]</a>
         
         {% endif %}
     
  ```
  
  - header 안에 다음과 같이 분리한다.
  
- `signup`, `login`  에  다음과 같이 분기를 만든다.
  
     ```python
     def signup(request):
         if request.user.is_authenticated:
             return redirect('articles:index')
     	......
         
     def login(request):  # 로그인은 세션 데이터를 만드는 것
         if request.user.is_authenticated:
             return redirect('articles:index')
     	......
  ```
  
     

## 6. Actions for authenticated user

- 로그인 상태인 유저만 게시글을 생성하고, 수정하고, 삭제할 수 있도록 관리한다.

1. articles/index.html -> if 문으로 로그인 확인 상태 or 비로그인 상태를 파악하여 관리한다.

   ```django
   {% extends 'base.html' %}
   
   {% block title %} Article::Index
   {% endblock title %}
   
   {% block container %}
   
     {% if user.is_authenticated %}
       <h2>Article List</h2>
       <a href="{% url 'articles:create' %}">[생성하기]</a>
       <hr>
     {% else %}
       <h4>로그인 해야 게시글을 만들 수 있습니다.</h4>
     {% endif %}
     {% for article in articles %}
       <div>
         <h3>{{ article.pk }}. {{ article.title }}</h3><a href="{% url 'articles:detail' article.pk%}">[자세히보기]</a>
       </div>
       <br>
     {% endfor %}
   
   {% endblock container %} 
   ```

2. articles/views.py

   ```python
   from django.contrib.auth.decorators import login_required
   
   @login_required  
   def create(request):
       
       if request.method == 'POST':
           # Article 생성 요청
           form = ArticleForm(request.POST)  #사용자의 데이터를 가져오겠다ㅓ.
   	......
   ```

   - `@login_required` : 로그인 상태에서만 다음의 함수를 실행할 수 있고, 로그인 상태가 아니라면 로그인 창을 불러와 로그인 하도록 유도하는 기능
   - 만약 계정관리 앱 이름이 `accounts`가 아니라면, `@login_required(<app이름>/<로그인url>)`로 설정해야지 로그인 페이지를 불러오게 된다.
   - 하지만 현재 로그인 view함수는 무조건 index페이지로 반환하는 로직이었다.

3. accounts/views.py

   ```python
   def login(request):  # 로그인은 세션 데이터를 만드는 것
       if request.user.is_authenticated:
           return redirect('articles:index')
   
       if request.method == 'POST':
           form = AuthenticationForm(request, request.POST)
           if form.is_valid():
               auth_login(request, form.get_user())  # get_user(): 사용자의 정보를 주는 함수, AuthenticationForm메소드 안에만 있는 함수
               
               next_page = request.GET.get('next') 
               return redirect(next_page or 'articles:index')  
       else:
           form = AuthenticationForm()
       context = {
           'form' : form
       }
       return render(request, 'accounts/login.html', context)
   
   
   ```

   - `next_page = request.GET.get('next')` : next라는 param를 달아 로그인 페이지로 보낸다. 

     ex) http://127.0.0.1:8000/accounts/login/?next=/articles/create/
   
   - ```python
     if next_page: 
     	return redirect(next_page)
     else:
    	return redirect('articles:index')
     ```

     -  url정보에 next페이지라는 애가 있으면! 넥스트페이지로 보내고, 아니면 인덱스로 보내달라는 로직
   -  next_page = 'articles/create/' 정보가 담겨있다.
   
- ```python
     return redirect(next_page or 'articles:index')
     ```
   
     - 위 로직과 동일한 코드

4. articles/templates/articles/detail.html

   ```django
   {% extends 'base.html' %}
   
   {% block title %}Article::Detail{% endblock title %}
   
   {% block container %}
   
   
   <h2>{{ article.title }}</h2>
   <p>{{ article.created_at }}</p>
   <p>{{ article.content }}</p>
   
   {% if user.is_authenticated %}
   
     <a href="{% url 'articles:update' article.pk %}">[수정하기]</a>
     <form action="{% url 'articles:delete' article.pk %}" method = 'POST'>
       {% csrf_token %}
       <button type="submit">삭제하기</button>  
     </form>
     <form action="{% url 'articles:comments_create' article.pk %}" method='POST'>
       {% csrf_token %}
       {{ form.as_table }}   <button type="submit">댓글작성</button>
     </form>
   
   {% endif %}
   <hr>
   {% for comment in comments %}
     <li> 
     {% if user.is_authenticated %}
       <form action="{% url 'articles:comments_delete' article.pk comment.pk %}" method="POST"> 
         {% csrf_token %}
         <span>{{ comment.pk }}  {{ comment }} {{ comment.created_at }}</span>
         <button type="submit">댓글삭제</button>
       </form>
     {% else %}
       <span>{{ comment.pk }}  {{ comment }} {{ comment.created_at }}</span>
     {% endif %}
     </li>
   {% endfor %}
   {% endblock container %}
   ```

   - `{% if user.is_authenticated %}` : 사용자가 인증이 되어 있으면, `{% endif %}`까지 작성되어 있는 로직을 반환하라.
   - 로그인 하기 전 `detail`페이지 상태![캡처5](C:\Users\student\Django\django_review2\images\캡처5.JPG)
   - 로그인 후 `detail`페이지 상태![캡처6](C:\Users\student\Django\django_review2\images\캡처6.JPG)

## 7. 회원탈퇴

1. urls.py

   ```python
   path('delete/', views.delete, name='delete'),
   
   ```

2. views.py

   ```python
   from django.views.decorators.http import require_POST
   
   @require_POST
   def delete(request):
       if request.user.is_authenticated:
           request.user.delete()
       return redirect('articles:index')
   ```

   - `@require_POST` : 로그아웃을 하기  위한 로직을 임포트 한다.

# 유저와 게시글과의 1:N 관계 연결 

- 하나의 유저는 두 개 이상의 게시글을 작성할 수 있다.
- 한 명의 유저가 여러개의 게시글에 `좋아요` 누를 수 있다.
- 회원 정보를 변경할 수 있다.(비밀번호, 등등)

## 1. 회원 정보 수정

1. urls.py 

   ```python
   path('update/', views.update, name='update'),
   
   ```

   - `articles` 에서 `update`를 할때처럼 `variable route`가 필요 없는 이유는 로그인 된 상태가 이미 `request`에 있기 때문

2. views.py

   ```python
   from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm
   
   def update(request):
       if request.method == 'POST':  # 포스트 요청을 받는다면 수정해주세요
           pass
       else:  # GET 요청을 받는다면 수정할 수 있는 페이지를 보여주세요
           form = UserChangeForm(instance=request.user)      
           context = { 'form' : form }
           return render(request, 'accounts/update.html', context)        
   
   ```

   - `form = UserChangeForm(instance=request.user)`  : request.user에  회원정보가 담겨져 있으므로 이를 인스턴스에 담아 논 상태로 반환해야 한다.

3. update.html

   ```django
   {% extends 'base.html' %}
   {% block title %}
   Accounts::Update
   {% endblock title %}
   
   {% block container %}
   <h2>회원 정보 수정</h2>
   <form  method='POST'>  
     {% csrf_token %}
     {{ form.as_p }}
     <button type="submit">수정하기</button>
   </form>
   
   {% endblock container %}
   ```

   - `action`을  기존` view` 함수와 같다면, 생략가능 

4. ![캡처7](C:\Users\student\Django\django_review2\images\캡처7.JPG)

   - 회원 정보에서 불필요한 요소를 제거한 뒤 사용자에게 제공한다. 그렇게 하기 위해 `forms.py`를 생성하여 새롭게 구성한다.

5. forms.py

   ```python
   from django.contrib.auth.forms import UserChangeForm
   from django.contrib.auth import get_user_model  
   
   class CustomUserChangeForm(UserChangeForm):
       
       class Meta:
           model = get_user_model() 
           fields = ['email', 'first_name', 'last_name']  
   ```

   - `from django.contrib.auth import get_user_model` : 현재 활성화(active)된 `user model`을 `return` 하는 함수.
   - `model = get_user_model()`: 유저 모델이 어떤 형태인지 우리는 모른다. 그렇기 때문에 다음의 메서드를 임포트 한다.
   - fields = ['email', 'first_name', 'last_name'] : 우리가 원하는 `fields`만 넣어야 한다. 알 수 있는 방법은 두가지 있다. 1) admin 계정 이용, 2) api 쪼개기

6. views.py 수정

   ```python
   from .forms import CustomUserChangeForm
   
   def update(request):
       if request.method == 'POST':  # 포스트 요청을 받는다면 수정해주세요
           form = CustomUserChangeForm(request.POST, instance=request.user)
           if form.is_valid():
               form.save()
               return redirect('articles:index')
       else:  # GET 요청을 받는다면 수정할 수 있는 페이지를 보여주세요
           # form = UserChangeForm(instance=request.user)  
           form = CustomUserChangeForm(instance=request.user)
   
       context = { 'form' : form }
       return render(request, 'accounts/update.html', context)        
   
   ```

   - `from .forms import CustomUserChangeForm` : 커스텀한 모델폼만 사용자에게 제공한다.
   - form = CustomUserChangeForm(instance=request.user)` : 우리가 커스텀한 form 내용만 노출해서 사용자에게 제공한다.

7. base.html

   ```django
   <a href="{% url 'accounts:update' %}">[회원정보수정]</a>
   
   ```

8. 결과창 : @login_reqired가 필요![캡처8](C:\Users\student\Django\django_review2\images\캡처8.JPG)

9. views.py

   ```python
   from django.contrib.auth.decorators import login_required
   
   @login_required
   
   ```

   

## 2. 비밀번호 변경

1. urls.py

   ```python
   path('password/', views.password, name='password'),
   ```

2. views.py  : `PasswordChangeForm` 임포트

   ```python
   from django.contrib.auth.forms import PasswordChangeForm 
   
   def password(request):
       if request.method =='POST':  # 실제 비밀번호 변경
           pass
       else:  # 사용자가 
           form = PasswordChangeForm(request.user)
           context = { 'form' : form }
           return render(request, 'accounts/password.html', context)
   ```

   - `form = PasswordChangeForm(request.user)` : `update` 와는 다르게 `instance=`로 받지 않고 `request.user`로 바로 받는다.

3. password.html

   ```django
   {% extends 'base.html' %}
   
   {% block title %}Accounts::Password
   {% endblock title %}
   
   {% block container %}
   <h2>비밀번호 변경</h2>
   <form method="POST">
     {% csrf_token %}
     {{ form.as_p }}
     <button type="submit" class='btn btn danger'>변경하기</button>
   </form>
   {% endblock container %}
   
   
   
   ```

   

4. views.py 마무리

   ```python
   from django.contrib.auth import update_session_auth_hash  
   
   @login_required
   def password(request):
       if request.method =='POST':  # 실제 비밀번호 변경
           form = PasswordChangeForm(request.user, request.POST)
           if form.is_valid():
               user = form.save()  
               update_session_auth_hash(request, user)
               return redirect('accounts:update')
       else:  # 사용자가 
           form = PasswordChangeForm(request.user)
       context = { 'form' : form }
       return render(request, 'accounts/password.html', context)
   ```

   - `from django.contrib.auth import update_session_auth_hash` :  세션 정보가 바뀔 때 자동으로 해쉬값을 업데이트 해주는 기능
   - `user = form.save()` 이렇게까지 하면 비밀번호는 변경이 되지만, 변경되고 나서 로그인이 풀린다.  그 이유는 비밀번호가 변경되면 **세션에 저장되어 있던 데이터가 바뀌면서**, 기존에 가지고 있던 세션값과 변경 후 세션이 달라지기 때문이다. 
   - 이를 해결하기 위해 `update_session_auth_hash(request, user)`를 입력한다.
   - 첫번째 인자 : request, 두번째인자 : user는 form.save()가 반환하는 값을 인자로 한다.
   - `@login_required` : 로그아웃 상태에서 GET요청으로 접근하지 못하도록 제한한다.



## 3. html 통합하기

- templates/accounts/ html 의 세부내용을 제외하고는 비슷하다. 

- ```django
  {% extends 'base.html' %}
  
  {% block title %}Accounts
  {% endblock title %}
  
  {% block container %}
  
  {% if request.resolver_match.url_name == 'signup' %}
  <h2>회원가입</h2>
  {% elif request.resolver_match.url_name == 'login' %}
  <h2>로그인</h2>
  {% elif request.resolver_match.url_name == "update" %}
  <h2>내 정보 수정</h2>
  {% else %}  
  <h2>비밀번호 변경</h2>
  {% endif %}
  
    <form method="POST">
      {% csrf_token %}
      {{ form.as_p }}
      <button type="submit">submit</button>
    </form>
  
  {% endblock container %}
  ```

## 4. articles 데이터와 user data 연결하기(n:n관계)

- 다대 다 관계에서는 하나의 테이블을 추가로 만들어 관리해야한다.

-  유저모델을 불러올 때, 다른 모든곳에서는 `get_user_model  `을 써야하지만, models.py를 작성할때 만큼은 `settings.AUTH_USER_MODEL` 를 이용하여 가져온다.

- articles/models.py

  ```python
  from django.conf import settings
  
  class Article(models.Model):
      title = models.CharField(max_length=20) # max_length는 필수 속성
      content = models.TextField()
      created_at = models.DateTimeField(auto_now_add=True) # 데이터가 새로 추가되었을 때만.
      updated_at = models.DateTimeField(auto_now=True)
      user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
      class Meta:
          ordering = ('-pk', )
  
  ```

  - `    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)` : 중요!!! `get_user_model` 이 아니다.
  - `user` 는 이 아티클에 대한 한 명의 유저정보를 저장하고 있다.
  - 반대로, 유저가 작성한 모든 게시글을 보여달라고 할때는 `user.Article_set_all()`로 호출해야한다

- ```bash
  $ python manage.py makemigrations
  
  You are trying to add a non-nullable field 'user' to article without a default; we can't do that (the database needs something to populate existing rows).
  Please select a fix:
   1) Provide a one-off default now (will be set on all existing rows with a null value for this column)
   2) Quit, and let me add a default in models.py
  
  
  Select an option: 1
  Please enter the default value now, as valid Python
  The datetime and django.utils.timezone modules are available, so you can do e.g. timezone.now
  Type 'exit' to exit this prompt
  
  >>> 2
  Migrations for 'articles':
    articles\migrations\0004_article_user.py
      - Add field user to article
      
  $ python manage.py migrate
  Operations to perform:
    Apply all migrations: admin, articles, auth, contenttypes, sessions
  Running migrations:
    Applying articles.0004_article_user... OK
  ```

  - 1번을 선택했다는 뜻은, 현재 작성되어 있는 모든 게시글의 작성자를 임의로 설정하겠다는 뜻.
  - 그 다음 2번을 선택했다는 것은, 2번아이디가 다 게시했다고 수정한다는 뜻.

- views.py create

  ```python
  @login_required
  def create(request):
      if request.method == 'POST':
          # Article 생성 요청
          form = ArticleForm(request.POST)  # title, content
          
          if form.is_valid():
              article = form.save(commit=False)  # 저장하겠다라는 코드
              article.user = request.user
              article.save()
              return redirect('articles:detail', article.pk)
      else:  # GET 요청
          # Article 을 생성하기 위한 페이지를 달라는 요청
  
          form = ArticleForm()
      context = {'form' : form}
      
      return render(request, 'articles/create.html', context)
  
  ```

  - comment 댓글기능 구현할 때와 같이, `form.save()` 가 반환하는 데이터에서 게시글의 user 정보를 request.user 정보로 입력한 후 저장한다.

    ```python
                article = form.save(commit=False)  # 저장하겠다라는 코드
                article.user = request.user
                article.save()
    
    ```

    

- detail.html

  ```django
  {% if article.user == request.user %}
    <a href="{% url 'articles:update' article.pk %}">[수정하기]</a>
    <form action="{% url 'articles:delete' article.pk %}" method = 'POST'>
      {% csrf_token %}
      <button type="submit">삭제하기</button>  
    </form>
  
  {% endif %}
  
  ```

  - 이전까지는 `{% if user.is_authenticated %}` 로 로그인 유무를 판단하여 게시글 수정, 삭제 기능의 노출을 제어했다면, 이제는 게시글 작성한 본인만이 지울 수 있도록 `{% if article.user == request.user %}` 을 통해 제어한다.

  