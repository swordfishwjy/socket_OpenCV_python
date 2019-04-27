import socket
import time
import picamera

# connect the client to server
client_socket = socket.socket()
client_socket.connect(('', 8000))

# make a file-like object out of the connection
connection = client_socket.makefile('wb')
try:
	camera = picamera.PiCamera()
	camera.resolution = (640, 480)
	camera.framerate =24
	camera.start_preview()
	time.sleep(2)
	# start recording, sending the output to the connection for 60s, then stop
	camera.start_recording(connection, format = 'h264')
	camera.wait_recording(30)
	camera.stop_recording
finally:
	connection.close()
	client_socket.close()

