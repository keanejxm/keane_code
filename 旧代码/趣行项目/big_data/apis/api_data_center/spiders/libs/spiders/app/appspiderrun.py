#!-*- coding:utf-8 -*-
"""
app运行程序
# author: Keane
# create date:
# update date: 2020/11/11
"""
import random
import logging
from spiders.libs.spiders.app.app_analysis_model.beijingribao import Beijingribao
from spiders.libs.spiders.app.app_analysis_model.guowuyuan import Guowuyuan
from spiders.libs.spiders.app.app_analysis_model.hebeijiwei import Heibeijiwei
from spiders.libs.spiders.app.app_analysis_model.henanribao import Heinanribao
from spiders.libs.spiders.app.app_analysis_model.jishi import Jishi
from spiders.libs.spiders.app.app_analysis_model.shanxiribao import Shanxiribao
from spiders.libs.spiders.app.app_analysis_model.shanxishengzhengfu import Shanxishengzhengfu
from spiders.libs.spiders.app.app_analysis_model.shanxishijuezhi import Shanxishijue
from spiders.libs.spiders.app.app_analysis_model.souhu import Souhunews
from spiders.libs.spiders.app.app_analysis_model.yangshi import Yangshinews
from spiders.libs.spiders.app.app_analysis_model.zhongguofunvbao import Zhongguofunv
from spiders.libs.spiders.app.app_analysis_model.zhongguoqingnian import Zhongguoqingnian
from spiders.libs.spiders.app.app_analysis_model.renminribao import Renminribao
from spiders.libs.spiders.app.app_analysis_model.xinhuashe import XinHuaShe
from spiders.libs.spiders.app.app_analysis_model.cankaoxiaoxi import CanKaoXiaoXi
from spiders.libs.spiders.app.app_analysis_model.jiefangjunbao import JieFangJunBao
from spiders.libs.spiders.app.app_analysis_model.guangmingribao import GuangMingRiBao
from spiders.libs.spiders.app.app_analysis_model.jiancharibao import JianChaRiBao
from spiders.libs.spiders.app.app_analysis_model.zhongguowenlian import ZhongGuoWenLian

class AppSchedule(object):
    def __init__(self):
        self.appname = input('请输入需要采集的app名字')
        self.appnamess = ['北京日报', '国务院', '河北纪委', '河南日报', '冀时', '山西日报', '山西省政府', '山西视觉', '搜狐新闻',
             '央视新闻', '中国妇女报', '中国青年报', '环球TIME', '新华社', '参考消息', '解放军报', '检察日报', '光明日报',
             '中国文联', ]
        appname = self.appname
        self.appnames = {'北京日报': Beijingribao(appname), '国务院': Guowuyuan(appname), '河北纪委': Heibeijiwei(appname),
            '河南日报': Heinanribao(appname), '冀时': Jishi(appname), '山西日报': Shanxiribao(appname),
            '山西省政府': Shanxishengzhengfu(appname), '山西视觉': Shanxishijue(appname), '搜狐新闻': Souhunews(appname),
            '央视新闻': Yangshinews(appname), '中国妇女报': Zhongguofunv(appname),
            '中国青年报': Zhongguoqingnian(appname), '人民日报': Renminribao(appname), '新华社': XinHuaShe(appname),
            '参考消息': CanKaoXiaoXi(appname), '解放军报': JieFangJunBao(appname), '检察日报': JianChaRiBao(appname),
            '光明日报': GuangMingRiBao(appname), '中国文联': ZhongGuoWenLian(appname)
            }
    def run(self):
        if self.appname:
            logging.info(f"正在采集{self.appname}")
            if self.appname in self.appnames.keys():
                print(self.appnames.get(self.appname))
                self.appnames.get(self.appname).run()
        else:
            while 1:
                appname = random.choice(self.appnamess)
                logging.info(f"正在采集{appname}")
                self.appnames.get(appname).run()
if __name__ == '__main__':
    app_schedule = AppSchedule()
    app_schedule.run()
