import os,re,socket,time

def time_compare(l,r,act):
	t1 = datetime.strptime(l, "%b %d %H:%M:%S %Y")
	t2 = datetime.strptime(r, "%b %d %H:%M:%S %Y")
	tact = datetime.strptime(act, "%b %d %H:%M:%S %Y")
	if max((t1,tact)) == tact and max((t2,tact))==t2:
		return True
	return False

def regex_check(reg,string):
	if len(string)<9: return False
	ls = string.split()
	m = re.search(reg,ls[8])
	print "ls, reg, m = ", ls,reg,m
	if m is None:
		return False
	return True
	
def hash_handle(file):
	time_is = time.ctime(os.path.getmtime(file))
	h = os.popen("md5sum " + file).read();
	h=h.split()
	print h
	return h[0],h[1],time_is

def index_handle(comm):
	ls = os.popen("ls -l").read()
	ls = ls.split("\n")
	ls.remove(ls[0])
	output=""
	if comm[1]=="longlist":
		# print "yes"
		for curr in ls:
			output = output + curr + "\n"

	if comm[1]=="shortlist":
		for curr in ls:
			l = comm[2] + " " + comm[3] + " " + comm[4] 
			r = comm[5] + " " + comm[6] + " " + comm[7]
			fori = curr.split();
			act = time.ctime(os.path.getmtime(fori[8]))
			if time_compare(l,r,act):
				output = output + curr + "\n";
	if comm[1]=="regex":
		for curr in ls:
			regg = comm[2]
 			if regex_check(regg,curr):
				output = output + curr + "\n";
	print output
	return output



port = 60001
s = socket.socket()
host = ""
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((host, port))
s.listen(5)

print "Server is up and listening!"
ip,addr = s.accept()
while True:
	data = ip.recv(1024)
	data = data.split(" ")
	print data
	if data[0]=="index":
		final = index_handle(data)
		ip.send(final)

	if data[0]=="hash":
		output=""
		if data[1]=="verify":
			file = data[2]
			h, for_file, stamp = hash_handle(file)
			output = output + "Hash Value is: " + h + "for file: "+ for_file + "\nTime Stamp is: " + stamp + "\n\n"
		else:
			all_files = os.listdir(os.curdir)
			print all_files
			for f in all_files:
				h,for_file, stamp = hash_handle(f)
				output = output + "Hash Value is: " + h + " for file: "+ for_file + "\nTime Stamp is: " + stamp + "\n\n"
		final=output
		ip.send(final)
	if data[0]=="download":	
		ls = os.popen("ls -l").read()
		ls = ls.split("\n")
		ls.remove(ls[0])
		output=""
		if data[1]=="TCP":
			c = os.stat(data[2])
			file_size = str(c.st_size)
			h,for_file, stamp = hash_handle(data[2])
			output = output + "Hash Value is: " + h + " for file: "+ for_file + "\nTime Stamp is: " + stamp + "\nSize " + file_size +"bytes\n\n"
			# output=""
			f = open(data[2],'rb')
		    
			l = f.read(1024)
			while (l):
				ip.send(l)
				print('Sent ',repr(l))
				l = f.read(1024)
			f.close()

		if data[2]=="UPD":
			print "udp"
	#ip.send(output)


s.shutdown(socket.SHUT_RDWR)


