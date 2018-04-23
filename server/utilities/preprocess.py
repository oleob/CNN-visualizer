import cv2
import numpy as np
import math

def pad_image(img):
    vertical = int((img.shape[1] - img.shape[0]))
    horizontal= int((img.shape[0] - img.shape[1]))
    if vertical < 0:
        top = 0
        bottom = 0
    else:
        top = math.floor(vertical/2)
        bottom = math.ceil(vertical/2)

    if horizontal < 0:
        left = 0
        right = 0
    else:
        left = math.floor(horizontal/2)
        right = math.ceil(horizontal/2)

    padded_img=cv2.copyMakeBorder(img, top=top, bottom=bottom, left=left, right=right, borderType= cv2.BORDER_REPLICATE)
    return padded_img
