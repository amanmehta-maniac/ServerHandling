import os,re,socket,time


s = socket.socket()
host = ""
port = 60001

s.connect((host, port))
while True:
	com = raw_input("prompt> ")
	s.send(com)
	# comm = com.split(" ")
	# if comm[0]=="download":
	# 	with open(comm[2], 'wb') as f:
	# 	    print 'file opened'
	# 	    while True:
	# 	        print('receiving data...')
	# 	        data = s.recv(1024)
	# 	        print data
	# 	        print('data=%s', (data))
	# 	        if not data:
	# 	            break
	# 	        # write data to a file
	# 	        f.write(data)
	# 	f.close()

	# else:
	data = s.recv(1024)
	print data