from django.db import models

# Create your models here.
class Article(models.Model):
    title = models.CharField(max_length=20) # max_length는 필수 속성
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True) # 데이터가 새로 추가되었을 때만.
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        ordering = ('-pk', )