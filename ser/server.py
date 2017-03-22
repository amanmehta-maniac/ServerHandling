import os,re,socket,time


port = 60000
s = socket.socket()
host = ""

s.bind((host, port))
s.listen(5)

print "Server is up and listening!"

ip,addr=s.accept()
while True:
	data = ip.recv(1024)
	data = data.



