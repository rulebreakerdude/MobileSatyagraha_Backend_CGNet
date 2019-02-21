import MySQLdb
import json
from datetime import datetime


mydb1 = MySQLdb.connect(
		host="cgdbaws.cv23wjqihuhm.ap-south-1.rds.amazonaws.com",
		port=3306,
		user="root",
		passwd="CGDBAWSsql"
		)
c1 = mydb1.cursor()
c1.execute('USE flaskdb;')
		
mydb2 = MySQLdb.connect(
		host="127.0.0.1",
		port=3306,
		user="root",
		passwd="Wmtp00lr!"
		)
c2 = mydb2.cursor()
c2.execute('USE audiwikiswara;')


sql_command="SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = 'lb_postings' ORDER BY ORDINAL_POSITION;"
c2.execute(sql_command)
db_response1=c2.fetchall()
column_names=""
num_columns = len(db_response1)
for row in db_response1:
	for word in row:
		column_names+=" "+word+","
column_names=column_names[0:len(column_names)-1]+" "



sql_command="SELECT max(id) FROM app_problem_list_backup;"
c1.execute(sql_command)
db_response1=c1.fetchall()
max_id = db_response1[0][0]
print max_id

sql_command="SELECT * FROM lb_postings WHERE id > \'"+str(max_id)+"\' order by id;"
c2.execute(sql_command)
db_response1=c2.fetchall()
print len(db_response1)

column_values=""
#db_response1=[list(x) for x in db_response1]
for row in db_response1:
	print row
	ampersand_s="("
	for i in range(0,num_columns-1):
		ampersand_s+="%s,"
	ampersand_s+="%s)"
	sql_command="INSERT INTO app_problem_list_backup ("+column_names+") VALUES "+ampersand_s+";"
	print sql_command
	c1.execute(sql_command,row)
	mydb1.commit()



c1.close()
mydb1.close()
c2.close()
mydb2.close()
print "done!"