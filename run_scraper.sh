#!/bin/bash

date >> log
./craigslist_crawler.py>>log 2>&1
df -h .>>log
date >> log
echo "-----------------------------------------" >>log
