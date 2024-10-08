# -*- coding:utf-8 -*-
"""
# project: 检查报纸名字是否存在
# author: Neil
# date: xxxx/xx/xx

"""

import pymysql
import csv

# 创建一个csv文件
f = open("./news.csv", 'w', newline="")
ff = csv.writer(f)
# 自定义标题
ff.writerow(["news_title"])

def check_is_exit(name_list):
    """
    查询数据库
    """
    conmysql = pymysql.connect(
        "192.168.32.18",
        "root",
        "moR7tzWCv$ZYBe*$",
        "big_data_platform")
    cursor = conmysql.cursor()
    for name in name_list:
        # 查询数据库
        sql = f"select platformName from epaper_template where platformName = '{name}';"
        cursor.execute(sql)
        mysql_result = cursor.fetchall()
        if mysql_result:
            print(f"该{name}存在")
        else:
            ff.writerow([name])
            print(f"该{name}不存在，请添加")
    cursor.close()
    conmysql.close()


if __name__ == '__main__':
    name_list = [
        "今晨6点", "青州通讯", "潍坊晚报", "淄博晚报", "黄河口晚刊", "济宁晚报", "聊城日报", "沂蒙晚报", "鲁南商报", "鲁中晨刊", "德州晚报", "枣庄晚报", "牡丹晚报",
        "青岛财经日报", "淄博财经新报", "农村大众报", "滕州日报", "黄海晨刊", "经济导报", "寿光日报", "济南铁道报", "山东法制报", "北方蔬菜报", "东方烟草报", "淄川工作",
        "青岛西海岸报", "新即墨报", "东昌时讯", "今日章丘", "金胶州", "今日邹平", "老年生活报", "人口健康报", "文登大众", "庆云报", "乐陵市报", "陵城报", "临邑大众", "画都周刊",
        "山东教育报", "东方烟草报·爱晚亭", "东方烟草报·中国烟机", "东方烟草报·中烟物流", "山东能源报", "夏津大众报", "东方烟草报·现代卷烟营销", "东方烟草报·鲁烟视窗", "华夏酒报",
        "东方烟草报·山东中烟", "东海之声", "平原时讯", "东方烟草报·山东视窗", "德州日报德周刊", "经济开发区报", "东方烟草报·金周刊", "东方烟草报·粤烟视窗", "东方烟草报·济南专刊",
        "东方烟草报·渝烟视窗", "东方烟草报·幸福家专刊", "东方烟草报·泰山周刊", "今日周村", "当代健康报", "齐河报", "人民医院", "德州联合医院", "德州中联", "山东大学齐鲁医院报",
        "山东大学报", "河南日报", "河南日报-农村版", "郑州日报", "新乡日报", "洛阳日报", "安阳日报", "驻马店日报", "周口日报", "漯河日报", "濮阳日报", "焦作日报", "南阳日报",
        "许昌日报", "济源日报", "商丘日报", "鹤壁日报", "开封日报", "信阳日报", "三门峡日报", "平顶山日报", "郑州晚报", "东方今报", "大河报", "河南商报", "平原晚报", "洛阳晚报",
        "洛阳商报", "安阳晚报", "安阳慈善", "天中晚报", "周口晚报", "漯河晚报", "南阳晚报", "许昌晨报", "京九晚报", "淇河晨报", "汴梁晚报", "信阳晚报", "黄河时报", "西部晨风",
        "平顶山晚报", "期货日报", "河南法制报", "医药卫生报", "中原地铁报", "许昌晨报小记者", "南都晨报", "河南报业人", "今日魏都", "睢阳", "今日消费", "今日安阳县", "今日孟州",
        "今日修武", "梁园", "大河健康报", "教育时报", "今日永城", "河南工人日报", "湖北日报", "长江日报", "农村新报", "黄石日报", "襄阳日报", "荆州日报", "三峡日报", "黄冈日报",
        "鄂州日报", "十堰日报", "孝感日报", "荆门日报", "咸宁日报", "随州日报", "恩施日报", "仙桃日报", "天门日报", "潜江日报", "楚天快报", "长江商报", "武汉晚报", "楚天都市报",
        "楚天都市报副刊", "武汉晨报", "changjiangweekly", "东楚晚报", "襄阳晚报", "荆州晚报", "三峡晚报", "三峡商报", "鄂东晚报", "十堰晚报", "孝感晚报", "荆门晚报",
        "香城都市报", "恩施晚报", "武汉商报", "今日京山", "今日房县", "今日保康", "武汉科技报", "武汉科技报·少年科普", "东风汽车报", "今日阳新", "今日大冶", "湖南日报", "长沙晚报",
        "衡阳日报", "株洲日报", "邵阳日报", "岳阳日报", "常德日报", "张家界日报", "益阳日报", "郴州日报", "永州日报", "怀化日报", "娄底日报", "团结报", "三湘都市报", "潇湘晨报",
        "今日女报", "衡阳晚报", "株洲晚报", "邵阳晚报", "岳阳晚报", "湘阴周刊", "常德晚报", "边城晚报", "娄底晚报", "浏阳日报", "当代商报", "大众卫生报", "新城市报",
        "娄底广播电视报", "株洲新区", "人才就业社保信息报", "文萃报", "湖南工人报", "快乐老人报", "益阳城市报", "经开区周刊", "科教新报", "今日宁乡", "星沙时报", "南方日报",
        "广州日报", "深圳特区报", "珠海特区报", "汕头日报", "佛山日报", "韶关日报", "河源日报", "梅州日报", "惠州日报", "汕尾日报", "东莞日报", "中山日报", "江门日报",
        "阳江日报", "湛江日报", "茂名日报", "西江日报", "清远日报", "潮州日报", "揭阳日报", "云浮日报", "羊城晚报地方版", "新快报", "南方都市报", "羊城晚报", "羊城地铁报",
        "今日广东·侨报", "可乐生活", "信息时报", "南粤侨情·星岛日报", "深圳都市报", "深圳商报", "深圳晚报", "晶报", "深圳侨报", "珠江晚报", "梦里水乡周讯-里水社区报", "珠江时报",
        "今日张槎·张槎社区报", "魅力石湾", "桂城社区周刊-桂城社区报", "儒林九江·九江社区报", "有为丹灶·丹灶社区报", "祖庙街道社区报", "樵山社区-西樵社区报", "狮山树本周讯-狮山社区报",
        "罗村孝德·罗村社区报", "珠江商报", "东莞时报", "东江时报", "湛江晚报", "茂名晚报", "投资快报", "21世纪经济报道", "民营经济报", "中山商报", "南方法治报", "宝安日报",
        "深圳日报英文版", "南方教育时报", "番禺日报", "佛山日报-今日禅城", "艺术周刊", "惠生活", "南方工报", "佛山日报-今日三水", "佛山日报-今日高明", "珠江医院报", "企石",
        "广东科技报", "南方农村报", "广东建设报", "广东横沥", "陶城报", "老人报", "白云山中一药业", "中一健康园地", "深圳青少年报", "广州白云化工", "广州敬修堂", "海大报",
        "健康养生周刊", "今日广东·美中报导", "广州海运报", "南方电网报", "增城日报", "海南日报", "海口日报", "三亚日报", "今日儋州", "南国都市报", "海南特区报", "证券导报",
        "海南农垦报", "国际旅游岛商报", "法制时报", "海口经济学院报", "海南师范大学报", "海南大学报", "四川日报", "成都日报", "攀枝花日报", "泸州日报", "德阳日报", "绵阳日报",
        "广元日报", "遂宁日报", "内江日报", "乐山日报", "南充日报", "宜宾日报", "广安日报", "达州日报", "巴中日报", "雅安日报", "眉山日报", "资阳日报", "阿坝日报", "甘孜日报",
        "凉山日报", "西南商报", "成都晚报", "天府早报", "新城快报", "成都商报", "华西都市报", "川江都市报", "德阳晚报", "广元晚报", "绵阳晚报", "三江都市报", "南充晚报",
        "宜宾晚报", "达州晚报", "巴中晚报", "消费质量报", "每日经济新闻", "金融投资报", "四川经济日报", "四川政协报", "龙泉开发", "教育导报", "华西社区报", "国防时报",
        "华西城市读本川南新闻", "华西城市读本川东北新闻", "四川工人日报", "达州广播电视报", "成都高新", "四川民族教育报", "遂宁广播电视报", "宏达世界", "铁道建设报", "竹海长宁",
        "人力资源报", "建材商界", "四川科技报", "都江堰报", "郫都报", "新成华", "今日绵竹", "凉山广播电视报", "四川法治报", "四川农村日报", "家庭与生活报", "精神文明报",
        "西南科技大学报", "贵州日报", "贵阳日报", "贵州民族报", "遵义日报", "六盘水日报", "安顺日报", "毕节日报", "铜仁日报", "黔东南日报", "黔南日报", "黔西南日报", "贵安新区报",
        "贵州都市报", "贵阳晚报", "黔中早报", "遵义晚报", "乌蒙新报", "毕节晚报", "劳动时报", "今日余庆", "纳雍报", "威宁每日新闻", "今日金沙", "茅台时讯", "保健酒业",
        "贵州习酒", "德江报", "中国酒都报", "凤冈报", "播州报", "碧江报", "技开公司", "赤水报", "龙里周讯", "娄山关", "习水报", "绥阳报", "新天通讯", "法制生活报", "大方报",
        "今日兴义", "贵州大学报", "云南日报", "昆明日报", "昭通日报", "曲靖日报", "玉溪日报", "保山日报", "楚雄日报", "红河日报", "文山日报", "普洱日报", "西双版纳报",
        "大理日报", "德宏团结报", "丽江日报", "怒江报", "迪庆日报", "临沧日报", "云岭先锋", "都市时报", "春城晚报", "春城地铁报", "云南信息报", "云南经济日报", "云南政协报",
        "今日安宁", "云南老年报", "七都晚刊", "滇中新区报", "致富天地", "金色时光", "蒙自", "民族时报", "个旧时讯", "今日云龙", "开远市讯", "边陲金平", "曲靖师院报", "陕西日报",
        "陕西农村报", "西安日报", "各界导报", "宝鸡日报", "咸阳日报", "铜川日报", "渭南日报", "延安日报", "榆林日报", "汉中日报", "安康日报", "商洛日报", "三秦都市报", "华商报",
        "阳光报", "西北信息报", "西安晚报", "陕西广播电视报", "汉江晨刊", "城市金融报", "西安商报", "民声报", "秦巴文旅", "西部法制报", "教师报", "城乡经济特刊", "陕西科技报",
        "城市经济导报", "韩城日报", "延长石油报", "劳动者报", "陕西东岭", "思源学院报", "秦汉快讯", "铁道设计报", "科教周刊", "文化周末", "农业科技报", "陕西工人报", "甘肃日报",
        "兰州日报", "甘肃农民报", "天水日报", "酒泉日报", "张掖日报", "金昌日报", "白银日报", "平凉日报", "陇东报", "定西日报", "陇南日报", "甘南日报", "民族日报", "嘉峪关日报",
        "西部商报", "兰州晚报", "兰州晨报", "天水晚报", "甘肃经济日报", "兰州新区报", "酒钢日报", "甘肃工人报", "天水日报·教育周刊", "甘肃科技报", "金昌周末", "雄关周末",
        "青海日报", "青海藏文报", "西宁晚报", "海东时报", "柴达木日报", "黄南报", "黄南报藏文版", "西海都市报", "格尔木日报", "青海法制报", "台湾（无主体）", "内蒙古日报",
        "呼呼和浩特日报", "包头日报", "乌海日报", "赤峰日报", "通辽日报", "鄂尔多斯日报", "呼伦贝尔日报", "巴彦淖尔日报", "乌兰察布日报", "兴安日报", "锡林郭勒日报", "阿拉善日报",
        "满洲里日报", "北方新报", "内蒙古晨报", "巴彦淖尔晚报", "鄂尔多斯日报·都市版", "科尔沁都市报", "北方周末报", "包头晚报", "内蒙古商报", "伊金霍洛报", "新报", "内蒙古旅游报",
        "呼和浩特晚报", "左旗通讯", "林海日报", "内蒙古法制报", "内蒙古科技报", "乳业时报", "林西时讯", "内蒙古医科大学报", "广西日报", "南宁日报", "柳州日报", "桂林日报",
        "梧州日报", "北海日报", "钦州日报", "贵港日报", "玉林日报", "右江日报", "贺州日报", "河池日报", "来宾日报", "左江日报", "北海晚报", "南国今报", "西江都市报",
        "当代生活报", "柳州晚报", "玉林晚报", "南宁晚报", "百色早报", "南国早报", "桂林晚报", "南国城报", "广西工人报", "今日龙胜", "今日兴宁", "马山时讯", "横县时讯",
        "北部湾大学", "广西医科大学", "鹿山视界", "百色学院报", "南宁师范学院报", "旅院人", "广西大学校报", "漓院信息", "广西科技大学报", "广西民族大学报", "信科月刊",
        "广西师范大学校报", "梧州学院报", "桂林理工大学报", "独秀青年", "宁夏日报", "银川日报", "石嘴山日报", "吴忠日报", "固原日报", "中卫日报", "新消息报", "银川晚报",
        "宁夏法治报", "华兴时报", "新知讯报", "小龙人学习报", "宁夏大学报", "神华能源报", "新疆日报", "兵团日报", "乌鲁木齐晚报", "博尔塔拉报", "昌吉日报", "巴音郭楞日报",
        "阿克苏日报", "克孜勒苏日报", "克拉玛依日报", "准噶尔时报", "塔里木日报", "伊犁垦区报", "天山建设报", "天山时报", "哈密开发报", "石河子日报", "新疆都市报", "生活晚报",
        "都市消费晨报", "库尔勒晚报", "新疆经济报", "新疆农民报", "独山子石化报", "新疆法制报", "新疆石油报", "西藏日报", "拉萨日报", "昌都报", "山南报", "拉萨晚报", "西藏商报",
        "西藏法制报", "",
    ]

    check_is_exit(name_list)