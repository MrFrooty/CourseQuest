from PIL import Image
import numpy as np


def average_linkedin_backgrounds(image_paths: list):
    images = [Image.open(image_path) for image_path in image_paths]
    arr = np.array([np.array(img) for img in images])
    avg_arr = np.mean(arr, axis=0).astype(np.uint8)
    avg_image = Image.fromarray(avg_arr)
    avg_image_path = "average_background.png"
    avg_image.save(avg_image_path)
    return avg_image_path
