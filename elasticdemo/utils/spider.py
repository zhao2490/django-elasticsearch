import os
import sys
from queue import Queue
from threading import Thread
from bs4 import BeautifulSoup
import json
import requests
from bs4.element import NavigableString
from elasticsearch import Elasticsearch
import uuid
import django

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) # 将项目路径添加到系统搜寻路径当中
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'elasticdemo.elasticdemo.settings') # 设置项目的配置文件
django.setup()  # 加载项目配置

from myes.models import Blog, Tag

es = Elasticsearch()

# 创建标签分类数据
# for i in ['文章', '问答', '讲堂', '头条']:
    # Tag.objects.create(title=i)

def get_art_content(url_temp):
    """
    获取文章具体内容
    :param url_temp:文章url
    :return:
    """
    tag_obj = Tag.objects.filter(id=1).first()
    url = "https://segmentfault.com%s" % url_temp
    print(url)
    headers = {
        'user-agent': 'user-agent: Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'
    }
    text = requests.get(url=url, headers=headers).text
    article = BeautifulSoup(text,'xml')
    art_title = article.select('#articleTitle a')[0].getText()
    art_image = article.select('div[class="article fmt article__content"] img')
    art_image_list = []
    for img in art_image:
        # 将文章中img标签的url取出放入数据库，并将原有tag内容改为"<img>img_node</img>",方便后面按照原有顺序插入图片
        art_image_list.append(img['src'])
        img.name = 'p'
        img.string = "<img>img_node</img>"
    art_image = json.dumps(art_image_list)
    art_content_html = article.select('div[class="article fmt article__content"]')
    art_content = ''
    for ele in art_content_html:
        if isinstance(ele,NavigableString):
            if ele.startswith('href="https://creativecommons.org/licenses/by-nc-nd'):
                break
            art_content += ele
        else:
            if ele.get_text().startswith('href="https://creativecommons.org/licenses/by-nc-nd'):
                break
            art_content += ele.get_text()
    uid = str(uuid.uuid4()).replace('-','')
    Blog.objects.create(
        title = art_title,
        img_url = art_image,
        content = art_content,
        uid = uid,
        blog_tag = tag_obj
    )
    body = dict(
        title=art_title,
        content=art_content,
        action_type=tag_obj.title,
        uid=uid
    )
    es.index(index='sifou',doc_type='doc',body=body)

def get_page_url(page_num):
    """
    爬取博客具体内容，创建本地数据
    :param page_num: 解析到每一篇博客的url
    :return:
    """
    url = 'https://segmentfault.com/blogs?page=%s' % page_num
    headers = {
        'user-agent': 'user-agent: Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'
    }

    html_text = requests.get(url=url, headers=headers).text
    soup = BeautifulSoup(html_text,'xml')
    art_list = soup.find_all('section')[0].select('div h2 a')
    for art in art_list:
        get_art_content(art['href'])


class ThreadPoolManager():
    """
    一个线程池
    """

    def __init__(self, thread_num):
        self.work_queue = Queue()
        self.thread_num = thread_num
        self.__init_threading_pool(self.thread_num)

    def __init_threading_pool(self, thread_num):
        for i in range(thread_num):
            t = ThreadManger(self.work_queue)
            t.start()

    def add_job(self, func, *args):
        self.work_queue.put((func, args))


class ThreadManger(Thread):
    """
    一个线程管理器
    """

    def __init__(self, work_queue):
        Thread.__init__(self)
        self.work_queue = work_queue
        self.daemon = False

    def run(self):
        while True:
            target, args = self.work_queue.get()
            target(*args)
            self.work_queue.task_done()


thread_pool = ThreadPoolManager(4)


def handle_task(page_start: int, page_end: int):
    """
    处理爬虫任务
    :param page_start: 起始页码,最小为1
    :param page_end: 结束页码
    :return:
    """
    if page_start < 1:
        page_start = 1
    for page_num in range(page_start, page_end):
        thread_pool.add_job(get_page_url, page_num)


handle_task(1, 5)