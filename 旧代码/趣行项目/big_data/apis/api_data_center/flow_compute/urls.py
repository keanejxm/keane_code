"""api URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""

from django.conf.urls import url
from . import views
from . import views_simhash
from . import views_baidu_api

urlpatterns = [
    # 通用接口。
    url(r"^common/options/$", views.flow_compute_options),

    # 计算simhash值
    url(r"^common/get_simhash_value/$", views_simhash.GetSimhash.as_view()),
    # 比较simhash值
    url(r"^common/compare_simhash_data/$", views_simhash.GetSimhash.as_view()),

    # 百度AI接口。
    # 判断正负面
    url(r"^baidu_api/sentiment_classify/$", views_baidu_api.JudgeArticlePositiveNegative.as_view()),
    # 判断文章分类
    url(r"^baidu_api/keyword/$", views_baidu_api.JudgeArticleClassify.as_view()),
    # 全文分词
    url(r"^baidu_api/lexer/$", views_baidu_api.FullTextParticiple.as_view()),
    # 生成文章摘要、提取文章主题
    url(r"^baidu_api/news_summary/$", views_baidu_api.CreateArticleAbstractTheme.as_view()),
    # 对文章聚类、归类
    url(r"^baidu_api/topic/$", views_baidu_api.ArticleClusteringClassified.as_view()),
    # 计算词频
    url(r"^baidu_api/word_frequency/$", views_baidu_api.WordFrequency.as_view()),
    # 自定义入口
    url(r"^baidu_api/nlp/$", views_baidu_api.NLP.as_view()),
]
