import MySQLdb
import json
from datetime import datetime

class database_flaskr:

	#db initialization and connection
	def __init__(self):
		self.mydb = MySQLdb.connect(
		  host="127.0.0.1",
		  port=3306,
		  user="root",
		  passwd="passwordMYSQL123"
		  )
		self.c = self.mydb.cursor()
		self.c.execute('USE audiwikiswara;')

	
	#getter and setters start here
	
	def fetchAll(self):
		db_response=self.c.execute(
			"SELECT id, message_input, user, user, status, tags, posted, title, audio_length FROM app_problem_list WHERE status = 3 AND tags LIKE \'%PROBLEM%\' ORDER BY posted DESC LIMIT 3;")
		db_response=self.c.fetchall()
		db_parse=[{"problem_id": str(x[0]),
					"problem_text": x[1].decode("utf-8"), 
					"phone_number_r": x[2],
					"phone_number_o": x[3],
					"status": str(x[4]),
					"comments": x[5],
					"datetime": str(x[6].strftime("%d %B")),
					"problem_desc": x[7].decode("utf-8"),
					"duration": str(x[8])} for x in db_response]
		return json.dumps(db_parse)
		
	def fetchBlock(self,s,e):
		song="%SONG%"
		news="%NEWS%"
		culture="%CULTURE%"
		bultoo="%BULTOO%"
		problem="%PROBLEM%"
		coal="%COAL%"
		mining="%MINING%"
		education="%EDUCATION%"
		food="%FOOD%"
		forest="%FOREST%"
		land="%LAND=%"
		electricity="%ELECTRICITY%"
		water="%WATER%"
		handpump="%HANDPUMP%"
		nrega="%NREGA%"
		db_response=self.c.execute(
			"SELECT id, message_input, user, user, status, tags, posted, title, audio_length FROM app_problem_list WHERE tags not like %s and tags not like %s and tags not like %s and tags not like %s and (tags LIKE %s or tags LIKE %s or tags LIKE %s or tags LIKE %s or tags LIKE %s or tags LIKE %s or tags LIKE %s or tags LIKE %s or tags LIKE %s or tags LIKE %s or tags LIKE %s) ORDER BY posted DESC LIMIT %s, %s;" 
			,(song,news,culture,bultoo,problem,coal,mining,education,food,forest,land,electricity,water,handpump,nrega,s,e))
		db_response=self.c.fetchall()
		db_parse=[{"problem_id": str(x[0]),
					"problem_text": x[1].decode("utf-8"), 
					"phone_number_r": x[2],
					"phone_number_o": x[3],
					"status": str(x[4]),
					"comments": x[5],
					"datetime": str(x[6].strftime("%d %B")),
					"problem_desc": x[7].decode("utf-8"),
					"duration": str(x[8])} for x in db_response]
		return json.dumps(db_parse)
		
	def fetchProblemAgainstUser(self,username):
		db_response_1=self.c.execute(
			"SELECT * FROM app_problems_per_user WHERE username = %s;",(username,))
		db_response_1=self.c.fetchall()
		db_response=self.c.execute(
			"SELECT id, message_input, user, user, status, tags, posted, title, audio_length FROM app_problem_list WHERE id = %s OR id = %s;" ,(db_response_1[0][1],db_response_1[0][2]))
		db_response=self.c.fetchall()
		db_parse=[{"problem_id": str(x[0]),
					"problem_text": x[1].decode("utf-8"), 
					"phone_number_r": x[2],
					"phone_number_o": x[3],
					"status": str(x[4]),
					"comments": x[5],
					"datetime": str(x[6].strftime("%d %B")),
					"problem_desc": x[7].decode("utf-8"),
					"duration": str(x[8])} for x in db_response]
		return json.dumps(db_parse)
		
	def fetchTest(self):
		db_response=self.c.execute("SELECT message_input FROM app_problem_list WHERE status = 3 ORDER BY posted DESC LIMIT 3;")
		db_response=self.c.fetchall()
		db_parse=[[x[0].decode("utf-8")] for x in db_response]
		return db_parse
		
	def fetchOne(self, problem_id):
		db_response=self.c.execute("SELECT id, message_input, user, user, status, tags, posted, title, audio_length FROM app_problem_list WHERE id = %s;",(problem_id,))
		db_response=self.c.fetchall()
		db_parse=[{"problem_id": str(x[0]),
					"problem_text": x[1].decode("utf-8"), 
					"phone_number_r": x[2],
					"phone_number_o": x[3],
					"status": str(x[4]),
					"comments": x[5],
					"datetime": str(x[6].strftime("%d %B")),
					"problem_desc": x[7].decode("utf-8"),
					"duration": str(x[8])} for x in db_response][0]

		return json.dumps(db_parse)
		
	def insertUser(self,username,password_hash,name,email):
		self.c.execute("INSERT INTO app_credentials (username, password_hash, name, email) VALUES (%s,%s,%s,%s);",(username,password_hash,name,email))
		self.mydb.commit()
		
	def registerComment(self,username,problem_id,comment):
		try:
			self.c.execute("INSERT INTO app_comments (username, problem_id, comments) VALUES (%s,%s,N'%s');",(username,problem_id,comment))
			self.mydb.commit()
		except:
			return str(sys.exc_info()[0])
		
	def userExists(self,username):
		db_response=self.c.execute("SELECT DISTINCT username FROM app_credentials WHERE username = %s ;",(username,))
		return db_response>0
		
	def authenticateUser(self,username,password_hash):
		db_response=self.c.execute("SELECT DISTINCT name FROM app_credentials WHERE username = %s and password_hash = %s;",(username,password_hash))
		db_response=self.c.fetchall()
		if len(db_response)>0:
			return db_response[0][0]
		else:
			return "incorrect password"
		
	def canAdoptProblem(self,username):
		db_response=self.c.execute("SELECT * FROM app_problems_per_user WHERE username = %s;",(username,))
		db_response=self.c.fetchall()
		if(len(db_response)==0):
			return "Yes"
		elif db_response[0][1] is '': 
			return "Yes"
		elif db_response[0][2] is '':
			return "Yes"
		else:
			return "No"
	
	def userCount(self,problem_id):
		db_response=self.c.execute("SELECT * FROM app_users_per_problem2 WHERE problem_id = %s;",(problem_id,))
		db_response=self.c.fetchall()
		if(len(db_response)==0):
			return 0
		elif db_response[0][1] is not '' and db_response[0][2] is not '':
			return 2
		elif db_response[0][1] is '' and db_response[0][2] is '':
			return 0
		else:
			return 1
			
	def adoptProblem(self,username,problem_id):
		db_response=self.c.execute("SELECT * FROM app_users_per_problem2 WHERE problem_id = %s;",(problem_id,))
		db_response=self.c.fetchall()
		if(len(db_response)==0):
			self.c.execute("INSERT INTO app_users_per_problem2 (problem_id, user1) VALUES (%s,%s);",(problem_id,username))
			self.mydb.commit()
			response="Adopted"
		elif db_response[0][1] is '':
			self.c.execute("UPDATE app_users_per_problem2 SET user1 = %s WHERE (problem_id = %s);",(username,problem_id))
			self.mydb.commit()
			response= "Adopted"
		elif db_response[0][2] is '':
			self.c.execute("UPDATE app_users_per_problem2 SET user2 = %s WHERE (problem_id = %s);",(username,problem_id))
			self.mydb.commit()
			response= "Adopted"
		else:
			response= "Users Full"
		if response != "Users Full":
			database_flaskr.registerProblemAgainstUser(self,username,problem_id)
		return response
	
	def registerProblemAgainstUser(self,username,problem_id):
		db_response=self.c.execute("SELECT * FROM app_problems_per_user WHERE username = %s;",(username,))
		db_response=self.c.fetchall()
		if(len(db_response)==0):
			self.c.execute("INSERT INTO app_problems_per_user (username, problem1) VALUES (%s,%s);",(username,problem_id))
			self.mydb.commit()
		elif db_response[0][1] is '': 
			self.c.execute("UPDATE app_problems_per_user SET problem1 = %s WHERE (username = %s);",(problem_id,username))
			self.mydb.commit()
		elif db_response[0][2] is '':
			self.c.execute("UPDATE app_problems_per_user SET problem2 = %s WHERE (username = %s);",(problem_id,username))
			self.mydb.commit()
			
	def unAdoptProblem(self,username,problem_id):
		db_response=self.c.execute("SELECT * FROM app_users_per_problem2 WHERE problem_id = %s;",(problem_id,))
		db_response=self.c.fetchall()
		if db_response[0][1]==username:
			self.c.execute("UPDATE app_users_per_problem2 SET user1 = %s WHERE (problem_id = %s);",('',problem_id))
			self.mydb.commit()
			response= "UnAdopted"
		elif db_response[0][2]==username:
			self.c.execute("UPDATE app_users_per_problem2 SET user2 = %s WHERE (problem_id = %s);",('',problem_id))
			self.mydb.commit()
			response= "UnAdopted"
		else:
			response= "Was it really your problem?"
		if response != "Was it really your problem?":
			database_flaskr.deRegisterProblemAgainstUser(self,username,problem_id)
		return response
	
	def deRegisterProblemAgainstUser(self,username,problem_id):
		db_response=self.c.execute("SELECT * FROM app_problems_per_user WHERE username = %s;",(username,))
		db_response=self.c.fetchall()
		if db_response[0][1]==problem_id: 
			self.c.execute("UPDATE app_problems_per_user SET problem1 = %s WHERE (username = %s);",('',username))
			self.mydb.commit()
		elif db_response[0][2]==problem_id:
			self.c.execute("UPDATE app_problems_per_user SET problem2 = %s WHERE (username = %s);",('',username))
			self.mydb.commit()
			
			
			
			
			
			
			