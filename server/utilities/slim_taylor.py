import tensorflow as tf
import cv2
from tensorflow.python.ops import nn_ops, gen_nn_ops
import numpy as np
import matplotlib.pyplot as plt

class Taylor:
    def __init__(self, input_image, init_fn, sess_config, traverse_graph, output_layer, epsilon=1e-10):
        self.epsilon = epsilon

        graph = tf.get_default_graph()
        #output_layer = graph.get_tensor_by_name('Softmax:0')
        layer = output_layer.op.inputs[0]
        relevances = [output_layer]
        relevances = traverse_graph(self, layer, relevances)

        self.init_fn = init_fn
        self.sess_config = sess_config
        self.input_image = input_image
        self.relevances = relevances

    def get_parent(self, child, num_skips):
        parent = child
        for i in range(num_skips):
            parent = [inp for inp in parent.op.inputs if not (inp.op.type=='Const')][0]
        return parent

    def backprop_conv(self, activation, weights, relevance, strides, padding):
        w_pos = tf.maximum(0., weights)
        z = tf.nn.conv2d(activation, w_pos, strides, padding) + self.epsilon
        s = relevance / z
        c = gen_nn_ops.conv2d_backprop_input(tf.shape(activation), w_pos, s, strides, padding)
        return activation * c

    def backprop_max_pool(self, activation, relevance, ksize, strides, padding):
        z = tf.nn.max_pool(activation, ksize, strides, padding) + self.epsilon
        #z = nn_ops.avg_pool(activation, ksize, strides, padding='SAME') + self.epsilon
        s = relevance / z
        #c = gen_nn_ops._avg_pool_grad(tf.shape(activation), s, ksize, strides, padding='SAME')
        c = gen_nn_ops.max_pool_grad_v2(activation, z, s, ksize, strides, padding)
        return activation * c

    def backprop_avg_pool(self, activation, relevance, ksize, strides, padding):
        z = tf.nn.avg_pool(activation, ksize, strides, padding) + self.epsilon
        s = relevance / z
        c = gen_nn_ops._avg_pool_grad(tf.shape(activation), s, ksize, strides, padding)
        return c * activation

    def backprop_inception(self, layer, activation, relevance):
        inputs = [inp for inp in layer.op.inputs if not (inp.op.type=='Const')]
        split_dim = tf.constant([int(inputs[0].shape[3]), int(inputs[1].shape[3]), int(inputs[2].shape[3]), int(inputs[3].shape[3])])
        r_1, r_3, r_5, r_p = tf.split(relevance, split_dim, axis=3)
        r_1x1 = self.backprop_1x1(inputs[0], activation, r_1)
        r_3x3 = self.backprop_nxn(inputs[1], activation, r_3)
        r_5x5 = self.backprop_nxn(inputs[2], activation, r_5)
        r_pool = self.backprop_inception_pool(inputs[3], activation, r_p)
        new_relevance = (r_1x1 + r_3x3 + r_5x5 + r_pool)
        return new_relevance

    def backprop_1x1(self, layer, activation, relevance):
        conv = self.get_parent(layer,2)
        weights = conv.op.inputs[1]
        strides = conv.op.get_attr('strides')
        padding = conv.op.get_attr('padding')
        return self.backprop_conv(activation, weights, relevance, strides, padding)

    def backprop_nxn(self, layer, activation_1x1, relevance_nxn):
        activation_nxn = self.get_parent(layer, 3)

        conv_nxn = self.get_parent(layer, 2)
        weights_nxn = conv_nxn.op.inputs[1]
        strides_nxn = conv_nxn.op.get_attr('strides')
        padding_nxn = conv_nxn.op.get_attr('padding')

        conv_1x1 = self.get_parent(conv_nxn, 3)
        weights_1x1 = conv_1x1.op.inputs[1]
        strides_1x1 = conv_1x1.op.get_attr('strides')
        padding_1x1 = conv_1x1.op.get_attr('padding')

        relevance_1x1 = self.backprop_conv(activation_nxn, weights_nxn, relevance_nxn, strides_nxn, padding_nxn)
        return self.backprop_conv(activation_1x1, weights_1x1, relevance_1x1, strides_1x1, padding_1x1)

    def backprop_inception_pool(self, layer, activation_pool, relevance_1x1):
        conv_1x1 = self.get_parent(layer, 2)
        activation_1x1 = self.get_parent(layer, 3)
        weights_1x1 = conv_1x1.op.inputs[1]
        ksize = activation_1x1.op.get_attr('ksize')
        strides = activation_1x1.op.get_attr('strides')
        padding = activation_1x1.op.get_attr('padding')
        strides_1x1 = conv_1x1.op.get_attr('strides')
        padding_1x1 = conv_1x1.op.get_attr('padding')
        relevance_pool = self.backprop_conv(activation_1x1, weights_1x1, relevance_1x1, strides_1x1, padding_1x1)
        return self.backprop_max_pool(activation_pool, relevance_pool, ksize, strides, padding)

    def backprop_conv_input(self, activation, weights, relevance, strides, padding, lowest=0., highest=1.):
        lowest = tf.reduce_min(activation)
        highest = tf.reduce_max(activation)
        W_p = tf.maximum(0., weights)
        W_n = tf.minimum(0., weights)

        L = tf.ones_like(activation, tf.float32) * lowest
        H = tf.ones_like(activation, tf.float32) * highest

        z_o = nn_ops.conv2d(activation, weights, strides, padding)
        z_p = nn_ops.conv2d(L, W_p, strides, padding)
        z_n = nn_ops.conv2d(H, W_n, strides, padding)

        z = z_o - z_p - z_n + 1e-10
        s = relevance / z

        c_o = nn_ops.conv2d_backprop_input(tf.shape(activation), weights, s, strides, padding)
        c_p = nn_ops.conv2d_backprop_input(tf.shape(activation), W_p, s, strides, padding)
        c_n = nn_ops.conv2d_backprop_input(tf.shape(activation), W_n, s, strides, padding)

        return activation * c_o - L * c_p - H * c_n

    def run_relevances(self):
        sess = tf.Session(config=self.sess_config)
        self.init_fn(sess)
        img = cv2.imread('./static/images/penguins3.jpg',1)
        result = sess.run(self.relevances, feed_dict={self.input_image: img})
        filepaths = []
        for r in range(len(result)):
            res = result[r]
            if(len(res.shape) >= 4 and res.shape[1] > 1):
                res = res[0,:,:,:]
                float_img = np.sum(res, axis=2)
                float_img /= float_img.max()
                float_img *= 255
                img = cv2.resize(float_img, (224, 224), interpolation=0).astype(np.uint8)
                img = cv2.applyColorMap(img, cv2.COLORMAP_JET)

                filepath = 'static/images/temp/{0}_{1}.jpg'.format(r, np.sum(res))
                cv2.imwrite(filepath, img)
                filepaths.append(filepath)
        sess.close()
        return filepaths
