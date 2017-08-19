#!/usr/bin/env python
# -*- coding: utf-8 -*-
# by vellhe 2017/8/14
import json

import logging
import requests
import time

try_num = 10
logger = logging.getLogger(__name__)
headers = {
    'Accept': 'application/json, text/plain, */*',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6',
    'Connection': 'keep-alive',
    # 'Cookie': '_T_WM=b6ca05a59f18cb990ddd268ca31fb691; WEIBOCN_WM=3349; ALF=1505266490; '
    #           'SCF=AjP4SWnHhPH6vz0Tc8g3NFCL8MhjFOMrOx432DF5IQO52X7u6ebnLchGezPKLLALywpF0'
    #           'mQymjSj0hVoPVHHpFE.; SUB=_2A250lI5qDeRhGeBN71ET8C_LzzWIHXVUdhIirDV6PUJbkt'
    #           'BeLWfbkW1q-kIPiGzXMYt7kGUcWn474Mz93A..; SUBP=0033WrSXqPxfM725Ws9jqgMF5552'
    #           '9P9D9WFCh6_hHLYD8SPs4nSkyes95JpX5o2p5NHD95Qce0B0eo5pS0B4Ws4Dqcjgi--fi-z7i'
    #           'Kysi--Ni-iFi-zXUJHjd5tt; SUHB=0tKaQOTlZqh8Ln; SSOLoginState=1502674490; M'
    #           '_WEIBOCN_PARAMS=oid%3D4140013283588453%26luicode%3D20000061%26lfid%3D4140013283588453',
    'Host': 'm.weibo.cn',
    'Referer': 'https://m.weibo.cn/status/4138591468653529',
    'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/60.0.3112.90 Mobile Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest',
}
proxies = {
    # 'http': 'http://111.202.120.52:8088',
    # 'https': 'http://111.202.120.52:8088',
}

max_rate = 3
_last_crawl_time = time.time()
_cur_count = 0
error_414_sleep_time = 60
error_403_sleep_time = 10


def is_rate_ok():
    global _last_crawl_time
    global _cur_count
    global max_rate
    now = time.time()
    d = now - _last_crawl_time
    if d > 1:
        _cur_count = 1
        _last_crawl_time = now
        return True
    else:
        if _cur_count >= max_rate:
            # 超过rate值
            return False
        else:
            _cur_count += 1
            return True


def get(url, referer=None):
    global try_num
    global _cur_count
    global headers
    _try_num = 0
    while not is_rate_ok():
        logger.info("rate is not ok, cur_count: %d, sleep...", _cur_count)
        time.sleep(1)
    _headers = headers.copy()
    if not referer:
        _headers['Referer'] = url
    else:
        _headers['Referer'] = referer
    while _try_num < try_num:
        _try_num += 1
        try:
            resp = requests.get(url, headers=_headers, proxies=proxies)
            if resp.status_code == 200 and resp.content:
                ret = json.loads(str(resp.content, encoding="utf-8"))
                if 'ok' in ret and ret['ok'] == 1:
                    return ret
                else:
                    logger.error("ret not ok, try_num %d, ret: %s, url: %s", _try_num, resp.content, url)
                    time.sleep(3)
            elif resp.status_code == 414 or resp.status_code == 403:
                logger.error("status_code %d, crawler_error, url: %s, sleep...", resp.status_code, url)
                if resp.status_code == 403:
                    time.sleep(error_403_sleep_time)
                else:
                    time.sleep(error_414_sleep_time)
                _try_num -= 1
                continue
            else:
                logger.error("request error, try_num %d code %d, url: %s", _try_num, resp.status_code, url)
                time.sleep(10)
            _cur_count -= 1
        except Exception as e:
            logger.error("request error, url: %s  %r", url, e)
            time.sleep(3)
    return None


if __name__ == "__main__":
    print(get("https://m.weibo.cn/api/container/getIndex?type=uid&value=5698023579&containerid=1076035698023579"))
