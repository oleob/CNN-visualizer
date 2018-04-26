import numpy as np
import tensorflow as tf
import cv2
import uuid
from datasets import imagenet

from utilities.slim_taylor import Taylor
import utilities.traverse as traverse
from utilities.preprocess import pad_image
from utilities.layer_names import inception_names, vgg_16_names

class Network:
    def __init__(self, network_name, input_layer, probabilities, init_fn):

        if network_name == 'InceptionV1':
            shift_index = False
            layer_names = inception_names
            traverse_graph = traverse.inception_v1
        elif network_name == 'vgg_16':
            shift_index = True
            layer_names = vgg_16_names
            traverse_graph = traverse.vgg_16
        else:
            raise Exception('Unkown network name: ' + str(network_name))

        self.init_fn = init_fn
        self.sess_config = tf.ConfigProto(device_count = {'GPU': 0})
        self.input_image = input_layer
        self.output_layer = probabilities
        self.traverse_graph = traverse_graph
        self.shift_index = shift_index
        self.imagenet_labels = imagenet.create_readable_names_for_imagenet_labels()
        self.layer_names = layer_names
        self.taylor = Taylor(self.input_image, self.init_fn, self.sess_config, self.traverse_graph, self.output_layer)

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

    def get_deep_taylor(self):
        return self.taylor.run_relevances()

    def get_layer_names(self):
        return self.layer_names

    def get_layer_activations(self, layer_name):
        #load image
        img = cv2.imread('./static/images/penguins3.jpg',1)
        sess = tf.Session(config=self.sess_config)
        self.init_fn(sess)
        #Get the tensor by name
        tensor = sess.graph.get_tensor_by_name(layer_name)
        print([inp for inp in tensor.op.inputs])

        img, units = sess.run([self.processed_image, tensor],feed_dict={self.input_image: img})
        img = 255*(img + 1.0)/2.0
        #format the filters
        filters = units[0,:,:,:]
        filter_size = units.shape[3]
        width = units.shape[1]
        height = units.shape[2]

        sorted_filters = list()
        for i in range(filter_size):
            fi = filters[:,:,i]
            sorted_filters.append((fi.sum(),i,fi))
        sorted_filters = sorted(sorted_filters, reverse=True, key=lambda tup: tup[0])
        filepaths = []
        for i in range(10):
            filter_tuple = sorted_filters[i]
            activation = filter_tuple[2]/filter_tuple[2].max()
            height, width, channels = img.shape
            activation = cv2.resize(activation,(width, height), interpolation=0)
            r,g,b = cv2.split(img)
            r = r*activation
            g = g*activation
            b = b*activation
            newImg = cv2.merge((r,g,b))


            #filepath = 'static/images/temp/'+ str(uuid.uuid4()) + '.jpg'
            filepath = 'static/images/temp/' + str(filter_tuple[1]) + '__' + str(filter_tuple[0]) + '.jpg'
            cv2.imwrite(filepath, newImg)
            filepaths.append(filepath)
        return filepaths
