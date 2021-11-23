from os import X_OK
import cv2
import dlib
import numpy as np 


PATH = 'shape_predictor_68_face_landmarks.dat'

predictor = dlib.shape_predictor(PATH)
detector = dlib.get_frontal_face_detector()

# class TooManyFaces(Exception):
#     pass

# class NoFaces(Exception):
#     pass

# Detect landpoints' on input image
def get_landmarks(image):
	
	return np.matrix([[t.x, t.y] for t in predictor(image, points[0]).parts()])


# Mark and point landmarks' on input image using numbers
def mark_landmarks(image, landmarks):
	image = image.copy()
	for i, point in enumerate(landmarks): #enumerate modify a list into a tuple, for example list = ['A','B','C'], enumerate(list) = [(0, 'A'), (1, 'B'), (2, 'C')]
		position = (point[0,0], point[0,1])
		cv2.putText(image, str(i), (position), fontFace=cv2.FONT_ITALIC, fontScale=0.4, color=(0,0,0))
		cv2.circle(image, position, 3, color=(0,255,0))

	return image

image = cv2.VideoCapture(0)

response, frame = image.read()

while True:
	response, frame = image.read()
	points = detector(frame, 1)
	if len(points) == 1:
		l = get_landmarks(frame)
		marked_image = mark_landmarks(frame, l)
		cv2.imshow(winname="FaceLandmarks", mat=marked_image)
		if cv2.waitKey(1) & 0xFF == ord('q'): #if there's no waitKey in between, the program will show the pic in such a short time, 0 actually, it looks like nothin is being shown.
			break
	else:
		cv2.imshow(winname="FaceLandmarks", mat=frame)

	if cv2.waitKey(1) & 0xFF == ord('q'):
	    break


cv2.destroyAllWindows()					
