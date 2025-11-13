from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from db import SessionDep
from fastapi import APIRouter, HTTPException, Request, Form, UploadFile, File
from models import User, UserCreate
from sqlmodel import select
from typing import Optional
from supabase_utils.supabase import upload_file_bucket

router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.post("/", response_model=User, status_code=201)
async def create_user(request: Request, session: SessionDep, name: str = Form(...), year: int = Form(...),
                      status: bool = Form(True), img: Optional[UploadFile] = File(None)):

    img_url = None
    if img:
        try:
            img_url = await upload_file_bucket(img)
        except Exception as e:
            raise HTTPException(status_code=404, detail=str(e))

    try:
        new_user = User(name=name, year=year, status=status, img=img_url)
        user = User.model_validate(new_user)
        session.add(user)
        await session.commit()
        await session.refresh(user)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))
    return user


@router.get("/{user_id}", response_class=HTMLResponse)
async def get_one_user(request: Request, user_id: int, session: SessionDep):
    user_db = await session.get(User, user_id)
    if not user_db:
        raise HTTPException(status_code=404, detail="User not found")
    return templates.TemplateResponse("user.html",
                                      {"request": request,
                                       "users": user_db}
                                      )


@router.get("/", response_class=HTMLResponse)
async def get_all_users(request: Request, session: SessionDep):
    query = select(User)

    result = await session.execute(select(User))

    users = result.scalars().all()
    return templates.TemplateResponse("user.html",
                                      {"request": request,
                                       "users": users})
