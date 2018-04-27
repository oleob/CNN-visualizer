
""" Contains functions for loading in a CNN with trained weights, and
building the entire visualization graph """

import tensorflow as tf
import numpy as np

import utilities.feature_vis.transformations as trans
import utilities.feature_vis.input_parameterization as par


def build(x_dim=224, y_dim=224, pad=None, jitter=None, rotate=None, scale=None, naive=False, dream_img=None):
    # parametrize the input space for better results
    # TODO: give the option to use more parameterization spaces
    if dream_img is None and naive is False:
        input_tensor = par.fft_img(x_dim, y_dim)
    else:
        input_tensor = par.naive_input(x_dim, y_dim, dream_img)

    # build a transformation graph, following the input-graph
    trans_graph = add_transforms(input_tensor, pad=pad, jitter=jitter, rotate=rotate, scale=scale)
    trans_graph = tf.identity(trans_graph, name='transformed')

    # need to define the dimensions because of tf.slim
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
