from fastapi import FastAPI, APIRouter, Depends
from pydantic import BaseModel
from databaseutils import transactions, userbase
from decimal import Decimal
import security

router = APIRouter()

@router.get("/currentbalance")
def checkbalance(username:str = Depends(security.getcurrentuser)):
    print(username)
    id = userbase.getid(username)
    print(id)
    if id != -1:
        bal = transactions.readbalance(id)
        print(bal)
        return {"message":bal}
    else:
        return {"message":"user_not_found"}

@router.post("/increaseby10")
def checkbalance(username:str = Depends(security.getcurrentuser)):
    print(username)
    id = userbase.getid(username)
    print(id)
    if id != -1:
        status = transactions.recordtransaction(id,Decimal("10.0"),"deposit")
        return {"message":status}
    else:
        return {"message":"user_not_found"}