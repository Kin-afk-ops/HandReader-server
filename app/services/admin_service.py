from werkzeug.security import generate_password_hash
from app.models.admin_model import Admin
from app import db

def create_admin_service(username, password, role="admin"):
    if not username or not password:
        return {"error": "Thiếu username hoặc password"}, 400

    if Admin.query.filter_by(username=username).first():
        return {"error": "Admin đã tồn tại"}, 409

    hashed_password = generate_password_hash(password)
    new_admin = Admin(username=username, password=hashed_password, role=role)

    db.session.add(new_admin)
    db.session.commit()

    return {
        "message": "Tạo admin thành công",
        "admin": {
            "id": new_admin.id,
            "username": new_admin.username,
            "role": new_admin.role
        }
    }, 201
