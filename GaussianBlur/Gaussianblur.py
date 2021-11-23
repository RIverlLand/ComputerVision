import cv2
# import numpy as np

image = cv2.imread('image/Computer.jpg')

r = (5, 5)
sigma1 = 1
sigma2 = 2
sigma3 = 3
sigma4 = 4

def main():
# while(True):
    cv2.imshow("Result of sigma=%d " %sigma1, Gaussianblur(r, sigma1)) #printing stuff will be feeding params to the %d by the % instead of putting a comma behind the sentence like in c language
    cv2.imshow("Result of sigma=%d " %sigma2, Gaussianblur(r, sigma2))
    cv2.imshow("Result of sigma=%d " %sigma3, Gaussianblur(r, sigma3))
    cv2.imshow("Result of sigma=%d " %sigma4, Gaussianblur(r, sigma4))
    cv2.waitKey(0)
    # if cv2.waitKey(1) & 0xFF == ord('q'): #what is this?
    #     break  
    cv2.destroyAllWindows()
    exit() #writting a exit in python programm would quit it as intended, using ctrl+c usually results in nothing in python programm.

# def main():
#     cv2.imshow("Result of sigma=%d" %sigma1, cv2.GaussianBlur(image, r, sigma1)) #Using function inside function is excutable, I failed before because of wrong param was fed into Blur function.

#     cv2.waitKey(0)
#     cv2.destroyAllWindows()
#     exit()

def Gaussianblur(radius, sigma):
    process_image = cv2.GaussianBlur(image, radius, sigma) #GaussianBlur requires the pic, radius aka the size of the filter and the sigma. So what's written in array would be 5x5 filter.
    return process_image


main()