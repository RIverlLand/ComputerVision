import numpy as np
import cv2
import argparse
from color_transfer import color_transfer

def str2bool(v):
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')

# color_range = [[0,0,0],[179,50,100]] #set the hsv color range
color_range = ([0,0,120],[150,70,255]) #GBR color range for red?

points = []
count = 0

capture = cv2.VideoCapture(0)
respone, target = capture.read()

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-s", "--source", required = True,
    help = "Path to the source image")
# ap.add_argument("-t", "--target", required = True,
#     help = "Path to the target image")
ap.add_argument("-c", "--clip", type = str2bool, default = 't',
    help = "Should np.clip scale L*a*b* values before final conversion to BGR? "
        "Approptiate min-max scaling used if False.")
ap.add_argument("-p", "--preservePaper", type = str2bool, default = 't',
    help = "Should color transfer strictly follow methodology layed out in original paper?")
args = vars(ap.parse_args())

source = cv2.imread(args["source"])

while True:
    response, frame = capture.read()
    height, width = frame.shape[:2]

    transfer = color_transfer(source, frame, clip=args["clip"], preserve_paper=args["preservePaper"])

    # hsv = cv2.cvtColor(transfer, cv2.COLOR_BGR2HSV) #transfer to HSV color

    mask = cv2.inRange(transfer, np.array(color_range[0]), np.array(color_range[1])) #point of having a color range is to rule out the color that will not contain in the video, however the color various from different light conditions.
    # a mask is the same size as our image, but has only two pixel values, 0 and 255 -- pixels with a value of 0 (background) are ignored in the original image while mask pixels with a value of 255 (foreground) are allowed to be kept
    kernel = np.ones((1,1),np.uint8)
    # mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel) #automatically erosion and dilation operation
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    masked = cv2.bitwise_and(frame, frame, mask=mask)


    _, contours, _ = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if len(contours) > 0:
        biggest_contour = max(contours, key=cv2.contourArea)
        cv2.drawContours(frame, biggest_contour, -1, (0,0,255), 3)
    cv2.imshow('image', transfer)
    cv2.imshow('origin', frame)
    cv2.imshow('masked', masked)

    if cv2.waitKey(1) & 0xFF == ord('q'):
	    break

capture.release()
cv2.destroyAllWindows()