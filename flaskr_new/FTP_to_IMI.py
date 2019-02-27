import ftplib

session = ftplib.FTP('59.162.167.59','Cgnet','mdy8YtLIzxf2')
file = open('118127.wav','rb')                  # file to send

#List the files in the current directory
print "File List:"
files = session.dir()
print files

session.storbinary('STOR First_Story.wav', file)     # send the file
file.close()                                    # close file and FTP
session.quit()