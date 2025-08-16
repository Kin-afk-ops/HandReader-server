from app.models.image_model import Image
from app.models.recognition_result_model import RecognitionResult
from app.extensions import db
from sqlalchemy import func, extract
from sqlalchemy.orm import joinedload



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
    images = Image.query.options(
        joinedload(Image.recognition_results)  
    ).all()

    result = []
    for img in images:
        # lấy result đầu tiên (vì chỉ có 1)
        r = img.recognition_results[0] if img.recognition_results else None

        result.append({
            "id": str(img.id),
            "user_id": str(img.user_id),
            "source": img.source,
            "image_url": img.image_url,
            "image_public_key": img.image_public_key,
            "created_at": img.created_at.isoformat(),
            # gộp trực tiếp các trường của recognition_result
            **({
                "recognized_text": r.recognized_text,
                "confidence": r.confidence,
                "is_saved_by_user": r.is_saved_by_user,
                "result_created_at": r.created_at.isoformat()
            } if r else {})
        })
    return result

def get_image_by_id_service(image_id):
    return Image.query.get(image_id)


def get_image_stats_service():
    results = (
        db.session.query(
            extract("month", Image.created_at).label("month"),
            extract("year", Image.created_at).label("year"),
            func.count(Image.id).label("images")
        )
        .group_by("year", "month")
        .order_by("year", "month")
        .all()
    )

    data = [
        {"month": int(month), "year": int(year), "images": count}
        for month, year, count in results
    ]

    return data

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
    db.session.query(RecognitionResult).filter_by(image_id=image_id).delete()
    db.session.commit()
    return image


