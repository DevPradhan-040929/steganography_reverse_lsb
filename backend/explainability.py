from PIL import ImageChops
import numpy as np

def calculate_capacity(image):
    width, height = image.size
    return (width * height * 3) // 8  # in characters

def generate_difference_image(original, stego):
    return ImageChops.difference(original, stego)

def lsb_change_count(original, stego):
    o = np.array(original).flatten()
    s = np.array(stego).flatten()
    return sum(o[i] != s[i] for i in range(len(o)))
