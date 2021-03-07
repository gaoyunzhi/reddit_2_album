#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import reddit_2_album
import album_sender
import yaml
from telegram.ext import Updater

with open('CREDENTIALS') as f:
	CREDENTIALS = yaml.load(f, Loader=yaml.FullLoader)
tele = Updater(CREDENTIALS['bot_token'], use_context=True)
chat = tele.bot.get_chat(CREDENTIALS['channel'])

def test(url):
	result = reddit_2_album.get(url)
	print(result)
	album_sender.send_v2(chat, result)
	
if __name__=='__main__':
	test('https://www.reddit.com/r/Feminism/comments/libkyn/i_thought_everyone_needed_to_see_this/')