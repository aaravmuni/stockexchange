from fastapi import APIRouter

import schemas
import database
from mysql.connector import IntegrityError, Error
from passlib.context import CryptContext

import security

router = APIRouter()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@router.post("/register")
def register_user(data:schemas.LoginRequest):
    conn = None
    cursor = None
    try:
        conn = database.pool.get_connection()
        cursor = conn.cursor()
        hashed = pwd_context.hash(data.password.strip())
        cursor.execute(
            "INSERT INTO users (username, password) VALUES (%s, %s)",
            (data.username.strip(), hashed)
        )
        cursor.execute(
            "INSERT INTO balances (user_id, balance) VALUES (%s, %s)",
            (cursor.lastrowid, 0.00)
        )
        conn.commit()
        token = security.createtoken(data.username.strip())
        return {"message": "user_created", "token": token}
    except IntegrityError:
        return {"message":"duplicate_username"}
    except Error:
        return {"message":"database_error"}
    finally:
        if cursor is not None:
            cursor.close()
        if conn is not None:
            conn.close()

@router.post("/login")
def login_user(data:schemas.LoginRequest):
    conn = None
    cursor = None
    try:
        conn = database.pool.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT password FROM users WHERE username = %s", (data.username.strip(),))
        result = cursor.fetchone()
    except Error:
        return {"message": "database_error"}
    finally:
        if cursor is not None:
            cursor.close()
        if conn is not None:
            conn.close()
    
    if result is None:
        return {"message": "user_notfound"}
    
    is_valid = pwd_context.verify(data.password.strip(), result[0])

    if not is_valid:
        return {"message": "wrong_password"}
    else:
        token = security.createtoken(data.username.strip())
        return {"message": "correct_password", "token": token}
