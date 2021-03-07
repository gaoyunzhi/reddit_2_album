#!/usr/bin/env python3
# -*- coding: utf-8 -*-

name = 'reddit_2_album'

from telegram_util import matchKey, cutCaption, getWid, parseDomain
from telegram_util import AlbumResult as Result
import yaml
import os

def getCredential():
    for root, _, files in os.walk("."):
        for file in files:
            if 'credential' in file.lower():
                 try:
                    with open(os.path.join(root, file)) as f:  
                        credential = yaml.load(f, Loader=yaml.FullLoader)
                        credential['reddit_client_id']
                        return credential
                except:
                    ...

credential = getCredential()

reddit = praw.Reddit(
    client_id=credential['reddit_client_id'],
    client_secret=credential['reddit_client_secret'],
    password=credential['reddit_password'],
    user_agent="testscript",
    username=credential['reddit_username'],
)

def get(path):
    reddit_id = path.split('/')[6]
    submission = reddit.submission(reddit_id)
    result = Result()
    if submission.url != submission.permalink:
        result.imgs = [submission.url]
    result.cap = '[ %s ]' % submission.title
    if submission.selftext:
        result.cap += '\n\n%s' % submission.selftext
    result.url = path 
    return result