from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, Http404
from django.conf import settings
from django.core.paginator import Paginator  # 分页器
from django.db.models import Q  # 查询类对象
import json
from datetime import datetime
import jieba
from .models import Category, News, Comment
jieba.initialize()
with open("D:\\involuntary\\works\\missing-semester-of-python\\121\\part2\\my_news_website\\news\\banns.txt",
          encoding="utf-8") as f:
    wsx = f.readlines()
    stop_words = set(item.replace("\n", "") for item in wsx)
# Create your views here.


def index(request):
    """
    主页 搜索栏在做了在做了
    """
    random_news_set = News.objects.order_by('?')
    news_list_info = random_news_set[0:settings.INDEX_NEWS_COUNT]
    return render(request, 'index.html', {'news_list': news_list_info})


def search(request):
    dataxw = request.GET
    query = dataxw['query']
    sorting = dataxw['sort']
    if not dataxw.getlist("month"):
        month_list = ['1', '2', '3', '4']
    else:
        month_list = dataxw.getlist("month")
    all = None
    for item in month_list:
        if all is None:
            all = Category.objects.get(id=(int(item) + 7)).news_set.all()
        else:
            all |= Category.objects.get(id=(int(item) + 7)).news_set.all()
    time1 = datetime.now()
    if query:
        x_blink = Q(title__icontains=query) | Q(contenTxt__icontains=query)
        found_news_blink = None
        sera_list = [word for word in jieba.cut_for_search(query) if word not in stop_words]
        for item in sera_list:
            if found_news_blink is None:
                found_news_blink = (Q(title__icontains=item) | Q(contenTxt__icontains=item))
            else:
                found_news_blink &= (Q(title__icontains=item) | Q(contenTxt__icontains=item))
        found_news = all.filter(x_blink | found_news_blink)

        if found_news:
            flag = 1  # 查到有新闻
            if int(sorting) == 1:
                found_news = found_news.order_by("-read_num")
        else:
            found_news = []
            flag = 2  # 查出没新闻
    else:
        found_news = []
        flag = 0  # 就没好好查
    time2 = datetime.now()

    paginator = Paginator(found_news, 10) # 又到分页器大爷出场了
    page_number = int(request.GET.get('page', 1))  # 自动填充一个param，如果有page那就是page，没有就默认1
    if page_number > paginator.num_pages:
        page_number = paginator.num_pages
    elif page_number < 1:
        page_number = 1
    page = paginator.page(page_number)
    if page_number < 6:  # 没有别的工具，只能手动操作力
        if paginator.num_pages <= 10:
            page_range = range(1, paginator.num_pages + 1)
        else:
            page_range = range(1, 11)
    elif (page_number >= 6) and (page_number <= paginator.num_pages - 5):
        page_range = range(page_number - 5, page_number + 5)
    else:
        page_range = range(paginator.num_pages - 9, paginator.num_pages + 1)

    dic = {
        'flag': flag,
        'count': found_news.count() if flag == 1 else 0,
        'page': page,
        'news_found': found_news,
        'range': page_range,
        'current_num': page.number,
        'news': page.object_list,
        'num_pages': paginator.num_pages,
        'has_previous': page.has_previous(),
        'has_next': page.has_next(),
        'secs': (time2 - time1).total_seconds(),
        'month_list': month_list,
        'query': query,
        'sorting': sorting
    }
    return render(request, 'search.html', context=dic)

def detail(request, pk):
    """
    一条新闻的视图文件
    """
    news = get_object_or_404(News, pk=pk)
    news_data = {}
    news.read_num += 1
    news.save()  # 点击量得加进去
    config_x = json.loads(news.config)
    img_x = json.loads(news.img_config)
    content_x = news.content

    news_data = {  # 给大家表演一个shi山
        'news_id': pk,
        'config': config_x,
        'category': news.category_title,
        'content': content_x,
        'pub_time': news.pub_time,
        'img_config': img_x,
        'read_num': news.read_num,
        'comment_num': news.comment_num,
        'short_arg': news.short_arg,
        'title': news.title,
        'author': news.author,
        'description': news.description,
        'origin': news.origin,
        'comments': news.comment_set.all(),
        'img_dir': news.image_dir
    }
    return render(request, 'news/default.html', context=news_data)


def category_list(request):
    all_cats = Category.objects.all()
    return render(request, 'category.html', {'categories': all_cats})


def category_detail(request, pk):
    cat = Category.objects.get(pk=pk)
    all_news = cat.news_set.all()
    count = all_news.count()
    paginator = Paginator(all_news, 10)
    page_number = int(request.GET.get('page', 1))  # 自动填充一个param，如果有page那就是page，没有就默认1
    if page_number > paginator.num_pages:
        page_number = paginator.num_pages
    elif page_number < 1:
        page_number = 1
    page = paginator.page(page_number)
    if page_number < 6:  # 没有别的工具，只能手动操作力
        if paginator.num_pages <= 10:
            page_range = range(1, paginator.num_pages + 1)
        else:
            page_range = range(1, 11)
    elif (page_number >= 6) and (page_number <= paginator.num_pages - 5):
        page_range = range(page_number - 5, page_number + 5)
    else:
        page_range = range(paginator.num_pages - 9, paginator.num_pages + 1)
    return render(request, 'cat_list.html', {'page': page,
                                             'pk': pk,
                                             'count': count,
                                             'range': page_range,
                                             'current_num': page.number,
                                             'news': page.object_list,
                                             'num_pages': paginator.num_pages,
                                             'has_previous': page.has_previous(),
                                             'has_next': page.has_next()})


def add_comment(request, pk):
    data = request.POST
    comment_content = data['content']
    newsx = News.objects.get(pk=pk)
    com_obj = Comment(content=comment_content, news=newsx, pub_time=datetime.now())
    newsx.comment_num += 1
    newsx.save()  # 评论量得加进去
    com_obj.full_clean()  # 对数据进行验证
    com_obj.save()  # 存储在表中，之前已经设定过用时间排序
    return HttpResponseRedirect(f'/news/article/{pk}')  # 重定向至新闻正文


def del_comment(request, pk, comid):
    Comment.objects.get(id=comid).delete()
    newsx = News.objects.get(id=pk)
    newsx.comment_num -= 1
    newsx.save()
    return HttpResponseRedirect(f'/news/article/{pk}')  # 重定向至新闻正文


def news_list(request):
    # news/list/?page=114514   params = {"page": 114514} 模拟新浪的处理方式
    all_news = News.objects.all()
    paginator = Paginator(all_news, 10)
    page_number = int(request.GET.get('page', 1))  # 自动填充一个param，如果有page那就是page，没有就默认1
    if page_number > paginator.num_pages:
        page_number = paginator.num_pages
    elif page_number < 1:
        page_number = 1
    page = paginator.page(page_number)
    if page_number < 6:  # 没有别的工具，只能手动操作力
        if paginator.num_pages <= 10:
            page_range = range(1, paginator.num_pages + 1)
        else:
            page_range = range(1, 11)
    elif (page_number >= 6) and (page_number <= paginator.num_pages - 5):
        page_range = range(page_number - 5, page_number + 5)
    else:
        page_range = range(paginator.num_pages - 9, paginator.num_pages + 1)

    return render(request, 'list.html', {'page': page,
                                         'range': page_range,
                                         'current_num': page.number,
                                         'news': page.object_list,
                                         'num_pages': paginator.num_pages,
                                         'has_previous': page.has_previous(),
                                         'has_next': page.has_next()})
