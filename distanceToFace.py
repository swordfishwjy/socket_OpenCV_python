#!/usr/bin/python
#-*-coding:utf-8 -*-

# 利用小孔成像的原理，计算人脸距离摄像头的距离，单位cm

import cv2
import numpy as np

def distanceCal(faceWidth, focalLength, pixelWidth):
	return (faceWidth * focalLength) / pixelWidth

# 需要先拍摄一张照片，计算出该摄像头的焦距
# calculate the focal Length first, based on a test image
faceWidth = 21 # cm
pixelWidth = 296 #pixel
faceDistance = 55 # cm
focalLength = (faceDistance * pixelWidth) / faceWidth

cap = cv2.VideoCapture(0)

face_cascade = cv2.CascadeClassifier('socket_example/lbpcascade_frontalface.xml')
# face_cascade = cv2.CascadeClassifier('hogcascade_pedestrians.xml')
# eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')


if (not cap.isOpened()):
	print "camera is closed"


while(1):
	ret, img = cap.read()
	# display image size

	cv2.putText(img, "frame size: height %s x width %s" %(img.shape[0],img.shape[1]), (25,25), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 255, 0), 2)

	gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

	faces = face_cascade.detectMultiScale(gray, 1.3, 5)

	if (len(faces) != 0) :
		for (x,y,w,h) in faces :
			cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
			# calculate the distance from camera to face
			distance_CM = distanceCal(faceWidth, focalLength, w)
			cv2.putText(img, "%.2fcm" %distance_CM, (x, y), cv2.FONT_HERSHEY_SIMPLEX, 2.0, (0, 255, 0), 3)
			
		# cv2.imwrite('calculateFocalLength.png', img)
		# print faces


	cv2.imshow('img',img)
	if cv2.waitKey(1) & 0xFF == ord('q'):
		break

cap.release()
cv2.destroyAllWindows()