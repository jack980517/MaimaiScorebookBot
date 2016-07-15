#coding:utf8
import telepot
import sqlite3
import time
from pprint import pprint

def handle(msg):
	if msg['chat']['type']!="private":
		bot.sendMessage(msg['chat']['id'],"Please message me privately to manage your scorebook.")
	else:
		if msg['text'].startswith('/start'): # Create scorebook for user
			c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='?'",str(msg['from']['id']))
			result=c.fetchall()
			if result==[]:
				c.execute("create table ? as select * from template",str(msg['from']['id']))
				bot.sendMessage(msg['chat']['id'],"Created scorebook for @"+msg['from']['username']+" ("+msg['from']['id']+")")
			else:
				bot.sendMessage(msg['chat']['id'],"You already have a scorebook here.")
		if msg['text'].startswith('!update'): # Update score
			input=msg['text'].split('\n')
			'''
			msg text example:
			Future
			remaster
			118250
			4000
			191100
			324050
			9
			1
			0
			'''
			

# Read token from file
f=open('token.txt')
bot = telepot.Bot(f.read())
f.close()
# Initialize SQL DB
global conn
conn=sqlite3.connect('scorebook.db')
c=conn.cursor()
bot.message_loop(handle)
try:
	while True:
		time.sleep(1)
except KeyboardInterrupt:
	conn.commit()
	conn.close()