import ftplib
import MySQLdb
import json
import subprocess
from datetime import datetime

path="/var/www/html/audio/"

mydb2 = MySQLdb.connect(
		host="127.0.0.1",
		port=3306,
		user="root",
		passwd="Wmtp00lr!"
		)
c2 = mydb2.cursor()
c2.execute('USE audiwikiswara;')


#fetch latest story file
sql_command="SELECT id FROM lb_postings WHERE status = 3 order by posted desc LIMIT 0,5;"
c2.execute(sql_command)
stories=c2.fetchall()
print stories


#fetch latest impact file
sql_command="SELECT id FROM lb_postings  where status = 3 and (tags like %s or message_input like %s or title like %s) order by posted desc LIMIT 0,5;"
c2.execute(sql_command,("%impact%","%impact%","%impact%",))
impacts=c2.fetchall()
print impacts

#convert files to wav
i=0
for story in stories:
	fileStoryName=path+str(story[0])+".mp3"
	name="s"+str(i)+".wav"
	subprocess.call(['ffmpeg', '-y', '-i', fileStoryName,  '-ar', '8000', '-ac', '1', '-b:a', "64k",  name])
	i=i+1

i=0
for impact in impacts:
	fileImpactName=path+str(impact[0])+".mp3"
	name="i"+str(i)+".wav"
	subprocess.call(['ffmpeg', '-y', '-i', fileImpactName,  '-ar', '8000', '-ac', '1', '-b:a', "64k",  name])
	i=i+1


#Connect via FTP and transfer the files
session = ftplib.FTP('59.162.167.59','Cgnet','mdy8YtLIzxf2')
#List the files in the current directory
print "File List:"
files = session.dir()
print files

for i in range(0,5):
	name="s"+str(i)+".wav"
	fileStory = open(name,'rb')  # file to send
	session.storbinary('STOR %s' %(name), fileStory)     # send the file
	fileStory.close()                                    # close file and FTP	
	
	name="i"+str(i)+".wav"
	fileImpact = open(name,'rb') # file to send
	session.storbinary('STOR %s' %(name), fileImpact)     # send the file
	fileImpact.close()                                    # close file and FTP
	
session.quit()

