
""" This file contains functions for visualizing different parts of a CNN, in
addition to some other ones related to visualization """

import tensorflow as tf
import time
import os
#os.environ["CUDA_VISIBLE_DEVICES"]="-1"
import uuid

from tensorflow.contrib import slim

import utilities.feature_vis.graph_builder as graph_builder
import utilities.feature_vis.misc as misc



def visualize_features(opt, init_fn, steps=200, lr=0.06, optimizer=None, save_run=False):

    num_visualizations = 1
    mix = False
    if isinstance(opt, list):
        num_visualizations = len(opt)
        if len(opt[0]) == 3:
            mix = True
            num_visualizations = 1
        elif num_visualizations == 1:
            opt = opt[0]

    # start the session
    with tf.Session() as sess:

        graph = tf.get_default_graph()

        # for op in graph.get_operations():
        #     print(op.name)

        # select tensors that we might want to access later
        image_tensor = graph.get_tensor_by_name('image:0')
        trans_tensor = graph.get_tensor_by_name('transformed:0')


        # create the optimizer to the graph
        optimizer = optimizer or tf.train.AdamOptimizer(learning_rate=lr)

        # tensorboard stuff ..uncomment to take a look at the graph
        # logdir = "tensorboard/"
        # writer = tf.summary.FileWriter(logdir, graph)
        # tf.summary.merge_all()

        # initialize all weights in the pre-trained network
        init_fn(sess)

        # train the network to optimize the image(s)
        start_time = time.time()
        filepaths = []
        for n in range(num_visualizations):

            # create the loss function
            if num_visualizations > 1:
                loss = create_loss(opt[n], graph)
            elif mix:
                loss = create_loss(opt, graph)
            else:
                loss = create_loss(opt, graph)

            # add the optimizer
            input_var = [var for var in tf.trainable_variables("variable")]
            opt_tensor = optimizer.minimize(-loss, var_list=input_var)

            # initialize specific variables between each run
            model_variables = tf.trainable_variables()
            optimizer_slots = [
                optimizer.get_slot(var, name)
                for name in optimizer.get_slot_names()
                for var in model_variables
                if optimizer.get_slot(var, name) is not None
            ]
            optimizer_var = [optimizer._beta1_power, optimizer._beta2_power]
            temp_var = input_var + optimizer_var + optimizer_slots
            sess.run(tf.initialize_variables(temp_var))

            #TODO: why isnt the naive option training??
            #sess.run(tf.global_variables_initializer())

            for i in range(steps):
                print("vis #", n, "\tstep:", i)

                # save the current optimized image (for testing purposes and cool animations)
                if save_run:
                    img = image_tensor.eval()
                    misc.save_image(img, 'static/images/temp/' + 'img' + str(i) + '.jpg')

                # optimize the image a little bit
                sess.run([loss, opt_tensor])

            img = image_tensor.eval()
            filepath = 'static/images/temp/' + 'img' + str(uuid.uuid4()) + '.jpg'
            misc.save_image(img, filepath)
            filepaths.append(filepath)

        duration = time.time() - start_time
        print("visualization complete\ttime:", duration)
        return filepaths


def create_loss(opt, graph):

    loss = 0

    # create loss from a single layer/channel
    if isinstance(opt, tuple):
        layer_name = opt[0]
        channel = opt[1]

        layer_tensor = graph.get_tensor_by_name(layer_name)
        # TODO: implement L2 loss?
        # image_tensor = graph.get_tensor_by_name("image:0")-0.5
        # l2 = tf.square(image_tensor)
        loss = tf.reduce_mean(layer_tensor[:, :, :, channel])  #-50*l2

    # create loss which is a mix of different optimization-objectives
    elif isinstance(opt, list):
        layer_tensor = graph.get_tensor_by_name(opt[0][0])
        channel_tensor = layer_tensor[:, :, :, opt[0][1]]
        loss = tf.reduce_mean(channel_tensor * opt[0][2])
        for i in range(1, len(opt)):
            layer_tensor = graph.get_tensor_by_name(opt[i][0])
            channel_tensor = layer_tensor[:, :, :, opt[i][1]]
            loss_inner = tf.reduce_mean(channel_tensor * opt[i][2])
            loss += loss_inner

    return loss



