#DB Functions

#import * safe
import MySQLdb
import re
from datetime import date, timedelta
from utilities import *

DB_USER = 'spark'
DB_PASSWD = 'Wmtp00lr!'
DB_HOST = '127.0.0.1'
DB_PORT = 3306
DB_NAME = 'audiwikiswara'


class Database:
    def __init__(self,db_port=DB_PORT,db_host=DB_HOST,
                db_user=DB_USER,db_passwd=DB_PASSWD,db_name=DB_NAME):
        self.db = MySQLdb.connect(port=db_port,host=db_host,
                                user=db_user,passwd=db_passwd)
        self.c = self.db.cursor()
        self.c.execute('USE '+db_name+';')
        
    def channelExists(self, channelNum):
        count = self.c.execute("SELECT * FROM stations WHERE number = %s",
                                (str(channelNum),))
        return count>0
        
    def getPostsInChannel(self, channelNum, swaraChannel, caller):
        # get circle of caller
        debugPrint("DEBUG caller = " + caller)
        self.c.execute("SELECT circle FROM mobileseries WHERE series = %s;", (str(caller)[:4],))
        circle = self.c.fetchall()
        if (len(circle)==0) or (not circle[0]) or (len(circle[0])==0) or (not circle[0][0]):
            circle = "un"
        else:
            circle = circle[0][0].lower()

        debugPrint('CIRCLE: "' + circle + '"')

        if (swaraChannel == "main"):
            # in the main channel, select by circle
            self.c.execute("SELECT * FROM lb_postings WHERE station = %s and status = 3 and upper(audio_file) like '%%MP3' and circle_" + circle + " = 1 and playon_main = 1 ORDER BY posted DESC;",(str(channelNum),))
        elif (swaraChannel == "training"):
            # in training channel, play everything regardless of 'status'
            self.c.execute("SELECT * FROM lb_postings WHERE station = %s and upper(audio_file) like '%%MP3' and playon_training = 1 ORDER BY posted DESC;",(str(channelNum),))
        else:
            # otherwise, select by channel
            self.c.execute("SELECT * FROM lb_postings WHERE station = %s and status = 3 and upper(audio_file) like '%%MP3' and playon_" + swaraChannel + " = 1 ORDER BY posted DESC;",(str(channelNum),))
        posts = self.c.fetchall()
        posts = [i[0] for i in posts]
        return posts

    def getImpactPostsInChannel(self, channelNum, swaraChannel, caller):
        debugPrint("DEBUG impact caller = " + caller)
        if swaraChannel == "main":
            self.c.execute("SELECT * FROM lb_postings WHERE station = %s and status = 3 and upper(title) like 'IMPACT%%' and upper(audio_file) like '%%MP3' and playon_main = 1 ORDER BY posted DESC;", (str(channelNum),))
        else:
            self.c.execute("SELECT * from lb_postings where station = %s and status = 3 and upper(title) like 'IMPACT%%' and upper(audio_file) like '%%MP3' and playon_" + swaraChannel + " = 1 ORDER BY posted DESC;", (str(channelNum),))
        posts = self.c.fetchall()
        posts = [i[0] for i in posts]
        return posts 
		
    def getCustomPostsInChannel(self, channelNum, swaraChannel, caller):
        debugPrint("DEBUG Custom caller = " + caller)
        if swaraChannel == "main":
            self.c.execute("SELECT * FROM lb_postings WHERE station = %s and status = 3 and user = %s and upper(audio_file) like '%%MP3' and playon_main = 1 ORDER BY posted DESC;", (str(channelNum),str(caller),))
        else:
            self.c.execute("SELECT * from lb_postings where station = %s and status = 3 and user = %s and upper(audio_file) like '%%MP3' and playon_" + swaraChannel + " = 1 ORDER BY posted DESC;", (str(channelNum),str(caller),))
        posts = self.c.fetchall()
        posts = [i[0] for i in posts]
        return posts 

    def getPostUser(self, channelNum,post):
        self.c.execute("SELECT user FROM lb_postings WHERE station = %s and id=%s;",(str(channelNum),str(post),))
        posts = self.c.fetchall()
        posts = [i[0] for i in posts]
        return posts[0]
    def getPostDetails(self, channelNum,post):
        self.c.execute("SELECT * FROM lb_postings WHERE station = %s and id=%s;",(str(channelNum),str(post),))
        posts = self.c.fetchall()
        #posts = [i[0] for i in posts]
        return posts
    def getAllPostsInChannel(self, channelNum):
        self.c.execute("SELECT * FROM lb_postings WHERE station = %s ORDER BY posted DESC;",
						(str(channelNum),))
        posts = self.c.fetchall()
        posts = [i[0] for i in posts]
        return posts
    
    def getAllPostsInChannelExceptImpact(self, channelNum):
        self.c.execute("SELECT * FROM lb_postings WHERE (station = %s) and (upper(title) not like 'IMPACT%%') ORDER BY posted DESC;", (str(channelNum),))
        posts = self.c.fetchall()
        posts = [i[0] for i in posts]
        return posts
    def getTagsforPost(self, channelNum, post):
        self.c.execute("SELECT tags  FROM lb_postings WHERE station = %s and id=%s;",(str(channelNum),str(post),))
        tags = self.c.fetchall()
        tags = [i[0] for i in tags]
        return tags

    def getTitleforPost(self, channelNum, post):
        self.c.execute("SELECT title  FROM lb_postings WHERE station = %s and id=%s;",(str(channelNum),str(post),))
        title = self.c.fetchall()
        title = [i[0] for i in title]
        return title
    
    def getMessageforPost(self, channelNum, post):
        self.c.execute("SELECT message_input  FROM lb_postings WHERE station = %s and id=%s;",(str(channelNum),str(post),))
        message = self.c.fetchall()
        message = [i[0] for i in message]
        return message
    def getLengthforPost(self, channelNum, post):
        self.c.execute("SELECT audio_length  FROM lb_postings WHERE station = %s and id=%s;",(str(channelNum),str(post),))
        length = self.c.fetchall()
        length = [i[0] for i in length]
        return length
    
    def deletePost(self, postID):
        self.c.execute("DELETE FROM lb_postings WHERE id = %s;",
                        (str(postID),))
        self.db.commit()


    def publishPost(self, postID):
        self.c.execute("UPDATE lb_postings SET status = 3 WHERE id = %s;",
						(str(postID),))
        self.db.commit()

    def updateAuthor(self, auth,postID):
        self.c.execute("UPDATE lb_postings SET author_id = %s WHERE id = %s;",(str(auth),str(postID),))
        self.db.commit()
    def updatePostLength(self, length,postID):
        self.c.execute("UPDATE lb_postings SET audio_length = %s WHERE id = %s;",(str(length),str(postID),))
        self.db.commit()
    
    def archivePost(self, postID):
        self.c.execute("UPDATE lb_postings SET status = 2 WHERE id = %s;",
						(str(postID),))
	self.db.commit()

    def newCall(self, user):
        self.c.execute("INSERT INTO callLog (user) values (%s);",(str(user),))
        self.db.commit()
        #Arjun patched for analytics
        self.c.execute("SELECT LAST_INSERT_ID() FROM callLog;")
        callID=self.c.fetchall()
        callID=[i[0] for i in callID]
        return callID[0]

    def removeUserfromKeypress(self, user):
        self.c.execute("delete from keyPress where phoneNumber={0} and sms_sent=false;".format(user))
        self.db.commit()


    def recordKeyPress(self, key, phoneNumber, call_id):
        debugPrint("recordKeyPress call_id=" + str(call_id) + " key=" + str(key) + " phoneNumber=" + str(phoneNumber));
        self.c.execute('SELECT id FROM keyPress where cdr_id = {0} and keypressed = {1} and phoneNumber = "{2}";'.format(call_id, key, phoneNumber))
        row = self.c.fetchone()
        if row is not None and len(row) > 0 and row[0] is not None:
            self.c.execute('UPDATE keyPress set cntr = cntr + 1 where cdr_id = {0} and keypressed = {1} and phoneNumber="{2}";'.format(call_id, key, phoneNumber))
        else:
            self.c.execute("INSERT INTO keyPress (keypressed, phoneNumber, cdr_id, cntr) values ({0}, '{1}', {2}, 1);".format(key, phoneNumber, call_id))
        self.db.commit()



    def recordKeyPress2(self, key, phoneNumber, call_id):
        # debugPrint("key is %d" % (key))
        debugPrint("call id is %d" % (call_id))
        self.c.execute("INSERT INTO keyPress (keypressed, phoneNumber, cdr_id) values ({0:d}, {1:s}, {2}) ON DUPLICATE KEY UPDATE cntr = cntr + 1;".format(key, phoneNumber, call_id))
        self.db.commit()

    def addUser(self, phoneNumberString):
        self.c.execute("INSERT INTO users (phone_number) " + \
                       "VALUES (%s);",(str(phoneNumberString),))
        self.db.commit()
    

    
    def addAuthor(self, phoneNumberString):
        self.c.execute("INSERT INTO lb_authors(nickname) " + \
                       "VALUES (%s);",(str(phoneNumberString),))
        self.db.commit()
        self.c.execute("SELECT LAST_INSERT_ID() FROM lb_authors;")
        authID=self.c.fetchall()
        authID=[i[0] for i in authID]
        return authID[0]
    
    def isUser(self, phoneNumberString):
        count = self.c.execute(
            "SELECT phone_number FROM users WHERE phone_number = %s;"
                                            ,(str(phoneNumberString),))
        return count>0
    
     
    
    def getAuthDetails(self, nickname):
        auth=self.c.execute("SELECT * FROM lb_authors WHERE nickname = %s;" ,(str(nickname),))
        if auth == 0:
            return auth
        else:
            auth=self.c.fetchall()
            auth=[i[0] for i in auth]
            return auth[0]

    def getCommentIDs(self):
        self.c.execute("""SELECT id from lb_postings WHERE status = 3 \
                        ORDER BY posted DESC;""")
        # Select the comments that haven't been archived.
        comments = self.c.fetchall()
        comments = [i[0] for i in comments]
        return comments

    def getAllCommentIDs(self):
        self.c.execute("""SELECT id from lb_postings ORDER BY posted DESC;""")
        # Select the comments that haven't been archived.
        comments = self.c.fetchall()
        comments = [i[0] for i in comments]
        return comments

   
    def addCommentToChannel(self, phoneNum,auth, channel, swaraChannel, from_app=0):
		    #self.c.execute("INSERT INTO lb_postings (user, station) VALUES (%s, %s);",(phoneNum, str(channel),))
		    #Arjun changed to turn off autopublish
        if (swaraChannel == "main"):
            playon_main = "1"
        else:
            playon_main = "0"
        if (swaraChannel == "gondi"):
            playon_gondi = "1"
        else:
            playon_gondi = "0"
        if (swaraChannel == "training"):
            playon_training = "1"
            emailsent = "1"
            smssent = "1"
        else:
            playon_training = "0"
            emailsent = "0"
            smssent = "0"

        self.c.execute("INSERT INTO lb_postings (user, station, status,author_id,sticky, playon_main, playon_gondi, playon_training, emailsent, smssent, from_app, channel) VALUES (%s, %s, 1, %s, 0, " + playon_main + ", " + playon_gondi + ", " + playon_training + ", " + emailsent + ", " + smssent + ", %s, %s);",(phoneNum, str(channel), str(auth), str(from_app), swaraChannel))
        self.db.commit()
        ids = str(self.c.lastrowid)
        extension = '.mp3'
        filename = ids + extension
        print filename
        self.c.execute("UPDATE lb_postings SET audio_file = %s WHERE id = %s;",(filename, ids))
        self.db.commit()
        return ids
		
    def addComment(self, phoneNum):
        self.c.execute("INSERT INTO lb_postings (user) VALUES (%s);", \
                       (phoneNum))
        self.db.commit()
        return self.c.lastrowid

    def skipComment(self, commentID):
        debugPrint("SKIPPING "+str(commentID))
        self.c.execute(
            "UPDATE lb_postings SET skip_count = skip_count + 1 WHERE id = %s;",
            (commentID,))
        self.db.commit()
		
    def addPlaybackEvent(self, postID, duration, callid):
        self.c.execute("INSERT INTO analytics (eventype, msglstnd, durlistndto, callid) VALUES (%s, %s, %s, %s);",('Listened', str(postID), str(duration),str(callid),))
        self.db.commit()
        return self.c.lastrowid

    def addImpactPlaybackEvent(self, postID, duration, callid):
        self.c.execute("INSERT INTO analytics (eventype, msglstnd, durlistndto, callid) VALUES (%s, %s, %s, %s);",('ImpactListened', str(postID), str(duration),str(callid),))
        self.db.commit()
		
    def addCustomPlaybackEvent(self, postID, duration, callid):
        self.c.execute("INSERT INTO analytics (eventype, msglstnd, durlistndto, callid) VALUES (%s, %s, %s, %s);",('CustomListened', str(postID), str(duration),str(callid),))
        self.db.commit()

    def addSkipEvent(self, postID, duration,callid):
        self.c.execute("INSERT INTO analytics (eventype, msglstnd, durlistndto, callid) VALUES (%s, %s, %s, %s);",('Skipped', str(postID), str(duration), str(callid),))
        self.db.commit()

    def addInvalidkeyEvent(self, key, when, duration, callid):        
        self.c.execute("INSERT INTO analytics (eventype, invdgtpsd, context, whenpressed,callid) VALUES (%s, %s, %s, %s, %s);" ,('Invalid Keypress', str(key), str(when), str(duration),str(callid),))
        self.db.commit()

    def addMessageRecordEvent(self, postID,callid):
        self.c.execute("INSERT INTO analytics (eventype, msgrcd, callid) VALUES (%s, %s,%s);",('Recorded', str(postID),str(callid),))
        self.db.commit()

    def getCountKeyPress(self, phoneNumber):
        """Return count of keypress for the given number"""
        self.c.execute("select cntr from keyPress where phoneNumber={0}".format(phoneNumber))
        cntr_tuple = self.c.fetchall()
        cntr = [cntrs[0] for cntrs in cntr_tuple]
        return cntr[0]

    def getcallIDByUser(self,phoneNumber):
        # cdr is not set up yet so just returning call ID for call fro mbill
        return 3171389;
        """Search the cdr table for the callid in cdr table for a given phone number"""
        self.c.execute("select id from cdr where src={0} order by calldate desc limit 1;".format(phoneNumber))
        call_id_tuple = self.c.fetchall()
        call_id = ''
        for call_ids in call_id_tuple:
            call_id = call_ids[0]
        return call_id
    
    def getID(self):
        self.c.execute("""SELECT id FROM cdr ORDER BY calldate DESC LIMIT 1;""")
        callidno = self.c.fetchall()

    def getSMSSubscribers(self):
        self.c.execute("""SELECT phone_number FROM users WHERE DATE_SUB(CURDATE(),INTERVAL 2 week) <= lastloggedin;""")
        numberlist = self.c.fetchall()
        numberlist = [i[0] for i in numberlist]
        return numberlist  

    def logUserTime(self,user):
        self.c.execute("UPDATE users SET lastloggedin=NOW() WHERE phone_number=%s;",(user,))
        self.db.commit()
        

    
    def updateLastSMS(self,user):
        self.c.execute("UPDATE users SET lastsmsed=NOW() WHERE phone_number=%s;",(user,))
        self.db.commit()

    def getSummaryforPost(self, channelNum, post):
        self.c.execute("SELECT sms_summary  FROM lb_postings WHERE station = %s and id=%s;",(str(channelNum),str(post),))
        title = self.c.fetchall()
        title = [i[0] for i in title]
        if title[0]==None:
            title="NULL"
        return title
			
    def getUnSMSedPostsInChannel(self, channelNum, lastid):
        self.c.execute("SELECT * FROM lb_postings WHERE station = %s and id > %s and status = 3 ORDER BY posted;",(str(channelNum),str(lastid),))
        posts = self.c.fetchall()
        posts = [i[0] for i in posts]
        return posts
    
    def getPostedTime(self, channelNum, postid):
        self.c.execute("SELECT posted FROM lb_postings WHERE station = %s and id = %s;",(str(channelNum),str(postid),))
        posttime = self.c.fetchall()
        posttime = [i[0] for i in posttime]
        #if posttime:
        return posttime[0]
        #else:
        #  return 0
    
    def getUnpushedPostsInChannel(self, channelNum, lastid):
        time=self.getPostedTime(channelNum,lastid)
        self.c.execute("SELECT id FROM lb_postings WHERE station = %s and posted > TIMESTAMP(%s) AND status = 3 ORDER BY posted;",(str(channelNum),str(time),))
        posts = self.c.fetchall()
        posts = [i[0] for i in posts]
        return posts

    def getUnSmsedPostsInChannel(self, channelNum):
        self.c.execute("SELECT id, user FROM lb_postings WHERE station = %s AND status = 3 AND smssent = 0 ORDER BY posted;", (str(channelNum),))
        posts = self.c.fetchall()
        #posts = [i[0] for i in posts]
        return posts

    def markPostAsSmsed(self, postid):
        self.c.execute("UPDATE lb_postings SET smssent = 1 WHERE id = %s;", (str(postid),))
        self.db.commit()

    def markPostAsSmsError(self, postid):
        self.c.execute("UPDATE lb_postings SET smssent = 2 WHERE id = %s;", (str(postid),))
        self.db.commit()

    def setImageFilename(self, postid, filename, filesize=0, filetype='application/octet-stream'):
        self.c.execute("UPDATE lb_postings SET image_file='{0}', image_size={1}, image_type='{2}' WHERE id={3}".format(filename, filesize, filetype, postid))
        self.db.commit()

    def addInfoFromApp(self, postid, imei, interviewee, lat_long, city_state, is_public_app=False):
        public_app = 0
        if is_public_app:
            public_app = 1
        self.c.execute("UPDATE lb_postings SET imei='{0}', interviewee = '{1}', lat_long = '{2}', city = '{3}', is_public_app = {4} where id={5}".format(imei, interviewee, lat_long, city_state, public_app, postid))
        self.db.commit()

    def get_call_data(self):
        self.c.execute("SELECT timeOfCall FROM callLog where timeOfCall >= '2011-01-01'")
        calls = self.c.fetchall()
        calls = [i[0] for i in calls]
        return calls

    def get_post_data(self):
        self.c.execute("SELECT posted FROM lb_postings WHERE status = 3 and posted >= '2011-01-01'")
        posts = self.c.fetchall()
        posts = [i[0] for i in posts]
        return posts

    def get_impact_data(self):
        self.c.execute("SELECT posted FROM lb_postings WHERE status = 3 and posted >= '2011-01-01' and title like '%mpact%'")
        impacts = self.c.fetchall()
        impacts = [i[0] for i in impacts]
        return impacts

    def get_id_title(self, num_days=0):
        if num_days == 0:
            self.c.execute("SELECT id, title, tags FROM lb_postings WHERE status = 3")
        else:
            limit_date = str(date.today() - timedelta(days=num_days))
            self.c.execute("SELECT id, title, tags FROM lb_postings WHERE status = 3 and posted >= '{0}'".format(limit_date))
        results = self.c.fetchall()
        if len(results) > 0:
            results = [(i[0], i[1], i[2]) for i in results]
        else:
            results = None
        return results

    def set_tags(self, ayedee, tags):
        self.c.execute("UPDATE lb_postings SET tags='{0}' WHERE id={1}".format(tags, ayedee))
        self.db.commit()

