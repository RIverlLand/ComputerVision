#Since the VideoCapture read pic as BRG color, the boundaries and color order should all be modified.
import cv2
import numpy as np
import argparse


capture = cv2.VideoCapture(0)
color = ("Blue", "Green", "Red", "White")

boundaries = [
	([17, 15, 100], [50, 56, 200]),
	([86, 31, 4], [220, 88, 50]),
	([25, 146, 190], [62, 174, 250]),
	([103, 86, 65], [145, 133, 128])
]

while(True):
    response, frame = capture.read()
    count = 0

    for (lower, upper) in boundaries: 
        lower = np.array(lower, dtype = "uint8")
        upper = np.array(upper, dtype = "uint8")
        mask = cv2.inRange(frame, lower, upper)
        output = cv2.bitwise_and(frame, frame, mask = mask)

        cv2.imshow(color[count], np.hstack([frame, output]))
        # cv2.imshow(color[count], output)

        #output of the video has some bias or missegmentation of color, maybe a white balance of the video captured is in need.
        #and of course, the bounderies are not well.

        count = count + 1

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

capture.release()
cv2.destroyAllWindows()