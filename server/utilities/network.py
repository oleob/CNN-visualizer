import tensorflow as tf
import numpy as np

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

    result = {}
    for x in range(20):
        result[sorted_labels[x][1]] = round(float(sorted_labels[x][0]), 4)
    return result

def init():
    model_path = './models/tensorflow_inception_graph.pb'
    load_model(model_path)

sess = tf.Session()
labels = open('./models/inception_labels.txt').read().split('\n')
init()
#get output layer
output_layer = sess.graph.get_tensor_by_name('output2:0')
