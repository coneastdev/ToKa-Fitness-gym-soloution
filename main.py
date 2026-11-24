from datetime import datetime, timezone, timedelta, UTC
from typing import Annotated
import os

from fastapi import FastAPI, Request, Form, Depends, HTTPException, status
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlmodel import SQLModel, create_engine, Session, select
from pydantic import BaseModel, Field
from pwdlib import PasswordHash
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jwt.exceptions import InvalidTokenError
import jwt
from dotenv import load_dotenv

from dbClasses import *
import validation

# JWT classes
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: int | None = None

# db setup
sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"
engine = create_engine(sqlite_url, echo=False)
SQLModel.metadata.create_all(engine)

# jwt setup
password_hash = PasswordHash.recommended()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Database indexing
def look_for_user(email: str, password: str) -> str:
    with Session(engine) as session:
        statement = select(Users).where(Users.email == email)
        results = session.exec(statement)
        if results:
            for user in results:
                if password_hash.verify(password, user.password):
                    return "fullmatch"
                else:
                    return "wrongpassword"
    return "notfound"

def get_user_by_id(id: int) -> Users | None:
    with Session(engine) as session:
        statement = select(Users).where(Users.id == id)
        results = session.exec(statement)
        if results:
            for user in results:
                return user
    return None

# JWT token
def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(UTC) + expires_delta
    else:
        expire = datetime.now(UTC) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, os.getenv('SECRET_KEY'), algorithm=os.getenv('ALGORITHM'))
    return encoded_jwt

async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, os.getenv('SECRET_KEY'), algorithms=os.getenv('ALGORITHM'))
        username = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(id=username)
    except InvalidTokenError:
        raise credentials_exception
    if token_data.id:
        user = get_user_by_id(token_data.id)
    else:
        raise credentials_exception
    return user

async def get_current_active_user(
    current_user: Annotated[Users, Depends(get_current_user)],
):
    if not current_user.active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

# fast api app
app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def main(request: Request):
    return templates.TemplateResponse(request=request, name="index.html")

@app.post("/token")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> Token:
    user = authenticate_user(fake_users_db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    minutes = os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES')
    try:
        if minutes:
            minutes = float(minutes)
        else:
            minutes = 0
    except:
        minutes = 0
    access_token_expires = timedelta(minutes=minutes)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")

@app.get("/login", response_class=HTMLResponse)
async def login(request: Request):
    return templates.TemplateResponse(request=request, name="login.html")

@app.post("/login", response_class=HTMLResponse)
async def login_post(request: Request, email: Annotated[str, Form()], password: Annotated[str, Form()]):
    succues = False

    if look_for_user(email, password) == "fullmatch":
        succues = True

    if succues:
        return templates.TemplateResponse(request=request, name="index.html")
    else:
        return templates.TemplateResponse(request=request, name="login.html")

@app.get("/signup", response_class=HTMLResponse)
async def signup(request: Request):
    return templates.TemplateResponse(request=request, name="signup.html")

@app.post("/signup", response_class=HTMLResponse)
async def signup_post(request: Request, name: Annotated[str, Form()], email: Annotated[str, Form()], password: Annotated[str, Form()], dob: Annotated[str, Form()]):
    succues = False

    user = Users(name=name, email=email, dob=validation.convert(dob), password=password_hash.hash(password), created=datetime.now(timezone.utc), active=True, member=False, accountType=0)

    if look_for_user(email, password) == "notfound":
        try:
            with Session(engine) as session:
                session.add(user)
                session.commit()
            succues = True
        except Exception as e:
            print(e)
    else:
        print("found user when tried to create")
    
    print("test")
    if succues:
        return templates.TemplateResponse(request=request, name="login.html")
    else:
        return templates.TemplateResponse(request=request, name="signup.html")

