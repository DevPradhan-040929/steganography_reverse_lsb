from PIL import ImageChops
import numpy as np
import numpy as np
import matplotlib.pyplot as plt
import math
import numpy as np
import numpy as np

def difference_map(original, stego):
    orig = np.array(original)
    steg = np.array(stego)

    diff = np.abs(orig - steg)

    diff = diff * 50
    diff = np.clip(diff,0,255)

    return diff.astype("uint8")
def show_lsb_plane(image):
    arr = np.array(image)
    lsb = arr & 1
    return lsb * 255
def calculate_psnr(mse):
    if mse == 0:
        return 100
    return 10 * math.log10((255 * 255) / mse)
def show_histogram(image):
    img_array = np.array(image)

    plt.hist(img_array.ravel(), bins=256)
    plt.title("Pixel Intensity Histogram")
    plt.xlabel("Pixel Value")
    plt.ylabel("Frequency")

    return plt


def calculate_mse(original, stego):
    original = np.array(original)
    stego = np.array(stego)

    mse = np.mean((original - stego) ** 2)
    return mse

def calculate_capacity(image):
    width, height = image.size
    return (width * height * 3) // 8  # in characters

def generate_difference_image(original, stego):
    return ImageChops.difference(original, stego)

def lsb_change_count(original, stego):
    o = np.array(original).flatten()
    s = np.array(stego).flatten()
    return sum(o[i] != s[i] for i in range(len(o)))



