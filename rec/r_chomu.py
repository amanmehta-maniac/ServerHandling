import re
import stat
import os
import socket                   
import time
import hashlib
from os.path import isfile, join
from os import listdir
from collections import *

s = socket.socket()             
host = ""
port = 60000    
port2 = 50000                
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
sock.bind((host, port2))
m = defaultdict()

s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.connect((host, port))
currTime = prevTime = time.time()
standardTime = 5
run = ''
while True:
	flag = 0
	prevTime = time.time()
	if abs(currTime - prevTime) >= standardTime:
		# print 'Entered'
		currTime = prevTime
		s.send('autoDownload')
		mTime2=defaultdict(float)
		while True:
			mTime = s.recv(1024)
			# print mTime
			if  mTime == 'Bye!': break
			mTime = mTime.split()
			mTime2[mTime[0]] = float(mTime[1])
		mTime1=defaultdict(float)
		for fileName in os.listdir(os.curdir):
			mTime1[fileName] = (os.stat(fileName).st_mtime)
		for i in mTime2:
			if mTime2[i] > mTime1[i]:
				print 'Downloading!',i
				run = 'download TCP ' + i
				s.send(run)
				run = run.split()
				if(run[0] == 'download'):
					with open(run[2], 'wb') as f:
						while True:
							if run[1] == 'TCP':
								data = s.recv(1024)
								time.sleep(0.1)
								if data == 'File finish':
									if flag == 1: break
									else: print 'Download finished!'
									break
								hashVal = s.recv(1024)
								time.sleep(0.1)								
								if str(hashlib.md5(data).hexdigest()) != hashVal: 
									flag = 1 
							f.write(data)
					if flag == 1: print 'Some error occurred!'
					f.close()		
	
	print '>>>',
	run = raw_input()
	s.send(run)
	run = run.split()
	data = ''
	c=hashlib.md5()
	if(run[0] == 'download'):
		with open(run[2], 'wb') as f:
			while True:
				if run[1] == 'TCP':
					data = s.recv(1024)
					if data == 'File finish':
						if flag == 1: break
						print 'Download finished!'
						break
					hashVal = s.recv(1024)
					if str(hashlib.md5(data).hexdigest()) != hashVal: 
						flag = 1 
				elif run[1] == 'UDP':
					data , adr = sock.recvfrom(1024)					
					if data == 'File finish':
						print 'Download finished!'
						break
				f.write(data)
		if run[1] == 'UDP':
			hashFile = s.recv(1024) 
			hash_md5 = hashlib.md5()
			with open(run[2], "rb") as f:
				for chunk in iter(lambda: f.read(4096), b""):
					hash_md5.update(chunk)
			if hash_md5.hexdigest() != hashFile: print 'Some error occurred!'
		if flag == 1: print 'Some error occurred!'
		f.close()		
	# elif(run[0] == 'download1'):
	# 	with open(run[1], 'wb') as f:
	# 		while True:
	# 			data, adr = sock.recvfrom(1024)
	# 			if data == 'File finish':
	# 				print 'Download finished!'
	# 				break
	# 			f.write(data)
	# 	f.close()		
	else:
		print s.recv(1024)




# with open('received_file', 'wb') as f:
#     print 'file opened'
#     while True:
#         print('receiving data...')
#         data = s.recv(1024)
#         print('data=%s', (data))
#         if not data:
#             break
#         # write data to a file
#         f.write(data)

# f.close()
# print('Successfully get the file')
# s.close()
# print('connection closed')
