from sqlalchemy.orm import Session
from fastapi import Response
import bcrypt
import jwt

import models
import schemas


SECRET_KEY = "abcdefghijklmnopqrtuvwxyz"
ALGORITHM = "HS256"


# ================= MOBILE CRUD =================

def create_mobile(db: Session, mobile: schemas.MobileCreate):

    db_mobile = models.Mobile(**mobile.model_dump())

    db.add(db_mobile)
    db.commit()
    db.refresh(db_mobile)

    return db_mobile


def get_mobiles(db: Session):
    return db.query(models.Mobile).all()


def get_mobile(db: Session, mobile_id: int):

    return db.query(models.Mobile).filter(
        models.Mobile.id == mobile_id
    ).first()


def get_by_brand(db: Session, brand_name: str):

    return db.query(models.Mobile).filter(
        models.Mobile.brand == brand_name
    ).all()


def update_mobile(
    db: Session,
    mobile_id: int,
    mobile: schemas.MobileCreate
):

    db_mobile = get_mobile(db, mobile_id)

    if not db_mobile:
        return None

    db_mobile.brand = mobile.brand
    db_mobile.model = mobile.model
    db_mobile.ram = mobile.ram
    db_mobile.storage = mobile.storage
    db_mobile.price = mobile.price

    db.commit()
    db.refresh(db_mobile)

    return db_mobile


def delete_mobile(db: Session, mobile_id: int):

    db_mobile = get_mobile(db, mobile_id)

    if not db_mobile:
        return None

    db.delete(db_mobile)
    db.commit()

    return db_mobile



# ================= USER CRUD =================


def create_user(user: schemas.UserCreate, db: Session):

    existing_user = db.query(models.User).filter(
        models.User.email == user.email
    ).first()


    if existing_user:
        return {
            "message": "Email already registered"
        }


    # Generate hashed password using salt
    hashed_password = bcrypt.hashpw(
        user.password.encode(),
        bcrypt.gensalt()
    ).decode()


    db_user = models.User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password,
        role=user.role
    )


    db.add(db_user)
    db.commit()
    db.refresh(db_user)


    return {
        "message": "User Registered Successfully"
    }



def validate_user(
    user: schemas.UserLogin,
    db: Session,
    response: Response
):

    user_exist = db.query(models.User).filter(
        models.User.email == user.email
    ).first()


    if not user_exist:
        return {
            "message": "User not found"
        }


    password_check = bcrypt.checkpw(
        user.password.encode(),
        user_exist.hashed_password.encode()
    )


    if not password_check:
        return {
            "message": "Invalid password"
        }


    payload = {
        "username": user_exist.username,
        "email": user_exist.email,
        "role": user_exist.role
    }


    token = jwt.encode(
        payload,
        SECRET_KEY,
        algorithm=ALGORITHM
    )


    response.set_cookie(
        key="access_token",
        value=token,
        httponly=True
    )


    return {
        "message": "Login Successful",
        "role": user_exist.role
    }