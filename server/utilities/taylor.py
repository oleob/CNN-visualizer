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
        img = cv2.imread('./static/images/dog-horse.jpg',1)
        self.img = cv2.resize(img, (224,224))
        self.output_layer = sess.graph.get_tensor_by_name('output2:0')
        self.new_output = tf.placeholder(tf.float32, self.output_layer.shape)
        self.labels = labels = open('./models/inception_labels.txt').read().split('\n')

    def __call__(self):
        #get values of output_layer
        # get softmax_gradients
        #output_node = tf.slice(output_layer, [0, np.argmax(units)], [1, 1])
        #print(self.sess.run(output, feed_dict={"input:0":[self.img]})[0])
        relevance = [self.new_output]
        #relevance = [self.output_layer]
        layer = self.output_layer.op.inputs[0]
        while not (layer.op.name=='input'):
            with tf.variable_scope(layer.op.name + '_taylor'):
                if 'softmax' in layer.op.name:
                    weights = self.graph.get_tensor_by_name(layer.op.name + '_w:0')
                    activation = self.get_parent(layer, 3)
                    relevance.extend(self.backprop_dense(activation, weights, relevance[-1]))
                    print(layer.op.name, activation.op.name)
                    layer = activation
                    #break
                elif 'avgpool0/reshape' in layer.op.name:
                    relevance.append(tf.reshape(relevance[-1], (-1, 1, 1, 1024)))
                    layer = self.get_parent(layer, 1)
                elif 'avgpool' in layer.op.name:
                    activation = self.get_parent(layer, 1)
                    relevance.append(self.backprop_avg_pool(activation, relevance[-1]))
                    layer = activation
                elif 'mixed' in layer.op.name:
                    print(layer.op.name, activation.op.name)
                    activation = self.get_parent(layer, 4)
                    relevance.append(self.backprop_inception(activation, layer, relevance[-1]))
                    #print(layer.op.name, activation.op.name)
                    layer = activation
                elif 'maxpool' in layer.op.name:
                    activation = self.get_parent(layer, 1)
                    relevance.append(self.backprop_max_pool(activation, relevance[-1]))
                    print(layer.op.name, activation.op.name)
                    layer = activation
                elif 'localresponsenorm' in layer.op.name:
                    layer = self.get_parent(layer, 1)
                elif 'conv2d0' in layer.op.name:
                    weights = self.graph.get_tensor_by_name(layer.op.name + '_w:0')
                    activation = self.get_parent(layer, 3)
                    print(layer.op.name, activation.op.name)
                    relevance.append(self.backprop_conv(activation, weights, relevance[-1], strides=[1, 2, 2, 1]))
                    #relevance.append(self.backprop_conv_input(activation, weights, relevance[-1]))
                    layer = activation
                elif 'conv' in layer.op.name:
                    weights = self.graph.get_tensor_by_name(layer.op.name + '_w:0')
                    activation = self.get_parent(layer, 3)
                    print(layer.op.name, activation.op.name)
                    relevance.append(self.backprop_conv(activation, weights, relevance[-1]))
                    layer = activation
                else:
                    print(layer.shape, [inp.op for inp in layer.op.inputs if not (inp.op.type=='Const')])
                    break

        return relevance

    def get_parent(self, child, num_skips):
        parent = child
        for i in range(num_skips):
            parent = [inp for inp in parent.op.inputs if not (inp.op.type=='Const')][0]
        return parent

    def backprop_inception(self, activation, layer, relevance):
        name = layer.op.name
        inputs = [inp for inp in layer.op.inputs if not (inp.op.type=='Const')]
        split_dim = [int(inputs[0].shape[3]), int(inputs[1].shape[3]), int(inputs[2].shape[3]), int(inputs[3].shape[3])]

        r_1, r_3, r_5, r_p = tf.split(relevance, split_dim, axis=3)
        r_1x1 = self.backprop_1x1(activation, name, r_1)
        r_3x3 = self.backprop_3x3(activation, name, r_3)
        r_5x5 = self.backprop_5x5(activation, name, r_5)
        r_pool = self.backprop_inception_max_pool(activation, name, r_p)
        new_relevance = (r_1x1 + r_3x3 + r_5x5 + r_pool)
        return new_relevance

    def backprop_dense(self, activation, weights, relevance):
        w_pos = tf.maximum(0.0, weights)
        z = tf.matmul(activation, w_pos) + self.epsilon
        s = relevance / z
        c = tf.matmul(s, tf.transpose(w_pos))
        return [c * activation]

    def backprop_max_pool(self, activation, relevance, ksize=[1, 3, 3, 1], strides=[1, 2, 2, 1]):
        z = tf.nn.max_pool(activation, ksize, strides, padding='SAME') + self.epsilon
        #z = nn_ops.avg_pool(activation, ksize, strides, padding='SAME') + self.epsilon
        s = relevance / z
        #c = gen_nn_ops._avg_pool_grad(tf.shape(activation), s, ksize, strides, padding='SAME')
        c = gen_nn_ops.max_pool_grad_v2(activation, z, s, ksize, strides, padding='SAME')
        return activation * c

    def backprop_inception_max_pool(self, activation, name, relevance, ksize=[1, 3, 3, 1], strides=[1, 1, 1, 1]):
        activation1 = self.graph.get_tensor_by_name(name + '_pool:0')
        activation2 = activation
        weights = self.graph.get_tensor_by_name(name + '_pool_reduce_w:0')

        new_relevance = self.backprop_conv(activation1, weights, relevance)

        z = tf.nn.max_pool(activation2, ksize, strides, padding='SAME') + self.epsilon
        #z = nn_ops.avg_pool(activation2, ksize, strides, padding='SAME') + self.epsilon
        s = new_relevance / z
        c = gen_nn_ops.max_pool_grad_v2(activation2, z, s, ksize, strides, padding='SAME')
        #c = gen_nn_ops._avg_pool_grad(tf.shape(activation2), s, ksize, strides, padding='SAME')
        return c * activation2

    def backprop_avg_pool(self, activation, relevance, ksize=[1, 7, 7, 1], strides=[1, 1, 1, 1]):
        z = tf.nn.avg_pool(activation, ksize, strides, padding='VALID') + self.epsilon
        s = relevance / z
        c = gen_nn_ops._avg_pool_grad(tf.shape(activation), s, ksize, strides, padding='VALID')
        return c * activation

    def backprop_conv(self, activation, weights, relevance, strides=[1, 1, 1, 1], padding='SAME'):
        w_pos = tf.maximum(0., weights)
        z = tf.nn.conv2d(activation, w_pos, strides, padding='SAME') + self.epsilon
        s = relevance / z
        c = gen_nn_ops.conv2d_backprop_input(tf.shape(activation), w_pos, s, strides, padding)
        return activation * c


    def backprop_1x1(self, activation, name, relevance):
        weights = self.graph.get_tensor_by_name(name + '_1x1_w:0')
        weights1 = self.graph.get_tensor_by_name(name + '_3x3_w:0')
        weights2 = self.graph.get_tensor_by_name(name + '_5x5_w:0')

        return self.backprop_conv(activation, weights, relevance)

    def backprop_3x3(self, activation, name, relevance):
        activation1 = self.graph.get_tensor_by_name(name + '_3x3_bottleneck:0')
        activation2 = activation
        weights1 = self.graph.get_tensor_by_name(name + '_3x3_w:0')
        weights2 = self.graph.get_tensor_by_name(name + '_3x3_bottleneck_w:0')
        new_relevance = self.backprop_conv(activation1, weights1, relevance)
        return self.backprop_conv(activation2, weights2, new_relevance)

    def backprop_5x5(self, activation, name, relevance):
        activation1 = self.graph.get_tensor_by_name(name + '_5x5_bottleneck:0')
        activation2 = activation
        weights1 = self.graph.get_tensor_by_name(name + '_5x5_w:0')
        weights2 = self.graph.get_tensor_by_name(name + '_5x5_bottleneck_w:0')
        new_relevance = self.backprop_conv(activation1, weights1, relevance)
        return self.backprop_conv(activation2, weights2, new_relevance)

    def backprop_conv_input(self, activation, weights, relevance, strides=[1, 2, 2, 1], padding='SAME', lowest=0., highest=1.):
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

    def run(self, relevance):

        output_values = np.zeros(int(self.output_layer.shape[1]))
        units = self.sess.run(self.output_layer, feed_dict={"input:0":[self.img]})[0]
        sorted_labels = []
        for i in range(len(self.labels)):
            sorted_labels.append((units[i], self.labels[i], i))
        #sort tuples on highest Probability
        sorted_labels = sorted(sorted_labels,reverse=True,key=lambda tup: tup[0])
        for i in range(20):
            print(sorted_labels[i])
        output_values[sorted_labels[0][2]] = 1

        result = self.sess.run(relevance, feed_dict={"input:0":[self.img], self.new_output: [output_values]})
        for r in range(len(result)):
            res = result[r]
            if(len(res.shape) >= 4):
                print(r, relevance[r].op.name, res.shape)
                res = res[0,:,:,:]
                #res = res[:,:,0] + res[:,:,1] + res[:,:,2]
                res = np.sum(res, axis=2)
                acti = res
                acti /= acti.max()
                fig = plt.figure()
                ax = fig.add_subplot(111)
                ax.axis('off')
                ax.imshow(acti, cmap='Reds', interpolation='nearest')

                fig.savefig('static/images/temp/{0}.jpg'.format(r))
            else:
                print('-', relevance[r].op.name, res[0])
            # acti = cv2.resize(acti, (224,224), interpolation=0)
            # r,g,b = cv2.split(self.img)
            # r = r*acti
            # g = g*acti
            # b = b*acti
            # newImg = cv2.merge((r,g,b))
            # cv2.imwrite('static/images/temp/' + str(su) + '.jpg', newImg)

    def print_layers(self):
        layer = self.output_layer
        while not (layer.op.name == 'input'):
            print(layer.op.name)
            layer = self.get_parent(layer, 1)

