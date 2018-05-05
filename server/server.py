import cv2
import numpy as np
import json
import io
import uuid
from flask import Flask, render_template, request, make_response, Response
from utilities.slim_network import Network
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
    layer_name = json.loads(request.data)['layer_name']
    result = pred_net.get_layer_activations(uploaded_image, layer_name)
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
    layer_name = json.loads(request.data)['layer_name']
    channel = json.loads(request.data)['channel']
    opt = (layer_name, channel)

    # parameters which can be used in the random transformation-graph
    pad = 16  # 16
    jitter = 8  # 8
    angles = list(range(-5, 5))  # (-5, 5)
    scales = np.arange(0.95, 1.1, 0.02, dtype='float32')  # (0.9, 1.1, 0.1)

    init_fn = init_network(network_name, 'visualize', pad=pad, jitter=jitter, rotate=angles, scale=scales, naive=False)
    net = Network(network_name, init_fn)
    filepaths = net.visualize(opt)
    return json.dumps(filepaths)

@app.route('/current_settings', methods=['GET'])
def current_settings():
    settings = {}
    settings['image_path'] = image_path
    settings['network_name'] = network_name
    return json.dumps(settings)

@app.route('/toast', methods=['GET'])
def toast():
    net.get_gradients('mixed3b')
    return 'hello'

if __name__ == '__main__':
    app.run()
