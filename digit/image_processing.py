import numpy as np
from tensorflow.keras.preprocessing.image import img_to_array
from PIL import Image, ImageOps


def to_grayscale(image):
    return image.convert('L')

def invert_colors(image):
    return ImageOps.invert(image)

def resize_image(image):
    return image.resize((32, 32), Image.LINEAR)

def process_image(image):
    image = to_grayscale(image)
    image = invert_colors(image)
    image = resize_image(image)
    img = img_to_array(image)
    img = np.expand_dims(img, axis=0)

    return img


def process_batch_image(images):
    if not images:
        return []
    batch = []
    for image in images:
        image = to_grayscale(image)
        image = invert_colors(image)
        image = resize_image(image)
        img = img_to_array(image)
        img = np.expand_dims(img, axis=0)
        batch.append(img)
    con = batch[0]
    for img in batch[1:]:
        con = np.concatenate((con, img), axis=0)
    return con