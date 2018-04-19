import cv2
import numpy as np

def pad_image(path):
    img = cv2.imread(path, 1)
    bordersize_v = int(np.amax([0.0, (img.shape[0] - img.shape[1])/2]))
    bordersize_h = int(np.amax([0.0, (img.shape[1] - img.shape[0])/2]))
    border=cv2.copyMakeBorder(img, top=bordersize_h, bottom=bordersize_h, left=bordersize_v, right=bordersize_v, borderType= cv2.BORDER_REPLICATE)
    name = path.split('/')[-1]
    new_path = './static/images/padded_imgs/' + name
    cv2.imwrite(new_path, border)
    return new_path
