#!/usr/bin/env bash

mkdir -p ./data/mongodb_data

rm ./data/mongodb_data/*.lock
nohup mongod --dbpath ./data/mongodb_data &>> ./logs/mongod_`date +%F`.log &

sleep 10

nohup python3 print_dafa.py 1307651590,6343201749 &>> ./logs/print_dafa_`date +%F`.log &

nohup python3 crawl_dafa.py 1307651590 &>> ./logs/crawl_dafa_1307651590_`date +%F`.log &
nohup python3 crawl_dafa.py 6343201749 &>> ./logs/crawl_dafa_6343201749_`date +%F`.log &
