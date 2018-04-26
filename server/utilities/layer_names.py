import tensorflow as tf

def inception_names(layer):
    names = []
    layer = layer.op.inputs[0]
    while not ('ExpandDims' in layer.name):
        #skip squeeze
        if 'SpatialSqueeze' in layer.name:
            layer = get_parent(layer, 1)
        #BiasAdd = end of convolution
        elif 'BiasAdd' in layer.name:
            activation = get_parent(layer, 3)
            names.append(create_name(layer))
            layer = activation
        #skip dropout
        elif 'Dropout' in layer.name:
            layer = get_parent(layer, 1)
        #AvgPool
        elif 'AvgPool' in layer.name:
            activation = get_parent(layer, 1)
            names.append(create_name(layer))
            layer = activation
        #end of inception module
        elif 'concat' in layer.name:
            activation = get_parent(layer, 4)
            names.append(create_name(layer))
            layer = activation
        #maxpool
        elif 'MaxPool' in layer.name:
            activation = get_parent(layer, 1)
            names.append(create_name(layer))
            layer = activation
        #end of concolution
        elif 'Relu' in layer.name:
            activation = get_parent(layer, 3)
            names.append(create_name(layer))
            layer = activation
        else:
            raise Exception('Unkown layer name: ' + str(layer.name))
    return names[::-1]

def vgg_16_names(layer):
    names = []
    layer = layer.op.inputs[0]
    while not ('ExpandDims' in layer.name):
        if 'squeezed' in layer.name:
            layer = get_parent(layer, 1)
        elif 'BiasAdd' in layer.name:
            activation = get_parent(layer, 2)
            names.append(create_name(layer))
            layer = activation
        elif 'dropout' in layer.name:
            layer = get_parent(layer, 1)
        elif 'Relu' in layer.name:
            activation = get_parent(layer, 3)
            names.append(create_name(layer))
            layer = activation
        elif 'MaxPool' in layer.name:
            activation = get_parent(layer, 1)
            names.append(create_name(layer))
            layer = activation
        else:
            raise Exception('Unkown layer name: ' + str(layer.name))
    return names[::-1]

def create_name(layer):
    name = {}
    name['name'] = layer.name.split('/')[-2]
    name['id'] = layer.name
    return name

def get_parent(child, num_skips):
    parent = child
    for i in range(num_skips):
        parent = [inp for inp in parent.op.inputs if not (inp.op.type=='Const')][0]
    return parent
