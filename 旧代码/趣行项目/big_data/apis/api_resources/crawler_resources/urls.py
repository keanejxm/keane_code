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

import crawler_resources.views as crawler_resources_views

urlpatterns = [
    # 获取微信万能Key。
    url(r'^get_random_wx_great_key[/]?$', crawler_resources_views.get_random_wx_great_key),
    # 获取微博采集用cookie。
    url(r'^get_random_wb_cookie[/]?$', crawler_resources_views.get_random_wb_cookie),
    # 获取阿布云代理配置。
    url(r'^get_abuyun_proxy[/]?$', crawler_resources_views.get_abuyun_proxy),
    # 获取河北日报作者列表。
    url(r'^get_hbrb_authors[/]?$', crawler_resources_views.get_hbrb_authors),
]
