import socket
import subprocess

# start a socket listening
server_socket = socket.socket()
server_socket.bind(('0.0.0.0', 8000))
server_socket.listen(0)

#accept a single connection and make a file-like object out of it
connection = server_socket.accept()[0].makefile('rb')
try:
	# run a viewer with a command line
	cmdline = ['/Applications/VLC.app/Contents/MacOS/VLC', '--demux', 'h264', '-']
	player = subprocess.Popen(cmdline, stdin=subprocess.PIPE)
	f = open('recordedFile.h264','wb')
	while True:
		# repeated read 1k of data from the connection and write it to the 
		# media player's stdin
		data = connection.read(1024)
		if not data:
			break
		player.stdin.write(data)
		f.write(data)
finally:
	connection.close()
	server_socket.close()
	player.terminate()
	f.close()