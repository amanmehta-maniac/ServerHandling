import os
import socket
import hashlib
from os.path import isfile, join
from os import listdir
import re
import stat
import time
from collections import *

port = 60000
port2 = 50000
s = socket.socket()
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) 
host = ""


s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

s.bind((host, port))
s.listen(5)

# filename = raw_input("Enter file to share:")
# print 'Server listening....'


class Execute:
    def __init__(self):
        pass
    
    def executeIndex(self, command):
        answer=''
        if command[1] == 'longlist':
            files = os.listdir(os.curdir)
            answer += ('Index'+' File') + '\n' + ('-----'+' ----') + '\n'
            for num,file in enumerate(files):
                answer += str( str(num+1)+') ' + file + '\n')

        if command[1] == 'shortlist':
            lowLim,HighLim = int(command[2]), int(command[3])
            allTimes, size = [], []
            getFiles = os.listdir(os.curdir)
            for file in getFiles:
                c=os.stat(file)
                allTimes.append(int(c.st_mtime))
                size.append(int(c.st_size))
            g = 0
            answer += ('Index'+' File'+' Size'+' Type') + '\n' + ('-----'+' ----'+' ----'+' ----') + '\n'
            for num,file in enumerate(getFiles):
                fileType = 'file'
                if os.path.isdir(file): fileType = 'directory'
                if allTimes[num] > lowLim and allTimes[num] < HighLim:
                    answer += str(str(g+1)+') ' + file + ' ' + str(size[num]) + ' ' + fileType + '\n')
                    g+=1
        if command[1] == 'regex':
            typeoOfFile = command[2]
            g = 0
            answer += ('Index' + ' File' + ' Size' + ' Type') + '\n' + ('-----' + ' ----' + ' ----' + ' ----') + '\n'
            for num,file in enumerate(os.listdir(os.curdir)):
                if re.search(typeoOfFile, file):
                    c=os.stat(file)
                    fileType = 'file'
                    if os.path.isdir(file): fileType = 'directory'
                    answer += str(str(g+1) + ')' + ' ' + os.path.join(os.curdir, file) + ' ' + str(c.st_size) + ' ' + fileType + '\n')
                    g+=1
        print answer
        return answer

    def executeHash(self, command):
        answer = ''
        if command[1] == 'verify':
            fileName = command[2]
            answer += ('Checksum ' + 'Last modified time') + '\n' + ('--------' + ' ---- --------- ----') + '\n'
            hash_md5 = hashlib.md5()
            if not os.path.isdir(fileName):
                with open(fileName, "rb") as f:
                    for chunk in iter(lambda: f.read(4096), b""):
                        hash_md5.update(chunk)
                answer += str(hash_md5.hexdigest() + ' ' +  str(os.stat(fileName).st_mtime)) + '\n'

        if command[1] == 'checkall':
            answer += ('Index' + ' Filename' + ' Checksum' + ' Last modified time') + '\n' + ('-----' + ' --------' + ' --------' + ' ---- --------- ----') + '\n'
            for num,fileName in enumerate(os.listdir(os.curdir)):
                hash_md5 = hashlib.md5()
                if not os.path.isdir(fileName):
                    with open(fileName, "rb") as f:
                        for chunk in iter(lambda: f.read(4096), b""):
                            hash_md5.update(chunk)
                    answer += str(str(num + 1)+')' + ' ' + fileName + ' ' + hash_md5.hexdigest() + ' ' + str(os.stat(fileName).st_mtime) + '\n')
        return answer
    def executeDownload(self,command):
        answer = ''
        x = hashlib.md5()
        fileName = command[2]
        if command[1] == 'TCP':
            f = open(fileName,'rb')
            l = f.read(1024)
            while (l):
                if not l: 
                    break
                conn.send(l)
                time.sleep(0.1)
                x.update(l)
                conn.send(str(hashlib.md5(l).hexdigest()))
                time.sleep(0.1)
                l = f.read(1024)
            f.close()
            time.sleep(0.1)
            conn.send('File finish')
        elif command[1] == 'UDP':
            f = open(fileName,'rb')
            l = f.read(1024)
            while (l):
                if not l: 
                    break
                sock.sendto(l,(host,port2))
                time.sleep(0.1)
                l = f.read(1024)
            f.close()
            time.sleep(0.1)
            sock.sendto('File finish',(host,port2))
            hash_md5 = hashlib.md5()
            with open(fileName, "rb") as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    hash_md5.update(chunk)
            conn.send(hash_md5.hexdigest())
            

    
    def autoDownload(self):
        mTime=defaultdict(float)
        for fileName in os.listdir(os.curdir):
            conn.send(fileName + ' ' + str(os.stat(fileName).st_mtime))
            time.sleep(0.1)
        conn.send('Bye!')

    def runAll(self, command):
        if command[0] == 'index':
            return self.executeIndex(command)
        if command[0] == 'hash':
            return self.executeHash(command)
        if command[0] == 'download':
            self.executeDownload(command)
        if command[0] == 'autoDownload':
            self.autoDownload()




conn, addr = s.accept()
function = Execute()
while True:
    command = conn.recv(1024)
    print '>>>', command
    command = command.split()
    print command
    if command:
        if command[0] != 'download' and command[0] != 'autoDownload': conn.send(function.runAll(command))
        else: function.runAll(command)
    else: break




conn.close()



# while True:
#     conn, addr = s.accept()
#     print 'Got connection from', addr
#     data = conn.recv(1024)
#     print data
#     print('Server received', repr(data))

#     f = open(filename,'rb')
#     print '>>>',command
#     command = command.split()
#     l = f.read(1024)
#     while (l):
#        conn.send(l)
#        print('Sent ',repr(l))
#        l = f.read(1024)
#     f.close()

#     print('Done sending')
#     conn.send('Thank you for connecting')
#     conn.close()
