
""" Contains functions for loading in a CNN with trained weights, and
building the entire visualization graph """

import tensorflow as tf
import numpy as np

import utilities.feature_vis.transformations as trans
import utilities.feature_vis.input_parameterization as par


def build(x_dim=224, y_dim=224, pad=None, jitter=None, rotate=None, scale=None,
          param_space='laplacian', laplace_levels=4, dream_img=None, decorrelate_colors=True):

    padded_dim = x_dim+2*pad

    # parametrize the input space for better and faster results
    if param_space == 'fourier':
        input_tensor = par.fourier_space(padded_dim, padded_dim)
    elif param_space == 'laplacian':
        input_tensor = par.laplacian_pyramid_space(padded_dim, padded_dim, laplace_levels)
    else:
        if dream_img is not None:
            dream_img = dream_img.astype("float32")
            dream_img = dream_img / 255
            scale_img = x_dim / len(dream_img)
            y_dim = int(scale_img * len(dream_img[0]))
        input_tensor = par.naive_space(x_dim+2*pad, y_dim+2*pad, dream_img, decorrelate_colors)

    # decorrelate the colors
    if decorrelate_colors:
        input_tensor = par.decorrelate_imagenet_colors(input_tensor)

    # sigmoid the tensor
    if dream_img is None:
        input_tensor = tf.nn.sigmoid(input_tensor[..., :3])

    # name the image-tensor so we can eval() it and see the results during optimization
    image_tensor = input_tensor[pad:x_dim+pad, pad: y_dim+pad]
    image_tensor = tf.identity(image_tensor, name='image')

    # build a transformation graph, following the input-graph
    trans_graph = add_transforms(input_tensor, pad=pad, jitter=jitter, rotate=rotate, scale=scale)
    trans_graph = tf.identity(trans_graph, name='transformed')

    # need to define the dimensions because of tf.slim
    x_dim_input = tf.shape(trans_graph)[0]
    y_dim_input = tf.shape(trans_graph)[1]

    defined_input = tf.reshape(trans_graph, shape=(x_dim_input, y_dim_input, 3))

    return defined_input


def add_transforms(tensor, pad, jitter, rotate, scale):
    # if pad is not None:
    #     tensor = trans.pad(tensor, pad, pad)
    if jitter is not None:
        tensor = trans.random_jitter(tensor, jitter)
    if rotate is not None:
        tensor = trans.random_rotate(tensor, rotate)
    if scale is not None:
        tensor = trans.random_scale(tensor, scale)
    #tensor = trans.random_jitter(tensor, 2)
    return tensor


def load_labels(path):
    pass
