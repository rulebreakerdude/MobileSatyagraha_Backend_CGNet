import MySQLdb
import json
import hashlib
from datetime import datetime

class database_flaskr:

	#db initialization and connection
	def __init__(self):
		self.mydb = MySQLdb.connect(
		  host="127.0.0.1",
		  port=3306,
		  user="root",
		  passwd="Wmtp00lr!"
		  )
		self.c = self.mydb.cursor()
		self.c.execute('USE audiwikiswara;')
	
	def convert(self):
		db_response=self.c.execute("SELECT * FROM app_credentials;")
		db_response=self.c.fetchall()
		for row in db_response:
			username=row[0]
			if username!="testing123":
				password_hash=hashlib.sha256(row[1]).hexdigest()
			else:
				password_hash=row[1]
			email=row[2]
			name=row[3]
			self.c.execute("INSERT INTO app_credentials_2 (username, password_hash, name, email) VALUES (%s,%s,%s,%s);",(username,password_hash,name,email))
			self.mydb.commit()
			print username,password_hash,email,name
		
mydb=database_flaskr()
mydb.convert()