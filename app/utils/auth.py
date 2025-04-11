from datetime import datetime, timedelta, timezone
import os
import jwt, secrets
from jwt.exceptions import InvalidTokenError

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

def create_access_token(data: dict, expiries_delta: timedelta | None = None):
    to_encode = data.copy()
    if expiries_delta:
        expire = datetime.now(timezone.utc) + expiries_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt