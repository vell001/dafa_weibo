#!/usr/bin/env python
# -*- coding: utf-8 -*-
# by vellhe 2017/8/19
import codecs
import json
import os
import shutil
import copy
import imgkit
import platform

import requests
import time
from bs4 import BeautifulSoup

import cups_printer
from result_saver import Saver

template_dir = "./weibo_template"


def html2img(html_path, img_path):
    if not os.path.exists(html_path):
        return False
    if 'linux' in platform.system().lower():
        options = {'width': '300', "xvfb": ""}
    else:
        options = {'width': '300'}
    if os.path.exists(img_path):
        os.remove(img_path)
    try:
        imgkit.from_file(html_path, img_path, options)
    except Exception as e:
        print(e)
    return os.path.exists(img_path)


def card2html_str(card, html_template):
    if not card or not html_template:
        return None
    soup = BeautifulSoup(html_template, "html.parser")
    header = soup.find('header')

    blog = card['mblog']
    user = blog['user']
    user_img = header.find('img')
    user_img['src'] = user['profile_image_url']
    header.find(id='user_name').string = user['screen_name']
    header.find(class_='time').string = blog['created_at']
    header.find(class_='from').string = blog['source']

    article = soup.find('article')
    textn = article.find(id='text')
    textn.clear()
    text = BeautifulSoup(blog['text'], "html.parser")
    textn.contents = text.contents

    media_wraps = article.find(class_='weibo-media-wraps')
    media_wraps_ul = media_wraps.ul
    li_template = copy.deepcopy(media_wraps_ul.contents[1])
    media_wraps_ul.clear()

    if 'pics' in blog:
        pics = blog['pics']
        if len(pics) > 4 or len(pics) == 3:
            classes = media_wraps['class']
            if "media-a" in classes:
                classes.remove("media-a")
                classes.append("media-b")
            li_template.div['class'].append('m-imghold-square')
        for pic in pics:
            li = copy.deepcopy(li_template)
            li.find('img')['src'] = pic['url']
            media_wraps_ul.append(li)

    # footer = soup.find('footer')
    # f = footer.find(id='forward')
    # footer.find(id='forward').string = str(blog['reposts_count'])
    # footer.find(id='comment').string = str(blog['comments_count'])
    # footer.find(id='liked').string = str(blog['attitudes_count'])
    return soup.prettify()


def card2html_file(card, out_dir):
    if not card or card['card_type'] != 9:
        return False
    if os.path.exists(out_dir):
        shutil.rmtree(out_dir)
    shutil.copytree("%s" % template_dir, out_dir)
    html_path = os.path.join(out_dir, "weibo.html")
    if not os.path.exists(html_path):
        return False
    html_template = None
    with codecs.open(html_path, "r", "utf-8") as f:
        html_template = f.read()

    if not html_template:
        return False
    html = card2html_str(card, html_template)
    with codecs.open(html_path, "w", "utf-8") as f:
        f.write(html)

    return True


if __name__ == "__main__":
    s = Saver("cards")
    # card = s.find_one({'itemid': '1076031307651590_-_4107790853662723'})
    # card2html_file(card, "tmp_card")
    # html2img(os.path.join("tmp_card", "weibo.html"), "tmp_card/out.jpg")

    # cups_printer.print_img("tmp_card/out.jpg")

    for card in s.find_many():
        if not card or card['card_type'] != 9:
            continue
        now = time.localtime()
        card['mblog']['created_at'] = time.strftime("%Y-%m-%d %H:%M", now)
        now_str = time.strftime("%Y-%m-%d_%H-%M-%S", now)
        tmp_dir = "tmp/" + card['mblog']['id']
        img_path = "out/" + card['mblog']['id'] + "_" + now_str + ".jpg"

        card2html_file(card, tmp_dir)
        html2img(os.path.join(tmp_dir, "weibo.html"), img_path)
