#coding:utf8
import telepot
import sqlite3
import time
from pprint import pprint

def handle(msg):
	if msg['chat']['type']!="private":
		bot.sendMessage(msg['chat']['id'],"Please manage me privately to manage your scorebook.")
	else:
		if msg['text']=='/start':
			

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