#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import reddit_2_album
import album_sender
import yaml
from telegram.ext import Updater

with open('CREDENTIALS') as f:
	CREDENTIALS = yaml.load(f, Loader=yaml.FullLoader)
tele = Updater(CREDENTIALS['bot_token'], use_context=True)
chat = tele.bot.get_chat(-1001085427906)

def test(url):
	result = reddit_2_album.get(url)
	print(result)
	album_sender.send_v2(chat, result)
	
if __name__=='__main__':
	test('https://www.reddit.com/r/chonglangTV/comments/mczh8j/%E5%85%B3%E4%BA%8E%E6%96%B0%E7%96%86%E9%9B%86%E4%B8%AD%E8%90%A5%E5%92%8C%E5%BC%BA%E5%88%B6%E5%8A%B3%E5%8A%A8/')