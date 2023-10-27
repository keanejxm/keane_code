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
import outside_search.views as intelligent_search_views


urlpatterns = [
    # 新浪搜索
    url(r"^xinlang_search/$", intelligent_search_views.xinlang_search_),
    # 360搜索
    url(r"^san60_search/$", intelligent_search_views.san60_search_),
    # 百度搜索
    url(r"^baidu_search/$", intelligent_search_views.baidu_search_),
    # 中国搜索
    url(r"^china_search/$", intelligent_search_views.china_search_),
    # 搜狗搜索
    url(r"^sougou_search/$", intelligent_search_views.sougou_search_),
    # bing搜索
    url(r"^bing_search/$", intelligent_search_views.bing_search_),
]
