#!/usr/bin/env python
# -*- coding: utf-8 -*-
# by vellhe 2017/8/11

import logging
from multiprocessing.pool import ThreadPool

import time

import weibo_request
from result_saver import Saver

logger = logging.getLogger(__name__)


class Cards(object):
    base_url = "https://m.weibo.cn/api/container/getIndex"
    cur_page = 1
    max_page = -1
    crawl_max_page = 100
    crawled_page = 0
    containerid = None
    thread_num = 2
    status = -1

    def __init__(self, u_id):
        self.u_id = u_id
        self.saver = Saver("cards")
        self.url = None

    def get_index(self, page=None, containerid=None):
        self.url = "%s?type=uid&value=%s" % (self.base_url, self.u_id)
        if page:
            self.url += "&page=%d" % page
        if containerid:
            self.url += "&containerid=%s" % containerid

        logger.debug("get_index: %s", self.url)

        return weibo_request.get(self.url)

    def save_ret(self, ret):
        if not ret:
            logger.error("ret is none, %s", self.url)
            return None
        cards = []
        if ret['cards']:
            for card in ret['cards']:
                card['uid'] = self.u_id
                card['crawled'] = False
                card['insert_time'] = time.time()
                cards.append(card)
            return self.saver.insert_many(cards, key_field="itemid")
        return None

    def run(self, tid):
        while True:
            self.cur_page += 1
            self.crawled_page += 1
            if not self.containerid or self.cur_page > self.max_page or self.crawled_page > self.crawl_max_page:
                break

            ret = self.get_index(self.cur_page, self.containerid)
            self.max_page = int(ret['cardlistInfo']['total'] / 10) + 1

            self.save_ret(ret)

    def start(self):
        if self.status > 0:
            logger.info("已经运行过了, %d", self.status)
            pass
        self.status = 0

        # 获取containerid
        if not self.containerid:
            try:
                ret = self.get_index()
                self.containerid = ret['tabsInfo']['tabs'][1]['containerid']
            except Exception as e:
                logging.error("containerid error: %r", e)

        if not self.containerid:
            logger.error("containerid 貌似有问题哦")
            self.status = 1
            pass

        # 获取max_page
        if self.max_page < 0:
            ret = self.get_index(1, self.containerid)
            self.max_page = int(ret['cardlistInfo']['total'] / 10) + 1
            self.save_ret(ret)

        if self.max_page < 0:
            logger.error("max_page貌似有问题哦")
            self.status = 1
            pass

        p = ThreadPool(self.thread_num)
        p.map(self.run, range(self.thread_num))
        p.close()
        p.join()

        self.status = 1

        logger.info("crawl succ uid:%s max_page:%d", self.u_id, self.max_page)

    def refresh_first_page(self, sleep_time=1):
        # 获取containerid
        if not self.containerid:
            try:
                ret = self.get_index()
                self.containerid = ret['tabsInfo']['tabs'][1]['containerid']
            except Exception as e:
                logging.error("containerid error: %r", e)

        if not self.containerid:
            logger.error("containerid 貌似有问题哦")
            self.status = 1
            pass

        while True:
            try:
                ret = self.get_index(1, self.containerid)
                saved_data = self.save_ret(ret)
                if saved_data:
                    logger.info("new cards: %r", saved_data)

                time.sleep(sleep_time)
            except Exception as e:
                logger.error("error %r", e)


if __name__ == "__main__":
    logging.basicConfig(filename='logs/blog_index.log', level=logging.INFO, format='%(asctime)s %(levelname)s %(filename)s[%(lineno)d]: '
                                                                                   '%(message)s', datefmt='[%d/%b/%Y %H:%M:%S]', )
    c = Cards("5698023579")
    c.start()
