"""
Convolutional Neural Network Model for SCRiPTeX Character Recognition Module.

Utilizes the TensorFlow Library
"""


import tensorflow as tf
import recognizer.texlookup as tl


# Parameters

NUM_CLASSES = 107
LEARNING_RATE = 0.001
SYMBOL_WIDTH = 32
SYMBOL_HEIGHT = 32


class Model:

    """
    Model class wraps creation and functions on network model. Passed model
    weights are loaded if path is given in constructor.
    """

    def __init__(self, model=None):

        self._image_size = 0
        self._x_input = 0
        self._x_image = 0
        self._y_ = 0
        self._w_conv1 = 0
        self._b_conv1 = 0
        self._w_conv2 = 0
        self._b_conv2 = 0
        self._w_fc1 = 0
        self._b_fc1 = 0
        self._w_fc2 = 0
        self._b_fc2 = 0
        self._h_conv1 = 0
        self._h_conv2 = 0
        self._h_pool1 = 0
        self._h_pool2 = 0
        self._h_pool2_flat = 0
        self._keep_prob = 0
        self._h_pool2_drop = 0
        self._y_output = 0
        self._cross_entropy = 0
        self._train_step = 0
        self._correct_prediction = 0
        self._accuracy = 0

        self._sess = tf.Session()
        self._build_model()
        if model is None:
            self._sess.run(tf.global_variables_initializer())
        else:
            self.load_model(model)


    def _build_model(self):

        """
        Builds the model for the network.
        """

        # Expected Output:
        # NUM_CLASSES character classes
        self._y_ = tf.placeholder(tf.float32, shape=[None, NUM_CLASSES])

        # Input Layer:
        # IMAGE_SIZE pixel values
        self._image_size = SYMBOL_WIDTH*SYMBOL_HEIGHT
        self._x_input = tf.placeholder(tf.float32, [None, self._image_size])
        self._x_image = tf.reshape(self._x_input, [-1, SYMBOL_WIDTH, SYMBOL_HEIGHT, 1])

        # First convolutional layer:
        _num_filters1 = 64
        _filter_size1 = 5
        _pool_size1 = 2
        self._w_conv1 = tf.Variable(tf.truncated_normal([_filter_size1, _filter_size1, 1, _num_filters1], stddev=0.1))
        self._b_conv1 = tf.Variable(tf.constant(0.1, shape=[_num_filters1]))

        # Second convolutional layer:
        _num_filters2 = 64
        _filter_size2 = 5
        _pool_size2 = 2
        self._w_conv2 = tf.Variable(tf.truncated_normal([_filter_size2, _filter_size2, _num_filters1, _num_filters2], stddev=0.1))
        self._b_conv2 = tf.Variable(tf.constant(0.1, shape=[_num_filters2]))

        # Fully-Connected Layers:
        _width = int((int((SYMBOL_WIDTH - (_filter_size1 - 1)) / _pool_size1) - (_filter_size2 - 1)) / _pool_size2)
        _height = int((int((SYMBOL_HEIGHT - (_filter_size1 - 1)) / _pool_size1) - (_filter_size2 - 1)) / _pool_size2)
        _fc1_size = _width*_height*_num_filters2
        _fc2_size = int((_fc1_size + NUM_CLASSES)/2)
        self._keep_prob = tf.placeholder(tf.float32)

        # First Fully-Connected Layer
        self._w_fc1 = tf.Variable(tf.truncated_normal([_fc1_size, _fc2_size], stddev=0.1))
        self._b_fc1 = tf.Variable(tf.constant(0.1, shape=[_fc2_size]))

        # Second Fully-Connected Layer
        self._w_fc2 = tf.Variable(tf.truncated_normal([_fc2_size, NUM_CLASSES], stddev=0.1))
        self._b_fc2 = tf.Variable(tf.constant(0.1, shape=[NUM_CLASSES]))

        # Define Model and Output Layer:
        # Convolute
        self._h_conv1 = tf.nn.conv2d(self._x_image, self._w_conv1,
                                     strides=[1, 1, 1, 1], padding='VALID') + self._b_conv1
        # Apply max pooling and Activation function (relu)
        self._h_pool1 = tf.nn.relu(tf.nn.max_pool(self._h_conv1,
                                                  ksize=[1, _pool_size1, _pool_size1, 1],
                                                  strides=[1, _pool_size1, _pool_size1, 1],
                                                  padding='VALID'))
        # Convolute
        self._h_conv2 = tf.nn.conv2d(self._h_pool1, self._w_conv2,
                                     strides=[1, 1, 1, 1], padding='VALID') + self._b_conv2
        # Apply max pooling and Activation function (relu)
        self._h_pool2 = tf.nn.relu(tf.nn.max_pool(self._h_conv2,
                                                  ksize=[1, _pool_size2, _pool_size2, 1],
                                                  strides=[1, _pool_size2, _pool_size2, 1],
                                                  padding='VALID'))
        # Flatten image into 1-dimensional tensor
        self._h_pool2_flat = tf.reshape(self._h_pool2, [-1, _width*_height*_num_filters2])
        # Drop-out
        self._h_pool2_drop = tf.nn.dropout(self._h_pool2_flat, self._keep_prob)
        # Fully-Connected Layer
        self._y_output = tf.matmul(tf.matmul(self._h_pool2_drop, self._w_fc1) + self._b_fc1, self._w_fc2) + self._b_fc2

        # Compute cross entropy
        self._cross_entropy = tf.reduce_mean(tf.nn\
                                .softmax_cross_entropy_with_logits(self._y_output, self._y_))
        # Gradient descent for optimization, minimizing cross entropy
        self._train_step = tf.train.AdamOptimizer(LEARNING_RATE)\
                                   .minimize(self._cross_entropy)
        # Determine accuracy by comparing actual and expected outputs
        self._correct_prediction = tf.equal(tf.argmax(self._y_output, 1), tf.argmax(self._y_, 1))
        self._accuracy = tf.reduce_mean(tf.cast(self._correct_prediction, tf.float32))

    def train_model(self, batch):

        """
        Trains the network on the passed batch.
        """

        # Train Network on batch
        self._sess.run(self._train_step, feed_dict={self._x_input: batch[0], self._y_: batch[1], self._keep_prob: 0.5})


    def test_model(self, batch):

        """
        Tests the network on the given batch and return the accuracy of the network.
        """

        # Compute accuracy for batch
        return self._sess.run([self._cross_entropy, self._accuracy],
                              feed_dict={self._x_input: batch[0], self._y_: batch[1], self._keep_prob: 1.0})


    def run_model(self, batch):

        """
        Runs the passed batch through the network and returns a list of indices.
        """

        # Compute indices for batch
        indices = self._sess.run(tf.argmax(tf.nn.softmax(self._y_output),
                                 dimension=1), feed_dict={self._x_input: batch, self._keep_prob: 1.0})
        recognizedsymbols = []
        numimages = len(indices)
        for i in range(numimages):
            recognizedsymbols.append(tl.get_tex(indices[i]))
            
        return recognizedsymbols

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
