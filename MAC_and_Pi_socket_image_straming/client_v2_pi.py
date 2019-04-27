import io
import cv2
import numpy as np
from picamera.array import PiRGBArray
from picamera import PiCamera
from time import sleep
import time
import socket
import struct

HOST = '192.168.0.7'
PORT = 8000


client_socket = socket.socket()
# print '111'
client_socket.connect((HOST, PORT))


# make a file-like object out of the connection
connection = client_socket.makefile('wb')
# print '222'
count = 0

try:
        # initialize the camera and grab a reference to the raw camera capture
        camera = PiCamera()
        camera.resolution = (1280, 720)
        camera.framerate = 32
        # rawCapture = PiRGBArray(camera, size=(640, 480))
        # allow the camera to warmup
        time.sleep(1)
        start = time.time()
        stream = io.BytesIO()
        # capture frames from the camera
        #for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
        for foo in camera.capture_continuous(stream, 'jpeg', use_video_port=True):
        	# grab the raw NumPy array representing the image, then initialize the timestamp
        	# and occupied/unoccupied text

                # write the length of the capture to the stream and flush to ensure it actually get sent
                connection.write(struct.pack('<L', stream.tell()))
                connection.flush()
                # rewind the stream and send the image data over the wire
                stream.seek(0)
                connection.write(stream.read())
                # reset the stream for the next capture
                stream.seek(0)
                stream.truncate()

                if time.time() - start > 10:
                        break
        # write a length of zero to the stream to signal we're done
        connection.write(struct.pack('<L', 0))
finally:
        connection.close()
        client_socket.close()
