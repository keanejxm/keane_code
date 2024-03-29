"""

# author: albert
# date: 2021/1/20 9:20
# update: 2021/1/20 9:20
"""
import hashlib

from api_common_utils.base_data import DEFAULT_USER_INFO_FIELDS, DEFAULT_PLATFORM_FIELDS, DEFAULT_WORKS_FIELDS


DEFAULT_WE_MEDIA_PLATFORM = dict(dict(), **DEFAULT_PLATFORM_FIELDS)
DEFAULT_WE_MEDIA_PLATFORM["type"] = 7
DEFAULT_WE_MEDIA_PLATFORM["types"] = [7]
DEFAULT_WE_MEDIA_PLATFORM_FIELDS = DEFAULT_WE_MEDIA_PLATFORM


DEFAULT_WE_MEDIA_USER_INFO = dict(dict(), **DEFAULT_USER_INFO_FIELDS)
DEFAULT_WE_MEDIA_USER_INFO["platformType"] = 7
DEFAULT_WE_MEDIA_USER_INFO["types"] = [7]
DEFAULT_WE_MEDIA_USER_INFO_FIELDS = DEFAULT_WE_MEDIA_USER_INFO


DEFAULT_WE_MEDIA_USER_WORKS = dict(dict(), **DEFAULT_WORKS_FIELDS)
DEFAULT_WE_MEDIA_USER_WORKS["platformType"] = 7
DEFAULT_WE_MEDIA_USER_WORKS_FIELDS = DEFAULT_WE_MEDIA_USER_WORKS


def md5(strsea, charset="UTF-8"):
    # 字符串转md5格式
    md5 = hashlib.md5()
    md5.update(strsea.encode(charset))
    return md5.hexdigest()