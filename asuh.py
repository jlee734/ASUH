#Regular Expression Library for parsing
import re
#Paramiko for SSH
import paramiko
from paramiko import SSHClient

#Strings as functions

ASUH_rand='''
def ASUH_rand(N,M):
	return [[random.randrange(1,100) for x in range(N)] for y in range(M)]
'''

ASUH_min='''
import random, Queue, threading
def ASUH_min(m):
#	print m
	q = Queue.PriorityQueue()
	for i in range(0,len(m)):
		tz = threading.Thread(target=a_min,args=(m[i],q))
		tz.start()
	print q.get()

def a_min(a,q):
	q.put(min(a))
'''

#Variable initialization that store variable and data from text file
variable_array=[]
workflow_array=[]
parameter_array=[]
ASUHfuncs=["rand","min"]
function_array=[]
output = open('output.txt','w')

#Parse input file using regular expressions
f = open("example.txt")
for line in f:
	parameter_array.append(re.search('\((.*?)\)',line).group(1))
	variable_array.append(re.search('(.*?)\=',line).group(1))
	workflow_array.append(re.search('\=(.*?)\(',line).group(1))

#Conversion of workflow functions into server computations
for i in xrange(len(workflow_array)):
	if workflow_array[i] in ASUHfuncs:
		function_array.append((variable_array[i]+'='+'ASUH_'+workflow_array[i]+'('+parameter_array[i]+')'))

#Insert your username and password here
#We recommend using password-less login via SSH Keys in order to preserve the security of passwords
user_ = 'pg'
pass_ = ''
host= 'twentyseven.info'
port= 22
#SSH Client initialization
ssh_client = SSHClient()
ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh_client.connect(host,username=user_, password=pass_)
transport = paramiko.Transport((host,port))
transport.connect(username=user_,password=pass_)
sftp = paramiko.SFTPClient.from_transport(transport)

#download
#filepath = ''
#localpath= ''
#sftp.get(filepath,localpath)

#upload
#serverpath = ''
#localpath= ''
#sftp.put(serverpath,localpath)


chan = ssh_client.invoke_shell()
stdin = chan.makefile('wb')
stdout = chan.makefile('rb')

#for testing
#stdin.write('mkdir c')

filepaths=['c/fileio.c', 'c/fileio.h', 'c/min.c', 'c/max.c', 'c/rand.c']
#for i in filepaths:
#	sftp.put(i, i)
sftp.mkdir("c")
sftp.put('c/fileio.c','c/fileio.c')
sftp.put('c/fileio.h','c/fileio.h')
sftp.put('c/min.c','c/min.c')
sftp.put('c/max.c','c/max.c')
sftp.put('c/rand.c','c/rand.c')
#SSH Client code execution
stdin.write(
'''
cd c\n
gcc -o rand filio.h fileio.c rand.c\n
gcc -o min fileio.h fileio.c min.c\n
gcc -o max fileio.h fileio.c max.c\n
./rand 100 100 i.csv\n
./min 100 100 i.csv o1.csv\n
./max 100 100 i.csv 02.csv\n
exit
'''
)

#stdin.write(
#'''
#python
#'''
#+ASUH_rand+ASUH_min)

#for i in function_array:
#	stdin.write('\n'+i)
#stdin.write('''
#exit()
#exit
#''')

output.write(stdout.read())

#SSH Client code termination
ssh_client.close()
sftp.get('c/o1.csv', 'c/o1.csv')
sftp.get('c/o2.csv', 'c/o2.csv')
sftp.close()
