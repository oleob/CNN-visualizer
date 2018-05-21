
""" Contains functions for loading in a CNN with trained weights, and
building the entire visualization graph """

import tensorflow as tf
import numpy as np

import utilities.feature_vis.transformations as trans
import utilities.feature_vis.input_parameterization as par


def build(x_dim=224, y_dim=224, pad=None, jitter=None, rotate=None, scale=None, param_space='laplacian', laplace_levels=4, dream_img=None):

    # parametrize the input space for better and faster results
    if param_space == 'fourier':
        input_tensor = par.fourier_space(x_dim, y_dim)
    elif param_space == 'laplacian':
        input_tensor = par.laplacian_pyramid_space(x_dim, y_dim, laplace_levels)
    else:
        input_tensor = par.naive_space(x_dim, y_dim)

    # name the image-tensor so we can eval() it and see the results during optimization
    input_tensor = tf.identity(input_tensor, name='image')

    # build a transformation graph, following the input-graph
    trans_graph = add_transforms(input_tensor, pad=pad, jitter=jitter, rotate=rotate, scale=scale)
    trans_graph = tf.identity(trans_graph, name='transformed')

    # need to define the dimensions because of tf.slim
    if pad is None: pad = 0
    prep_graph = trans_graph[pad:x_dim+pad, pad:y_dim+pad, :]
    prep_graph = tf.reshape(prep_graph, shape=(x_dim, y_dim, 3))

    return prep_graph


def add_transforms(tensor, pad, jitter, rotate, scale):
    if pad is not None:
        tensor = trans.pad(tensor, pad)
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
