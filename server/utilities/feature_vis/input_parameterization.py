
""" Different parameterizations of the input space (which can vastly improve the
optimization process) goes here """


import tensorflow as tf
import numpy as np

import utilities.feature_vis.misc as misc
from preprocessing import vgg_preprocessing

canonical_color_correlations = np.asarray([[0.26, 0.09, 0.02],
                                           [0.27, 0.00, -0.05],
                                           [0.27, -0.09, 0.03]]).astype("float32")

def decorrelate_imagenet_colors(tensor):
    flat_rgb = tf.reshape(tensor, [-1, 3])
    flat_rgb = tf.matmul(flat_rgb, canonical_color_correlations.T)
    tensor = tf.reshape(flat_rgb, tf.shape(tensor))
    return tensor


def correlate_imagenet_colors(tensor):
    color_correlations_inv = np.linalg.inv(canonical_color_correlations)
    flat_rgb = tf.reshape(tensor, [-1, 3])
    flat_rgb = tf.matmul(flat_rgb, color_correlations_inv.T)
    tensor = tf.reshape(flat_rgb, tf.shape(tensor))
    return tensor


def fourier_space(x_dim=200, y_dim=200):
    print("creating a fourier base img")
    # find the dimensions of the frequency space
    r_freq, c_freq = x_dim, y_dim//2 + 1

    # create arrays of the frequency bins in both directions
    r_freq_bins = np.fft.fftfreq(y_dim)[:, None]
    c_freq_bins = np.fft.fftfreq(x_dim)[:c_freq]

    # initialize the space with random values
    initial_values = 0.01 * np.random.randn(2, 3, r_freq, c_freq).astype("float32")
    with tf.variable_scope("variable"):
        spectrum_var = tf.Variable(initial_values)
    spectrum = tf.complex(spectrum_var[0], spectrum_var[1])

    # scale with the
    freq = np.sqrt(np.square(r_freq_bins) + np.square(c_freq_bins))
    # replace 0.0, so we can divide
    freq[freq == 0.0] = 1.0 / max(y_dim, x_dim)
    spectrum_scale = 1.0 / freq
    scaled_spectrum = spectrum * spectrum_scale

    # take the inverse 2d-fft to get back to a standard rgb-image
    rgb = tf.spectral.irfft2d(scaled_spectrum)
    rgb = rgb[:3, :y_dim, :x_dim]
    rgb = tf.transpose(rgb, [1, 2, 0])

    return rgb


def naive_space(x_dim=200, y_dim=200, dream_img=None, decorrelate_colors=True):

    if dream_img is not None:
        if decorrelate_colors:
            dream_img = correlate_imagenet_colors(dream_img)
        initial_values = tf.convert_to_tensor(dream_img)
        initial_values = tf.expand_dims(initial_values, 0)
        initial_values = tf.image.resize_bilinear(initial_values, [x_dim, y_dim])
        initial_values = tf.squeeze(initial_values)
    else:
        initial_values = 0.01 * np.random.randn(x_dim, y_dim, 3).astype("float32")

    with tf.variable_scope("variable"):
        rgb = tf.Variable(initial_values)

    return rgb


def laplacian_pyramid_space(x_dim=200, y_dim=200, laplace_levels=4):

    pyramid_tensor = 0

    for n in range(laplace_levels):

        # compute the dimensions of a smaller image
        temp_x_dim = x_dim // 2**n
        temp_y_dim = y_dim // 2**n

        # initalize a random laplacian which will be added to the pyramid
        # we need 4 dimensions because resize_bilinear expects a rank of 4
        initial_values = 0.01 * np.random.randn(1, temp_x_dim, temp_y_dim, 3).astype("float32")
        with tf.variable_scope("variable"):
            temp_tensor = tf.Variable(initial_values)
            print(temp_tensor.shape)
        temp_tensor = tf.image.resize_bilinear(temp_tensor, [x_dim, y_dim])
        pyramid_tensor += temp_tensor

    # remove unnecessary batch dimension
    rgb = tf.squeeze(pyramid_tensor)

    return rgb


