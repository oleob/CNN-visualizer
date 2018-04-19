import numpy as np
import os
import tensorflow as tf
import matplotlib.pyplot as plt
import cv2

checkpoints_dir = 'checkpoints'

from datasets import imagenet
from nets import inception
from preprocessing import inception_preprocessing

from tensorflow.contrib import slim

from utilities.slim_taylor import Taylor
from utilities.net_funcs.inception_v1 import traverse_graph

class Network:
    def __init__(self):
        image_size = inception.inception_v1.default_image_size

        img = tf.read_file('./static/images/penguins3.jpg')
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

        sess = tf.Session()
        init_fn(sess)
        self.sess = sess
        self.output_layer = probabilities
        self.checkpoints_dir = 'checkpoints'

    def predict(self):

        probabilities = self.sess.run(self.output_layer)
        probabilities = probabilities[0, 0:]
        sorted_inds = [i[0] for i in sorted(enumerate(-probabilities), key=lambda x:x[1])]

        names = imagenet.create_readable_names_for_imagenet_labels()
        for i in range(5):
            index = sorted_inds[i]
            print('Probability %0.2f%% => [%s]' % (probabilities[index] * 100, names[index]))

    def print_layers(self):
        layer = self.sess.graph.get_tensor_by_name('Softmax:0') #TODO replace with output_layer
        while not ('ExpandDims' in layer.name):
            print(layer.name, layer.shape)
            layer = self.get_parent(layer, 1)

    def get_parent(self, child, num_skips):
        parent = child
        for i in range(num_skips):
            parent = [inp for inp in parent.op.inputs if not (inp.op.type=='Const')][0]
        return parent

    def deep_taylor(self):
        taylor = Taylor(self.sess, traverse_graph)
        relevances = taylor()
        taylor.run_relevances(relevances)
