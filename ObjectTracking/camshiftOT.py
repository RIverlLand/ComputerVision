import numpy as np
import cv2

capture = cv2.VideoCapture(0)

response, frame = capture.read()

track = (240,100,400,160)

# crop area of tracking window
cropped = frame[track[0]:track[0]+track[1], track[2]:track[2]+track[3]]
# aka. cropped = frame[240:340, 400:460]

# BGR to HSV
cropped_hsv = cv2.cvtColor(cropped, cv2.COLOR_BGR2HSV)

color_range = [[0,0,0],[0,0,0]]

# filter values between the specified range
filter_mask = cv2.inRange(cropped_hsv, np.array(color_range[0]), np.array(color_range[1]))

# calculates the color histograms for an array of images.
cropped_hist = cv2.calcHist([cropped_hsv], [0], filter_mask, [180], [0,180])

# Normalize all values to range 0,255
cv2.normalize(cropped_hist, cropped_hist, 0, 255, cv2.NORM_MINMAX)

# Calculate centroid shift but finish when it has moved atleast 1 pixel
finish = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 1)

while True:
	response, frame = capture.read()
	frame = cv2.flip(frame, 1)
	if response == True:
		hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

		# calcBackProject takes the histogram generated by calcHist and projects it back 
		# onto an image. The result is the probability that each pixel 
		# belongs to the image that originally generated the histogram.
		hist_back = cv2.calcBackProject([hsv], [0], cropped_hist, [0,180], 1)

		# Apply Cam Shift
		res, track = cv2.CamShift(hist_back, track, finish)
		points = cv2.boxPoints(res)
		points = np.int0(points)

		# poly lines for adaptive box
		found = cv2.polylines(frame, [points], True, 255, 2)

		cv2.imshow('Tracked Object', found)
		if cv2.waitKey(1) & 0xFF == ord('q'):
			break

	else:
		break

capture.release()
cv2.destroyAllWindows()				

