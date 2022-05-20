import numpy as np
from skimage import exposure
from tensorflow.keras.preprocessing.image import img_to_array
import base64
from PIL import Image, ImageOps, ImageChops
from io import BytesIO


def replace_transparent_background(image):
    image_arr = np.array(image)
    if len(image_arr.shape) == 2:
        return image

    alpha1 = 0
    r2, g2, b2, alpha2 = 255, 255, 255, 255

    red, green, blue, alpha = image_arr[:, :, 0], image_arr[:, :, 1], image_arr[:, :, 2], image_arr[:, :, 3]
    mask = (alpha == alpha1)
    image_arr[:, :, :4][mask] = [r2, g2, b2, alpha2]

    return Image.fromarray(image_arr)


def trim_borders(image):
    bg = Image.new(image.mode, image.size, image.getpixel((0,0)))
    diff = ImageChops.difference(image, bg)
    diff = ImageChops.add(diff, diff, 2.0, -100)
    bbox = diff.getbbox()
    if bbox:
        return image.crop(bbox)
    
    return image

def pad_image(image):
    return ImageOps.expand(image, border=30, fill='#fff')


def to_grayscale(image):
    return image.convert('L')

def invert_colors(image):
    return ImageOps.invert(image)

def resize_image(image):
    return image.resize((32, 32), Image.LINEAR)

def process_image(image):
    # image = replace_transparent_background(image)
    # image = trim_borders(image)
    # image = pad_image(image)
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
        # image = trim_borders(image)
        # image = pad_image(image)
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