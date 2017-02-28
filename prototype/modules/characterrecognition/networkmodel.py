"""
Convolutional Neural Network Model for SCRiPTeX Character Recognition Module.

Utilizes the TensorFlow Library
"""


import tensorflow as tf


# Parameters

NUM_CLASSES = 107
LEARNING_RATE = 0.6
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
        self._w_conv = 0
        self._b_conv = 0
        self._w_fc = 0
        self._b_fc = 0
        self._h_conv = 0
        self._h_pool = 0
        self._h_pool_flat = 0
        self._keep_prob = 0
        self._h_pool_drop = 0
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

        # Convolutional layer:
        _num_feature_maps = 32
        _filter_size = 5
        _pool_size = 2
        self._w_conv = tf.Variable(tf.zeros([_filter_size, _filter_size, 1, _num_feature_maps]))
        self._b_conv = tf.Variable(tf.zeros([_num_feature_maps]))

        # Fully-Connected Layer:
        _width = int((SYMBOL_WIDTH - (_filter_size - 1)) / _pool_size)
        _height = int((SYMBOL_HEIGHT - (_filter_size - 1)) / _pool_size)
        self._keep_prob = tf.placeholder(tf.float32)
        self._w_fc = tf.Variable(tf.zeros([_width*_height*_num_feature_maps, NUM_CLASSES]))
        self._b_fc = tf.Variable(tf.zeros([NUM_CLASSES]))

        # Define Model and Output Layer:
        # Convolute
        self._h_conv = tf.nn.conv2d(self._x_image, self._w_conv,
                                    strides=[1, 1, 1, 1], padding='VALID') + self._b_conv
        # Apply max pooling and Activation function (sigmoid)
        self._h_pool = tf.nn.sigmoid(tf.nn.max_pool(self._h_conv,
                                                    ksize=[1, _pool_size, _pool_size, 1],
                                                    strides=[1, _pool_size, _pool_size, 1],
                                                    padding='VALID'))
        # Flatten image into 1-dimensional tensor
        self._h_pool_flat = tf.reshape(self._h_pool, [-1, _width*_height*_num_feature_maps])
        # Drop-out prevents overfitting
        self._h_pool_drop = tf.nn.dropout(self._h_pool_flat, self._keep_prob)
        # Fully-Connected Layer
        self._y_output = tf.matmul(self._h_pool_drop, self._w_fc) + self._b_fc

        # Compute cross entropy
        self._cross_entropy = tf.reduce_mean(tf.nn\
                                .softmax_cross_entropy_with_logits(self._y_output, self._y_))
        # Gradient descent for optimization, minimizing cross entropy
        self._train_step = tf.train.GradientDescentOptimizer(LEARNING_RATE)\
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
        return self._sess.run(self._accuracy,
                              feed_dict={self._x_input: batch[0], self._y_: batch[1], self._keep_prob: 1.0})


    def run_model(self, batch):

        """
        Runs the passed batch through the network and returns a list of indices.
        """

        # Compute indices for batch
        return self._sess.run(tf.argmax(tf.nn.softmax(self._y_output),
                                        dimension=1), feed_dict={self._x_input: batch, self._keep_prob: 1.0})

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
