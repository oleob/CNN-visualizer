
""" This file contains functions for transforming tensorflow tensors that
represents images. These are used in order to get better-looking results
when performing feature-visualizations. """

import tensorflow as tf
import math

# TODO: fill in the rest of the functions


def random_param(param_list):
    random_index = tf.random_uniform((), 0, len(param_list), dtype='int32')
    param = tf.constant(param_list)[random_index]
    param = tf.identity(param, name='random')
    return param


def pad(tensor, pad):
    padding = tf.constant([[pad, pad], [pad, pad], [0, 0]])
    return tf.pad(tensor, padding, constant_values=0.459)


def jitter(tensor, jitter_x, jitter_y):
    pass


# the following function is really just a random crop ..this implementation assumes that there is
# sufficient padding at the start, so a random crop sorta has the same effect on helping the visualization
def random_jitter(tensor, pixels):
    dimensions = tf.shape(tensor)
    height, width = dimensions[0], dimensions[1]
    new_dimensions = [height - pixels, width - pixels, 3]
    tensor = tf.random_crop(tensor, new_dimensions)
    return tensor


def rotate(tensor, angle):
    pass


def random_rotate(tensor, param_list):
    angle = random_param(param_list)
    angle = tf.cast(angle, dtype='float32')
    radian = angle * tf.constant(math.pi, dtype='float32') / 180
    tensor = tf.contrib.image.rotate(tensor, radian)
    return tensor


def scale(tensor, factor):
    pass


def random_scale(tensor, param_list):
    factor = random_param(param_list)
    dimensions = tf.shape(tensor)
    height, width = tf.cast(dimensions[0], dtype='float32'), tf.cast(dimensions[1], dtype='float32')
    scale_height, scale_width = tf.cast(height * factor, dtype='int32'), tf.cast(width * factor, dtype='int32')
    tensor = tf.expand_dims(tensor, 0)
    tensor = tf.image.resize_bilinear(tensor, [scale_height, scale_width])
    tensor = tf.squeeze(tensor, 0)
    return tensor




