from PIL import Image    # ⬅️ THÊM DÒNG NÀY
import torch
from vietocr.tool.config import Cfg
from vietocr.tool.predictor import Predictor
import cv2

# Load model khi server khởi động
config = Cfg.load_config_from_name('vgg_transformer')
config['weights'] = './model/transformerocr.pth'
config['device'] = 'cuda' if torch.cuda.is_available() else 'cpu'
config['predictor']['beamsearch'] = True


def resize_image(image, width=256):
    h, w = image.shape[:2]
    aspect_ratio = h / w
    new_height = int(width * aspect_ratio)
    return cv2.resize(image, (width, new_height))

predictor = Predictor(config)

def predict_text_from_image(image_np):
    image = resize_image(image_np)  # ✅ dùng đúng biến đầu vào
    image_pil = Image.fromarray(image)
    result = predictor.predict(image_pil)
    return result