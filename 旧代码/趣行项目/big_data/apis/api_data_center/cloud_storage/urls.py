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
from cloud_storage.views import bos_exists, bos_check_key_exists, \
    bos_upload, bos_upload_by_url, bos_upload_image_by_url_and_compute_hash, bos_parse_html

urlpatterns = [
    url(r"^bos/exists/?$", bos_exists),
    url(r"^bos/check_key_exists/?$", bos_check_key_exists),
    url(r"^bos/upload/?$", bos_upload),
    url(r"^bos/upload_by_url/?$", bos_upload_by_url),
    url(r"^bos/upload_image_by_url_and_compute_hash/?$", bos_upload_image_by_url_and_compute_hash),
    url(r"^bos/parse_html/?$", bos_parse_html),
]
