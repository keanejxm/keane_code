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
import batch_compute.views as analysis_views

urlpatterns = [
    # 根据query获取并按照score分数从高到底获取相似的文章
    url(r"^query_works_list/$", analysis_views.get_query_works_list),
    # 判断是否原创
    url(r"^judge_work_original/$", analysis_views.judge_work_original),
    # 获取相似文章，通过query【es搜索】
    url(r"^query_similar_works/$", analysis_views.get_query_works_similar),
    # 获取相似文章,通过simhash【simhash搜索】
    url(r"^simhash_similar_works/$", analysis_views.get_simhash_works_similar),
    # 获取相似文章,通过simhash或query【simhash或es搜索】
    url(r"^query_simhash_similar_works/$", analysis_views.get_query_simhash_works_similar),
    # 获取相似文章,通过海明距离计算
    url(r"^distance_similar_works/$", analysis_views.get_distance_works_similar),
]
