from fastapi.responses import HTMLResponse
from db import SessionDep
from fastapi import APIRouter, HTTPException, Request, Form, File, UploadFile
from models import User, UserCreate
from sqlmodel import select
from fastapi.templating import Jinja2Templates
from typing import Optional

from supa.supabase import upload_to_bucket

router = APIRouter()

templates = Jinja2Templates(directory="templates")


@router.post("/", response_model=User, status_code=201)
async def create_user(request: Request,
                      session: SessionDep,
                      name: str = Form(...),
                      year: int = Form(...),
                      status: bool = Form(True),
                      img: Optional[UploadFile] = File(None)
                      ):

    img_url = None
    if img:
        try:
            img_url = await upload_to_bucket(img)
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))

    try:
        new_user = UserCreate(name=name, year=year, status=status, img=img_url)

        user = User.model_validate(new_user)
        session.add(user)
        await session.commit()
        await session.refresh(user)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    return user


@router.get("/{user_id}", response_class=HTMLResponse)
async def get_one_user(request: Request, user_id: int, session: SessionDep):
    user_db = await session.get(User, user_id)
    if not user_db:
        raise HTTPException(status_code=404, detail="User not found")
    return templates.TemplateResponse("user.html", {"request": request, "user": user_db})

##Adicion de un CARD para user y se inyecta en cada uno segun se requiere
## Separar en user_detail y user_list

@router.get("/", response_class=HTMLResponse)
async def get_all_users(request: Request, session: SessionDep):
    result = await session.execute(select(User))
    users = result.scalars().all()
    return templates.TemplateResponse("user.html",
                                      {"request": request, "user": users})
