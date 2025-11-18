from pydantic import BaseModel, EmailStr
from typing import List

class PermissionRead(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True


class ProfileRead(BaseModel):
    id: int
    name: str
    permissions: List[PermissionRead]

    class Config:
        from_attributes = True


class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str
    profile_id: int | None = None


class UserRead(BaseModel):
    id: int
    name: str
    email: EmailStr
    is_admin: bool
    profile: ProfileRead | None

    class Config:
        from_attributes = True
