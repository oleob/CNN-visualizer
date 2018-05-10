import cv2
import numpy as np
import json
import io
import uuid
import tensorflow as tf
import os
import time
import operator
from flask import Flask, render_template, request, make_response, Response
from utilities.slim_network import Network, VisNetwork
from utilities.cleaner import clear_temp_folder
from utilities.network_initializer import init_network

clear_temp_folder()
network_name = 'InceptionV1'
app = Flask(__name__, static_folder='./static', template_folder='./static')
pred_net = None
image_path = './static/images/penguins3.jpg'
uploaded_image = cv2.imread(image_path,1)

def init_pred_net():
    global pred_net
    if pred_net is None:
        init_fn = init_network(network_name, 'predict')
        pred_net = Network(network_name, init_fn)


@app.route('/activations', methods=['POST'])
def activations():
    init_pred_net()
    data = json.loads(request.data)
    layer_name = data['layer_name']
    num_activations = int(data['num_activations'])
    result = pred_net.get_layer_activations(uploaded_image, layer_name, num_activations, False)
    return json.dumps({'result': result})

@app.route('/deep_taylor', methods=['POST'])
def deep_taylor():
    init_pred_net()
    num_filters = int(json.loads(request.data)['num_filters'])
    results = pred_net.get_deep_taylor(uploaded_image, num_filters)
    return json.dumps({'results': results})

@app.route('/upload_image', methods=['POST'])
def upload_image():
    img = request.files['image']
    in_memory_file = io.BytesIO()
    img.save(in_memory_file)
    data = np.fromstring(in_memory_file.getvalue(), dtype=np.uint8)
    img = cv2.imdecode(data, 1)
    global uploaded_image
    uploaded_image = img
    filepath = 'static/images/temp/'+ str(uuid.uuid4()) + '.jpg'
    cv2.imwrite(filepath, img)
    global image_path
    image_path = filepath
    return json.dumps({'status': 'ok', 'image_path': filepath})

@app.route("/predict", methods=['GET'])
def predict():
    init_pred_net()
    prediction = pred_net.predict(uploaded_image, 5, False) #TODO replace 5 with number from call
    return json.dumps(prediction)

@app.route('/predict_multiple', methods=['POST'])
def predict_multiple():

    layer_name = json.loads(request.data)['layer_name']
    channel = int(json.loads(request.data)['channel'])

    images = []
    init_fn = init_network(network_name, 'predict_multiple')
    pred_net = Network(network_name, init_fn, False)
    paths = []
    print("loading imagenet..")
    for subdir, dirs, files in os.walk('./static/valid_64x64'):
        for file in files:
            if file.endswith('.png'):
                path = subdir + os.sep + file
                paths.append(path)
                image = cv2.imread(path, 1)
                images.append(image)
    print("..loading complete")
    start_time = time.time()
    batch_size = 1000
    num_batches = 15  #int(50000/batch_size)
    results = []
    for i in range(num_batches):
        batch = images[i * batch_size:(i + 1) * batch_size]
        results = results + pred_net.predict_multiple(batch, layer_name, channel)
        print("batch", i, "/", num_batches, "complete")
    path_value = dict(zip(paths, results))
    path_value_sorted = sorted(path_value.items(), key=operator.itemgetter(1))
    path_value_sorted.reverse()
    paths = [item[0] for item in path_value_sorted][:10]
    duration = time.time() - start_time
    print("prediction complete\ttime:", duration)

    return json.dumps({'filepaths': paths})

@app.route('/change_settings', methods=['POST'])
def change_settings():
    global network_name
    global pred_net
    network_name = json.loads(request.data)['network_name']
    pred_net = None
    return json.dumps({'status': 'ok'})

@app.route('/layer_names', methods=['GET'])
def layer_names():
    init_pred_net()
    return json.dumps({'names' : pred_net.get_layer_names()})

