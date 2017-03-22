import os,re,socket,time


def index_handle(comm):
	ls = os.popen("ls -l").read()
	ls = ls.split("\n")
	ls.remove(ls[0])
	# ls = ls.split()
	# ls[0] contains 1st line of ls -l output
	output=""
	if comm[1]=="longlist":
		for x in xrange(0,len(ls)-1):
			output = output + ls[x] + "\n"
	if comm[1]=="shortlist":
		for x in xrange(0,len(ls)-1):
			l = comm[2] + " " + comm[3] + " " + comm[4] 
			r = comm[5] + " " + comm[6] + " " + comm[7]
			 


port = 60000
s = socket.socket()
host = ""

s.bind((host, port))
s.listen(5)

print "Server is up and listening!"

ip,addr=s.accept()
while True:
	data = ip.recv(1024)
	data = data.split(" ")
	if data[0]=="index":
		index_handle(data)



