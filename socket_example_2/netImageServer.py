import io
import socket
import struct 
from PIL import Image

# start a socket, listening to all the connections on 0.0.0.0:8000
server_socket = socket.socket()
server_socket.bind(('0.0.0.0', 8000))
server_socket.listen(0)
# accept a single connection and make a file-like object out of it
connection = server_socket.accept()[0].makefile('rb')
print 'someone connected'
filename = 'pic/test'
count = 0
try:
	while True:
		# read the length of image as a 32-bit unsigned int, if the length is zero, quit the loop
		image_len = struct.unpack('<L', connection.read(struct.calcsize('<L')))[0]
		if not image_len:
			break;
		# construct a stream to hold the image data and read the image, data from connection
		image_stream = io.BytesIO()
		image_stream.write(connection.read(image_len))
		# rewind the stream, open it as an image with PIL and do some process on it
		image_stream.seek(0)
		image = Image.open(image_stream)
		print('Image is %dx%d' %image.size)
		count = count + 1
		image.save('pic/test%d.jpg' % count)
		image.verify()
		print('Image is verified')
finally:
	connection.close()
	server_socket.close()

