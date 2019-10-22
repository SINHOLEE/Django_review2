
from django.views.decorators.http import require_POST, require_GET
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .forms import ArticleForm, CommentForm
from .models import Article, Comment
from django.http import HttpResponse
from IPython import embed

# Create your views here.

@require_GET
def index(request):
    articles = Article.objects.all()
    return render(request, 'articles/index.html', {'articles': articles})


@require_GET
def detail(request, article_pk):
    # 사용자가 적어보낸 article_pk를 통해 detail page를 보여준다.
    # 특정 한개의 article을 꺼내는 방법
    article = get_object_or_404(Article, pk=article_pk)
    comments = article.comments.all()
    form = CommentForm()
    context = {
        'article' : article,
        'form' : form,
        'comments' : comments,  
        }
    return render(request, 'articles/detail.html', context)


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


@login_required
def update(request, article_pk):
    article = get_object_or_404(Article, pk=article_pk)

    if article.user == request.user:
        if request.method == 'POST':
            form = ArticleForm(request.POST, instance=article)  # 기존에 존재하는 인스턴스 안에 새롭게 받은 데이터로 바꾸겠다.
            if form.is_valid():
                form.save()
                return redirect('articles:detail', article_pk)
            
        else: # GET으로 들어옴
            form = ArticleForm(instance=article)  # 특정 인스턴스를 form안에 넣은채로 form을 생성하겠다.
    else:
        return redirect('articles:detail', article_pk)
    context = {'form':form}
    return render(request,'articles/update.html',context )


# @login_required  # 쓰지 않는 이유 : 어차피 next_page의 url을 받아오는 method가 GET이므로 require_POST 에서 막힌다. 그러므로 다른 로직을 사용한다.(1
@require_POST
def delete(request, article_pk):
    if request.user.is_authenticated:
        # article_pk에 맞는 article을 꺼낸다.
        article = get_object_or_404(Article, pk=article_pk)
        # 삭제한다.
        if article.user == request.user:
            article.delete()
        else:
            return redirect('articles:detail', article_pk)
    return redirect('articles:index')
    

def like(request, article_pk):
    # 유저와 아티클의 정보를 각 각 갖고 있어야 한다.
    user = request.user
    article = get_object_or_404(Article, pk=article_pk)
    if article.liked_users.filter(pk=user.pk).exists():
        user.liked_articles.remove(article)
    else:
        user.liked_articles.add(article)  # 유저가 좋아요 누른 아티클들에 현재 article을 추가하겠다.
    return redirect('articles:detail', article_pk)



@require_POST
def comments_create(request, article_pk):
    if request.user.is_authenticated:

        form = CommentForm(request.POST)
        article = get_object_or_404(Article, pk=article_pk)
        if form.is_valid():
            new_form = form.save(commit=False)
            new_form.article = article
            new_form.user = request.user
            new_form.save()
        return redirect('articles:detail', article_pk)
    return HttpResponse('You are Unauthorized : 401 ERROR', status=401)


@require_POST
def comments_delete(request, article_pk, comment_pk):
    if request.user.is_authenticated:

        comment = get_object_or_404(Comment, pk=comment_pk)
        
        if request.user == comment.user:
            comment.delete()
        else:
            return redirect('articles:index')

    return redirect('articles:detail', article_pk)
