import tensorflow as tf
import numpy as np
import cv2
import uuid
import utilities.taylor as taylor

def load_model(model_path):
    with tf.gfile.FastGFile(model_path, 'rb') as f:
        graph_def = tf.GraphDef()
        graph_def.ParseFromString(f.read())
        tf.import_graph_def(graph_def, name='')

def predict(img):
    #resize image
    img = cv2.resize(img, (224,224))
    #calculate the score for each class
    units = sess.run(output_layer, feed_dict={"input:0":[img]})[0]
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
input_layer = sess.graph.get_tensor_by_name('input:0')
def get_layer_activations(layer_name):
    #load image
    img = cv2.imread('./static/images/penguins3.jpg',1)
    img = cv2.resize(img, (224,224))
    #Get the tensor by name
    tensor = sess.graph.get_tensor_by_name(layer_name + ':0')
    #predict
    units = sess.run(output_layer, feed_dict={"input:0":[img]})[0]
    # get softmax_gradients
    node = tf.slice(output_layer, [0, np.argmax(units)], [1, 1])

    #create gradient graph
    grad = tf.gradients(node, tensor)
    #Run the tensor and gradient with the image as input

    units, gradients = sess.run([tensor,grad],feed_dict={"input:0":[img]})
    #format gradients
    gradients = gradients[0][0]
    #format the filters
    filters = units[0,:,:,:]
    filter_size = units.shape[3]
    width = units.shape[1]
    height = units.shape[2]
    n_columns = 13
    n_rows = 10

    sorted_filters = list()
    for i in range(filter_size):
        fi = filters[:,:,i]
        gr = np.array(gradients[:,:,i]).flatten()
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

def get_gradients(layer_name):
    img = cv2.imread('./static/images/penguins3.jpg',1)
    tensor = sess.graph.get_tensor_by_name(layer_name + ':0')


    print(np.array(sess.run(grad, feed_dict={"input:0":[img]})).shape)

def print_layers():
    #taylor.print_names()
    taylor.test(sess)

def deep_taylor():
    layers = ['softmax2', 'softmax2_pre_activation/matmul', ]
    graph = tf.get_default_graph()
    tensor = graph.get_tensor_by_name('mixed3a_3x3_bottleneck_pre_relu/conv:0')
    w = graph.get_tensor_by_name('mixed3a_3x3_bottleneck_w:0').eval(session=sess)
    for n in graph.get_operations():
        print(n.name, set(inp.op for inp in n.inputs))

def get_lrp():
    #load image
    img = cv2.imread('./static/images/tinydog.jpg',1)
    #img = cv2.resize(img, (224,224))
    #predict
    units = sess.run(output_layer, feed_dict={"input:0":[img]})[0]
    # get softmax_gradients
    node = tf.slice(output_layer, [0, np.argmax(units)], [1, 1])
    scores = input_layer*tf.gradients(node,input_layer)
    lrp = sess.run(scores, feed_dict={"input:0":[img]})[0][0]
    lrp = lrp[:,:,0] + lrp[:,:,1] + lrp[:,:,2]
    lrp = lrp/lrp.max()
    r,g,b = cv2.split(img)
    r = r*lrp
    g = g*lrp
    b = b*lrp
    newImg = cv2.merge((r,g,b))
    cv2.imwrite('static/images/temp/lrp.jpg', newImg)
