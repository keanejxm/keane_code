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

from django.conf.urls import url, include


urlpatterns = [
    # 爬虫模板。
    url(r'^dc/spider_templates/', include("operate_spider_templates.urls")),
    # 爬虫。
    url(r'^dc/spiders/', include("spiders.urls")),
    # 流计算。
    url(r'^dc/flow_compute/', include("flow_compute.urls")),
    # 批计算。
    url(r'^dc/batch_compute/', include("batch_compute.urls")),
    # 外部检索。
    url(r'^dc/outside_search/', include("outside_search.urls")),
    # 文件云存储。
    url(r'^dc/cloud_storage/', include("cloud_storage.urls")),
    # 主题监控。
    url(r'^dc/monitor/', include("monitor.urls")),
    # 外部接口。
    url(r'^dc/outside/', include("outside.urls")),
]
