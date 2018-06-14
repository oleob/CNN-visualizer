import cv2
import numpy as np
import json
import io
import uuid
import tensorflow as tf
import os
import time
import random
from flask import Flask, render_template, request, make_response, Response
from utilities.slim_network import Network, VisNetwork
from utilities.cleaner import clear_temp_folder
from utilities.network_initializer import init_network

clear_temp_folder()
network_name = 'InceptionV1'
app = Flask(__name__, static_folder='./static', template_folder='./static')
pred_net = None
image_path = './static/images/penguins3.jpeg'
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

    layer_name = json.loads(request.data)['layer_name'] + ":0"
    channel = int(json.loads(request.data)['channel'])

    image_patches = []
    patch_dim = 64
    patches_per_img = 30
    init_fn = init_network(network_name, 'predict_multiple')
    pred_net = Network(network_name, init_fn, False)
    paths = []
    print("loading imagenet..")
    i = 0
    for subdir, dirs, files in os.walk('./static/test'):
        for file in files:
            if file.endswith('.JPEG'):
                print(i)
                i += 1
                path = subdir + os.sep + file
                image = cv2.imread(path, 1)
                width, height = len(image), len(image[0])
                for _ in range(patches_per_img):
                    x_start = random.randint(0, width-patch_dim)
                    x_end = x_start + patch_dim
                    y_start = random.randint(0, height-patch_dim)
                    y_end = y_start + patch_dim
                    patch = image[x_start:x_end, y_start:y_end, :]
                    image_patches.append(patch)

    print("..loading complete,", len(image_patches), "loaded")
    start_time = time.time()
    batch_size = 1000
    # TODO: fix timeout bug
    num_batches = int(len(image_patches) / batch_size)
    results = []
    for i in range(num_batches):
        batch = image_patches[i * batch_size:(i + 1) * batch_size]
        results = results + pred_net.predict_multiple(batch, layer_name, channel)
        print("batch", i, "/", num_batches, "complete")

    image_patches = image_patches[:len(results)]
    patch_value = zip(image_patches, results)
    patch_value_sorted = sorted(patch_value, key=lambda x: x[1])
    patch_value_sorted.reverse()
    patches = [item[0] for item in patch_value_sorted][:100]
    activation_values = [item[1] for item in patch_value_sorted][:100]
    duration = time.time() - start_time
    print("prediction complete\ttime:", duration)

    # save the images (for testing purposes), until the timeout-bug is fixed
    import PIL.Image
    for i in range(len(patches)):
        img = PIL.Image.fromarray(patches[i])
        val = str(round(activation_values[i], 2))
        img.save('static/images/temp/' + 'tiny_img' + str(i) + "_" + val + '.jpg', "JPEG")

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

    layer_name = json.loads(request.data)['layer_name'] + ":0"
    channel = json.loads(request.data)['channel']
    mix = json.loads(request.data)['mix']
    decorrelate_colors = json.loads(request.data)['decorrelate']

    if channel == '':
        channel_list = [None]
    elif isinstance(channel, int):
        channel_list = [channel]
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
    scale = float(json.loads(request.data)['scale'])
    if scale == 0:
        scales = None
    else:
        lower_scale, upper_scale = max(0.1, 1.0 - scale), 1.0 + scale
        scales = np.arange(lower_scale, upper_scale, 0.01, dtype='float32')

    param_space = json.loads(request.data)['param_space']

    init_fn = init_network(network_name, 'visualize', param_space=param_space, x_dim=dim, y_dim=dim,
                           pad=pad, jitter=jitter, rotate=angles, scale=scales, decorrelate_colors=decorrelate_colors)
    net = VisNetwork(init_fn)

    steps = int(json.loads(request.data)['steps'])
    lr = float(json.loads(request.data)['lr'])

    print(opt_list)

    filepaths = net.visualize(opt_list, steps=steps, lr=lr)
    return json.dumps({'filepaths': filepaths})

@app.route('/deep_dream', methods=['POST'])
def deep_dream():

    print(request.data)

    layer_name = json.loads(request.data)['layer_name'] + ":0"
    channel = json.loads(request.data)['channel']

    mix = False
    decorrelate_colors = json.loads(request.data)['decorrelate']

    if channel == '':
        channel_list = [None]
    elif isinstance(channel, int):
        channel_list = [channel]
    elif "," in channel:
        channel_list = channel.split(",")
        channel_list = [int(ch) for ch in channel_list]
        mix = True
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
    scale = float(json.loads(request.data)['scale'])
    if scale == 0:
        scales = None
    else:
        lower_scale, upper_scale = 1.0 - scale, 1.0 + scale
        scales = np.arange(lower_scale, upper_scale, 0.01, dtype='float32')

    param_space = 'naive'
    print(scales)

    dream_img = cv2.cvtColor(uploaded_image, cv2.COLOR_RGB2BGR)
    pad_dims = ((pad, pad), (pad, pad), (0, 0))
    dream_img = np.pad(dream_img, pad_width=pad_dims, mode='constant', constant_values=127)


    init_fn = init_network(network_name, 'visualize', param_space=param_space, x_dim=dim, y_dim=dim,
                           pad=pad, jitter=jitter, rotate=angles, scale=scales,
                           dream_img=dream_img, decorrelate_colors=decorrelate_colors)
    net = VisNetwork(init_fn)

    steps = int(json.loads(request.data)['steps'])
    lr = float(json.loads(request.data)['lr'])

    print(opt_list)

    filepaths = net.visualize(opt_list, steps=steps, lr=lr)
    return json.dumps({'filepaths': filepaths})

@app.route('/current_settings', methods=['GET'])
def current_settings():
    settings = {}
    settings['image_path'] = image_path
    settings['network_name'] = network_name
    return json.dumps(settings)

@app.route('/all_activations', methods=['GET'])
def all_activations():
    init_pred_net()
    layers = json.loads(toast())['layers']
    pred_net.get_all_activations(uploaded_image, layers, 10)
    return('Done')

@app.route('/layer_info', methods=['GET'])
def toast():
    init_pred_net()
    ops = tf.get_default_graph().get_operations()
    rel_ops = []
    for op in ops:
        if not ('_taylor' in op.name) and ('Conv2D' in op.name or 'Relu' in op.name or 'BiasAdd' in op.name or (str(op.name).endswith('concat') and len(op.name)>6) or 'Pool' in op.name):
            rel_ops.append(op)
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
            split = op.name.split('/')
            if 'Mixed' in op.name:
                info['name'] = split[-4] + ':'+ split[-3] +':' + split[-2]
            else:
                info['name'] = split[-2]
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
            split = op.name.split('/')
            if 'Mixed' in op.name:
                info['name'] = split[-4] + ':' + split[-2]
            else:
                info['name'] = split[-2]
            info['size'] = str(op.get_attr('ksize'))
            info['strides'] = str(op.get_attr('strides'))
            info['shape'] = str(tf.get_default_graph().get_tensor_by_name(op.name + ':0').shape)
            layer['info'] = info
            increment = 1
        else:
            layer = {}
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