@app.route('/visualize', methods=['POST'])
def visualize():

    print(request.data)

    layer_name = json.loads(request.data)['layer_name']
    channel = json.loads(request.data)['channel']
    mix = json.loads(request.data)['mix']

    if channel == '':
        channel_list = [None]
    elif "," in channel:
        channel_list = channel.split(",")
        channel_list = [int(ch) for ch in channel_list]
    else:
        channel_list = [int(channel)]

    opt_list = []
    for ch in channel_list:
        if mix:
            opt = (layer_name, ch, 1)
        else:
            opt = (layer_name, ch)
        opt_list.append(opt)

    dim = int(json.loads(request.data)['dim'])

    # TODO: find a way to pad only the minimal required amount
    pad = int(json.loads(request.data)['pad'])
    jitter = int(json.loads(request.data)['jitter'])
    angle = int(json.loads(request.data)['rotation'])
    angles = list(range(-angle, angle)) or None
    scales = np.arange(0.95, 1.1, 0.02, dtype='float32')  # (0.9, 1.1, 0.1)

    param_space = json.loads(request.data)['param_space']
    naive = True if param_space == 'naive' else False

    init_fn = init_network(network_name, 'visualize', x_dim=dim, y_dim=dim, pad=pad, jitter=jitter, rotate=angles, scale=None, naive=naive)
    net = VisNetwork(init_fn)

    steps = int(json.loads(request.data)['steps'])
    lr = float(json.loads(request.data)['lr'])

    print(opt_list)

    filepaths = net.visualize(opt_list, steps=steps, lr=lr, naive=naive)
    return json.dumps({'filepaths': filepaths})

@app.route('/current_settings', methods=['GET'])
def current_settings():
    settings = {}
    settings['image_path'] = image_path
    settings['network_name'] = network_name
    return json.dumps(settings)

@app.route('/layer_info', methods=['GET'])
def toast():
    init_pred_net()
    ops = tf.get_default_graph().get_operations()
    rel_ops = []
    for op in ops:
        if not ('_taylor' in op.name) and ('Conv2D' in op.name or 'Relu' in op.name or 'BiasAdd' in op.name or (str(op.name).endswith('concat') and len(op.name)>6) or 'Pool' in op.name):
            rel_ops.append(op)
    for o in rel_ops:
        print(o.name)
    layers = []
    i = 0
    def make_layer(op, i):
        layer = {}
        if 'Conv2D' in op.name:
            j = 1
            while i + j < len(rel_ops):
                if 'Relu' in rel_ops[i+j].name or (i+j+1 == len(rel_ops)):
                    layer['output'] = rel_ops[i+1].name
                    break
                else:
                    j += 1

            info = {}
            info['name'] = op.name.split('/')[-2]
            info['operation'] = 'Convolution'
            info['padding'] = str(op.get_attr('padding'))
            info['strides'] = str(op.get_attr('strides'))
            info['filter_dimensions'] = str(op.inputs[1].shape)
            info['shape'] = str(tf.get_default_graph().get_tensor_by_name(op.name + ':0').shape)

            layer['info'] = info
            increment = j + 1
        elif 'Pool' in op.name:
            layer['output'] = op.name
            if 'MaxPool' in op.name:
                layer['operation'] = 'Max Pool'
            else:
                layer['operation'] = 'Average Pool'

            info = {}
            info['name'] = op.name.split('/')[-2]
            info['size'] = str(op.get_attr('ksize'))
            info['strides'] = str(op.get_attr('strides'))
            info['shape'] = str(tf.get_default_graph().get_tensor_by_name(op.name + ':0').shape)
            layer['info'] = info
            increment = 1
        return layer, increment
    children = []
    while i < len(rel_ops):
        op = rel_ops[i]
        if 'concat' in op.name:
            layer = {}
            layer['output'] = op.name
            layer['children'] = children
            layer['info'] = {'name': op.name.split('/')[-2], 'operation': 'Inception'}
            children = []
            i += 1
            layers.append(layer)
        else:
            layer, increment = make_layer(op, i)
            if 'Mixed' in op.name:
                children.append(layer)
            else:
                layers.append(layer)
            i += increment

    return(json.dumps({'layers': layers}))
if __name__ == '__main__':
    app.run()
