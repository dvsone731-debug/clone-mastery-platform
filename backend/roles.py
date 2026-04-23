from fastapi import HTTPException
from jose import jwt

SECRET = "SUPER_SECRET_KEY"
ALGO = "HS256"

def require_role(token: str, allowed: list):
    try:
        data = jwt.decode(token, SECRET, algorithms=[ALGO])
        if data["role"] not in allowed:
            raise HTTPException(403, "Not authorized")
        return data
    except:
        raise HTTPException(401, "Invalid token")
