#!/usr/bin/env python
# -*- coding: utf-8 -*-
# by vellhe 2017/8/14
from pymongo import MongoClient


class Saver:
    def __init__(self, name):
        self.client = MongoClient('127.0.0.1', 27017)
        self.db = self.client["db_weibo_dafa"]
        self.collection = self.db[name]

    def insert_many(self, data, key_field=None):
        if key_field:
            data = [d for d in data if key_field in d and not self.collection.find_one({key_field: d[key_field]})]
        else:
            data = [d for d in data if not self.collection.find_one(d)]
        if data:
            self.collection.insert_many(data)

        return data


    def update_one(self, key, value):
        self.collection.update_one(key, {'$set': value, "$currentDate": {"lastModified": True}})

    def find_one(self, key=None):
        return self.collection.find_one(key)

    def find_many(self, key=None):
        return self.collection.find(key)


if __name__ == "__main__":
    s = Saver('test')
    s.insert_many([
        {'id': 'test001', 'test': 'haha1'},
        {'id': 'test002', 'test': 'haha2'},
        {'id': 'test001', 'test': 'haha3'},
        {'id': 'test001', 'test': 'haha4'},
        {'id': 'test005', 'test': 'haha5'},
    ], key_field='id')
    print(s.collection.find().count())

    # s.update_one({'id': 'test002'}, {'crawled': False})

    # s = Saver('cards')
    # card = s.find_one({'crawled': False})
    # print(card)

    # s = Saver('comments')
    # comments = s.find_many({'pid': '4140013283588453'})
    # for comment in comments:
    #     print(comment)
