from PIL import Image
import numpy as np

END_MARKER = '1111111111111110'

def text_to_binary(text):
    return ''.join(format(ord(c), '08b') for c in text) + END_MARKER

def binary_to_text(binary):
    chars = [binary[i:i+8] for i in range(0, len(binary), 8)]
    message = ''
    for char in chars:
        if char == '11111111':
            break
        message += chr(int(char, 2))
    return message

def hide_message(image, secret_text):
    image = image.convert("RGB")
    data = np.array(image)
    flat = data.flatten()

    binary_secret = text_to_binary(secret_text)

    if len(binary_secret) > len(flat):
        raise ValueError("Message too large for image")

    for i, bit in enumerate(binary_secret):
        flat[i] = (flat[i] & ~1) | int(bit)

    stego_data = flat.reshape(data.shape)
    return Image.fromarray(stego_data)

def extract_message(image):
    data = np.array(image).flatten()
    binary = ''.join(str(pixel & 1) for pixel in data)

    end = binary.find(END_MARKER)
    return binary_to_text(binary[:end])
