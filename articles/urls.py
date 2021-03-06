from django.urls import path
from . import views

app_name = 'articles'  # 이름 지정하기
urlpatterns = [
    path('create/', views.create, name='create' ),
    path('', views.index, name='index'),
    path('<int:article_pk>/', views.detail, name='detail'),
    path('<int:article_pk>/update/', views.update, name='update'),
    path('<int:article_pk>/delete/', views.delete, name='delete'),
    path('<int:article_pk>/like/', views.like, name='like'),
    path('<int:article_pk>/comments/', views.comments_create, name='comments_create'),
    path('<int:article_pk>/comments/<int:comment_pk>/delete/', views.comments_delete, name='comments_delete'),
    # user_pk == 게시글 작성자의 유저 아이디
    path('<int:article_pk>/follow/<int:user_pk>/', views.follow, name='follow'),
    
]
