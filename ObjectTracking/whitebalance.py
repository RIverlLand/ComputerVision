#soruce : https://stackoverflow.com/questions/45926871/webcam-color-calibration-using-opencv

import numpy as np

def show_image(title, image, width = 300):
    # resize the image to have a constant width, just to
    # make displaying the images take up less screen real
    # estate
    r = width / float(image.shape[1])
    dim = (width, int(image.shape[0] * r))
    resized = cv2.resize(image, dim, interpolation = cv2.INTER_AREA)

    # show the resized image
    cv2.imshow(title, resized)


def hist_match(source, template):
    """
    Adjust the pixel values of a grayscale image such that its histogram
    matches that of a target image

    Arguments:
    -----------
        source: np.ndarray
            Image to transform; the histogram is computed over the flattened
            array
        template: np.ndarray
            Template image; can have different dimensions to source
    Returns:
    -----------
        matched: np.ndarray
            The transformed output image
    """

    oldshape = source.shape
    source = source.ravel()
    template = template.ravel()

    # get the set of unique pixel values and their corresponding indices and
    # counts
    s_values, bin_idx, s_counts = np.unique(source, return_inverse=True,
                                            return_counts=True)
    t_values, t_counts = np.unique(template, return_counts=True)

    # take the cumsum of the counts and normalize by the number of pixels to
    # get the empirical cumulative distribution functions for the source and
    # template images (maps pixel value --> quantile)
    s_quantiles = np.cumsum(s_counts).astype(np.float64)
    s_quantiles /= s_quantiles[-1]
    t_quantiles = np.cumsum(t_counts).astype(np.float64)
    t_quantiles /= t_quantiles[-1]

    # interpolate linearly to find the pixel values in the template image
    # that correspond most closely to the quantiles in the source image
    interp_t_values = np.interp(s_quantiles, t_quantiles, t_values)

    return interp_t_values[bin_idx].reshape(oldshape)

# from matplotlib import pyplot as plt
# from scipy.misc import lena, ascent
import cv2

source = cv2.imread('/media/somadetect/Lexar/color_transfer_data/1/frame10.png')
s_b = source[:,:,0]
s_g = source[:,:,1]
s_r = source[:,:,2]
template =  cv2.imread('/media/somadetect/Lexar/color_transfer_data/5/frame6.png')
t_b = source[:,:,0]
t_r = source[:,:,1]
t_g = source[:,:,2]

matched_b = hist_match(s_b, t_b)
matched_g = hist_match(s_g, t_g)
matched_r = hist_match(s_r, t_r)

y,x,c = source.shape
transfer  = np.empty((y,x,c), dtype=np.uint8)

transfer[:,:,0] = matched_r
transfer[:,:,1] = matched_g
transfer[:,:,2] = matched_b

show_image("Template", template)
show_image("Target", source)
show_image("Transfer", transfer)
cv2.waitKey(0)