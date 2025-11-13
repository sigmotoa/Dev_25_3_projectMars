import datetime
from sqlmodel import SQLModel, Field, Relationship
from utils import Kind
from typing import Optional


class UserBase(SQLModel):
    name: str | None = Field(description="User name")
    year: int | None = Field(description="User year")
    status: bool | None = Field(description="User status", default=True)
    img:Optional[str] = Field(description="User image", default=None)

class PetBase(SQLModel):
    name: str  | None = Field(description="Pet name")
    year: int  | None= Field(description="Pet year")
    kind: Kind  | None = Field(description="Pet kind", default=Kind.Dog)
    alive: bool | None = Field(description="Pet alive", default=True)

class VetBase(SQLModel):
    name: str | None = Field(description="Vet name")

class AppointmentBase(SQLModel):
    pet_id: int
    vet_id: int

class Appointment(AppointmentBase, table=True):
    vet_id: int | None = Field(default=None,foreign_key="vet.id", primary_key=True)
    pet_id: int | None = Field(default=None, foreign_key="pet.id", primary_key=True)
    date: datetime.datetime | None = Field(default_factory=datetime.datetime.now)



class User(UserBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    pets: list["Pet"] = Relationship(back_populates="user")


class Pet(PetBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    user_id:int =Field(foreign_key="user.id")
    user: User = Relationship(back_populates="pets")

    vets: list["Vet"] = Relationship(back_populates="pets", link_model=Appointment)

class Vet(VetBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    pets: list["Pet"] = Relationship(back_populates="vets", link_model=Appointment)

class UserCreate(UserBase):
    img:Optional[str] = None


class PetCreate(PetBase):
    user_id:int =Field(foreign_key="user.id")

class PetUpdate(PetBase):
    pass


class VetCreate(VetBase):
    pass


class AppointmentCreate(AppointmentBase):
    pass


