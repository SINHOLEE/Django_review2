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