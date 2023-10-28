#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
日期工具组。
# author: Trico
# date: 2020.1.8
# update: 2020.1.8
"""

import re
import time
import datetime


def str_to_timestamp(str_text):
    """
    Sylvan作品，字符串转化时间戳。
    :return:
    """

    # 参数验证。
    if not str_text or not isinstance(str_text, str):
        raise TypeError("The insert values({}) is not a type of str.".format(type(str_text)))

    # noinspection PyBroadException
    try:
        # 分析精确时间。
        final_timestamp = int(time.mktime(time.strptime(str_text, '%Y-%m-%dT%H:%M:%S.%fZ')))
        final_timestamp += 3600 * 8
        return final_timestamp
    except Exception:
        pass

    str_text = str_text.strip().replace("\n", "").replace(" ", "")
    # noinspection PyBroadException
    try:
        if str(str_text).startswith("http"):
            temp = re.search(r"http[s]?://(.*?)/", str_text).group()
            str_text = str(str_text).replace(temp, "")
        pattern = r"(?P<year>(20|21)\d{2})[_.年/-]?" \
                  r"(?P<month>\d{1,2})[_.月/-]?" \
                  r"(?P<day>\d{1,2})[_.日/]?" \
                  r"([\s]{0,4}" \
                  r"(?P<hour>\d{1,2})[:：]" \
                  r"(?P<minute>\d{1,2})([:：]" \
                  r"(?P<second>\d{1,2}))?)?"
        match = re.search(pattern, str_text, flags=0)
        if match is not None:
            group_dict = match.groupdict()
            year = "0000"
            month = "00"
            day = "00"
            hour = "00"
            minute = "00"
            second = "00"
            if 'year' in group_dict:
                year = group_dict["year"]
                if len(year) == 2:
                    nowyear = str(datetime.datetime.now().year)[0:2]
                    year = nowyear + year
            if 'month' in group_dict:
                month = group_dict["month"]
                if len(month) == 1:
                    month = "0" + month
            if 'day' in group_dict:
                day = group_dict["day"]
                if len(day) == 1:
                    day = "0" + day
            if group_dict["hour"] is not None:
                hour = group_dict["hour"]
                if len(hour) == 1:
                    hour = "0" + hour
            if group_dict["minute"] is not None:
                minute = group_dict["minute"]
                if len(minute) == 1:
                    minute = "0" + minute
            if group_dict["second"] is not None:
                second = group_dict["second"]
                if len(second) == 1:
                    second = "0" + second
            public_time = year + month + day + hour + minute + second
            time_array = time.strptime(public_time, "%Y%m%d%H%M%S")
            time_stamp = int(time.mktime(time_array))
            if time_stamp < int(time.time()):
                return time_stamp
    except Exception:
        return None

    return None


def relative_str_to_timestamp(input_string):
    """
    将相对时间字符串转为时间戳，如"昨天"、"1小时前"。
    :return:
    """

    # 参数验证。
    if not isinstance(input_string, str):
        raise TypeError("The insert values({}) is not a type of str.".format(type(input_string)))

    # 当前时刻。
    now = int(time.time())

    # noinspection PyBroadException
    try:
        match_obj = re.search(r".*?(\d+)秒前", input_string, flags=re.S | re.I)
        if match_obj:
            groups = match_obj.groups()
            if groups:
                number = int(groups[0])
                final_timestamp = now - number
                return int(final_timestamp)

        match_obj = re.search(r".*?(\d+)分钟前", input_string, flags=re.S | re.I)
        if match_obj:
            groups = match_obj.groups()
            if groups:
                number = int(groups[0])
                final_timestamp = now - number * 60
                return int(final_timestamp)

        match_obj = re.search(r".*?(\d+)小时前", input_string, flags=re.S | re.I)
        if match_obj:
            groups = match_obj.groups()
            if groups:
                number = int(groups[0])
                final_timestamp = now - number * 3600
                return int(final_timestamp)

        if input_string == "昨天":
            final_timestamp = now - 1 * 86400
            return int(final_timestamp)

        if input_string == "前天":
            final_timestamp = now - 2 * 86400
            return int(final_timestamp)

        match_obj = re.search(r".*?(\d+)天前", input_string, flags=re.S | re.I)
        if match_obj:
            groups = match_obj.groups()
            if groups:
                number = int(groups[0])
                final_timestamp = now - number * 86400
                return int(final_timestamp)

        if input_string == "刚刚":
            final_timestamp = now
            return int(final_timestamp)

        # noinspection PyBroadException
        try:
            final_timestamp = time.mktime(time.strptime(input_string, "%Y.%m.%d"))
            return int(final_timestamp)
        except Exception:
            # print(traceback.format_exc())
            pass

        # noinspection PyBroadException
        try:
            year_s, mon_s, day_s = input_string.split("-")
            if len(mon_s) == 1:
                mon_s = "0%s" % mon_s
            if len(day_s) == 1:
                day_s = "0%s" % day_s
            input_string = "-".join([year_s, mon_s, day_s])
            final_timestamp = time.mktime(time.strptime(input_string, "%Y-%m-%d"))
            return int(final_timestamp)
        except Exception:
            # print(traceback.format_exc())
            pass
    except Exception:
        return None

    return None


if __name__ == '__main__':
    print(str_to_timestamp("http://tw.fjtv.net/folder744/2020-01-20/2154224.html"))
    # print(relative_str_to_timestamp("昨天"))
