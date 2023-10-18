from datetime import datetime, timedelta
from functools import wraps
import jwt
from flask import request
from werkzeug.security import generate_password_hash, check_password_hash
from agenda.db import db
from agenda.config import Config

from . import api, models

# users_data = [
#     {"id": 1, "username": "user0", "email": "user0@kodemia.mx"},
#     {"id": 2, "username": "user1", "email": "user1@kodemia.mx"},
#     {"id": 3, "username": "user2", "email": "user2@kodemia.mx"},
# ]



def token_required(func):
    @wraps(func)
    def wrapper():
        authorization = request.headers.get("Authorization")
        prefix = "Bearer "

        if not authorization:
            return {"detail": 'Missing "Authorization" header'}, 401

        if not authorization.startswith(prefix):
            return {"detail": "Invalid token prefix"}, 401

        token = authorization.split(" ")[1]
        if not token:
            return {"detail": "Missing token"}, 401

        try:
            payload = jwt.decode(token, Config.SECRET_KEY, algorithms=["HS256"])
        except jwt.exceptions.ExpiredSignatureError:
            return {"detail": "Token expired"}, 401
        except jwt.exceptions.InvalidTokenError:
            return {"detail": "Invalid token"}, 401

        request.user = db.session.execute(
            db.select(models.User).where(models.User.id == payload["sub"])
        ).scalar_one()

        return func()

    return wrapper


@api.route("/users/<int:user_id>", methods=["GET", "PUT", "DELETE"])
@api.route("/users/", methods=["GET", "POST"])
def users_endpoint(users_id=None):
    try:
        data = request.get_json()
    except:
        pass

    users = models.User.query.all()
    if request.method == "GET":
  
        return [{"id": users.id, "name": users.first_name, "last_name": users.last_name} for users in users]

    
    if request.method == "POST":
        users = models.User(first_name=data["first_name"],
                            last_name=data["last_name"],
                            email=data["email"],
                            password=data["password"]
                            )

        db.session.add(users)
        db.session.commit()

        return {"detail": f"users {users.first_name} created successfully"}




@api.route("/contacts/<int:contacts_id>", methods=["GET", "PUT", "DELETE"])
@api.route("/contacts/", methods=["GET", "POST"])
def contacts_endpoint(contacts_id=None):
    try:
        data_contact = request.get_json()
    except:
        pass

    if contacts_id is not None:
        contacts = models.Contact.query.get_or_404(contacts_id, "contacts not found")
        if request.method == "GET":
            return {"id": contacts.id, "name": contacts.name}

        if request.method == "PUT":
            contacts.name = data_contact["name"]
            msg = f"contacts {contacts.name} modified"

        if request.method == "DELETE":
            db.session.delete(contacts)
            msg = f"contacts {contacts.first_name} deleted"

        db.session.commit()
        return {"detail": msg}

    if request.method == "GET":
        contacts = models.Contact.query.all()
        return [{"id": contacts.id, "name": contacts.first_name} for contacts in contacts]

    if request.method == "POST":
        contacts = models.Contact(first_name=data_contact["first_name"],
                            last_name=data_contact["last_name"],
                            email=data_contact["email"],
                            mobile=data_contact["mobile"],
                            phone=data_contact["phone"],
                            user_id=data_contact["user_id"]
                            )

        db.session.add(contacts)
        db.session.commit()

        return {"detail": f"contacts {contacts.first_name} created successfully"}
