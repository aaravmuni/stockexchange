from fastapi import FastAPI
from pydantic import BaseModel, Field
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

import mysql.connector
from mysql.connector import IntegrityError, Error, pooling
from passlib.context import CryptContext

import os
import jwt
from datetime import datetime, timezone, timedelta

SECRET_KEY = os.environ.get("JWT_SECRET", "backup")
ALGORITHM = "HS256"
TOKEN_EXPIRE_MINUTES = 30

def createtoken(username:str) -> str:
    time = datetime.now(timezone.utc)
    payload = {
        "sub":username,
        "iat":time,
        "exp":time + timedelta(minutes = TOKEN_EXPIRE_MINUTES)
    }
    return jwt.encode(payload,SECRET_KEY,algorithm=ALGORITHM)

pool = mysql.connector.pooling.MySQLConnectionPool(
    pool_name="sqlpool",
    pool_size=5,
    host="localhost",
    user="exchangedbuser",
    password="123",
    database="exchangelogin"
)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class LoginRequest(BaseModel):
    username:str = Field(min_length=1, max_length=100)
    password:str = Field(min_length=1, max_length=72)

@app.post("/register")
def register_user(data:LoginRequest):
    try:
        conn = pool.get_connection()
        cursor = conn.cursor()
        hashed = pwd_context.hash(data.password.strip())
        cursor.execute(
            "INSERT INTO users (username, password) VALUES (%s, %s)",
            (data.username.strip(), hashed)
        )
        conn.commit()
        return {"message":"user_created"}
    except IntegrityError:
        return {"message":"duplicate_username"}
    except Error:
        return {"message":"database_error"}
    finally:
        if cursor is not None:
            cursor.close()
        if conn is not None:
            conn.close()

@app.post("/login")
def login_user(data:LoginRequest):
    try:
        conn = pool.get_connection()
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
        token = createtoken(data.username.strip())
        return {"message": "correct_password", "token": token}

app.mount("/", StaticFiles(directory="frontend", html = True),name="static")