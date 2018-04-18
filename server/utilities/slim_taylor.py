import tensorflow as tf
import cv2
from tensorflow.python.ops import nn_ops, gen_nn_ops
import numpy as np
import matplotlib.pyplot as plt

class Taylor:
    def __init__(self, sess, epsilon=1e-10):
        self.sess = sess
        self.epsilon = epsilon
        self.graph = sess.graph
        self.output_layer = sess.graph.get_tensor_by_name('Softmax:0')
        self.new_output = tf.placeholder(tf.float32, self.output_layer.shape)

    def __call__(self):
        relevances = [self.output_layer]
        layer = self.output_layer.op.inputs[0]
        while not ('ExpandDims' in layer.name):
            print(layer.name)
            with tf.variable_scope(layer.op.name + '_taylor'):
                #if squeeze skip to next node
                if 'SpatialSqueeze' in layer.name:
                    layer = self.get_parent(layer, 1)
                #if BiasAdd = end of convolution
                elif 'BiasAdd' in layer.name:
                    conv = self.get_parent(layer,1)
                    weights = self.get_parent(conv.op.inputs[1], 1)
                    activation = self.get_parent(layer, 3)
                    relevances.append(self.backprop_conv(activation, weights, relevances[-1], strides=conv.op.get_attr('strides')))
                    layer = activation
                elif 'Dropout' in layer.name:
                    layer = self.get_parent(layer, 1)
                elif 'AvgPool' in layer.name:
                    activation = self.get_parent(layer, 1)
                    ksize = layer.op.get_attr('ksize')
                    strides = layer.op.get_attr('strides')
                    padding = layer.op.get_attr('padding')
                    relevances.append(self.backprop_avg_pool(activation, relevances[-1], ksize, strides, padding))
                    layer = activation
                elif 'concat' in layer.name:
                    activation = self.get_parent(layer, 4)
                    relevances.append(self.backprop_inception(layer, activation, relevances[-1]))
                    #print(layer.op.name, activation.op.name)
                    layer = activation
                elif 'MaxPool' in layer.name:
                    activation = self.get_parent(layer, 1)
                    ksize = layer.op.get_attr('ksize')
                    strides = layer.op.get_attr('strides')
                    padding = layer.op.get_attr('padding')
                    relevances.append(self.backprop_avg_pool(activation, relevances[-1], ksize, strides, padding))
                    layer = activation
                elif 'Relu' in layer.name:
                    activation = self.get_parent(layer, 3)
                    conv = self.get_parent(layer, 2)
                    weights = self.get_parent(conv.op.inputs[1], 1)
                    if not ('ExpandDims' in activation.name):
                        relevances.append(self.backprop_conv(activation, weights, relevances[-1], strides=conv.op.get_attr('strides')))
                    else:
                        relevances.append(self.backprop_conv_input(activation, weights, relevances[-1], strides=conv.op.get_attr('strides')))
                    layer = activation
                else:
                    print('end:', layer.name)
                    break

        return relevances

    def get_parent(self, child, num_skips):
        parent = child
        for i in range(num_skips):
            parent = [inp for inp in parent.op.inputs if not (inp.op.type=='Const')][0]
        return parent

    def backprop_conv(self, activation, weights, relevance, strides=[1, 1, 1, 1], padding='SAME'):
        w_pos = tf.maximum(0., weights)
        z = tf.nn.conv2d(activation, w_pos, strides, padding='SAME') + self.epsilon
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
        c = gen_nn_ops._avg_pool_grad(tf.shape(activation), s, ksize, strides, padding=padding)
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
        weights = self.get_parent(conv.op.inputs[1], 1)
        return self.backprop_conv(activation, weights, relevance, strides=conv.op.get_attr('strides'))

    def backprop_nxn(self, layer, activation_1x1, relevance_nxn):
        activation_nxn = self.get_parent(layer, 3)
        conv_nxn = self.get_parent(layer, 2)
        conv_1x1 = self.get_parent(conv_nxn, 3)
        weights_nxn = self.get_parent(conv_nxn.op.inputs[1], 1)
        weights_1x1 = self.get_parent(conv_1x1.op.inputs[1], 1)
        relevance_1x1 = self.backprop_conv(activation_nxn, weights_nxn, relevance_nxn, strides=conv_nxn.op.get_attr('strides'))
        return self.backprop_conv(activation_1x1, weights_1x1, relevance_1x1, strides=conv_1x1.op.get_attr('strides'))

    def backprop_inception_pool(self, layer, activation_pool, relevance_1x1):
        conv_1x1 = self.get_parent(layer, 2)
        activation_1x1 = self.get_parent(layer, 3)
        weights_1x1 = self.get_parent(conv_1x1.op.inputs[1], 1)
        ksize = activation_1x1.op.get_attr('ksize')
        strides = activation_1x1.op.get_attr('strides')
        padding = activation_1x1.op.get_attr('padding')
        relevance_pool = self.backprop_conv(activation_1x1, weights_1x1, relevance_1x1)
        return self.backprop_avg_pool(activation_pool, relevance_pool, ksize = ksize, strides = strides, padding = padding)

    def backprop_conv_input(self, activation, weights, relevance, strides, padding='SAME', lowest=0., highest=1.):
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

    def run_relevances(self, relevances):
        result = self.sess.run(relevances)
        for r in range(len(result)):
            res = result[r]
            if(len(res.shape) >= 4):
                print(r, relevances[r].op.name, res.shape)
                res = res[0,:,:,:]
                #res = res[:,:,0] + res[:,:,1] + res[:,:,2]
                acti = np.sum(res, axis=2)
                acti /= acti.max()
                fig = plt.figure()
                ax = fig.add_subplot(111)
                ax.axis('off')
                ax.imshow(acti, cmap='Reds', interpolation='nearest')

                fig.savefig('static/images/temp/{0}_{1}.jpg'.format(r, np.sum(res)))
            else:
                print('-', relevances[r].op.name, result[r][0])
