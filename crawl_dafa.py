#!/usr/bin/env python
# -*- coding: utf-8 -*-
# by vellhe 2017/8/16
import logging
import sys
from sys import argv

from blog_index import Cards

logger = logging.getLogger(__name__)


def crawl(user_id):
    c = Cards(user_id)
    logger.info("===== refresh_first_page start ======")
    c.refresh_first_page()


if __name__ == "__main__":
    logging.basicConfig(stream=sys.stdout, level=logging.INFO, format='%(asctime)s %(levelname)s %('
                                                                      'filename)s[%(lineno)d]: '
                                                                      '%(message)s',
                        datefmt='[%d/%b/%Y %H:%M:%S]', )
    # c = Cards("1307651590")
    # crawl all
    # c.crawl_max_page = 10000000
    # c.start()

    if not argv or len(argv) < 2:
        logger.error("请输入要爬取的用户id")
    else:
        crawl(argv[1])
