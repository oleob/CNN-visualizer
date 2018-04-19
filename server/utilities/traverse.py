import tensorflow as tf

def inception_v1(self, layer, relevances):
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

def vgg_16 (self, layer, relevances):
    return 'wooo'
