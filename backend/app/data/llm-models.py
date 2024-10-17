import random
import tensorflow as tf


class Text2ImageModel:
    def __init__(self, model_path):
        self.model = tf.keras.models.load_model(model_path)

    def generate_image(self, text):
        image = self.model.generate_image(text)
        image.save('static/images/' + str(random.randint(1, 1000)) + '.png')
