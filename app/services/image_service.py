from app.models.image_model import Image
from app.extensions import db


import cloudinary
import cloudinary.uploader
import os
from dotenv import load_dotenv
from flask import request, jsonify

# Load biến môi trường
load_dotenv()


    

# Hàm upload ảnh
def upload_image_cloudinary(file):
    cloudinary.config(
      cloud_name=os.getenv("CLOUD_NAME"),
      api_key=os.getenv("CLOUD_API_KEY"),
      api_secret=os.getenv("CLOUD_API_SECRET")
    )

    result = cloudinary.uploader.upload(file)
    return {
        "image_url": result["secure_url"],
        "public_key": result["public_id"]
    }


def create_image_service(user_id, source, image_url, image_public_key):
    image = Image(user_id=user_id, source=source, image_url=image_url, image_public_key=image_public_key)
    db.session.add(image)
    db.session.commit()
    return image

def get_all_images_service():
    return Image.query.all()

def get_image_by_id_service(image_id):
    return Image.query.get(image_id)

def update_image_service(image_id, data):
    image = Image.query.get(image_id)
    if not image:
        return None
    image.source = data.get('source', image.source)
    image.image_url = data.get('image_url', image.image_url)
    db.session.commit()
    return image

def delete_image_service(image_id):
    image = Image.query.get(image_id)
    if not image:
        return None
    db.session.delete(image)
    db.session.commit()
    return image
