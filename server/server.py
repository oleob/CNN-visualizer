from flask import Flask, render_template, request, make_response, Response
from utilities.slim_network import Network
from utilities.cleaner import clear_temp_folder
import cv2
import numpy as np
import json
import io

clear_temp_folder()

app = Flask(__name__, static_folder='./static', template_folder='./static')
net = Network('InceptionV1', add_vis_graph=True, naive=False, x_dim=200, y_dim=200)
#net = Network('vgg_16', add_vis_graph=True, naive=False)

@app.route('/activations', methods=['POST'])
def activations():
    layer_name = json.loads(request.data)['layer_name']
    filepaths = net.get_layer_activations(layer_name)
    return json.dumps({'filepaths': filepaths})

@app.route('/deep_taylor', methods=['POST'])
def deep_taylor():
    filepaths = net.get_deep_taylor()
    return json.dumps({'filepaths': filepaths})

@app.route("/predict", methods=["POST"])
def predict():
    image = request.files['image']
    in_memory_file = io.BytesIO()
    image.save(in_memory_file)
    data = np.fromstring(in_memory_file.getvalue(), dtype=np.uint8)
    img = cv2.imdecode(data, 1)
    prediction = net.predict(img, 5, False) #TODO replace 5 with number from call
    return json.dumps(prediction)

@app.route('/change_settings', methods=['POST'])
def change_settings():
    network_name = json.loads(request.data)['network_name']
    global net
    net = Network(network_name)
    return json.dumps({'status': 'ok'})

@app.route('/layer_names', methods=['GET'])
def layer_names():
    return json.dumps({'names' : net.get_layer_names()})

@app.route('/visualize', methods=['POST'])
def visualize():
    layer_name = json.loads(request.data)['layer_name']
    channel = json.loads(request.data)['channel']
    opt = (layer_name, channel)
    filepaths = net.visualize(opt)
    return json.dumps(filepaths)

@app.route('/toast', methods=['GET'])
def toast():
    net.get_gradients('mixed3b')
    return 'hello'

if __name__ == '__main__':
    app.run()
