#coding:utf8
import telepot
import sqlite3
import time
from pprint import pprint

def handle(msg):
	try:
		if msg['chat']['type']!="private":
			raise Exception("Please message me privately to manage your scorebook.")
		else:
			if msg['text'].startswith('/start'): # Create scorebook for user
				if conn.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='?'",str(msg['from']['id']))==[]:
					c.execute("create table ? as select * from template",str(msg['from']['id']))
					bot.sendMessage(msg['chat']['id'],"Created scorebook for "+msg['from']['first_name']+"(@"+msg['from']['username']+", "+msg['from']['id']+")")
				else:
					bot.sendMessage(msg['chat']['id'],"You already have a scorebook here.")
			if msg['text'].startswith('!update'): # Update score
				input=msg['text'].split('\n')[1:]
				'''
				msg text example:
				Future
				remaster
				118250
				4000
				191100
				324050
				486
				9
				1
				0
				'''
				diff=input[1].lower()
				if diff not in ['easy','basic','advanced','expert','master']:
					raise Exception("Invalid difficulty")
				for i in range(2,len(input)):
					input[i]=int(input[i])
				score=input[2]+input[3]+input[4]+input[5]
				currentscore=conn.execute("select %s from %s where music_title_eng='%s'"%(diff,str(msg['from']['id']),input[0].lower())).next()
				if score>currentscore:
					conn.execute("update %s set %s=%d,%s=%d,%s=%d,%s=%d,%s=%d,%s=%d,%s=%d,%s=%d,%s=%d where music_title_eng='%s'"%(str(msg['from']['id']),diff,score,"tap_"+diff,input[2],"hold_"+diff,input[3],"slide_"+diff,input[4],"break_"+diff,input[5],"perfect_"+diff,input[6],"great_"+diff,input[7],"good_"+diff,input[8],"miss_"+diff,input[9],input[0]))
				else:
					
	except Exception as e:
		bot.sendMessage(msg['chat']['id'],e.message)
# Read token from file
f=open('token.txt')
bot = telepot.Bot(f.read())
f.close()
# Initialize SQL DB
global conn
conn=sqlite3.connect('scorebook.db')
bot.message_loop(handle)
try:
	while True:
		time.sleep(1)
except KeyboardInterrupt:
	conn.commit()
	conn.close()
