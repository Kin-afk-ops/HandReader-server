  # ⬅️ THÊM DÒNG NÀY
import torch
from vietocr.tool.config import Cfg
from vietocr.tool.predictor import Predictor
import cv2
import base64
import io
from PIL import Image
import matplotlib.pyplot as plt

# Load model khi server khởi động
# config = Cfg.load_config_from_name('vgg_transformer')
# config['weights'] = './model/transformerocr2.pth'
# config['device'] = 'cuda' if torch.cuda.is_available() else 'cpu'
# config['vocab'] = "aAàÀảẢãÃáÁạẠăĂằẰẳẲẵẴắẮặẶâÂầẦẩẨẫẪấẤậẬbBcCdDđĐeEèÈẻẺẽẼéÉẹẸêÊềỀểỂễỄếẾệỆfFgGhHiIìÌỉỈĩĨíÍịỊjJkKlLmMnNoOòÒỏỎõÕóÓọỌôÔồỒổỔỗỖốỐộỘơƠờỜởỞỡỠớỚợỢpPqQrRsStTuUùÙủỦũŨúÚụỤưƯừỪửỬữỮứỨựỰvVwWxXyYỳỲỷỶỹỸýÝỵỴzZ0123456789!\"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~ –—‘’“”…"
# config['predictor']['beamsearch'] = False
# config['cnn']['pretrained']=False
config = Cfg.load_config_from_name('vgg_transformer')
config['weights'] = './model/vgg_transformer.pth'

config['cnn']['pretrained']=False
config['device'] = 'cuda' if torch.cuda.is_available() else 'cpu'
config['predictor']['beamsearch']=False
predictor = Predictor(config)



def resize_image(image, width=256):
    h, w = image.shape[:2]
    aspect_ratio = h / w
    new_height = int(width * aspect_ratio)
    return cv2.resize(image, (width, new_height))


def predict_text_from_image(image_np):
    result = predictor.predict(image_np)
    return result


def split_lines_from_image(image, threshold=2):
    # """
    # Tách dòng từ ảnh văn bản bằng histogram theo hàng.
    # Trả về danh sách ảnh numpy (mỗi ảnh là 1 dòng).
    # """

    # Nếu ảnh là grayscale hoặc màu, xử lý về grayscale
    if len(image.shape) == 3:
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Nhị phân hóa ảnh (chữ trắng trên nền đen)
    _, threshed = cv2.threshold(image, 127, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)

    # Tính histogram theo chiều dọc (theo hàng)
    hist = cv2.reduce(threshed, 1, cv2.REDUCE_AVG).reshape(-1)

    H = image.shape[0]
    uppers = [y for y in range(H-1) if hist[y] <= threshold and hist[y+1] > threshold]
    lowers = [y for y in range(H-1) if hist[y] > threshold and hist[y+1] <= threshold]

    # Trả về list ảnh dòng
    lines = []
    for i in range(min(len(uppers), len(lowers))):
        line_img = image[uppers[i]:lowers[i], :]
        if line_img.shape[0] > 10:  # loại bỏ nhiễu dòng quá nhỏ
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
