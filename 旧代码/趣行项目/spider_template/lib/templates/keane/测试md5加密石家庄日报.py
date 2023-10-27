# Author Keane
# coding=utf-8
# @Time    : 2021/1/9 17:16
# @File    : 测试md5加密石家庄日报.py
# @Software: PyCharm
import hashlib
def md5(strsea, charset="UTF-8"):
    """
    字符串转md5格式。
    :param strsea:
    :param charset:
    :return:
    """

    md5 = hashlib.md5()
    md5.update(strsea.encode(charset))
    return md5.hexdigest()
s= {
    "version":"1.1.3",
    "timestamp":"1610344412953",
    "tid":"959",
    "siteId":"1",
    "siteid":"1",
    # "sign":"5230b1507ac352396a00bda13268f9bc",
    "reqPagenum":"2",
    "nonce":"1622475814",
    "device":"00000000-15c7-18b7-8e6b-6f8e0033c587",
}
s = {
    "navigate_id":"1029",
    "have_own":"1",
    "app_version":"7.0.4",
    "tenantid":"a0892868981b0e99967d4a486cc02b43",
    # "sign":"62a2e5c8cecdc1b33c10e182dbd976c4",
    "client":"android",
    "cms_app_id":"13",
    "api_version":"3.6.2",
    "app_id":"3",
}



# aa = "b11ebd23bb617a75"
aa = ""
a = sorted(s,reverse=False)

sss = dict()
for i in a:
    # sss = dict()
    aa += (i+"="+s.get(i)+",")
print(aa)
aa = '{api_version=3.6.2,app_id=3,app_version=7.0.4,client=android,cms_app_id=13,have_own=1,navigate_id=1029,tenantid=a0892868981b0e99967d4a486cc02b43}'
print(md5(str(aa)))
