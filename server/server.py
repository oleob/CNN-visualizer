from flask import Flask, render_template, request, make_response, Response
import utilities.network as net
from utilities.cleaner import clear_temp_folder
import cv2
import numpy as np
import json
import io

clear_temp_folder()

app = Flask(__name__, static_folder='./static', template_folder='./static')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/activations', methods=['POST'])
def activations():
    layer_name = json.loads(request.data)['layer_name']
    filepaths = net.get_layer_activations(layer_name)
    return json.dumps({'filepaths': filepaths})

@app.route("/predict", methods=["POST"])
def predict():
    image = request.files['image']
    in_memory_file = io.BytesIO()
    image.save(in_memory_file)
    data = np.fromstring(in_memory_file.getvalue(), dtype=np.uint8)
    img = cv2.imdecode(data, 1)
    prediction = net.predict(img)
    return json.dumps(prediction)

@app.route('/toast', methods=['GET'])
def toast():
    net.get_gradients('mixed3b')
    return 'hello'

if __name__ == '__main__':
    app.run()
