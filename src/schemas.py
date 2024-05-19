from datetime import date
from typing import Optional
from pydantic import BaseModel, EmailStr, Field

class ContactBase(BaseModel):
    first_name: str = Field(max_length=50)
    last_name: str = Field(max_length=50)
    email: EmailStr = Field(max_length=100)
    phone_number: str = Field(max_length=20)
    birth_date: date
    additional_info: Optional[str] = None


class ContactResponse(ContactBase):
    id: int

    class Config:
        orm_mode = True