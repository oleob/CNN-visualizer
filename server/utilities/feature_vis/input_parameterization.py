
""" Different parameterizations of the input space (which can vastly improve the
optimization process) goes here """


import tensorflow as tf
import numpy as np

import utilities.feature_vis.misc as misc
from preprocessing import vgg_preprocessing


# TODO: in case of deepdream, convert the rgb image into the fourier space first
def fft_img(x_dim=200, y_dim=200):
    # input_array = misc.random_noise_img(batch_size, x_dim, y_dim)
    # #input_shape = [batch_size, 3, x_dim, y_dim]
    # t = tf.transpose(input_array, [0, 3, 1, 2])
    # fft = tf.spectral.fft2d(t)
    # ir_fft = tf.spectral.irfft2d(fft)
    # print(ir_fft.shape)
    # img = tf.transpose(ir_fft, [])
    # img = PIL.Image.fromarray(img.astype('uint8'))
    # img.show()

    print("creating a fourier base img")
    # find the frequencies in the y-direction
    freq_y = np.fft.fftfreq(y_dim)[:, None]
    # find the freq in x direction ..in case of odd input dimension,
    # keep one additional frequency and later cut off 1 pixel
    if x_dim % 2 == 1:
        freq_x = np.fft.fftfreq(x_dim)[:x_dim // 2 + 2]
    else:
        freq_x = np.fft.fftfreq(x_dim)[:x_dim // 2 + 1]
    # TODO: get a better grip on the following steps
    freq = np.sqrt(np.square(freq_x) + np.square(freq_y))
    freq_height, freq_width = freq.shape
    init_val = 0.01 * np.random.randn(2, 3, freq_height, freq_width).astype("float32")
    with tf.variable_scope("variable"):
        spectrum_var = tf.Variable(init_val)
    spectrum = tf.complex(spectrum_var[0], spectrum_var[1])
    spectrum_scale = 1.0 / np.maximum(freq, 1.0 / max(y_dim, x_dim))
    spectrum_scale = spectrum_scale*np.sqrt(x_dim*y_dim)
    scaled_spectrum = spectrum * spectrum_scale
    img = tf.spectral.irfft2d(scaled_spectrum)
    img = img[:3, :y_dim, :x_dim]
    img = tf.transpose(img, [1, 2, 0])
    # imgs = tf.expand_dims(img, 0)

    # create a tensor of the list of image-tensors
    # TODO: why divide by 4? ..found the reason somewhere
    # fft_tensor = tf.stack(imgs) / 4.0
    fft_tensor = img / 4.0

    # decorrelate the colors
    # TODO: understand the following color-decorrelation a bit better, the following is just for imagenet
    color_correlation_svd_sqrt = np.asarray([[0.26, 0.09, 0.02],
                                             [0.27, 0.00, -0.05],
                                             [0.27, -0.09, 0.03]]).astype("float32")
    max_norm_svd_sqrt = np.max(np.linalg.norm(color_correlation_svd_sqrt, axis=0))
    flat = tf.reshape(fft_tensor, [-1, 3])
    color_correlation_normalized = color_correlation_svd_sqrt / max_norm_svd_sqrt
    flat = tf.matmul(flat, color_correlation_normalized.T)
    rgb = tf.reshape(flat, tf.shape(fft_tensor))

    # sigmoid the tensor
    rgb = tf.nn.sigmoid(rgb[..., :3])

    # forget height and width of the input
    # zero = tf.identity(0)
    # rgb = rgb[:, zero:, zero:, :]

    # name the image-tensor so we can eval() it and see the results during optimization
    rgb = tf.identity(rgb, name='image')

    return rgb


def naive_input(x_dim=200, y_dim=200, dream_img=None):

    if dream_img is None:
        dream_img = misc.random_noise_img(x_dim, y_dim)
    with tf.variable_scope("variable"):
        rgb = tf.Variable(dream_img, dtype='float32')

    # forget height and width of the input
    # zero = tf.identity(0)
    # rgb = rgb[zero:, zero:, :]

    # name the image-tensor so we can eval() it and see the results during optimization
    rgb = tf.identity(rgb, name='image')

    return rgb

