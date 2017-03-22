import os,re,socket,time

def time_compare(l,r,act):
	t1 = datetime.strptime(l, "%b %d %H:%M:%S %Y")
	t2 = datetime.strptime(r, "%b %d %H:%M:%S %Y")
	tact = datetime.strptime(act, "%b %d %H:%M:%S %Y")
	if max((t1,tact)) == tact and max((t2,tact))==t2:
		return True
	return False

def regex_check(reg,string):
	ls = string.split()
    m = re.search(reg,ls[8])
    if m is None:
        return False
    return True
	
def hash_handle(file):
	time = time.ctime(os.path.getmtime(file))
	h = os.popen("md5sum " + file).read();
	return h,time

def index_handle(comm):
	ls = os.popen("ls -l").read()
	ls = ls.split("\n")
	ls.remove(ls[0])
	output=""
	if comm[1]=="longlist":
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
			if regex_check(comm[2],curr):
				output = output + curr + "\n";

	return output



port = 60000
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
	if data[0]=="index":
		final = index_handle(data)
		ip.send(final)
	if data[0]=="hash":
		output=""
		if data[1]=="verify":
			file = data[2]
			h, stamp = hash_handle(file)
			output 



s.shutdown(socket.SHUT_RDWR)


