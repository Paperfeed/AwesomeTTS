# -*- coding: utf-8 -*-


from PyQt4 import QtGui,QtCore

#Supported Languages       
# code , Language, windows charset encoding
slanguages = [['af', 'Afrikaans', 'cp1252'], #or iso-8859-1
['sq', 'Albanian',	'cp1250'], #or iso 8859-16
['ar', 'Arabic',	'cp1256'], #or iso-8859-6
['hy', 'Armenian',	'armscii-8'],
['ca', 'Catalan',	'cp1252'], #or iso-8859-1
['zh', 'Chinese',	'cp936'],
['hr', 'Croatian',	'cp1250'], #or iso-8859-2
['cs', 'Czech',		'cp1250'], #or iso-8859-2
['da', 'Danish',	'cp1252'], #or iso-8859-1
['nl', 'Dutch',		'cp1252'], #or iso-8859-1
['en', 'English',	'cp1252'], #or iso-8859-1
['fi', 'Finnish',	'cp1252'], #or iso-8859-1
['fr', 'French',	'cp1252'], #or iso-8859-1
['de', 'German',	'cp1252'], #or iso-8859-1
['el', 'Greek',		'cp1253'], #or iso-8859-7
['ht', 'Haitian Creole','cp1252'], #or iso-8859-1
['hi', 'Hindi',		'cp1252'], #or iso-8859-1
['hu', 'Hungarian',	'cp1250'], #or iso-8859-2
['is', 'Icelandic',	'cp1252'], #or iso-8859-1
['id', 'Indonesian'],
['it', 'Italian',	'cp1252'], #or iso-8859-1
['ja', 'Japanese',	'cp932'], #or shift_jis, iso-2022-jp, euc-jp
['ko', 'Korean',	'cp949'], #or euc-kr
['la', 'Latin'],
['lv', 'Latvian',	'cp1257'], #or iso-8859-13
['mk', 'Macedonian',	'cp1251'], #iso-8859-5
['no', 'Norwegian',	'cp1252'], #or iso-8859-1
['pl', 'Polish',	'cp1250'], #or iso-8859-2
['pt', 'Portuguese',	'cp1252'], #or iso-8859-1
['ro', 'Romanian',	'cp1250'], #or iso-8859-2
['ru', 'Russian',	'cp1251'], #or koi8-r, iso-8859-5
['sr', 'Serbian',	'cp1250'], # cp1250 for latin, cp1251 for cyrillic
['sk', 'Slovak',	'cp1250'], #or iso-8859-2
['es', 'Spanish',	'cp1252'], #or iso-8859-1
['sw', 'Swahili',	'cp1252'], #or iso-8859-1
['sv', 'Swedish',	'cp1252'], #or iso-8859-1
['tr', 'Turkish',	'cp1254'], #or iso-8859-9
['vi', 'Vietnamese',	'cp1258'],
['cy', 'Welsh',		'iso-8859-14']]



TTS_ADDRESS = 'http://translate.google.com/translate_tts'


import os, re, subprocess, urllib, cookielib, time
from random import uniform
from anki.utils import stripHTML
from urllib import quote_plus
import awesometts.config as config
import awesometts.util as util
from subprocess import Popen, PIPE, STDOUT
import urllib2




# Prepend http proxy if one is being used.  Scans the environment for
# a variable named "http_proxy" for all operating systems
# proxy code contributted by Scott Otterson
proxies = urllib.getproxies()

if len(proxies)>0 and "http" in proxies:
	proxStr = re.sub("http:", "http_proxy:", proxies['http'])
	TTS_ADDRESS = proxStr + "/" + TTS_ADDRESS



def get_language_id(language_code):
	x = 0
	for d in slanguages:
		if d[0]==language_code:
			return x
		x = x + 1


def playGoogleTTS(text, language):
	text = re.sub("\[sound:.*?\]", "", stripHTML(text.replace("\n", "")).encode('utf-8'))
	address = TTS_ADDRESS+'?tl='+language+'&q='+ quote_plus(text)

	if subprocess.mswindows:
		param = ['mplayer.exe', '-ao', 'win32', '-slave', '-user-agent', "'Mozilla/5.0'", address]
		if config.subprocessing:
			subprocess.Popen(param, startupinfo=util.si, stdin=PIPE, stdout=PIPE, stderr=STDOUT)
		else:
			subprocess.Popen(param, startupinfo=util.si, stdin=PIPE, stdout=PIPE, stderr=STDOUT).communicate()
	else:
		param = ['mplayer', '-slave', '-user-agent', "'Mozilla/5.0'", address]
		if config.subprocessing:
			subprocess.Popen(param, stdin=PIPE, stdout=PIPE, stderr=STDOUT)
		else:
			subprocess.Popen(param, stdin=PIPE, stdout=PIPE, stderr=STDOUT).communicate()

def playfromtagGoogleTTS(fromtag):
	for item in fromtag:
		match = re.match("(.*?):(.*)", item, re.M|re.I)
		playGoogleTTS(match.group(2), match.group(1))

def playfromHTMLtagGoogleTTS(fromtag):
	for item in fromtag:
		text = ''.join(item.findAll(text=True))
		voice = item['voice']
		playGoogleTTS(text, voice)

def recordGoogleTTS(form, text):
	global DefaultGoogleVoice
	DefaultGoogleVoice = form.comboBoxGoogle.currentIndex() #set new Default
	return TTS_record_old(text, slanguages[form.comboBoxGoogle.currentIndex()][0])


