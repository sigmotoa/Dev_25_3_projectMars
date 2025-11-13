from contextlib import asynccontextmanager
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi import FastAPI, UploadFile, File, Form, Request, HTTPException
from fastapi.staticfiles import StaticFiles
import appoinment
import pet
import estudiantes
import user
import vet
import images
from db import create_tables


##from pet import APIRouter

@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_tables(app)
    yield


app = FastAPI(lifespan=lifespan, title="Pet API")

app.mount("/templates", StaticFiles(directory="templates"), name="templates")
app.mount("/img", StaticFiles(directory="upload"), name="img")
app.include_router(pet.router, tags=["pet"], prefix="/pets")
app.include_router(user.router, tags=["user"], prefix="/users")
app.include_router(vet.router, tags=["vet"], prefix="/vets")
app.include_router(appoinment.router, tags=["appointment"], prefix="/appointments")

templates = Jinja2Templates(directory="templates")


# app.include_router(estudiantes.router, tags=["estudiantes"], prefix="/estudiantes" )


@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    result = await images.upload_file(file)
    return result


@app.get("/", response_class=HTMLResponse, status_code=200)
async def root(request: Request):
    return templates.TemplateResponse(
        request=request, name="index.html"
    )


@app.get("/hello/{name}", response_class=HTMLResponse)
async def say_hello(request: Request, name: str):
    return templates.TemplateResponse(
        request=request,
        name="hello.html",
        context={"texto": name.upper()}
    )

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return templates.TemplateResponse(
        "error.html",
        {"request": request, "status_code": exc.status_code, "detail": exc.detail},
        status_code=exc.status_code,
    )