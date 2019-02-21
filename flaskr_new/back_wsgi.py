import sys
sys.path.insert(0,"/var/www/flaskr/")

from back import application

if __name__=="__main__":
	application.run()