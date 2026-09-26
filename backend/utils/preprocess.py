import numpy as np
import tensorflow as tf
from tensorflow.keras.applications.vgg19 import preprocess_input

IMG_SIZE = (224, 224)

def preprocess_image(image_path):
    image = tf.keras.utils.load_img(
        image_path,
        target_size=IMG_SIZE
    )

    image_array = tf.keras.utils.img_to_array(
        image
    )

    image_array = np.expand_dims(
        image_array,
        axis=0
    )

    image_array = preprocess_input(
        image_array
    )

    return image_array