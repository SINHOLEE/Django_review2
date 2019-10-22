from django.db import models
from django.conf import settings

# Create your models here.

class Article(models.Model):
    title = models.CharField(max_length=20) # max_length는 필수 속성
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True) # 데이터가 새로 추가되었을 때만.
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    # n:n 관계를 좋아요 기능으로 구현한다. article과 user의 관계
    liked_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='liked_articles')
    # user model을 불러올때는 꼭! settings.AUTH_USER_MODEL로 접근한다. (중요!)
    # article.liked_users.all()
    # user.liked_articles.all()
    class Meta:
        ordering = ('-pk', )


class Comment(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='comments')
    content = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='comments')
    class Meta:
        ordering = ('-pk',)
    def __str__(self):
        return self.content


