import jwt
from datetime import datetime, timezone, timedelta
import config

from fastapi import HTTPException,Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

def createtoken(username:str) -> str:
    time = datetime.now(timezone.utc)
    payload = {
        "sub":username,
        "iat":time,
        "exp":time + timedelta(minutes = config.TOKEN_EXPIRE_MINUTES)
    }
    return jwt.encode(payload,config.SECRET_KEY,algorithm=config.ALGORITHM)

bearerparser = HTTPBearer()

def getcurrentuser(creds:HTTPAuthorizationCredentials = Depends(bearerparser))->str:
    token = creds.credentials
    try:
        payload = jwt.decode(token,config.SECRET_KEY,algorithms=[config.ALGORITHM])
        return payload["sub"]
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="token_expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="invalid_token")