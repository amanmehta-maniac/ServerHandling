import os,re,socket,time


s = socket.socket()
host = ""
port = 60000

s.connect((host, port))
while True:
	com = raw_input("prompt> ")
	s.send(com)
	data = s.recv(1024)
	print data