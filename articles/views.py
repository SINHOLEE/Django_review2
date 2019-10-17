
from django.views.decorators.http import require_POST, require_GET
from django.shortcuts import render, redirect, get_object_or_404
from .forms import ArticleForm, CommentForm
from .models import Article, Comment
from IPython import embed

# Create your views here.

@require_GET
def index(request):
    articles = Article.objects.all()
    
    return render(request, 'articles/index.html', {'articles': articles})


# @require_GET
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


def create(request):
    if request.method == 'POST':
        # Article 생성 요청
        form = ArticleForm(request.POST)  #사용자의 데이터를 가져오겠다ㅓ.
        # embed()
        if form.is_valid():
            form.save()  # 저장하겠다라는 코드
            
            return redirect('articles:index')
    else:  # GET 요청
        # Article 을 생성하기 위한 페이지를 달라는 요청

        form = ArticleForm()
    context = {'form' : form}
    
    return render(request, 'articles/create.html', context)


def update(request, article_pk):
    article = get_object_or_404(Article, pk=article_pk)
    if request.method == 'POST':
        form = ArticleForm(request.POST, instance=article)  # 기존에 존재하는 인스턴스 안에 새롭게 받은 데이터로 바꾸겠다.
        if form.is_valid():
            form.save()
            return redirect('articles:detail', article_pk)
        
    else: # GET으로 들어옴
        form = ArticleForm(instance=article)  # 특정 인스턴스를 form안에 넣은채로 form을 생성하겠다.
    context = {'form':form}
    return render(request,'articles/update.html',context )


# @require_POST
def delete(request, article_pk):
     # article_pk에 맞는 article을 꺼낸다.
    article = get_object_or_404(Article, pk=article_pk)
    # 삭제한다.
    article.delete()
    
    return redirect('articles:index')

@require_POST
def comments_create(request, article_pk):
    form = CommentForm(request.POST)
    article = get_object_or_404(Article, pk=article_pk)
    if form.is_valid():
        new_form = form.save(commit=False)
        new_form.article = article
        new_form.save()
    return redirect('articles:detail', article_pk)


@require_POST
def comments_delete(request, article_pk, comment_pk):
    comment = get_object_or_404(Comment, pk=comment_pk)
    comment.delete()

    return redirect('articles:detail', article_pk)
