# -*- coding:utf-8 -*-
"""

# author: albert
# date: 2020/12/28
# update: 2020/12/28
"""
import cchardet
from random import choice
from loguru import logger
from retrying import retry
from requests import request, RequestException

from api_common_utils.proxy import get_abuyun_proxies


@retry(stop_max_attempt_number=3, retry_on_result=lambda x: x is None, wait_fixed=2000)
def downloader(url, method=None, header=None, timeout=None, binary=False, json=False, **kwargs):
    logger.info(f'Scraping {url}')
    _header = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36"}
    _maxTimeout = timeout if timeout else 5
    _headers = header if header else _header
    _method = "GET" if not method else method
    try:
        response = request(method=_method, url=url, headers=_headers, proxies=get_abuyun_proxies(), **kwargs)
        encoding = cchardet.detect(response.content)['encoding']
        if response.status_code == 200:
            if json:
                return response.json()
            return response.content if binary else response.content.decode(encoding)
        elif 200 < response.status_code < 400:
            logger.info(f"Redirect_URL: {response.url}")
        logger.error('Get invalid status code %s while scraping %s', response.status_code, url)
    except RequestException as e:
        logger.error(f'Error occurred while scraping {url}, Msg: {e}', exc_info=True)


if __name__ == '__main__':
    pass