def TTS_record_old(text, language):
	text = re.sub("\[sound:.*?\]", "", stripHTML(text.replace("\n", "")).encode('utf-8'))
	url = TTS_ADDRESS+'?tl=' + language + '&q=' + text
	cookie = 'PREF=ID=86407e90cde8b907:U=9484059a8a1d2bcd:FF=4:LR=lang_en|lang_nl:LD=en:CR=2:TM=1361915611:LM=1366208091:GM=1:SG=1:S=kcO-GQbhBXiiXu7V; NID=67=REkGJ-g0wzEy5QPIKD_cX9o3yUw9VXoHb-qyS8w6qyWYWq_oCGWJon5vJ8V5Yg6QDrXA1LOkPRaVTkrX_YX-6Bz_Y9glnILDCifTE57SRFlRBf1L32_F3ncDw5uleoiyfQtHDGXthPvXgyt6p_pJ3ITdZiC10oKGM7M8b5AAZMz_D1ESKmtKE3d7uXcc-vBy1m0F3_1PFYN73SzUXka-kBF79SZ0fDtE8H9Er652D3DNseJSmg2YVMbY9JeQqA; SID=DQAAAE8BAAAuFM32zsvEOFydoEWOaE2cqqnksFSUAT9DP375tWueV_hIS1rJAKLpxyTqMThk4iUstXKJAub8T-xhhptcCq2-HtsCpHAHdlS8N0pWqvrlnYG1rpLltqAJivex1U5MlIi5JIzDnufD9bp8JjLQnbpe1NO3N4Ya8BefLVEPlfKi3zUVs_AaMsmsF5h4_lhsz91LrRKi9Lb-qQhO3XOl9BHF9q7FHrkVQz6Q7E6a3Y5IchHUEdOHoiXaHWI_LQI9pHSSlVLlT1pgzhVLp-w7rgVaSlBQLu48hBP1XRGNiqGSQobB7g1zkJIdDWQRMAgoP9mtQr7fJ6YPDhQQn8DjSE_e3JzkafpVwoQBETU3wJMp7a7igXMiHbFPpczBa32qa5VL_ls5imhLHKFXFGKU7qzUI9amFKGlq6PMLWerghufnBbV_onfgT9dwMsxbVdzmBE; HSID=AMjtxpc0Ym2NlGxni; APISID=pO-iHi7nSk_X_-H9/AR7f9xYUMTKcNwv6z; GDSESS=ID=d5de0ada6ebb0180:TM=1366207841:C=c:IP=178.85.254.34-:S=APGng0vQoVEWoUe0cvIlLVGfMX4zD35pZg'
	request = urllib2.Request(url)
	request.add_header('Host', 'translate.google.com')
	request.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.2; WOW64; rv:20.0) Gecko/20100101 Firefox/20.0')
	request.add_header('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')
	request.add_header('Accept-Language', 'en-gb,en;q=0.5')
	request.add_header('Accept-Encoding', 'gzip, deflate')
	# request.add_header('Cookie', cookie)
	request.add_header('Connection', 'keep-alive')
	# opener = urllib2.build_opener()
	
	# With cookies
	cj = cookielib.CookieJar()
	opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
	
	
	md5sum = util.string_to_md5(text)
	file = md5sum + '.mp3'
	
	try:
		if os.stat(file).st_size <= 1024:
			#file is smaller than 1kbyte and should be deleted
			os.remove(file)
	except Exception:
		# Carry on, file probably doesn't exist
		pass
		
	if not os.path.isfile(file):
		# File doesn't exist yet
		f = open(file, "wb")
		try:
			ttsResult = opener.open(request)
			# Add delay to refrain from battering Google's servers
			time.sleep(uniform(1, 4))
		except urllib2.HTTPError as e:
			# No internet or blocked from Google
			return 'ERROR'
		
		if ttsResult:
			f.write(ttsResult.read())
		f.close()
		
		try:
			if os.stat(file).st_size <= 1024:
				# File is smaller than 256 bytes and should be deleted
				os.remove(file)
				return 'ERROR'
		except Exception:
			# File doesn't exist while it should! 
			return 'ERROR'
		
	return file

def filegenerator_layout(form):
	global DefaultGoogleVoice
	verticalLayout = QtGui.QVBoxLayout()
	textEditlabel = QtGui.QLabel()
	textEditlabel.setText("Language:")

	font = QtGui.QFont()
       	font.setFamily("Monospace")
	form.comboBoxGoogle = QtGui.QComboBox()
	form.comboBoxGoogle.setFont(font)
	form.comboBoxGoogle.addItems([d[0] +' - '+ d[1] for d in slanguages])
	form.comboBoxGoogle.setCurrentIndex(DefaultGoogleVoice) # get Default

	verticalLayout.addWidget(textEditlabel)
	verticalLayout.addWidget(form.comboBoxGoogle)
	return verticalLayout

def filegenerator_run(form):
	global DefaultGoogleVoice
	DefaultGoogleVoice = form.comboBoxGoogle.currentIndex() #set new Default
	return TTS_record_old(unicode(form.texttoTTS.toPlainText()), slanguages[form.comboBoxGoogle.currentIndex()][0])

def filegenerator_preview(form):
	return playGoogleTTS(unicode(form.texttoTTS.toPlainText()), slanguages[form.comboBoxGoogle.currentIndex()][0])

DefaultGoogleVoice = get_language_id('zh')

TTS_service = {'g' : {
'name': 'Google',
'play' : playGoogleTTS,
'playfromtag' : playfromtagGoogleTTS,
'playfromHTMLtag' : playfromHTMLtagGoogleTTS,
'record' : recordGoogleTTS,
'filegenerator_layout': filegenerator_layout,
'filegenerator_preview': filegenerator_preview,
'filegenerator_run': filegenerator_run}}
