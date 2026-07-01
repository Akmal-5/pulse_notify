import os
from dotenv import load_dotenv
from datetime import datetime , timedelta , timezone
from typing import Annotated
import jwt
from jwt import PyJWTError , ExpiredSignatureError
from fastapi import HTTPException , status , Depends
from fastapi.security import HTTPBearer , HTTPAuthorizationCredentials

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"

security  = HTTPBearer()

def jwt_encode_access (user_data : dict) :
    
    data_copy = user_data.copy()
    
    now = datetime.now(timezone.utc)
    
    expire = now + timedelta(minutes=30)
    
    data_copy.update({"exp" : expire , "type" : "access"})
    
    return jwt.encode(data_copy , SECRET_KEY , algorithm=ALGORITHM)

def jwt_encode_refresh (user_data : dict) :
    
    data_copy = user_data.copy()
    
    now = datetime.now(timezone.utc)
    
    expire = now + timedelta(weeks=2)
    
    data_copy.update({"exp":expire , "type" : "refresh"})
    
    return jwt.encode(data_copy , SECRET_KEY , algorithm=ALGORITHM)


def jwt_decode (auth : Annotated[HTTPAuthorizationCredentials , Depends(security)]) :
    token = auth.credentials
    try :
        token_deocde = jwt.decode(token , SECRET_KEY , [ALGORITHM])
        
        if token_deocde.get("type") != "access" :
            
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED ,
                                detail="Invalid token type")
            
        user_id = token_deocde.get("user_id")
        return user_id
    
    except ExpiredSignatureError :
        raise HTTPException(status_code=401, detail="Token expired")
    
    except PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
    
def jwt_decode_refresh(auth: Annotated[HTTPAuthorizationCredentials, Depends(security)]):
    token = auth.credentials
    
    try:
        token_decode = jwt.decode(token, SECRET_KEY, [ALGORITHM])
        if token_decode.get("type") != "refresh":
            raise HTTPException(status_code=401, detail="Invalid token type")
        return token_decode
    
    except ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Refresh token expired")
    
    except PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid refresh token")