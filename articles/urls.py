from django.urls import path
from . import views

app_name = 'articles'  # 이름 지정하기
urlpatterns = [
    path('create/', views.create, name='create' ),
    path('', views.index, name='index'),
    path('<int:article_pk>/', views.detail, name='detail'),
    path('<int:article_pk>/update/', views.update, name='update'),
    path('<int:article_pk>/delete/', views.delete, name='delete'),
]
