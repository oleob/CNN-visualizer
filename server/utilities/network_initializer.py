import tensorflow as tf
import os

from nets import inception, vgg
from preprocessing import inception_preprocessing, vgg_preprocessing
from utilities.feature_vis import graph_builder

from tensorflow.contrib import slim

checkpoints_dir = 'checkpoints'


def init_network(network_name, network_type, naive=False, x_dim=-1, y_dim=-1, pad=None, jitter=None, rotate=None, scale=None):

    #Reset graph
    tf.reset_default_graph()
    #Set functions and variables which depend on the selected network
    if network_name == 'InceptionV1':
        preprocessor = inception_preprocessing.preprocess_image
        image_size = inception.inception_v1.default_image_size
        scope = inception.inception_v1_arg_scope
        num_classes = 1001
        net = inception.inception_v1

    elif network_name =='vgg_16':
        preprocessor = vgg_preprocessing.preprocess_image
        image_size = vgg.vgg_16.default_image_size
        scope = vgg.vgg_arg_scope
        num_classes = 1000
        net = vgg.vgg_16
    else:
        raise Exception('Unkown network name: ' + str(network_name))

    #set x_dim and y_dim if not set before
    if x_dim == -1:
        x_dim = image_size
    if y_dim == -1:
        y_dim = image_size

    #Create network input
    if network_type=='predict':
        input_layer = tf.placeholder(tf.uint8, shape=(None, None, 3))
        input_layer = tf.identity(input_layer, name='input_layer')
        input_graph = tf.convert_to_tensor(input_layer, dtype=tf.uint8)
        input_graph = preprocessor(input_graph, x_dim, y_dim, is_training = False)
        input_graph = tf.expand_dims(input_graph, 0)
    elif network_type=='visualize':
        input_layer = graph_builder.build(x_dim, y_dim, pad=pad, jitter=jitter, rotate=rotate, scale=scale, naive=naive)
        input_layer = tf.identity(input_layer, name='input_layer')
        if network_name=='InceptionV1':
            lower, upper = (0, 1)
            input_graph = lower + input_layer * (upper - lower)
            input_graph = tf.subtract(input_graph, 0.5)
            input_graph = tf.multiply(input_graph, 2.0)
        elif network_name=='vgg_16':
            # TODO: find correct preprocessing steps for vgg_16
            input_graph = preprocessor(input_layer, x_dim, y_dim, is_training=False)
        input_graph = tf.expand_dims(input_graph, 0)
        input_graph = tf.identity(input_graph, name='test')
    else:
        raise Exception('Unkown network type: ' + network_type)
    with slim.arg_scope(scope()):
        logits, _ = net(input_graph, num_classes=num_classes, is_training=False)
        probabilities = tf.nn.softmax(logits)
        probabilities = tf.identity(probabilities, name='probabilities')
        init_fn = slim.assign_from_checkpoint_fn(os.path.join(checkpoints_dir, '{0}.ckpt'.format(network_name)), slim.get_model_variables(network_name))

    return init_fn
