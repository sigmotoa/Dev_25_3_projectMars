from fastapi.templating import Jinja2Templates
from fastapi import FastAPI, UploadFile, File, Form, Request, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
import bucket
import appoinment
import pet
import estudiantes
import user
import vet
from db import create_tables, init_db
##from pet import APIRouter

##Clever
from contextlib import asynccontextmanager
import os

from dotenv import load_dotenv


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db(app)
    yield


app = FastAPI(lifespan=lifespan, title="Pet API")

app.mount("/templates", StaticFiles(directory="templates"), name="templates")
app.mount("/static", StaticFiles(directory="bucket"), name="static")
templates = Jinja2Templates(directory="templates")
app.include_router(pet.router, tags=["pet"], prefix="/pets")
app.include_router(user.router, tags=["user"], prefix="/users")
app.include_router(vet.router, tags=["vet"], prefix="/vets")
app.include_router(appoinment.router, tags=["appointment"], prefix="/appointments")


# app.include_router(estudiantes.router, tags=["estudiantes"], prefix="/estudiantes" )

@app.post("/bucket")
async def save_bucket(file: UploadFile = File(...)):
    result = await bucket.upload_file(file)
    return result


@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="hello.html"

    )


@app.get("/hello/{name}", response_class=HTMLResponse)
async def say_hello(request:Request, name: str):
    return templates.TemplateResponse(
        "index.html",
        {"request": request, "name": name}
    )

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return templates.TemplateResponse(
        "error.html",
        {"request": request, "status_code": exc.status_code, "detail": exc.detail},
        status_code=exc.status_code,
    )




