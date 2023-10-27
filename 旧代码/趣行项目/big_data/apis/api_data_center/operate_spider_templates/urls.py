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
import operate_spider_templates.views as spider_templates_views


urlpatterns = [
    # 新增电子报采集模板。
    url(r"^templates/epaper_template_create$", spider_templates_views.epaper_template_create),
    # 删除电子报模板
    url(r"^templates/epaper_template_delete$", spider_templates_views.epaper_template_delete),
    # 更新电子报模板
    url(r"^templates/epaper_template_update$", spider_templates_views.epaper_template_update),
]
