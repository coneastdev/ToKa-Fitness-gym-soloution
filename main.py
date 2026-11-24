from datetime import datetime, timezone
from typing import Annotated

from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlmodel import SQLModel, create_engine, Session, select
from pydantic import BaseModel, Field

from dbClasses import *
import validation

sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

engine = create_engine(sqlite_url, echo=False)

SQLModel.metadata.create_all(engine)

def look_for_user(email: str, password: str) -> str:
    with Session(engine) as session:
        statement = select(Users).where(Users.email == email)
        results = session.exec(statement)
        if results:
            for user in results:
                if user.password == password:
                    return "fullmatch"
                else:
                    return "wrongpassword"
    return "notfound"

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def main(request: Request):
    return templates.TemplateResponse(request=request, name="index.html")

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

    password = validation.hash(password, email)

    user = Users(name=name, email=email, dob=validation.convert(dob), password=password, created=datetime.now(timezone.utc), active=True, member=False, accountType=0)

    if look_for_user(email, password) == "notfound":
        try:
            with Session(engine) as session:
                session.add(user)
                session.commit()
        except Exception as e:
            print(e)
    else:
        print("found user when tried to create")
    
    print("test")
    if succues:
        return templates.TemplateResponse(request=request, name="login.html")
    else:
        return templates.TemplateResponse(request=request, name="signup.html")

