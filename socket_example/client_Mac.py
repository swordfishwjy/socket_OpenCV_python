#!/usr/bin/python
#-*-coding:utf-8 -*-

import socket
import cv2
import numpy
import pickle
import time
import json

# socket.AF_INET用于服务器与服务器之间的网络通信
# socket.SOCK_STREAM代表基于TCP的流式socket通信
sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
sock.setblocking(1)
# host = socket.gethostname()
host = '134.124.243.52'
# 连接服务端
address_server = (host, 8010)
sock.connect(address_server)

# 从摄像头采集图像
capture = cv2.VideoCapture(0)
time.sleep(0.1)
ret, frame = capture.read()
encode_param=[int(cv2.IMWRITE_JPEG_QUALITY),90] #设置编码参数

# while ret:

# 首先对图片进行编码，因为socket不支持直接发送图片
result, imgencode = cv2.imencode('.jpg', frame)
data = numpy.array(imgencode)
stringData = data.tostring()
# 首先发送图片编码后的长度
print (str(len(stringData)))
sock.sendall(str(len(stringData)).ljust(16))
# 然后一个字节一个字节发送编码的内容
# 如果是python对python那么可以一次性发送，如果发给c++的server则必须分开发因为编码里面有字符串结束标志位，c++会截断
# for i in range (0,len(stringData)):
# 	sock.send(stringData[i])
# ret, frame = capture.read()
# #试图发送全部字节
sock.sendall(stringData)

# trigger a smart contract to get the service of edge server

# 接收server发送的返回信息,得到脸部的数组坐标信息，比如 [[592 208 322 322]]
data_r = sock.recv(1024)
faces = pickle.loads(data_r)
if (len(faces) != 0):
    for (x,y,w,h) in faces:
        cv2.rectangle(frame,(x,y),(x+w,y+h),(255,255,0),2)

# cancel comment do only do stream video
# cv2.imshow('processed image', frame)
# if cv2.waitKey(1) & 0xFF == ord('q'):
#     break

cv2.imwrite('./processed.png',frame)

if(len(faces) != 0):
    request = {'result':'Face Detected!!!'}
    strjson = json.dumps(request,sort_keys=True)
    print(strjson)
else:
    request = {'result':'Nothing detected...'}
    strjson = json.dumps(request,sort_keys=True)
    print(strjson)
    # capture next video frame
    # ret, frame = capture.read()


sock.close()
cv2.destroyAllWindows()
