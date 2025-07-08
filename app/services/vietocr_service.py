  # ⬅️ THÊM DÒNG NÀY
import torch
from vietocr.tool.config import Cfg
from vietocr.tool.predictor import Predictor
import cv2
import base64
import io
from PIL import Image
import matplotlib.pyplot as plt
import numpy as np
import requests


# Load model khi server khởi động
# config = Cfg.load_config_from_name('vgg_transformer')
# config['weights'] = './model/transformerocr2.pth'
# config['device'] = 'cuda' if torch.cuda.is_available() else 'cpu'
# config['vocab'] = "aAàÀảẢãÃáÁạẠăĂằẰẳẲẵẴắẮặẶâÂầẦẩẨẫẪấẤậẬbBcCdDđĐeEèÈẻẺẽẼéÉẹẸêÊềỀểỂễỄếẾệỆfFgGhHiIìÌỉỈĩĨíÍịỊjJkKlLmMnNoOòÒỏỎõÕóÓọỌôÔồỒổỔỗỖốỐộỘơƠờỜởỞỡỠớỚợỢpPqQrRsStTuUùÙủỦũŨúÚụỤưƯừỪửỬữỮứỨựỰvVwWxXyYỳỲỷỶỹỸýÝỵỴzZ0123456789!\"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~ –—‘’“”…"
# config['predictor']['beamsearch'] = False
# config['cnn']['pretrained']=False
# config = Cfg.load_config_from_file("./model/config (1).yml")
# config = Cfg.load_config_from_name('vgg_transformer') 
# config['weights'] = './model/transformerocr (3).pth'

# config['cnn']['pretrained']=False
# config['device'] = 'cuda' if torch.cuda.is_available() else 'cpu'
# config['predictor']['beamsearch']=False
# predictor = Predictor(config)


def resize_padding(img, size=(32, 512), pad_color=255):
    img_h, img_w = img.shape[:2]
    target_h, target_w = size
    ratio = target_h / img_h
    new_w = int(img_w * ratio)
    new_w = min(new_w, target_w)
    resized = cv2.resize(img, (new_w, target_h))
    new_img = np.ones((target_h, target_w), dtype=np.uint8) * pad_color
    new_img[:, :new_w] = resized
    return new_img


def resize_padding(img, size=(32, 512), pad_color=255):
    img_h, img_w = img.shape[:2]
    target_h, target_w = size
    ratio = target_h / img_h
    new_w = int(img_w * ratio)
    new_w = min(new_w, target_w)
    resized = cv2.resize(img, (new_w, target_h))
    new_img = np.ones((target_h, target_w), dtype=np.uint8) * pad_color
    new_img[:, :new_w] = resized
    return new_img




# def predict_text_from_image(image_np):
#     result = predictor.predict(image_np)
#     return result



def predict_text_from_image( base64_img):
    response = requests.post(
        url="https://primate-crucial-blatantly.ngrok-free.app/ocr",
        json={
            "base64_img":base64_img
            
        }
    )

    print("response in: ", response.elapsed.total_seconds() )

    if response.status_code == 200:
        return response.json().get("response_message")
    else:
        print("error", response.status_code, response.text)
        return None




# ----- Tách dòng từ ảnh -----
# Tách dòng từ ảnh OpenCV


def split_lines_from_image(image_rgb, threshold=2):
    """
    Tách các dòng văn bản từ ảnh RGB (màu), không thay đổi kích thước, không chuyển grayscale.
    :param image_rgb: Ảnh đầu vào dạng RGB (numpy array)
    :param threshold: Ngưỡng histogram để xác định dòng
    :return: List ảnh từng dòng, vẫn giữ màu RGB
    """

    # Chuyển sang grayscale chỉ để phân tích (ảnh gốc vẫn giữ nguyên)
    gray = cv2.cvtColor(image_rgb, cv2.COLOR_RGB2GRAY)

    # Nhị phân hóa ảnh: chữ trắng nền đen (inverted)
    _, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

    # Tính histogram theo chiều dọc (hàng)
    hist = cv2.reduce(binary, 1, cv2.REDUCE_AVG).reshape(-1)
    height = binary.shape[0]

    # Tìm ranh giới trên-dưới của các dòng
    uppers = [i for i in range(height - 1) if hist[i] <= threshold and hist[i + 1] > threshold]
    lowers = [i for i in range(height - 1) if hist[i] > threshold and hist[i + 1] <= threshold]

    # Cắt từng dòng từ ảnh gốc RGB
    lines = []
    for i in range(min(len(uppers), len(lowers))):
        y1, y2 = uppers[i], lowers[i]
        line_img = image_rgb[y1:y2, :]
        if line_img.shape[0] > 10:  # loại bỏ nhiễu
            lines.append(line_img)

    return lines


def base64_to_pil_image(base64_str):
    if ',' in base64_str:
        base64_str = base64_str.split(',')[1]
    image_data = base64.b64decode(base64_str)
    return Image.open(BytesIO(image_data)).convert('RGB')  # đảm bảo ảnh màu

# Bước 3: Hàm dùng mô hình VietOCR để nhận dạng
def predict_from_base64(base64_str):
    # image = base64_to_pil_image(base64_str)
    # img = "./1.png"
    img = Image.open("D:/code/luan_van/project/server/app/services/10001.jpg")

    result = predictor.predict(img)
    return result
