import tensorflow as tf
import numpy as np
import cv2
import uuid

def load_model(model_path):
    with tf.gfile.FastGFile(model_path, 'rb') as f:
        graph_def = tf.GraphDef()
        graph_def.ParseFromString(f.read())
        tf.import_graph_def(graph_def, name='')

def predict(img):
    #calculate the score for each class
    units = np.round(np.mean(sess.run(output_layer, feed_dict={"input:0":[img]}), axis=0),decimals = 3)
    #get all labels
    sorted_labels = []
    #add labels to values
    for i in range(len(labels)):
        sorted_labels.append((units[i], labels[i]))
    #sort tuples on highest Probability
    sorted_labels = sorted(sorted_labels,reverse=True,key=lambda tup: tup[0])

    result = []
    for x in range(20):
        item = {}
        item['name'] = sorted_labels[x][1]
        item['value'] = round(float(sorted_labels[x][0]), 4)
        result.append(item)
    return result

def init():
    model_path = './models/tensorflow_inception_graph.pb'
    load_model(model_path)

sess = tf.Session()
labels = open('./models/inception_labels.txt').read().split('\n')
init()
#get output layer
output_layer = sess.graph.get_tensor_by_name('output2:0')

def get_layer_activations(layer_name):
    img = cv2.imread('./static/images/penguins3.jpg',1)
    #Get the tensor by name
    tensor = sess.graph.get_tensor_by_name(layer_name + ':0')
    #Run the tensor with the image as input
    units = sess.run(tensor,feed_dict={"input:0":[img]})
    filters = units[0,:,:,:]
    filter_size = units.shape[3]
    width = units.shape[1]
    height = units.shape[2]
    n_columns = 13
    n_rows = 10

    sorted_filters = list()
    for i in range(filter_size):
        fi = filters[:,:,i]
        sorted_filters.append((fi.sum(),i,fi))
    sorted_filters = sorted(sorted_filters, reverse=True, key=lambda tup: tup[0])
    filepaths = []
    for i in range(20):
        filter_tuple = sorted_filters[i]
        print(filter_tuple[0])
        activation = filter_tuple[2]/filter_tuple[2].max()
        height, width, channels = img.shape
        activation = cv2.resize(activation,(width, height), interpolation=0)
        r,g,b = cv2.split(img)
        r = r*activation
        g = g*activation
        b = b*activation
        newImg = cv2.merge((r,g,b))

        filepath = 'static/images/temp/'+ str(uuid.uuid4()) + '.jpg'
        cv2.imwrite(filepath, newImg)
        filepaths.append(filepath)
    return filepaths
