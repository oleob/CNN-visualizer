import cv2
import numpy as np
import math

def pad_image(img):
    bordersize_v = int(np.amax([0.0, (img.shape[0] - img.shape[1])/2]))
    bordersize_h = int(np.amax([0.0, (img.shape[1] - img.shape[0])/2]))
    padded_img = cv2.copyMakeBorder(img, top=bordersize_h, bottom=bordersize_h, left=bordersize_v, right=bordersize_v, borderType= cv2.BORDER_REPLICATE)
    return padded_img
