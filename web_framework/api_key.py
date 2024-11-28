from fastapi import FastAPI, Depends, Security, HTTPException, status, Response, Cookie, Request
import uvicorn
from fastapi.security import APIKeyHeader, APIKeyCookie, HTTPBasic, HTTPBasicCredentials
from fastapi.responses import JSONResponse
from typing import Annotated
import secrets
from pydantic import BaseModel
from jose import JWTError, jwt
from passlib.context import CryptContext

# to get a string like this run:
# openssl rand -hex 32
SECRET_KEY = "7ac1f34550626327b09a57148e2e9de1a1e38052a8003d2596dcf1c04b4d83f0"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
    
api_key_header = APIKeyHeader(name="X-API-Key")
cookie_scheme = APIKeyCookie(name="session")
http_basic = HTTPBasic()
app = FastAPI()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

api_keys={"key1":"value1"}
cookies = {"key1":"value1"}
users = {"apple":"123"}
users_db = {
    "apple":{
        "username": "apple",
        "hashed_password": "$2b$12$Uu1vGRWzsTo1ZZhK7EqVGeROlmRhC1e8DgSR2XQ24Q60cJN9Vz0Ti" #123
    },
    "apple2":{
        "username": "apple",
        "hashed_password": "$2b$12$Uu1vGRWzsTo1ZZhK7EqVGeROlmRhC1e8DgSR2XQ24Q60cJN9Vz0Ti" #123
    }
    
}

def check_api_key_header(api_header: str=Security(api_key_header)):
    if api_header not in api_keys:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing or invalid API key"
        )
    return api_keys[api_header]

def check_api_key_cookie(cookie: str=cookie_scheme):
    print(cookie)
    if cookie not in cookies:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing or invalid API key"
        )
    return cookies[cookie]

class User(BaseModel):
    username: str
    password: str
    
def get_password_hash(password):
    return pwd_context.hash(password)

def if_user_exists(db, username: str):
    return username in db

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def authenticate_user(users_db, user:Annotated[User, Depends()]):
    exist = if_user_exists(users_db, user.username)
    if not exist or not verify_password(user.password, users_db[user.username]["hashed_password"])  :
        return False
    return True


def get_current_sign_in_user(request:Request):
    if len(request.cookies) == 1:
        username = list(request.cookies.keys())[0]
        return username
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid cookie",
        )
    
@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/sign_in_cookie", tags=["Sign in & return Cookies"])
async def sign_in_cookie(account: Annotated[User, Depends()], request:Request):
    if not authenticate_user(users_db, account):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if request.cookies:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Already sign in",
            headers={"WWW-Authenticate": "Bearer"},
        )
    response = JSONResponse(content={"Result": "Success"})
    response.set_cookie(key=account.username+"_hashed_session", value=account.username)
    return response

@app.get("/logout_cookie", tags=["Sign out & Delete Cookies"])
async def session_logout(response: Response, current_user: Annotated[str, Depends(get_current_sign_in_user)]):
    response.delete_cookie(key=current_user)
    return {"status": "logged out"}
    

@app.get("/basic_auth", tags=["Auth: Basic auth"])
async def basic_auth(credentials: Annotated[HTTPBasicCredentials, Depends(http_basic)]):
    if not credentials.username in users:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Basic"},
        )

    correct_password_bytes = users[credentials.username].encode('ascii')
    current_password_bytes = credentials.password.encode("utf8")
    is_correct_password = secrets.compare_digest(
        current_password_bytes, correct_password_bytes
    )
    if not is_correct_password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username

@app.get("/auth_header",tags=["Auth: APIkeyheader"])
async def auth_keys(user:dict = Depends(check_api_key_header)):
    return user

@app.get("/auth_cookie",tags=["Auth: APIkeycookie"])
async def auth_cookies(session: str = Depends(check_api_key_cookie)):
    return session

if __name__ == "__main__":
    # Start the sever, set reload=True for testing
    uvicorn.run("api_key:app", host="0.0.0.0", port=8032, log_level="info", reload=True)
