from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from db import SessionDep
from fastapi import APIRouter, HTTPException, Request
from models import User, UserCreate
from sqlmodel import select

router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.post("/", response_model=User, status_code=201)
async def create_user(new_user: UserCreate, session: SessionDep):
    user = User.model_validate(new_user)
    session.add(user)
    await session.commit()
    await session.refresh(user)
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
