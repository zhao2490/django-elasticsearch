from django.db import models

# Create your models here.

class Blog(models.Model):
    title = models.CharField(max_length=128)
    img_url = models.CharField(max_length=4096)
    content = models.TextField()
    uid = models.CharField(max_length=64)
    blog_tag = models.ForeignKey('Tag',on_delete=True)


class Tag(models.Model):
    title = models.CharField(max_length=64)