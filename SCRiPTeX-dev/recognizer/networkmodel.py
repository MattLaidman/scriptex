"""
Convolutional Neural Network Model for SCRiPTeX Character Recognition Module.

Utilizes the TensorFlow Library
"""


import tensorflow as tf


# Constants

NUM_CLASSES = 126
SYMBOL_WIDTH = 32
SYMBOL_HEIGHT = 32


# Parameters

LEARNING_RATE = 0.001

NUM_FILTERS1 = 64
FILTER_SIZE1 = 5
POOL_SIZE1 = 2

NUM_FILTERS2 = 64
FILTER_SIZE2 = 5
POOL_SIZE2 = 2

FC1_SIZE = 5*5*NUM_FILTERS2 # 64 5x5 filters at this point
FC2_SIZE = 512


class Model:

    """
    Model class wraps creation and functions on network model. Passed model
    weights are loaded if path is given in constructor.
    """

    def __init__(self, model=None):

        self._sess = tf.Session()
        self._build_model()
        if model is None:
            self._sess.run(tf.global_variables_initializer())
        else:
            self.load_model(model)

    def __del__(self):

        del self._sess

    def _build_model(self):

        """
        Builds the model for the network.
        """

        # _m1 prefix denotes the symbol model.
        # _m2 prefix denotes the script model.

        # Expected Output:
        # NUM_CLASSES character classes
        self._m1_y_ = tf.placeholder(tf.float32, shape=[None, NUM_CLASSES])

        # Input Layer:
        # IMAGE_SIZE pixel values
        self._m1_image_size = SYMBOL_WIDTH*SYMBOL_HEIGHT
        self._m1_x_input = tf.placeholder(tf.float32, [None, self._m1_image_size])
        self._m1_x_image = tf.reshape(self._m1_x_input, [-1, SYMBOL_WIDTH, SYMBOL_HEIGHT, 1])

        # First convolutional layer:
        self._m1_w_conv1 = tf.Variable(tf.truncated_normal([FILTER_SIZE1, FILTER_SIZE1, 1,
                                                            NUM_FILTERS1], stddev=0.1))
        self._m1_b_conv1 = tf.Variable(tf.constant(0.1, shape=[NUM_FILTERS1]))

        # Second convolutional layer:
        self._m1_w_conv2 = tf.Variable(tf.truncated_normal([FILTER_SIZE2, FILTER_SIZE2,
                                                            NUM_FILTERS1, NUM_FILTERS2],
                                                           stddev=0.1))
        self._m1_b_conv2 = tf.Variable(tf.constant(0.1, shape=[NUM_FILTERS2]))

        # Fully-Connected Layers:
        self._m1_keep_prob = tf.placeholder(tf.float32)

        # First Fully-Connected Layer
        self._m1_w_fc1 = tf.Variable(tf.truncated_normal([FC1_SIZE, FC2_SIZE], stddev=0.1))
        self._m1_b_fc1 = tf.Variable(tf.constant(0.1, shape=[FC2_SIZE]))

        # Second Fully-Connected Layer
        self._m1_w_fc2 = tf.Variable(tf.truncated_normal([FC2_SIZE, NUM_CLASSES], stddev=0.1))
        self._m1_b_fc2 = tf.Variable(tf.constant(0.1, shape=[NUM_CLASSES]))

        # Define Model and Output Layer:
        # Convolute
        self._m1_h_conv1 = tf.nn.conv2d(self._m1_x_image, self._m1_w_conv1,
                                        strides=[1, 1, 1, 1], padding='VALID') + self._m1_b_conv1
        # Apply max pooling and Activation function (relu)
        self._m1_h_pool1 = tf.nn.relu(tf.nn.max_pool(self._m1_h_conv1,
                                                     ksize=[1, POOL_SIZE1, POOL_SIZE1, 1],
                                                     strides=[1, POOL_SIZE1, POOL_SIZE1, 1],
                                                     padding='VALID'))
        # Convolute
        self._m1_h_conv2 = tf.nn.conv2d(self._m1_h_pool1, self._m1_w_conv2,
                                        strides=[1, 1, 1, 1], padding='VALID') + self._m1_b_conv2
        # Apply max pooling and Activation function (relu)
        self._m1_h_pool2 = tf.nn.relu(tf.nn.max_pool(self._m1_h_conv2,
                                                     ksize=[1, POOL_SIZE2, POOL_SIZE2, 1],
                                                     strides=[1, POOL_SIZE2, POOL_SIZE2, 1],
                                                     padding='VALID'))
        # Flatten image into 1-dimensional tensor
        self._m1_h_pool2_flat = tf.reshape(self._m1_h_pool2, [-1, FC1_SIZE])
        # Drop-out
        self._m1_h_pool2_drop = tf.nn.dropout(self._m1_h_pool2_flat, self._m1_keep_prob)
        # Fully-Connected Layer
        self._m1_y_output = tf.matmul(tf.matmul(self._m1_h_pool2_drop, self._m1_w_fc1) + \
                                      self._m1_b_fc1, self._m1_w_fc2) + self._m1_b_fc2

        # Compute cross entropy
        self._m1_cross_entropy = tf.reduce_mean(tf.nn\
                                .softmax_cross_entropy_with_logits(self._m1_y_output, self._m1_y_))
        # ADAM for optimization, (Gradient Descent with Momentum) minimizing cross entropy
        self._m1_train_step = tf.train.AdamOptimizer(LEARNING_RATE)\
                                   .minimize(self._m1_cross_entropy)
        # Determine accuracy by comparing actual and expected outputs
        self._m1_correct_prediction = tf.equal(tf.argmax(self._m1_y_output, 1),
                                               tf.argmax(self._m1_y_, 1))
        self._m1_accuracy = tf.reduce_mean(tf.cast(self._m1_correct_prediction, tf.float32))


        # Expected Output:
        # NUM_CLASSES character classes
        self._m2_y_ = tf.placeholder(tf.float32, shape=[None, NUM_CLASSES])

        # Input Layer:
        # IMAGE_SIZE pixel values
        self._m2_image_size = SYMBOL_WIDTH*SYMBOL_HEIGHT
        self._m2_x_input = tf.placeholder(tf.float32, [None, self._m2_image_size])
        self._m2_x_image = tf.reshape(self._m2_x_input, [-1, SYMBOL_WIDTH, SYMBOL_HEIGHT, 1])

        # First convolutional layer:
        self._m2_w_conv1 = tf.Variable(tf.truncated_normal([FILTER_SIZE1, FILTER_SIZE1, 1,
                                                            NUM_FILTERS1], stddev=0.1))
        self._m2_b_conv1 = tf.Variable(tf.constant(0.1, shape=[NUM_FILTERS1]))

        # Second convolutional layer:
        self._m2_w_conv2 = tf.Variable(tf.truncated_normal([FILTER_SIZE2, FILTER_SIZE2,
                                                            NUM_FILTERS1, NUM_FILTERS2],
                                                           stddev=0.1))
        self._m2_b_conv2 = tf.Variable(tf.constant(0.1, shape=[NUM_FILTERS2]))

        # Fully-Connected Layers:
        self._m2_keep_prob = tf.placeholder(tf.float32)

        # First Fully-Connected Layer
        self._m2_w_fc1 = tf.Variable(tf.truncated_normal([FC1_SIZE, FC2_SIZE], stddev=0.1))
        self._m2_b_fc1 = tf.Variable(tf.constant(0.1, shape=[FC2_SIZE]))

        # Second Fully-Connected Layer
        self._m2_w_fc2 = tf.Variable(tf.truncated_normal([FC2_SIZE, NUM_CLASSES], stddev=0.1))
        self._m2_b_fc2 = tf.Variable(tf.constant(0.1, shape=[NUM_CLASSES]))

        # Define Model and Output Layer:
        # Convolute
        self._m2_h_conv1 = tf.nn.conv2d(self._m2_x_image, self._m2_w_conv1,
                                        strides=[1, 1, 1, 1], padding='VALID') + self._m2_b_conv1
        # Apply max pooling and Activation function (relu)
        self._m2_h_pool1 = tf.nn.relu(tf.nn.max_pool(self._m2_h_conv1,
                                                     ksize=[1, POOL_SIZE1, POOL_SIZE1, 1],
                                                     strides=[1, POOL_SIZE1, POOL_SIZE1, 1],
                                                     padding='VALID'))
        # Convolute
        self._m2_h_conv2 = tf.nn.conv2d(self._m2_h_pool1, self._m2_w_conv2,
                                        strides=[1, 1, 1, 1], padding='VALID') + self._m2_b_conv2
        # Apply max pooling and Activation function (relu)
        self._m2_h_pool2 = tf.nn.relu(tf.nn.max_pool(self._m2_h_conv2,
                                                     ksize=[1, POOL_SIZE2, POOL_SIZE2, 1],
                                                     strides=[1, POOL_SIZE2, POOL_SIZE2, 1],
                                                     padding='VALID'))
        # Flatten image into 1-dimensional tensor
        self._m2_h_pool2_flat = tf.reshape(self._m2_h_pool2, [-1, FC1_SIZE])
        # Drop-out
        self._m2_h_pool2_drop = tf.nn.dropout(self._m2_h_pool2_flat, self._m2_keep_prob)
        # Fully-Connected Layer
        self._m2_y_output = tf.matmul(tf.matmul(self._m2_h_pool2_drop, self._m2_w_fc1) + \
                                      self._m2_b_fc1, self._m2_w_fc2) + self._m2_b_fc2

        # Compute cross entropy
        self._m2_cross_entropy = tf.reduce_mean(tf.nn\
                                .softmax_cross_entropy_with_logits(self._m2_y_output, self._m2_y_))
        # ADAM for optimization, (Gradient Descent with Momentum) minimizing cross entropy
        self._m2_train_step = tf.train.AdamOptimizer(LEARNING_RATE)\
                                   .minimize(self._m2_cross_entropy)
        # Determine accuracy by comparing actual and expected outputs
        self._m2_correct_prediction = tf.equal(tf.argmax(self._m2_y_output, 1),
                                               tf.argmax(self._m2_y_, 1))
        self._m2_accuracy = tf.reduce_mean(tf.cast(self._m2_correct_prediction, tf.float32))


    def train_symbol_model(self, batch):

        """
        Trains the network on the passed batch.
        """

        # Train Network on batch
        self._sess.run(self._m1_train_step, feed_dict={self._m1_x_input: batch[0],
                                                       self._m1_y_: batch[1],
                                                       self._m1_keep_prob: 0.5})

    def train_script_model(self, batch):

        """
        Trains the network on the passed batch.
        """
        self._sess.run(self._m2_train_step, feed_dict={self._m2_x_input: batch[0],
                                                       self._m2_y_: batch[1],
                                                       self._m2_keep_prob: 0.5})

    def test_symbol_model(self, batch):

        """
        Tests the network on the given batch and return the accuracy of the network.
        """

        # Compute accuracy for batch
        return self._sess.run([self._m1_cross_entropy, self._m1_accuracy],
                              feed_dict={self._m1_x_input: batch[0], self._m1_y_: batch[1],
                                         self._m1_keep_prob: 1.0})
                                         
    def test_script_model(self, batch):

        """
        Tests the network on the given batch and return the accuracy of the network.
        """

        # Compute accuracy for batch
        return self._sess.run([self._m2_cross_entropy, self._m2_accuracy],
                              feed_dict={self._m2_x_input: batch[0], self._m2_y_: batch[1],
                                         self._m2_keep_prob: 1.0})


    def run_model(self, batch, sindex):

        """
        Runs the passed batch through the network and returns a list of indices.
        """

        num_chars = len(batch)
        indices = []

        for i in range(num_chars):
            temp = []
            temp.append(batch[i])
            if sindex[i] == 0:
                indices.append(self._sess.run(tf.argmax(tf.nn.softmax(self._m1_y_output),
                                                        dimension=1),
                                              feed_dict={self._m1_x_input: temp,
                                                         self._m1_keep_prob: 1.0})[0])
            else:
                indices.append(self._sess.run(tf.argmax(tf.nn.softmax(self._m2_y_output),
                                                        dimension=1),
                                              feed_dict={self._m2_x_input: temp,
                                                         self._m2_keep_prob: 1.0})[0])
            del temp[0]
        return indices

    def save_model(self, model):

        """
        Saves the model weights to the passed file.
        """

        saver = tf.train.Saver()
        saver.save(self._sess, model)


    def load_model(self, model):

        """
        Loads the model weights from the passed file.
        """

        saver = tf.train.Saver()
        saver.restore(self._sess, model)
