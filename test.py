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
	test('https://www.reddit.com/r/Feminism/comments/lmlxk9/being_decent_isnt_difficult/')
	# test('https://www.reddit.com/r/Feminism/comments/llt9y5/a_womans_place_is_one_of_servitude/')
	# test('http://www.reddit.com/r/Feminism/comments/lz1nj2/truth/')
	# test('http://www.reddit.com/r/Feminism/comments/lyz02f/behold_the_protective_power_of_soiled_sanity_pads/')
	# test('http://www.reddit.com/r/Feminism/comments/lya1fw/the_answer_is_no/')
	# test('https://www.reddit.com/r/Feminism/comments/lwz97t/dump_the_dimorphism_between_female_and_male_brain/')
	# test('https://www.reddit.com/r/Feminism/comments/lu9nbg/exactly/')
	# test('https://www.reddit.com/r/Feminism/comments/lqz8cp/genderneutral_laws_would_make_topless_women_legal/')
	# test('https://www.reddit.com/r/Feminism/comments/ll27y8/wild/')