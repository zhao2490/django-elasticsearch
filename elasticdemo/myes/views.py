from django.shortcuts import render
from django.views import View
# Create your views here.
from elasticsearch import Elasticsearch
from myes.models import Blog, Tag
from django.http import JsonResponse
import json

es = Elasticsearch()


class IndexView(View):
    def get(self, request):
        tag_obj = Tag.objects.all()
        return render(request, 'index.html', {'tag_obj': tag_obj})

    def post(self, request):
        TAGS_LIST = ['文章', '问答', '讲堂', '头条']
        search_msg = request.POST.get('search_msg')
        action_type = request.POST.get('action_type')
        if action_type not in TAGS_LIST:
            action_type = ' '.join(TAGS_LIST)
        body = {
            "size": 2,
            "query": {
                "bool": {
                    "must": [
                        {
                            "match": {
                                "title": search_msg
                            }
                        },
                        {
                            "match": {
                                "action_type": action_type
                            }
                        }
                    ]
                }
            },
            "highlight": {
                "pre_tags": "<b style='color:red;font-size:16px;'>",
                "post_tags": "</b>",
                "fields": {
                    "title": {}
                }
            }
        }
        res = es.search(index='sifou', doc_type='doc', body=body, filter_path=['hits.total', 'hits.hits'])
        print(res)
        return JsonResponse(res)


class ArticleView(View):
    def get(self, request,uid):
        article_obj = Blog.objects.filter(uid=uid).first()
        content = article_obj.content.split(r'<img>img_node</img>')
        url_list = json.loads(article_obj.img_url)
        article_content = ''
        i = 0
        try:
            for line in content:
                article_content += line
                article_content += '<br/>'
                article_content += "<img src=%s>"%url_list[i]
                i += 1
        except IndexError:
            for line in content[i:]:
                article_content += line
        article_content.replace(r'\r','<br/>')
        article_content.replace(r'\n','<br/>')
        return render(request, 'article.html', {'article_title': article_obj.title,'article_content':article_content},)
