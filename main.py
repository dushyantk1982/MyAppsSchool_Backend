from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from pydantic import BaseModel
from ldap3 import Server, Connection, ALL
from auth import create_access_token, SECRET_KEY, ALGORITHM
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta, timezone
from fastapi.middleware.cors import CORSMiddleware
from auth_google import router as google_auth_router

# Load environment variables from .env file
load_dotenv()

# Access the LDAP server in the code
LDAP_SERVER = os.getenv("LDAP_SERVER")
LDAP_BASE_DN = os.getenv("LDAP_BASE_DN")
LDAP_ADMIN_DN = os.getenv("LDAP_ADMIN_DN")
LDAP_ADMIN_PASSWORD = os.getenv("LDAP_ADMIN_PASSWORD")
# SECRET_KEY = os.getenv("SECRET_KEY")

# print(f"LDAP Server: {LDAP_SERVER}")  # Debugging (remove later)

app = FastAPI()

# Include OAuth route
app.include_router(google_auth_router)

# Allow request from ReactJS
origins = [
    "http://localhost:5173", 
    "http://127.0.0.1:5173",
    "http://localhost",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Secret Key for JWT Configuration
SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

#Mock User Databse(Only for test)
fake_users_db = {
    "admin" : {"username" : "admin", "password" : "admin123", "role" : "admin"},
    "user" : {"username" : "user", "password" : "user123", "role" : "user"},
}

# OAuth2 Password flow for Login
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

#  Function to generate JWT Token
def create_access_token(data : dict, expires_delta : timedelta):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + expires_delta
    to_encode.update({"exp" : expire.timestamp()})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# Function to verify JWT token
def verify_token(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        exp = payload.get("exp")
        if exp and datetime.now(timezone.utc).timestamp() > exp:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token expired")
        return payload
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

# Function to get current user
async def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
        return payload
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Token")


# Function to authenticate user via LDAP
def authenticate_user(username: str, password: str):
    user_dn = f"cn={username},{LDAP_BASE_DN}"
    server = Server(LDAP_SERVER, get_info=ALL)
    try:
        conn = Connection(server, user=user_dn, password=password, auto_bind=True)
        return conn.bind()
    except:
        return False


# Login route to authenticate user and return JWT token
@app.post("/token")
def login(form_data: OAuth2PasswordRequestForm = Depends()):

    user = fake_users_db.get(form_data.username)

    if not user or user["password"] != form_data.password: 
        raise HTTPException(status_code=401, detail="Invalid Credentials")
    
    access_token = create_access_token(data={"sub": user["username"], "role": user["role"]},
                                       expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
                                       ) 
    return {"access_token": access_token, "token_type": "bearer"}

# Protected route (Only accessible with a valid token)
@app.get("/protected")
# async def protected_route(token: str = Depends(oauth2_scheme)):
async def protected_route(payload: dict = Depends(verify_token)):
    return {
        "message": f"Hello {payload['sub']}, you have accessed a protacted route",
          "role": payload["role"],
          }











    # try:
    #     payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    #     role = payload.get("role")
    #     username = payload.get("sub")
    #     return{"message" : f"Hello {username}, you have accessed a protected route!", "role": role}
    # except:
    #     raise HTTPException(status_code=401, detail="Invalid Credentials")


        # if not username:
        #     raise HTTPException(status_code=401, detail="Invalid Token")
    # except jwt.ExpireSignatureError:
    #     raise HTTPException(status_code=401, detail="Token Expired")
    # except jwt.InvalidTokenError:
    #     raise HTTPException(status_code=401, detail="Invalid Token")
    
    # return{"message" : f"Hello {username}, you have accessed a purotected route!", "role": role}


#  Define a Pydantic model for request body
# class LoginRequest(BaseModel):
#     username: str
#     password: str

# def authenticate_user(username: str, password: str):
#     """Authenticate user with LDAP server"""
#     user_dn = f"cn={username},{LDAP_BASE_DN}"
#     server = Server(LDAP_SERVER, get_info=ALL)
    
    # Try different formats for user_dn based on your LDAP setup
    # possible_dn_formats = [
    #     f"cn={username},{LDAP_BASE_DN}",
    #     f"uid={username},{LDAP_BASE_DN}",
    #     f"mail={username},{LDAP_BASE_DN}",
    #     f"sAMAccountName={username},{LDAP_BASE_DN}"
    # ]
    
    # server = Server(LDAP_SERVER, get_info=ALL)
    # for user_dn in possible_dn_formats:
    #     try:
    #         conn = Connection(server, user=user_dn, password=password, auto_bind=True)
    #         print(f"Authentication successful for {user_dn}")  # Debugging
    #         return {"message": "Authentication successful"}
    #     except Exception as e:
    #         print(f"Failed authentication for {user_dn}: {e}")  # Debugging

    # # If all attempts fail, return unauthorized error
    # raise HTTPException(status_code=401, detail="Invalid credentials")

    # try:
    #     conn = Connection(server, user=user_dn, password=password, auto_bind=AUTO_BIND_NO_TLS)
    #     return {"message": "Authentication successful", "user" : username}
    # except Exception:
    #     raise HTTPException(status_code=401, detail="Invalid credentials")

# @app.post("/login")
# def login(request: LoginRequest):
#     return authenticate_user(request.username, request.password)
