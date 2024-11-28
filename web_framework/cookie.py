from fastapi import FastAPI, Depends, HTTPException, status, APIRouter
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import random
from fastapi import Request
from fastapi import Body
import uvicorn

# User Database (for demonstration purposes)
users = {}

# In-memory session storage (for demonstration purposes)
sessions = {}

app = FastAPI()

def authenticate_user(credentials: HTTPBasicCredentials = Depends(security)):
    user = users.get(credentials.username)
    if user is None or user["password"] != credentials.password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Basic"},
        )
    return user

@app.post("/signup")
def sign_up(username: str = Body(...), password: str = Body(...)):
    user = users.get(username)
    if user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Username already exists",
        )
    new_user_id = len(users) + 1
    new_user = {
        "username": username,
        "password": password,
        "user_id": new_user_id
    }
    users[username] = new_user
    return {"message": "User registered successfully"}

# Login endpoint - Creates a new session
@router.post("/login")
def login(user: dict = Depends(authenticate_user)):
    session_id = create_session(user["user_id"])
    return {"message": "Logged in successfully", "session_id": session_id}

if __name__ == "__main__":
    # Start the sever, set reload=True for testing
    uvicorn.run("cookie:app", host="0.0.0.0", port=8022, log_level="info", reload=True)