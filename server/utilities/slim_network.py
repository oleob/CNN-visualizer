import numpy as np
import os
import tensorflow as tf
import matplotlib.pyplot as plt
import cv2

checkpoints_dir = 'checkpoints'

from datasets import imagenet
from nets import inception, vgg
from preprocessing import inception_preprocessing, vgg_preprocessing

from tensorflow.contrib import slim

from utilities.slim_taylor import Taylor
import utilities.traverse as traverse
from utilities.preprocess import pad_image
from utilities.layer_names import inception_names

class Network:
    def __init__(self, network_name):
        tf.reset_default_graph()
        self.input_image = tf.placeholder(tf.uint8, shape=(None, None, 3))
        image = tf.convert_to_tensor(self.input_image, dtype=tf.uint8)
        if network_name == 'InceptionV1':
            shift_index = False
            traverse_graph = traverse.inception_v1
            image_size = inception.inception_v1.default_image_size
            processed_image = inception_preprocessing.preprocess_image(image, image_size, image_size, is_training=False)
            processed_images  = tf.expand_dims(processed_image, 0)
            with slim.arg_scope(inception.inception_v1_arg_scope()):
                logits, _ = inception.inception_v1(processed_images, num_classes=1001, is_training=False)
                probabilities = tf.nn.softmax(logits)

                init_fn = slim.assign_from_checkpoint_fn(os.path.join(checkpoints_dir, 'inception_v1.ckpt'), slim.get_model_variables('InceptionV1'))
                self.layer_names = inception_names(tf.get_default_graph().get_tensor_by_name('Softmax:0'))
        elif network_name == 'vgg_16':
            shift_index = True
            traverse_graph = traverse.vgg_16
            image_size = vgg.vgg_16.default_image_size
            processed_image = vgg_preprocessing.preprocess_image(image, image_size, image_size, is_training=False)
            processed_images  = tf.expand_dims(processed_image, 0)

            # Create the model, use the default arg scope to configure the batch norm parameters.
            with slim.arg_scope(vgg.vgg_arg_scope()):
                logits, _ = vgg.vgg_16(processed_images, num_classes=1000, is_training=False)
                probabilities = tf.nn.softmax(logits)

                init_fn = slim.assign_from_checkpoint_fn(os.path.join(checkpoints_dir, 'vgg_16.ckpt'), slim.get_model_variables('vgg_16'))
        self.init_fn = init_fn
        self.sess_config = tf.ConfigProto(device_count = {'GPU': 0})
        self.output_layer = probabilities
        self.traverse_graph = traverse_graph
        self.checkpoints_dir = 'checkpoints'
        self.shift_index = shift_index
        self.imagenet_labels = imagenet.create_readable_names_for_imagenet_labels()


    def predict(self, img, num_items, pad_image):
        if pad_image:
            img = pad_image(img)

        sess = tf.Session(config=self.sess_config)
        self.init_fn(sess)
        probabilities = sess.run(self.output_layer, feed_dict={self.input_image:img})
        probabilities = probabilities[0, 0:]
        sorted_inds = [i[0] for i in sorted(enumerate(-probabilities), key=lambda x:x[1])]

        shift = 0
        if self.shift_index:
            shift = 1
        results = []
        for i in range(num_items):
            index = sorted_inds[i]

            item = {}
            item['name'] = self.imagenet_labels[index + shift]
            item['value'] = round(float(probabilities[index]), 4)
            results.append(item)
        return results

    def print_layers(self):
        sess = tf.Session(config=self.sess_config)
        self.init_fn(sess)
        layer = sess.graph.get_tensor_by_name('Softmax:0') #TODO replace with output_layer
        while not ('ExpandDims' in layer.name):
            print(layer.name, layer.shape)
            layer = self.get_parent(layer, 1)

    def get_parent(self, child, num_skips):
        parent = child
        for i in range(num_skips):
            parent = [inp for inp in parent.op.inputs if not (inp.op.type=='Const')][0]
        return parent

    def deep_taylor(self):
        taylor = Taylor( self.init_fn, self.sess_config, self.traverse_graph)
        relevances = taylor()
        taylor.run_relevances(relevances)

    def get_layer_names(self):
        return self.layer_names
