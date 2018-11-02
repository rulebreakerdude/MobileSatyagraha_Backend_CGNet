from db_repo import *

mydb=database_flaskr()

print mydb.fetchBlock(1,100)
