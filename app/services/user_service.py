from app import db
from app.models.user_model import User
from werkzeug.security import generate_password_hash
from datetime import datetime

def create_user_service(data):
    password = data.get("password")
    hashed_password = None  # <-- đảm bảo có biến này
    if password:
        hashed_password = generate_password_hash(password)
    user = User(
        name=data.get("name"),
        email=data.get("email"),
        password=hashed_password,
        role=data.get("role", "user")
    )
    db.session.add(user)
    db.session.commit()
    return user



def get_all_users_service():
    return User.query.all()


def get_user_by_uid_service(userId: str):
    user = User.query.filter_by(id=userId).first()
    return user


def update_user_service(user_id, data):
    user = User.query.get(user_id)
    if not user:
        return None

    # Cập nhật thông tin
    user.name = data.get("name", user.name)
    user.email = data.get("email", user.email)
    user.role = data.get("role", user.role)
    user.updated_at = datetime.utcnow()
    db.session.commit()
    return user



def delete_user_service(user_id):
    user = User.query.get(user_id)
    if not user:
        return False

    db.session.delete(user)
    db.session.commit()
    return True
