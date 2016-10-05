#coding:utf8

##################################### TODO #####################################
# Unify column names and input names
# Unify columns from different tables
# Add column for AR


import telepot
import sqlite3
import os
from pprint import *

# Read token from file
f=open('token.txt')
bot = telepot.Bot(f.read())
f.close()
# Initialize SQL DB
global conn
conn=sqlite3.connect('scorebook.db')
while True:
	try:
		if os.path.exists('lastoffset'):
			f=open('lastoffset')
			offset=int(f.read())
			f.close()
		else:
			offset=0
		updates=bot.getUpdates(offset=offset+1)
		if updates==[]:
			continue
		else:
			f=open('lastoffset','w')
			f.write(str(updates[-1]['update_id']))
			f.close()
			for i in updates:
				msg=i['message']
				try:
					if msg['chat']['type']!="private":
						raise Exception("Please message me privately to manage your scorebook.")
					else:
						if msg['text'].startswith('/start'): # Create scorebook for user
							if conn.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='%s'"%(str(msg['from']['id']))).fetchall()==[]:
								conn.execute("create table '%s' as select * from template"%(str(msg['from']['id'])))
								bot.sendMessage(msg['chat']['id'],"Created scorebook for "+msg['from']['first_name']+"(@"+msg['from']['username']+", "+str(msg['from']['id'])+")")
							else:
								bot.sendMessage(msg['chat']['id'],"You already have a scorebook here.")
						if msg['text'].startswith('/help'): # Help
							f=open('help.txt')
							helpmsg=f.read()
							f.close()
							bot.sendMessage(msg['chat']['id'],helpmsg,parse_mode='Markdown')
						if msg['text'].startswith('!update'): # Update score
							input=msg['text'].split('\n')[1:]
							diff=input[1].lower()
							if diff not in ['easy','basic','advanced','expert','master','remaster']:
								raise Exception("Invalid difficulty")
							for i in range(2,len(input)):
								input[i]=int(input[i])
							# Read song info and analyze
							songmaxscores=conn.execute("select tap_%s,hold_%s,slide_%s,break_%s from '%s' where music_title_eng='%s'"%(diff,diff,diff,diff,'musicinfo',input[0].lower())).fetchall()
							if songmaxscores==[]:
								raise Exception('No such song')
							songmaxscores=songmaxscores[0]
							songmaxscore=sum(songmaxscores)
							score=input[2]+input[3]+input[4]+input[5]
							totalnotes=[songmaxscores[0]/500,songmaxscores[1]/1000,songmaxscores[2]/1500,songmaxscores[3]/2500]
							msgtext="Tap: %d/%d\nHold: %d/%d\nSlide: %d/%d\nBreak: %d/%d/%d\n\nPerfect: %d\nGreat: %d\nGood: %d\nMiss: %d\n\n%.2f%%\n%d/%d/%d\n\n"%(input[2],songmaxscores[0],input[3],songmaxscores[1],input[4],songmaxscores[2],input[5],songmaxscores[3],songmaxscores[3]/25*26,input[6],input[7],input[8],input[9],1.0*score/songmaxscore*100,score,songmaxscore,sum(songmaxscores[:-1])+songmaxscores[-1]/25*26)
							# Check for any errors
							for i in range(0,4):
								if sum(input[6:])>sum(totalnotes):
									raise Exception('Note count error')
								if input[i+2]>songmaxscores[i]:
									if i==3 and input[5]<=songmaxscores[3]/25*26:
										continue
									else:
										raise Exception('Score error')
							# Compare and update score
							currentscore=conn.execute("select %s from '%s' where music_title_eng='%s'"%(diff,str(msg['from']['id']),input[0].lower())).fetchone()[0]
							if score>currentscore:
								msgtext+="New high score! Updating record."
								conn.execute("update '%s' set %s=%d,%s=%d,%s=%d,%s=%d,%s=%d,%s=%d,%s=%d,%s=%d,%s=%d where music_title_eng='%s'"%(str(msg['from']['id']),diff,score,"tap_"+diff,input[2],"hold_"+diff,input[3],"slide_"+diff,input[4],"break_"+diff,input[5],"perfect_"+diff,input[6],"great_"+diff,input[7],"good_"+diff,input[8],"miss_"+diff,input[9],input[0]))
							else:
								msgtext+="Score not higher than current record. Not updating."
							bot.sendMessage(msg['chat']['id'],msgtext)
						if msg['text'].startswith('!query'): # Query existing record
							input=msg['text'].split('\n')[1:]
							result=conn.execute("select * from '%s' where music_title_eng='%s'"%(str(msg['from']['id']),input[0])).fetchall()
							bot.sendMessage(msg['chat']['id'],pformat(result))
				except KeyboardInterrupt:
					raise
				except Exception as e:
					bot.sendMessage(msg['chat']['id'],pformat(e))
	except KeyboardInterrupt:
		print 'Shutting down...'
		conn.commit()
		conn.close()
		exit()