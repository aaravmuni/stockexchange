from fastapi import FastAPI
from pydantic import BaseModel, Field
from fastapi.middleware.cors import CORSMiddleware

import mysql.connector
from mysql.connector import IntegrityError, Error, pooling
from passlib.context import CryptContext

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
        return {"message": "correct_password"}
