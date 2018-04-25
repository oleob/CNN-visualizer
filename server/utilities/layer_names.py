import tensorflow as tf

def inception_names(layer):
    names = []
    conv_count = 0
    inception_count = 0
    max_pool_count = 0
    avg_pool_count = 0
    layer = layer.op.inputs[0]
    while not ('ExpandDims' in layer.name):
        #skip squeeze
        if 'SpatialSqueeze' in layer.name:
            layer = get_parent(layer, 1)
        #BiasAdd = end of convolution
        elif 'BiasAdd' in layer.name:
            activation = get_parent(layer, 3)
            names.append(create_name(layer, 'Conv:', conv_count))
            conv_count += 1
            layer = activation
        #skip dropout
        elif 'Dropout' in layer.name:
            layer = get_parent(layer, 1)
        #AvgPool
        elif 'AvgPool' in layer.name:
            activation = get_parent(layer, 1)
            names.append(create_name(layer, 'AvgPool:', avg_pool_count))
            avg_pool_count += 1
            layer = activation
        #end of inception module
        elif 'concat' in layer.name:
            activation = get_parent(layer, 4)
            names.append(create_name(layer, 'Inception:', inception_count))
            inception_count += 1
            layer = activation
        #maxpool
        elif 'MaxPool' in layer.name:
            activation = get_parent(layer, 1)
            names.append(create_name(layer, 'MaxPool:', max_pool_count))
            max_pool_count += 1
            layer = activation
        #end of concolution
        elif 'Relu' in layer.name:
            activation = get_parent(layer, 3)
            names.append(create_name(layer, 'Conv:', conv_count))
            conv_count += 1
            layer = activation
    return names[::-1]

def create_name(layer, type, count):
    name = {}
    name['name'] = layer.name.split('/')[-2]
    name['id'] = layer.name
    return name

def get_parent(child, num_skips):
    parent = child
    for i in range(num_skips):
        parent = [inp for inp in parent.op.inputs if not (inp.op.type=='Const')][0]
    return parent
