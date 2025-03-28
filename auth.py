from datetime import datetime, timedelta
from typing import Optional
import jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone

# Secret key for JWT (Change this in production)
SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60  # 1 hour expiry

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Function to generate JWT Token
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire.timestamp()})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
