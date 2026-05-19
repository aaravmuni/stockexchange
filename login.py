from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class LoginRequest(BaseModel):
    username:str
    password:str

@app.post("/register")
async def register_user(data:LoginRequest):
    pass

@app.post("/login")
async def login_user(data:LoginRequest):
    pass