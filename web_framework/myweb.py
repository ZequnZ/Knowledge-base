from datetime import datetime, timedelta, timezone
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel
import uvicorn

# to get a string like this run:
# openssl rand -hex 32
SECRET_KEY = "7ac1f34550626327b09a57148e2e9de1a1e38052a8003d2596dcf1c04b4d83f0"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

app = FastAPI()

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str | None = None


users_db = {
    "apple":{
        "username": "apple",
        "email": "appleme@qq.com",
        "hashed_password": "$2b$12$Uu1vGRWzsTo1ZZhK7EqVGeROlmRhC1e8DgSR2XQ24Q60cJN9Vz0Ti"
    }
}

class User(BaseModel):
    username: str
    email: str | None = None
    
class UserSignup(User):
    password: str
    
class UserInDB(User):
    hashed_password: str

def get_password_hash(password):
    return pwd_context.hash(password)

def add_user_into_db(username:str, user_dict: dict):
    users_db[username] = user_dict
    
def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def authenticate_user(users_db, username: str, password: str):
    user = get_user(users_db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

@app.post("/signup")
async def user_sign_up(user: Annotated[UserSignup, Depends()]) -> UserInDB:
    # existing user
    if user.username in users_db:
        raise HTTPException(status_code=400, detail="The username is existing")
    else:
        hashed_password = get_password_hash(user.password)
        
    print(user.username, hashed_password)
    
    # Create UserInDB instance
    user_in_db = UserInDB(username=user.username, email=user.email, hashed_password=hashed_password)
    
    # add user into db
    add_user_into_db(user.username, user_in_db.model_dump())
    return user_in_db

@app.post("/token")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
)-> Token:
    user = authenticate_user(users_db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    # else:
    #     return {"username": form_data.username, "result":'success'}
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")
    
    
async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = get_user(users_db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user    
    
@app.get("/users/me/", response_model=User)
async def read_users_me(
    current_user: Annotated[User, Depends(get_current_user)],
):
    return current_user
    

if __name__ == "__main__":
    # Start the sever, set reload=True for testing
    uvicorn.run("myweb:app", host="0.0.0.0", port=8002, log_level="info", reload=True)