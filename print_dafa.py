#!/usr/bin/env python
# -*- coding: utf-8 -*-
# by vellhe 2017/8/19
import logging
import os

import sys
from sys import argv

import time

from card_to_img import card2html_file, html2img
from cups_printer import print_img
from result_saver import Saver

logger = logging.getLogger(__name__)
interval_time = 1
s = Saver("cards")


def print_card(card):
    if 'insert_time' in card:
        insert_time = time.localtime(card["insert_time"])
    else:
        insert_time = time.localtime()
    card['mblog']['created_at'] = time.strftime("%Y-%m-%d %H:%M", insert_time)
    time_str = time.strftime("%Y-%m-%d_%H-%M-%S", insert_time)
    tmp_dir = "tmp/" + card['mblog']['id']

    img_path = "out/" + str(card['mblog']['user']['id']) + "/" + card['mblog']['id'] + "_" + time_str + ".jpg"

    if not os.path.exists(os.path.dirname(img_path)):
        os.makedirs(os.path.dirname(img_path))

    card2html_file(card, tmp_dir)
    html2img(os.path.join(tmp_dir, "weibo.html"), img_path)
    if print_img(img_path):
        logger.info("print succ")
    else:
        logger.error("print error")


def get_exist_cards(listen_ids):
    init_cards = dict()
    for _id in listen_ids:
        init_cards[_id] = []
        for card in s.find_many({"mblog.user.id": int(_id), 'card_type': 9}):
            if card['itemid'] not in init_cards[_id]:
                init_cards[_id].append(card['itemid'])
    return init_cards


def print(listen_ids):
    init_cards = get_exist_cards(listen_ids)

    while True:
        try:
            start_time = time.time()
            has_new = False

            for _id in listen_ids:
                for card in s.find_many({"mblog.user.id": int(_id), 'card_type': 9,
                                         "itemid": {"$nin": init_cards[_id]}}):
                    logger.info("new card: %s", card['itemid'])
                    print_card(card)
                    has_new = True

            if has_new:
                init_cards = get_exist_cards(listen_ids)

            spend_time = time.time() - start_time
            if spend_time < interval_time:
                time.sleep(interval_time - spend_time)
        except Exception as e:
            logger.error("error: %r", e)


if __name__ == "__main__":
    logging.basicConfig(stream=sys.stdout, level=logging.INFO, format='%(asctime)s %(levelname)s %('
                                                                      'filename)s[%(lineno)d]: '
                                                                      '%(message)s',
                        datefmt='[%d/%b/%Y %H:%M:%S]', )
    # listen_ids = [
    #     '1307651590',  # dafa
    #     '6343201749',  # vell
    # ]
    # print(listen_ids)

    if not argv or len(argv) < 2:
        logger.error("请输入要爬取的用户id,逗号隔开")
    else:
        print(argv[1].split(','))
