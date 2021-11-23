import cv2
import numpy as np

def sketch(frame):
	'''
	Generate sketch given an image
	@paramaters: frame 
	'''
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	gray_blur = cv2.GaussianBlur(gray, (5,5), 0)
	edges = cv2.Canny(gray_blur, 10, 50) #def Canny(image, threshold1, threshold2, edges=..., apertureSize=..., L2gradient=...) -> typing.Any
	#Canny function detects edges but only in gray images and with required two thresholds.
	ret, mask = cv2.threshold(edges, 100, 255, cv2.THRESH_BINARY_INV)
	return mask, gray, gray_blur


capture = cv2.VideoCapture(0)

while (True):
	response, frame = capture.read()
	mask, gray, gray_blur = sketch(frame)
	cv2.imshow("Those edges", mask)
	cv2.imshow("original pic_gray", gray)
	# cv2.imshow("original pic_grayblur", gray_blur) #gaussianblur: pic doing covolution with Normal(gaussian) distribution. To eliminate details of the pic before doing processing with it.
	# cv2.imshow("original pic", sketch(frame).gray)
	if cv2.waitKey(1) & 0xFF == ord('q'):
		break

capture.release()
cv2.destroyAllWindows()			