from pydantic import BaseModel, constr
from typing import List, Optional

class UserBase(BaseModel):
    email: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    is_active: bool

    class Config:
        orm_mode = True

class PasswordResetResponse(BaseModel):
    msg: str

class PasswordReset(BaseModel):
    token: str
    new_password: constr(min_length=3) # type: ignore

class MagazineBase(BaseModel):
    title: str
    description: str

class Magazine(MagazineBase):
    id: int

    class Config:
        orm_mode = True

class SubscriptionPlanBase(BaseModel):
    magazine_id: int
    duration_months: int
    price: int
    discount_percentage: Optional[int] = 0


class SubscriptionPlan(SubscriptionPlanBase):
    id: int

    class Config:
        orm_mode = True

class SubscriptionBase(BaseModel):
    plan_id: int


class SubscriptionCreate(SubscriptionBase):
    magazine_id: int


class Subscription(SubscriptionBase):
    id: int
    user_id: int

    class Config:
        orm_mode = True
