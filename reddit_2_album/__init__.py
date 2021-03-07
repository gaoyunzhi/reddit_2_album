#!/usr/bin/env python3
# -*- coding: utf-8 -*-

name = 'reddit_2_album'

from telegram_util import matchKey, cutCaption, getWid, parseDomain
from telegram_util import AlbumResult as Result
import yaml

reddit = praw.Reddit(
	client_id=credential['reddit_client_id'],
	client_secret=credential['reddit_client_secret'],
	password=credential['reddit_password'],
	user_agent="testscript",
	username=credential['reddit_username'],
)

try:
	with open('CREDENTIALS') as f:
		credential = yaml.load(f, Loader=yaml.FullLoader)
	export_to_telegraph.token = credential.get('telegraph_token')
except:
	pass

def getCap(b, path):
	wrapper = (b.find('div', class_='weibo-text') or 
		b.find('div', class_='post f') or 
		b.find('div', class_='topic-richtext') or
		b.find('p', id='first', class_='lead'))
	if 'douban' in path:
		topic = b.find('p', class_='topic-say')
		topic = topic and topic.text
		wrapper = b.find('blockquote') or wrapper
		if topic and wrapper:
			wrapper.insert(0, '【%s】' % topic)
		title = b.find('td', class_='tablecc')
		if title:
			return title.text[3:]
	if 'zhihu' in path:
		answer = b.find('div', class_='RichContent-inner')
		answer = answer and answer.text.strip()
		if answer:
			return cutCaption(answer, '', 200)
	if not wrapper:
		return ''
	return export_to_telegraph.exportAllInText(wrapper)

def getCapForce(b, path):
	for name in ['h1', 'h2']:
		if b.find(name):
			text = b.find(name).text
			if 'douban' in path:
				return text.split('-')[-1]
			else:
				return text
	# don't know if this is the right thing to do, revisit if needed
	center = readee.export(path, content = str(b))
	try:
		return cutCaption(center.get_text(separator='\n').strip(), '', 200)
	except:
		return ''

def isWeiboArticle(path):
	return matchKey(path, ['card', 'ttarticle']) and 'weibo.c' in path

def isValidSrc(candidate):
	return candidate and not matchKey(candidate, ['data:image'])

def getValidSrc(*candidates):
	for candidate in candidates:
		if isValidSrc(candidate):
			return candidate

def getSrc(img, path):
	src = getValidSrc(img.get('data-full'), img.get('data-original'), 
		img.get('data-actualsrc'), img.get('src'), img.get('data-src'))
	src = src and src.strip()
	if not src:
		return 
	if not img.parent or not img.parent.parent:
		return 
	if 'reddit' in path:
		if img.parent.name != 'a':
			return
		return img.parent['href']
	if 'blog.boxun' in path:
		return '/'.join(path.split('/')[:-1] + [src])
	if isWeiboArticle(path) and 'sinaimg' in src:
		return src
	wrapper = img.parent.parent
	if 'detail' in sys.argv:
		print(str(wrapper.get('class')))
	if matchKey(str(wrapper.get('class')) or '', IMG_CLASSES):
		return src
	return

def enlarge(src, img):
	if not src:
		return None
	src = src.replace('/m/', '/l/')
	if 'animate' in img.parent.get('class', ''):
		src = '.'.join(src.split('.')[:-1]) + '.mp4'
	return src

def withDomain(path, x):
	if x.startswith('//'):
		return 'https:' + x
	if 'slideshare' in x:
		x = x.split('?')[0]
	if x and x[0] == '/':
		return parseDomain(path) + x
	return x

def getImgs(b, path):
	raw = [enlarge(getSrc(img, path), img) for img in b.find_all('img')]
	return [withDomain(path, x) for x in raw if x]

def getVideo(b):
	for video in b.find_all('video'):
		if not video.parent or not video.parent.parent:
			continue
		wrapper = video.parent.parent
		source = video.find('source')
		source = source and source['src']
		if source:
			return source
		if not matchKey(str(wrapper.get('id')), ['video_info']):
			continue
		return video['src']

def getContent(path, force_cache=False):
	if isWeiboArticle(path):
		new_url = ('https://card.weibo.com/article/m/aj/detail?id=' + 
			getWid(path) + '&_t=' + str(int(time.time())))
		json = yaml.load(
			cached_url.get(new_url, headers={'referer': path}, force_cache=force_cache), 
			Loader=yaml.FullLoader)
		return '<div><title>%s</title>%s</div>' % (json['data']['title'], json['data']['content'])
	return cached_url.get(path, force_cache=force_cache)

def get(path):
	reddit_id = path.split('/')[6]
	reddit.submission(reddit_id)
	result = Result()
	result.imgs = getImgs(b, path)
	result.cap = getCap(b, path)
	result.url = path
	return result