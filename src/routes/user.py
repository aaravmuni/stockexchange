from fastapi import APIRouter
from fastapi import Depends
import security

router = APIRouter()

@router.get("/me")
def readme(username:str = Depends(security.getcurrentuser)):
    return {"username": username}