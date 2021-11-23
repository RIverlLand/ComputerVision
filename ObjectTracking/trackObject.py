#Problem about this object tracking is that it only finds out the biggest object in sight, which generated from the canny result, it is not trust-worthy nor efficient. Judging by color or something else could do a better job?

import numpy as np
import cv2

capture = cv2.VideoCapture(0)

# Color range of object in HSV
color_range = [[0,0,0],[179,50,100]]
#Collor range in HSV is different from the gray scale, instead of range like 100,255 we implement HSV color.

points = []
count = 0

# Get first frame+
response, frame = capture.read() #BGR as default
height, width = frame.shape[:2]

while True:
	response, frame = capture.read()
	frame = cv2.flip(frame, 1) #flip the pic, 1 is horizontal, 0 is vertical, -1 is both
	contours_frame = frame.copy()
	
	# converting to hsv
	hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
	# cv2.imshow('HSV color', hsv)
	
	# threshold values between range
	mask = cv2.inRange(hsv, np.array(color_range[0]), np.array(color_range[1]))  #The cv2.inRange function expects three arguments: the first is the image were we are going to perform color detection, the second is the lower limit of the color you want to detect, and the third argument is the upper limit of the color you want to detect.

	# Finding contours
	_, contours, _ = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

	#第二个参数表示轮廓的检索模式，有四种（本文介绍的都是新的cv2接口）：
    # cv2.RETR_EXTERNAL表示只检测外轮廓
    # cv2.RETR_LIST检测的轮廓不建立等级关系
    # cv2.RETR_CCOMP建立两个等级的轮廓，上面的一层为外边界，里面的一层为内孔的边界信息。如果内孔内还有一个连通物体，这个物体的边界也在顶层。
    # cv2.RETR_TREE建立一个等级树结构的轮廓。



	# Computing centroids
	centroids = int(height/2), int(width/2)
	radius = 0

	if len(contours) > 0: 
		# Find largest contour
		biggest_contour = max(contours, key=cv2.contourArea) #Key is the function applied on each argument, ex. max(1,-2,3,-4, abs) returns -4 instead of 3.
		(x,y), radius = cv2.minEnclosingCircle(biggest_contour) #minEnclosingCircle finds a circle to wrap around the found contours.
		cv2.drawContours(contours_frame, contours, -1, (0,0,255), 3)
		cv2.imshow('contours', contours_frame)
		M = cv2.moments(biggest_contour)
		try:
			a = int(M['m10']/M['m00'])
			b = int(M['m01']/M['m00'])
			centroids = (a, b) 
		except:
			a = int(height/2)
			b = int(width/2)
			centroids = a,b

		# Threshold contours	
		if radius > 25:
			print (radius)
			cv2.circle(frame, (int(x), int(y)), int(radius), (0,0,255), 2)
			cv2.circle(frame, centroids, 5, (0,255,0), -1)

	points.append(centroids)
	
	# track points
	if radius > 25:
		print (radius)
		for i in range(1, len(points)):
			try:
				cv2.line(frame, points[i-1], points[i], (0,255,0), 2)
			except:
				pass

		count += 0					

	else:
		count += 1	

		# Remove trail when no object in 10 frames
		if count == 10:
			points = []
			count = 0		

	cv2.imshow('Tracked Object', frame)
	# cv2.imshow('Sketch output', mask)
	if cv2.waitKey(1) & 0xFF == ord('q'):
		break

capture.release()
cv2.destroyAllWindows()