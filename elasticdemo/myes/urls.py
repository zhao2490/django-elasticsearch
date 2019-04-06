from django.urls import re_path, path
from myes.views import IndexView, ArticleView

urlpatterns = [
    re_path('^$', IndexView.as_view()),
    re_path('article/(\w+)', ArticleView.as_view())
]