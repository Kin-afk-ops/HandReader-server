import cv2
import numpy as np
import base64
from PIL import Image
import io



def base64_to_image(base64_str):

    if ',' in base64_str:
        base64_str = base64_str.split(',')[1]
    img_data = base64.b64decode(base64_str)
    image = Image.open(io.BytesIO(img_data)).convert("RGB")
    return image
