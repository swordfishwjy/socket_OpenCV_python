#!/usr/bin/python
#-*-coding:utf-8 -*-

import socket
import cv2
import numpy
import pickle
import io
from picamera.array import PiRGBArray
from picamera import PiCamera
import time

# socket.AF_INET用于服务器与服务器之间的网络通信
# socket.SOCK_STREAM代表基于TCP的流式socket通信
sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
host = '192.168.0.7'
# 连接服务端
address_server = (host, 8010)
sock.connect(address_server)

# 从Rasp Pi Camera Module 采集图像
camera = PiCamera()
camera.resolution = (720, 480)
camera.framerate = 32
rawCapture = PiRGBArray(camera, size=(720, 480))
# allow the camera to warmup
time.sleep(2)

encode_param=[int(cv2.IMWRITE_JPEG_QUALITY),90] #设置编码参数
# capture frames from the camera
for capture in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
	# grab the raw NumPy array representing the image, then initialize the timestamp
	# and occupied/unoccupied text
        frame = capture.array
        result, imgencode = cv2.imencode('.jpg', frame)
        data = numpy.array(imgencode)
        stringData = data.tostring()
        # 首先发送图片编码后的长度
        sock.send(str(len(stringData)).ljust(16))
        print (str(len(stringData)).ljust(16))

        sock.sendall(stringData)
        
        # truncate the stream to the current position
        rawCapture.truncate(0)
        # 接收server发送的返回信息,得到脸部的数组坐标信息，比如 [[592 208 322 322]]
        data_r = sock.recv(1024)
        faces = pickle.loads(data_r)
        print(faces)
        if (len(faces) != 0):
                for (x,y,w,h) in faces:
                        cv2.rectangle(frame,(x,y),(x+w,y+h),(255,255,0),2)   
        cv2.imshow('processed image', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    

sock.close()
cv2.destroyAllWindows()
