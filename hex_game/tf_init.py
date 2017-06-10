import keras
import tensorflow as tf

config = tf.ConfigProto()
sess = tf.Session(config=config)
keras.backend.set_session(sess)
