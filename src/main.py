from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from routes import auth,user

app = FastAPI()

app.include_router(auth.router)
app.include_router(user.router)

app.mount("/", StaticFiles(directory="frontend", html = True),name="static")