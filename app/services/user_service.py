from app import db
from app.models.user_model import User
from werkzeug.security import generate_password_hash

def create_user_service(data):
    hashed_password = generate_password_hash(data.get("password"))
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
