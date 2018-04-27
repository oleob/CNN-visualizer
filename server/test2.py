import numpy as np
import os
import tensorflow as tf
import matplotlib.pyplot as plt
import cv2

checkpoints_dir = 'checkpoints'

try:
    import urllib2 as urllib
except ImportError:
    import urllib.request as urllib

from datasets import imagenet
from nets import inception
from preprocessing import inception_preprocessing

from tensorflow.contrib import slim

image_size = inception.inception_v1.default_image_size

def print_layers(output_layer):
    layer = output_layer
    while not (layer.op.name == 'input'):
        print(layer.op.name, [inp.op.name for inp in layer.op.inputs if not (inp.op.type=='Const')])
        layer = get_parent(layer, 1)

def get_parent(child, num_skips):
    parent = child
    for i in range(num_skips):
        parent = [inp for inp in parent.op.inputs if not (inp.op.type=='Const')][0]
    return parent

with tf.Graph().as_default():
    img = tf.read_file('./static/images/dog-horse.jpg')
    image = tf.image.decode_jpeg(img, channels=3)
    processed_image = inception_preprocessing.preprocess_image(image, image_size, image_size, is_training=False)
    processed_images  = tf.expand_dims(processed_image, 0)

    input_layer = tf.placeholder(tf.float32, (None, 224, 244, 3))

    # Create the model, use the default arg scope to configure the batch norm parameters.
    with slim.arg_scope(inception.inception_v1_arg_scope()):
        logits, _ = inception.inception_v1(processed_images, num_classes=1001, is_training=False)
    probabilities = tf.nn.softmax(logits)

    init_fn = slim.assign_from_checkpoint_fn(
        os.path.join(checkpoints_dir, 'inception_v1.ckpt'),
        slim.get_model_variables('InceptionV1'))

    with tf.Session() as sess:
        init_fn(sess)
        output_layer = sess.graph.get_tensor_by_name('Softmax:0')
        print_layers(output_layer)
        # for op in tf.get_default_graph().as_graph_def().node:
        #     if not ('save' in op.name or 'BatchNorm' in op.name):
        #         print(op.name)
        np_image, probabilities = sess.run([image, probabilities])
        probabilities = probabilities[0, 0:]
        sorted_inds = [i[0] for i in sorted(enumerate(-probabilities), key=lambda x:x[1])]

    plt.figure()
    plt.imshow(np_image.astype(np.uint8))
    plt.axis('off')
    plt.show()

    names = imagenet.create_readable_names_for_imagenet_labels()
    for i in range(5):
        index = sorted_inds[i]
        print('Probability %0.2f%% => [%s]' % (probabilities[index] * 100, names[index]))
