from werkzeug.security import generate_password_hash,check_password_hash
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


def update_admin_password_service(admin_id, current_password, new_password):
    admin = Admin.query.get(admin_id)

    if not admin:
        return {"message": "Admin không tồn tại."}, 404

    if not check_password_hash(admin.password, current_password):
        return {"message": "Mật khẩu hiện tại không đúng."}, 400



    admin.password = generate_password_hash(new_password)
    db.session.commit()

    return {"message": "Cập nhật mật khẩu thành công."}, 200


def get_all_admins_service():
    admins = Admin.query.filter_by(role='admin').all()  # chỉ lấy role='admin'
    return [
        {
            "id": str(admin.id),
            "username": admin.username,
            "role": admin.role,
            "created_at": admin.created_at.isoformat(),
            "updated_at": admin.updated_at.isoformat()
        }
        for admin in admins
    ]

def delete_admin_service(admin_id):
    admin = Admin.query.get(admin_id)
    if not admin:
        return {"message": "Admin không tồn tại"}, 404

    db.session.delete(admin)
    db.session.commit()
    return {"message": "Xóa admin thành công"}, 200