from django.db import models


# Create your models here.

class Category(models.Model):
    """
    a certain category
    """
    title = models.CharField(max_length=200)
    app_label = 'news'

    def __str__(self):
        return self.title

    class Meta:
        app_label = 'news'


# class Keywords(models.Model):
#     """
#     a certain keyword
#     """
#     name = models.CharField(max_length=200)

class News(models.Model):
    """
    a certain news
    """
    config = models.JSONField()  # 真实的json
    # 有一些变量其实是可以不用的(毕竟我都有json了) 我还是给他弄上了
    # 毕竟这样的调用要正常不少
    pub_time = models.DateTimeField()  # 发布时间
    short_arg = models.TextField()
    category_title = models.CharField(max_length=200, null=True)
    contenTxt = models.TextField(null=True)
    read_num = models.IntegerField()  # 热 度
    author = models.CharField(max_length=200)  # 作者
    origin = models.URLField()  # 原新闻链接
    title = models.CharField(max_length=200)  # 标题
    description = models.TextField()  # 摘要
    content = models.JSONField()  # 内容
    img_config = models.JSONField()
    comment_num = models.IntegerField()
    image_dir = models.JSONField(null=True)

    def __str__(self):
        return self.title

    # 关联外键
    category = models.ForeignKey(
        'Category',
        on_delete=models.SET_NULL,
        null=True,
    )

    class Meta:
        # News.objects提出数据时按照列表指定的字段排序
        ordering = ['-pub_time']


class Comment(models.Model):
    """
    a certain comment
    其实没什么大的要求，有内容有时间就很足够了
    """
    # author = models.CharField(max_length=200)  # 作者
    content = models.TextField()
    pub_time = models.DateTimeField(auto_now_add=True)  # 这样就该是多少就是多少了

    # 关联外键
    news = models.ForeignKey(
        'News',
        on_delete=models.CASCADE,  # 跟随删除
        null=False,
    )

    class Meta:  # 画瓢
        ordering = ['-pub_time']
