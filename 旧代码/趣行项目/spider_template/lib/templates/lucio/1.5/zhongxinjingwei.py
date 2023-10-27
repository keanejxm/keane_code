# -*- encoding:utf-8 -*-
"""
@功能:今日合川解析模板
@AUTHOR：lucio
@文件名：zhongxinjingwei.py
@时间：2021/1/12  9:20
"""

import requests
import json
import re
from lxml import etree

# from lib.templates.initclass import InitClass
# from lib.templates.appspider_m import Appspider
from lib.templates.appspider_m import Appspider
from lib.templates.initclass import InitClass

headers = {
    'timestamp': '1610424810982',
    'appKey': 'JWAPP',
    'accessToken': '0363fd7458f162dced08e9e887ecdf75',
    'Host': 'jw.jwview.com',
    'Accept-Encoding': 'gzip',
    'User-Agent': 'okhttp/3.8.0',
    'Connection': 'keep-alive',
}


class ZhongXinJingWei(Appspider):

    def analyze_articlelists(self):
        self.session = requests.Session()
        channelsid = ['高层', '宏观', '金融', '基金', '银行', '股市', '理财', '视频', '图片',
                      '产经', '房产', '科技', '汽车', '游戏', '原创', '推荐', '财人', ]
        for channel in channelsid:

            url = f'http://jw.jwview.com/jwview/getNewsList?user=351564689718625&' \
                  f'pageIndex=1&pageSize=20&searchType=1&channel={channel}'

            r = self.session.get(url=url, headers=headers).text
            datas = json.loads(r)
            print(datas)
            for data in datas[f'data']:
                article_item = InitClass().article_fields()
                article_item['channelID'] = channel
                article_item['appname'] = '中新经纬'
                article_item['channelname'] = channel
                article_item['title'] = data['title']
                article_item['source'] = data['source']
                article_item['content'] = data['content']
                article_item['pubtime'] = InitClass().date_time_stamp(data['pubtime'])
                article_item['articlecovers'] = data['sharePic']
                if data['dataPics']:
                    article_item['images'] = [img['src'] for img in data['dataPics']]

                article_item['videos'] = data['video']
                if article_item['videos']:
                    article_item['videocover'] = data['sharePic']
                    article_item['workerid'] = data['id']
                if type(article_item['articlecovers']) != list:
                    article_item['articlecovers'] = [article_item['articlecovers']]
                if type(article_item['images']) != list:
                    article_item['images'] = [article_item['images']]
                if type(article_item['videos']) != list:
                    article_item['videos'] = [article_item['videos']]
                if type(article_item['videocover']) != list:
                    article_item['videocover'] = [article_item['videocover']]
                print(article_item)
                print(json.dumps(article_item, indent=4, ensure_ascii=False))
                print(f'正在爬取{article_item["channelname"]}频道')
            # break

    def run(self):
        self.analyze_articlelists()


if __name__ == '__main__':
    ob = ZhongXinJingWei('中新经纬')
    ob.run()
