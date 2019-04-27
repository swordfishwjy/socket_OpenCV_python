import socket
import cv2
import numpy as np
import io
import struct 
import time


HOST = '0.0.0.0'
PORT = 8000

server_socket = socket.socket()
server_socket.bind((HOST, PORT))
server_socket.listen(0)

# conn, addr = server_socket.accept()
# print 'Connected by', addr

# accept a single connection and make a file-like object out of it
connection = server_socket.accept()[0].makefile('rb')
# construct a stream to hold the image data and read the image, data from connection
image_stream = io.BytesIO()

count = 0
start_time = time.time()

#Load a cascade file for detecting faces.
face_cascade = cv2.CascadeClassifier('lbpcascade_frontalface.xml')

try:
	while True:
		# read the length of image as a 32-bit unsigned int, if the length is zero, quit the loop
		image_len = struct.unpack('<L', connection.read(struct.calcsize('<L')))[0]
		if not image_len:
			break;

		image_stream.write(connection.read(image_len))
		# rewind the stream
		# image_stream.seek(0)
		image_np = np.fromstring(image_stream.getvalue(), dtype = np.uint8)
		image_stream.seek(0)
		image_cv = cv2.imdecode(image_np,1)

		# face detection with opencv
		#Convert to grayscale
		gray = cv2.cvtColor(image_cv,cv2.COLOR_BGR2GRAY)

		#Look for faces in the image using the loaded cascade file
		faces = face_cascade.detectMultiScale(gray, 1.3, 5)

		# print "Found " +str(len(faces))+" face(s)"

		# #Draw a rectangle around every found face
		# if (len(faces) != 0):
		# for (x,y,w,h) in faces:
		# 	cv2.rectangle(image_cv,(x,y),(x+w,y+h),(255,255,0),2)
		cv2.imshow("Face detection", image_cv)

		count = count + 1
		# print count
		# cv2.imwrite('pic/caputre%d.jpg' %count, image_cv)
		if cv2.waitKey(1) & 0xFF == ord('q'):
			break

		
finally:
	print "Deal with %d face images" %count 
	print time.time()-start_time
	connection.close()
	server_socket.close()




