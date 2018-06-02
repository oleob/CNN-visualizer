
""" Miscellaneous functions and random stuff goes here """

import numpy as np
import random
import PIL.Image
import cv2


# display image
def show_image(img):
    img = img * 255
    img = PIL.Image.fromarray(img.astype('uint8'))
    img.show()


# save image as jpg
def save_image(img, path):
    if img.ndim == 4:
        img = np.squeeze(img)
    img = img * 255
    cv2.imwrite(path, cv2.cvtColor(img, cv2.COLOR_RGB2BGR))


def save_image_naive(img, path):
    img = np.clip(img / 255.0, 0, 1) * 255
    img = PIL.Image.fromarray(img.astype('uint8'))
    img.save(path)


def show_image_naive(img):
    img = np.clip(img / 255.0, 0, 1) * 255
    img = PIL.Image.fromarray(img.astype('uint8'))
    img.show()


# generate an array-image with random noise (from a gaussian distribution)
def random_noise_img(x_dim=200, y_dim=200):
    array = np.zeros((x_dim, y_dim, 3))
    for x in range(x_dim):
        for y in range(y_dim):
            array[x][y][0] = float(min(255, max(0, random.gauss(117, 2.55))))
            array[x][y][1] = float(min(255, max(0, random.gauss(117, 2.55))))
            array[x][y][2] = float(min(255, max(0, random.gauss(117, 2.55))))
    return array


# generate an array of images with one grayscale color
def grey_img(batch_size=1, x_dim=200, y_dim=200, rgb_values=117):
    array = np.full((batch_size, x_dim, y_dim, 3), rgb_values)
    rand_pixel = int(x_dim/2)
    array[0][rand_pixel][rand_pixel][0] = float(min(255, max(0, 0)))
    array[0][rand_pixel][rand_pixel][0] = float(min(255, max(0, 0)))
    array[0][rand_pixel][rand_pixel][0] = float(min(255, max(0, 0)))
    return array








