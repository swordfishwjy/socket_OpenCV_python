import io
import cv2
import numpy
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import socket

# HOST = '134.124.243.11'
# PORT = 8000

# client_socket = socket.socket()
# client_socket.connect((HOST, PORT))

count = 0

# initialize the camera and grab a reference to the raw camera capture
camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 32
rawCapture = PiRGBArray(camera, size=(640, 480))
# allow the camera to warmup
time.sleep(2)
start = time.time()
# capture frames from the camera
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
	# grab the raw NumPy array representing the image, then initialize the timestamp
	# and occupied/unoccupied text
        image = frame.array

        cv2.imshow("Hello",image)
        count = count + 1
        cv2.imwrite('images/campute%d.jpg' %count, image)
        
        # client_socket.sendall(image)
        # data = client_socket.recv(2048)
        # while not data:
        #         print 'no'
        #         data = client_socket.recv(2048)
        # print 'client got'     
        
        #Load a cascade file for detecting faces. The detection maching learning algorithm cause "slow"g
 #        face_cascade = cv2.CascadeClassifier('/home/pi/opencv-3.1.0/data/haarcascades/haarcascade_frontalface_alt.xml')

 #        #Convert to grayscale
 #        gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)

 #        #Look for faces in the image using the loaded cascade file
 #        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5,minSize=(30,30), flags=cv2.cv.CV_HAAR_SCALE_IMAGE)

 #        #print "Found " +str(len(faces))+" face(s)"
 #        count = count + 1
 #        print count

 #        #Draw a rectangle around every found face
 #        #for (x,y,w,h) in faces:
 #            #cv2.rectangle(image,(x,y),(x+w,y+h),(255,255,0),2)
	
	# # show the frame
 #        #cv2.imshow("Frame", image)
	key = cv2.waitKey(1) & 0xFF
	# # clear the stream in preparation for the next frame
	rawCapture.truncate(0)
	# if the `q` key was pressed, break from the loop
	if key == ord("q"):
                client_socket.close()
                break

        if time.time() - start >5:
                break
