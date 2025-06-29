import cv2
import numpy as np
import base64
from PIL import Image
import io

# def base64_to_image(base64_str):
#     img_data = base64.b64decode(base64_str)
#     np_arr = np.frombuffer(img_data, np.uint8)
#     img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

#     # ✅ Tiền xử lý ảnh:
#     gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)        # Chuyển về grayscale
#     _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)  # Nhị phân hóa ảnh

#     return thresh  # Trả về ảnh sau xử lý


def base64_to_image(base64_str):

    if ',' in base64_str:
        base64_str = base64_str.split(',')[1]
    img_data = base64.b64decode(base64_str)
    image = Image.open(io.BytesIO(img_data)).convert("RGB")
    return image
