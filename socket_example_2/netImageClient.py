import io
import socket
import struct
import time
import picamera

# connect a client socket to my_server:8000 (my_server is the hostname of the server)
client_socket = socket.socket()
client_socket.connect(('192.168.0.7', 8000))
# make a file-like object out of the connection
connection = client_socket.makefile('wb')
try:
	camera = picamera.PiCamera()
	camera.resolution = (1024, 768)
	# start a preview and let the camera warm up for 2 seconds
	camera.start_preview()
	time.sleep(2)
	# we find out the size of each capture first and then write it to the connection
	start = time.time()
	stream = io.BytesIO()
	for foo in camera.capture_continuous(stream, 'jpeg'):
		# write the length of the capture to the stream and flush to ensure it actually get sent
		connection.write(struct.pack('<L', stream.tell()))
		connection.flush()
		# rewind the stream and send the image data over the wire
		stream.seek(0)
		connection.write(stream.read())
		# if we've been capturing for more than 30 seconds, quit
		if time.time() - start > 30:
			break
		# reset the stream for the next capture
		stream.seek(0)
		stream.truncate()

	# write a length of zero to the stream to signal we're done
	print 'Times up'
	connection.write(struct.pack('<L', 0))
finally:
	connection.close()
	client_socket.close()