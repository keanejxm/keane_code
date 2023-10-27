#!-*- coding:utf-8 -*-
"""
app基础数据
# author: Keane
# create date:
# update date: 2020/11/11
"""
# from appspider_total.appspider_ import Appspider
import time


class AppSpiderParam(object):

    @staticmethod
    def appspider_channel_param():
        channel_param = {
            '腾讯新闻': ['https://r.inews.qq.com/getQNChannels?',
                     {
                         'Cookie': 'RK=iqwphwSmGc; ptcz=1cdc843a1bd6ae6846b53b86d6166320c4f99a73e2d3883becb4a19a2dc2a2f'
                                   '6; pgv_pvid=4397206384; pgv_pvi=9772086272; o_cookie=1197523286; pac_uid=1_11975232'
                                   '86',
                         'Host': 'r.inews.qq.com',
                         'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko'
                                       ') Chrome/84.0.4147.125 Safari/537.36'
                     },
                     {
                         'omgid': '03c39e5b8ee7114dcfcb5e46cf95557a99860010215910',
                         'QIMEI36': 'e2a782e57e66069d6b56b3d8100012c14819',
                         'devid': '824e2a6bfa704b05&appver=25_android_6.2.70',
                         'uid': '824e2a6bfa704b05',
                         'trueVersion': '6.2.70',
                         'suid': '8gMc3n5d7YIVsTrc4wt5',
                         'qimei': '824e2a6bfa704b05',
                         'qn-sig': 'ce845794c53a9d753cbeeb1c4d10995b',
                         'qn-rid': '1005_9697d295-3903-44fa-8698-b6cfd5960f59',
                         'qn-newsig': '9a90c7bff45dfe007592e13bbfc072546c0ecb00f2cf88092e8b7ff24b239392',
                         'qn_channel_sig': '714ff4e574b53715f407be95a41495e1a2521345bfaba3c28d6e519e4eef0ef8 HTTP/1.1'
                     }, 'get'
                     ],
            '网易新闻': ['http://c.m.163.com/nc/topicset/android/subscribe/manage/listspecial.html',
                     {
                         'Host': 'c.m.163.com',
                         'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko'
                                       ') Chrome/84.0.4147.125 Safari/537.36'
                     },
                     {

                     }, 'get'
                     ],
            '搜狐新闻': ['https://api.k.sohu.com/api/channel/v7/list.go?',
                     {
                         'Cookie': 'SUV=1602589077883sk9jo8; IPLOC=CN5300; gidinf=x099980109ee12434ceb7fc7a000b04931be'
                                   '0487c7b7; t=1602749719576',
                         'Host': 'api.k.sohu.com',
                         'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko'
                                       ') Chrome/84.0.4147.125 Safari/537.36'
                     },
                     {
                         'rt': 'xml',
                         'supportLive': '1',
                         'supportWeibo': '1',
                         'v': '6.4.6',
                         'version': '6.4.6',
                         'cdma_lng': '',
                         'cdma_lat': '',
                         'up': '1, 13557, 297993, 2063, 3, 283, 4, 6, 5, 2, 11, 50, 45, 960591, 279, 12, 954509, 337, '
                               '98, 16, 177, 248, 49, 65, 960377, 25, 4313, 960596, 960516, 960614, 8922, 790793',
                         'down': '',
                         'local': '283',
                         'change': '0',
                         'isStartUp': '1',
                         'recomState': '1',
                         'browseOnly': '0',
                         'gbcode': '130100',
                         'localgbcode': '130100',
                         'housegbcode': '',
                         'p1': 'NjcyNDIwNzk3MjEzMTk4NDM4Ng ==',
                         'gid': '02ffff11061101da51831f3e1fffc99d7c5e8af9bca87b',
                         'pid': '-1',
                         'apiVersion': '42'
                     }, 'get'

                     ],
            '央视新闻': ['http://m.news.cntv.cn/special/json/fl808/index.json?',
                     {
                         'Host': 'm.news.cntv.cn',
                         'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko'
                                       ') Chrome/84.0.4147.125 Safari/537.36'
                     },
                     {
                         'app_version': '808'
                     },
                     'get'
                     ],
            '环球TIME': ['https://api.hqtime.huanqiu.com/api/news/category',
                       {
                           'accept': 'application/vnd.hq_time.v2+json',
                           'content-type': 'application/json',
                           'user-agent': '(Linux; Android 6.0.1; Build/Android MuMu) huanqiuTIME/9.11.3',
                           'clientversion': 'Android/v9.11.3',
                           'x-timestamp': '1604394657',
                           'x-nonce': '38w9li1b',
                           'x-sign': 'cee88dc08c9e0789542a93a3670b84f64970f17dbf17b483c88df57f6cdc43e6',
                           'Host': 'api.hqtime.huanqiu.com',
                           'Connection': 'Keep-Alive',
                           'Accept-Encoding': 'gzip',
                           'If-Modified-Since': 'Mon, 02 Nov 2020 09:27:38 GMT'
                       },
                       {},
                       'get'
                       ],
            '参考消息': [
                'http://m.api.ckxx.net/v2/start?',
                {
                    'User-Agent':'Maa-Proxymaa-http-ok',
                    'Host':'m.api.ckxx.net',
                    'Connection':'Keep-Alive',
                    'Accept-Encoding':'gzip',

                },
                {
                    'cachetime':'1606200506',
                    'system_version':'6.0.1',
                    'sign':'76b6bc2954d0d9aa8d54ea4f7c45c607',
                    'nav_width':'405',
                    'time':'1606202545805',
                    'siteid':'10001',
                    'newmigu':'migu',
                    'clientid':'1',
                    'modules':'common:2',
                    'app_version':'2.3.8',
                    'device_id':'08:00:27:3F:09:3B',
                    'system_width':'810',
                    'system_name':'android',
                    'ip':'10.0.2.15',
                    'device_model':'MuMu',
                    'nav_height':'115',
                    'system_height':'1440',
                    'device_version':'AndroidMuMu',
                    'type':'android',
                },
                'get'
            ],
            '山西日报': ['http://sxapi.sxrbw.com/api/v2/menus/?',
                     {
                         'User-Agent': 'Mozilla/5.0 (Linux; Android 10; PACM00 Build/QP1A.190711.020; wv) AppleWebKit/'
                                       '537.36 (KHTML, like Gecko) Version/4.0 Chrome/77.0.3865.92 Mobile Safari/537.3'
                                       '6',
                         'Host': 'sxapi.sxrbw.com'
                     },
                     {
                         'clientVersionCode': '61',
                         'pjCode': 'code_sxrb',
                         'device_size': '1080.0x2200.0',
                         'deviceOs': '10',
                         'channel': 'huawei',
                         'deviceModel': 'OPPO-PACM00',
                         'clientVersion': '4.4.6',
                         'udid': 'e0f96ff828fd0219',
                         'platform': 'android'
                     },
                     'get'
                     ],
            '河南日报': ['https://api.henandaily.cn/v2/content/gettopcategory?',
                     {
                         'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 6.0.1; MuMu Build/V417IR)',
                         'Host': 'api.henandaily.cn'
                     },
                     {
                         'device_type': 'android',
                         'user_id': '0',
                         'token': '8de8af6f01e8a9b8b2a649a9'
                     },
                     'get'
                     ],
            '新京报': ['https://api.bjnews.com.cn/api/v101/channel/channel_list.php?',
                    {
                        'url_name': 'base',
                        'Device-Token': '1a0018970a1c42e0fb7',
                        'x-client-id': 'e8e733778f9dfc1e',
                        'version': 'v204',
                        'channel': 'bjnews_app',
                        'Host': 'api.bjnews.com.cn',
                        'User-Agent': 'okhttp/3.14.0',
                    },
                    {
                        'time': str(int(time.time() * 1000)),
                        'sign': '50cdc6ef1e210c422f1b29b18fb6b68c'
                    },
                    'get'
                    ],
            '北京日报': ['https://ie.bjd.com.cn/rest/site/api/5b165687a010550e5ddc0e6a/column/list/customer/get?',
                     {
                         'app_key': 'newsroom-cms',
                         'app_secret': 'bbbbbbaaaaaaaaaaaaa',
                         'Host': 'ie.bjd.com.cn',
                         'Connection': 'Keep-Alive',
                         'User-Agent': 'okhttp/3.11.0',
                     },
                     {'udid': 'e8e733778f9dfc1e'},
                     'get'
                     ],
            '冀时': ['http://mapi.plus.hebtv.com/api/open/js/get_home_columns?',
                   {
                       'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 6.0.1; MuMu Build/V417IR) m2oSmartCity_367 1.0.0',
                       'X-API-TIMESTAMP': '1603952072436OdJARo',
                       'X-API-SIGNATURE': 'MzA5YzQ5OGM4YTAyZjJkZTY5YTYxYzdhNTJhNGM5ZDIwZDRmYjlmZQ==',
                       'X-API-VERSION': '3.2.1',
                       'X-AUTH-TYPE': 'sha1',
                       'X-API-KEY': '05049e90fa4f5039a8cadc6acbb4b2cc',
                       'Host': 'mapi.plus.hebtv.com',
                   },
                   {
                       'count': '10',
                       'system_version': '6.0.1',
                       'app_version': '3.2.1',
                       'client_type': 'android',
                       'client_id_android': '71156911959c161775965150d97153c7',
                       'locating_city': '石家庄',
                       'appkey': 'b7269c8f9a318c69a59dc430cef3ab59',
                       'version': '3.2.1',
                       'appid': 'm2ovki73ruqwcwmw8b',
                       'language': 'Chinese',
                       'location_city': '石家庄',
                       'device_token': '09371b9507237be54a4467d4eb4a7815',
                       'phone_models': 'MuMu',
                       'package_name': 'com.ihope.hbdt',
                   }, 'get'
                   ],
            '河北纪委': ['http://dev.hebnews.cn/jwcms/index.php?',
                     {
                         'Host': 'dev.hebnews.cn',
                         'Connection': 'keep-alive',
                         'Accept': 'application/json',
                         'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0.1; MuMu Build/V417IR; wv) AppleWebKit/537.36 '
                                       '(KHTML, like Gecko) Version/4.0 Chrome/52.0.2743.100 Mobile Safari/537.36 Html'
                                       '5Plus/1.0',
                         'X-Requested-With': 'XMLHttpRequest',
                         'Cookie': 'acw_tc=7ceef32116039579513747484e2c28db6bf64ab33579b5becbc32b531e',
                     },
                     {
                         'm': 'getindata',
                         'c': 'index',
                         'a': 'get_menus',
                         'pcatid': '0',
                         'type': '1',
                     }, 'get'
                     ],
            '山西省政府': ['http://app2017.shanxi.gov.cn/model_1/channels.json',
                      {
                          'Host': 'app2017.shanxi.gov.cn',
                          'Connection': 'Keep-Alive',
                          'Accept-Encoding': 'gzip',
                          'User-Agent': 'okhttp/3.4.1'
                      },
                      {}, 'get'
                      ],
            '山西视觉': ['http://sjz.sxrb.com/app/channel/config/v1.0',
                     {
                         'version': 'android-1.5',
                         'Host': 'sjz.sxrb.com',
                         'Connection': 'Keep-Alive',
                         'Accept-Encoding': 'gzip',
                         'User-Agent': 'okhttp/3.2.0'
                     },
                     {}, 'get'
                     ],
            '大众日报': ['http://phoneapi2.xrdz.dzng.com/index.php/columns/getColumns?',
                     {
                         'User-Agent': 'okhttp-okgo/jeasonlzy',
                         'Host': 'phoneapi2.xrdz.dzng.com'
                     },
                     {
                         ''
                     }, 'get'
                     ],
            '黑龙江日报': ['http://sjdb.hljnews.cn:8080/DBNewsAppService_v1.3.0/getListCategoryNew.do?',
                      {
                          'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 6.0.1; MuMu Build/V417IR)',
                          'Host': 'sjdb.hljnews.cn:8080'
                      },
                      {
                          'flag': '1'
                      }, 'get'
                      ],
            '无线石家庄': ['http://mobile.sjzntv.cn/sjz3/news_recomend_column_sy.php?',
                      {
                          'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 6.0.1; MuMu Build/V417IR) m2oSmartCity_'
                                        '167 1.0.0',
                          'X-API-TIMESTAMP': str(int(time.time() * 10000)) + 'ZkA5v',
                          'X-API-SIGNATURE': 'ZTkwYWIzYjBhZDIyMmNhNWZkYzU5YTVkMzNiMzRiZmQ5ODA0N2ZhZg==',
                          'X-API-VERSION': '3.0.2',
                          'X-AUTH-TYPE': 'sha1',
                          'X-API-KEY': '5878a7ab84fb43402106c575658472fa',
                          'Host': 'mobile.sjzntv.cn',
                          'Connection': 'Keep-Alive',
                          'Accept-Encoding': 'gzip',
                      },
                      {
                          'system_version': '6.0.1',
                          'app_version': '3.0.2',
                          'client_type': 'android',
                          'client_id_android': '5a82ed4964b6fb092ef41abdb423cc7c',
                          'locating_city': '石家庄',
                          'appkey': 'BJaFDrsqqZQelNRXE6EhUXmlfzhq5Rox',
                          'version': '3.0.2',
                          'appid': '8',
                          'language': 'Chinese',
                          'location_city': '石家庄',
                          'device_token': '1a4a6bd80889376755a733dd919e1a81',
                          'phone_models': 'MuMu',
                          'package_name': 'com.hoge.android.app.wxsjz',
                      }, 'get'
                      ],
            '中国青年报': ['https://i.cyol.com/peony/v1/group?',
                      {
                          'cache': '2000',
                          'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhcHBpZCI6MSwiZGV2aWNlX2lkIj'
                                           'oiMWI3NTNmNmItODc0NS0zNDg2LWEwYzAtNWM3N2RlZGQ1NmQzIiwiZXhwIjoxNjExOTczODY0'
                                           'LCJpc3MiOiI5cDZ5anVvYVZ4bjBWd3dtU3R0SWNtM1hKd21jZlJDayIsInBsYXRmb3JtIjoibW'
                                           '9iaWxlIiwic2l0ZSI6MCwidWlkIjoiYW5vbnltb3VzIn0.ZbNNXxLCwrl8OBFNZD1a6-xfH6zO'
                                           'U3a0gOzL-nwsr10',
                          'X-Request-Id': '1b753f6b-8745-3486-a0c0-5c77dedd56d3',
                          'Content-Type': 'application/json',
                          'X-Platform': 'android',
                          'X-Version': '4.3.3',
                          'X-Brand': 'Android MuMu',
                          'Host': 'i.cyol.com',
                          'Connection': 'Keep-Alive',
                          'Accept-Encoding': 'gzip',
                          'User-Agent': 'okhttp/3.11.0',
                          'If-Modified-Since': 'Fri, 30 Oct 2020 02:34:26 GMT'
                      },
                      {
                          'module_name': 'home',
                          'type': 'nav',
                          'channel': '28Dga1xp'
                      },
                      'get'
                      ],
            '中国妇女报': ['http://weixing.cnwomen.com.cn:8080/amc/client/listSubscribeColumn?',
                      {
                          'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 6.0.1; MuMu Build/V417IR)',
                          'Host': 'weixing.cnwomen.com.cn:8080'
                      },
                      {
                          'nodeCode': '3372ff6d-56e1-4a0a-b812-e9b6d3ba2dcd',
                          'contentType': '0,6,11'
                      }, 'get'
                      ],
            '法制日报': ['http://appwx.legaldaily.com.cn:8080/amc/client/listSubscribeColumn?',
                     # 'http://appwx.legaldaily.com.cn:8080/amc/client/listLocalColumn?'
                     {
                         'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 6.0.1; MuMu Build/V417IR)',
                         'Host': 'appwx.legaldaily.com.cn:8080'
                     },
                     {
                         'nodeCode': 'ecdc5307-888e-4322-8817-f04bd81a7e82',
                         'contentType': '0,6,11'
                     }, 'get'
                     ],
            '国务院': ['https://app.www.gov.cn/govdata/gov/source.json',
                    {
                        'User-Agent': 'okhttp/3.14.1 GovCnAndroid/4.1.0 (yingyongbao; 24)',
                        'Cache-Control': 'no-store',
                        'Host': 'app.www.gov.cn'
                    },
                    {}, 'get'
                    ],
            '人民日报': ['https://app.peopleapp.com/Api/700/HomeApi/showCategory?',
                     {
                         'Cookie': 'acw_tc="276082a816043885967987403ed20069be76016a6d4b0270c25278022e1f31";$Path="/";'
                                   '$Domain="app.peopleapp.com"; SERVERID=f0c2519d15ca3b0cae13b80f9d03fb94|1604388603|'
                                   '1604388596',
                         'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 6.0.1; MuMu Build/V417IR);DailyNewspaper/7.0.2',
                         'Content-Type': 'application/x-www-form-urlencoded',
                         'Host': 'app.peopleapp.com'
                     },
                     {
                         'city': '',
                         'citycode': '',
                         'device': '1b753f6b-8745-3486-a0c0-5c77dedd56d3',
                         'device_model': 'MuMu',
                         'device_os': 'Android 6.0.1',
                         'device_product': 'Netease',
                         'device_size': '810*1440',
                         'device_type': '1',
                         'district': '',
                         'fake_id': '56034407',
                         'from': '',
                         'ids': '234,1,2,114,102,115,229,7,4,5,6,235,9,10,12,13',
                         'interface_code': '702',
                         'latitude': '',
                         'longitude': '',
                         'province': '',
                         'province_code': '23502043',
                         'to': '',
                         'version': '7.0.2',
                         'securitykey': 'd48822196478d0a6dc5cbbdcfef400e1',
                     }, 'get'
                     ],
            '新华社': ['https://xhpfmapi.zhongguowangshi.com/v708/core/nav',
                    {
                        "Content-Type": "application/json; charset=UTF-8",
                        "Content-Length": "541",
                        "Host": "xhpfmapi.zhongguowangshi.com",
                        "Connection": "Keep-Alive",
                        "Accept-Encoding": "gzip",
                        "User-Agent": "okhttp/3.11.0"
                    },
                    {},"post",
                    {"address": "", "city": "", "clientApp": "104", "clientBundleID": "net.xinhuamm.mainclient",
                     "clientDate": 1606134301, "clientDev": 0, "clientHeight": 1440,
                     "clientId": "f221e4273243227eea38e62d465b1e56",
                     "clientLable": "00000000-7f00-1df9-ffff-fffff1062248", "clientLatitude": 0.0,
                     "clientLongitude": 0.0, "clientMarket": "198", "clientModel": "MuMu", "clientNet": "wifi",
                     "clientOS": "6.0.1", "clientPrison": "0", "clientToken": "f221e4273243227eea38e62d465b1e56",
                     "clientType": 2, "clientVer": "7.1.4", "clientWidth": 810, "h5request": 0, "loginStatus": 0,
                     "province": "", "userID": 0}
                    ]
        }
        return channel_param
