import re 
from datetime import datetime

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlmodel import Field, SQLModel, create_engine

import dbClasses

sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

engine = create_engine(sqlite_url, echo=True)

SQLModel.metadata.create_all(engine)

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")
 
# Uses adapated AI generated code from task 1 C
def validate_credentials(email: str, password: str) -> int: 
    """Check if email and password are valid"""
    email_valid = bool(re.fullmatch( 
        # contains text @ text . text
        r"[A-Za-z0-9.!#$%&'*+/=?^_`{|}~-]+"
        r"@[A-Za-z0-9](?:[A-Za-z0-9]{0,61}[A-Za-z0-9])?" 
        r"(?:\.[A-Za-z0-9](?:[A-Za-z0-9]{0,61}[A-Za-z0-9])?)+", email,)
    ) 
    
    password_valid = ( 
        # contains lowercase, uppercase, number and special char
        isinstance(password, str) 
        and len(password) >= 8 
        and re.search(r"[A-Z]", password)
        and re.search(r"[a-z]", password) 
        and re.search(r"\d", password) 
        and re.search(r"[^A-Za-z0-9]", password) 
    ) is not False 

    if email_valid and password_valid: 
        return 0 
    if not email_valid and not password_valid: 
        return 1 
    if not email_valid: 
        return 2 
    return 4 


@app.get("/", response_class=HTMLResponse)
async def main(request: Request):
    return templates.TemplateResponse(request=request, name="index.html")

@app.get("/login", response_class=HTMLResponse)
async def login(request: Request):
    return templates.TemplateResponse(request=request, name="login.html")

@app.post("/login", response_class=HTMLResponse)
async def login_post(request: Request):
    succues = False
    if succues:
        return templates.TemplateResponse(request=request, name="index.html")
    else:
        return templates.TemplateResponse(request=request, name="login.html")

@app.get("/signup", response_class=HTMLResponse)
async def signup(request: Request):
    return templates.TemplateResponse(request=request, name="signup.html")

@app.post("/signup", response_class=HTMLResponse)
async def signup_post(request: Request):
    succues = False
    if succues:
        return templates.TemplateResponse(request=request, name="index.html")
    else:
        return templates.TemplateResponse(request=request, name="signup.html")