import json
import os
from datetime import datetime, timedelta
import traceback
import numpy as np
from news.models import News, Category

path = r'D:\involuntary\works\missing-semester-of-python\part1\websites'
files = os.listdir(path)

# News.objects.all()

for file in files:
    try:
        all_path = path + '\\' + file
        config_path = all_path + r'\config.json'
        img_path = all_path + r'\images\img_config.json'
        article_path = all_path + r'\article.txt'
        content = {}
        contenTxt = ''
        with open(config_path, 'r') as f:
            json_config = f.read()
        xconfig = json.loads(json_config)
        with open(article_path, 'r', encoding='utf-8') as g:
            pas = g.readlines()
            index = 0
            for item in pas:
                content[f'{index}'] = item.rstrip()
                contenTxt += item.rstrip()
                index += 1
        with open(img_path, 'r') as h:
            img_config = h.read()
            img_bababa = json.loads(img_config)
        short = content['0'][:50] if content['0'] else "无预览"
        category = ""
        now_time = datetime.now()
        pub_time = datetime.strptime(xconfig['publish_time'], '%Y-%m-%d %H:%M')
        if pub_time + timedelta(days=60) > now_time:
            category = "两个月以内"
        elif pub_time + timedelta(days=90) > now_time:
            category = "三个月以内"
        elif pub_time + timedelta(days=120) > now_time:
            category = "四个月以内"
        else:
            category = "其他"
        xx = f'{file}\\images\\'
        whiw = [(xx + f'{img_bababa["data"][key][0]}') for key in img_bababa['data'].keys()]
        new_news = News(config=json_config,
                        pub_time=pub_time,
                        read_num=np.random.randint(low=10, high=100000),
                        author=xconfig['author'],
                        origin=xconfig['url'],
                        title=xconfig['title'],
                        description=xconfig['description'],
                        category_title=category,
                        content=content,
                        short_arg=short + "......",
                        img_config=img_config,
                        comment_num=0,
                        contenTxt=contenTxt,
                        category=Category.objects.get(title=category),
                        image_dir=whiw,
                        )
        new_news.save()
    except:
        print(traceback.print_exc())
