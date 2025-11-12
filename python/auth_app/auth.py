import uvicorn
from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from datetime import datetime, timedelta
import jwt
import bcrypt
from starlette.responses import HTMLResponse

from python.auth_app.users_db import close_db
from users_db import USERS_DB, new_user

app = FastAPI()
SECRET_KEY = "super_secret_key" # w praktyce trzymane w zmiennych środowiskowych
ALGORITHM = "HS256"
security = HTTPBearer()
class LoginData(BaseModel):
    username: str
    password: str

def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")

@app.post("/login")
def login(data: LoginData):
    username = data.username
    password = data.password.encode('utf-8')
    if username not in USERS_DB:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    hashed_pw = USERS_DB[username]['password']
    if not bcrypt.checkpw(password, hashed_pw):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    payload = {
        "sub": username,
        "is_admin": USERS_DB[username]['is_admin'],
        "iat": datetime.utcnow(),
        "exp": datetime.utcnow() + timedelta(hours=1)
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return {"access_token": token, "token_type": "bearer"}

@app.post("/register")
def register(data: LoginData ,user_data: dict = Depends(verify_token)):
    if not user_data.get("is_admin"):
        raise HTTPException(status_code=403, detail="You are not an admin")
    username = data.username
    password = data.password.encode('utf-8')
    if username in USERS_DB:
        raise HTTPException(status_code=401, detail="Username already registered")
    if new_user(username, password) == False:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return {"username" : username,"registering proccess" : "success"}

@app.get("/test")
def test(current_user: str = Depends(verify_token)):
    return {"test": "test"}

@app.get("/me")
def me(current_user: str = Depends(verify_token)):
    return current_user

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)
