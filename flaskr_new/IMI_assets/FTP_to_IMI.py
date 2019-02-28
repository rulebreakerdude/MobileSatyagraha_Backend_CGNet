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
sql_command="SELECT id FROM lb_postings WHERE status = 3 order by posted desc;"
c2.execute(sql_command)
db_response1=c2.fetchall()[0][0]
print db_response1
fileStoryName=path+str(db_response1)+".mp3"
print fileStoryName

#fetch latest story file
sql_command="SELECT id FROM lb_postings  where status = 3 and (tags like %s or message_input like %s or title like %s) order by posted desc;"
c2.execute(sql_command,("%impact%","%impact%","%impact%",))
db_response1=c2.fetchall()[0][0]
print db_response1

fileImpactName=path+str(db_response1)+".mp3"

#convert files to wav
subprocess.call(['ffmpeg', '-y', '-i', fileStoryName,  '-ar', '8000', '-ac', '1', '-b:a', "64k",  'fileStory.wav'])
subprocess.call(['ffmpeg', '-y', '-i', fileImpactName,  '-ar', '8000', '-ac', '1', '-b:a', "64k",  'fileImpact.wav'])


#Connect via FTP and transfer the files
session = ftplib.FTP('59.162.167.59','Cgnet','mdy8YtLIzxf2')


fileStory = open('fileStory.wav','rb')  # file to send
fileImpact = open('fileImpact.wav','rb') # file to send

#List the files in the current directory
print "File List:"
files = session.dir()
print files

session.storbinary('STOR First_Story.wav', fileStory)     # send the file
session.storbinary('STOR Impact_Story.wav', fileImpact)     # send the file
fileStory.close()                                    # close file and FTP
fileImpact.close()                                    # close file and FTP
session.quit()