def test(sess):
    taylor = Taylor(sess)
    taylor.print_layers()
    relevance = taylor()
    taylor.run(relevance)

def print_names():
    operations = tf.get_default_graph().get_operations()
    for op in operations:
        print(op.name)

def print_layers(sess):
    output_layer = sess.graph.get_tensor_by_name('output2:0')
    node_names = [inp.op.name for inp in output_layer.op.inputs]
    visited = []
    nodes = [output_layer]
    nodes.extend([inp for inp in output_layer.op.inputs])
    while len(nodes) > 0:
        layer = nodes.pop(0)
        if 'mixed' in layer.op.name:
            print (layer.op.name , [inp.op for inp in layer.op.inputs])
            # conv_1x1 = layer.inputs[1].op.inputs[0].op.inputs[0].op
            # conv_3x3 = layer.inputs[2].op
            # conv_5x5 = layer.inputs[3].op
            # pool = layer.inputs[4].op
            #print(layer.name, [conv_1x1, backprop_3x3(conv_3x3), conv_5x5, pool])
        else:
            inputs = [inp for inp in layer.op.inputs]
            print(layer.op.name, [inp.op for inp in layer.op.inputs])
            visited.append(layer.op.name)
            for inp in inputs:
                if (not inp.op.name in node_names) and (not inp.op.type=='Const'):
                    nodes.append(inp)
                    node_names.append(inp.op.name)
