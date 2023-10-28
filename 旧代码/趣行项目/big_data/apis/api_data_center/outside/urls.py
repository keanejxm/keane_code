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
from . import views_wechat_assistant
from . import views_image_hash

urlpatterns = [
    # 判断正负面。
    url(r"^get_emotional_data/$", views.GeteMotionalData.as_view()),
    # 微信助手。
    url(r"^wechat_assistant/$", views_wechat_assistant.WeChatAssistant.as_view()),
    # 图片哈希（通过url获取）。
    url(r"^image_hash_by_url/$", views_image_hash.api_image_hash_by_url),
]
