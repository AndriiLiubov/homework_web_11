from typing import List, Optional
from datetime import date, timedelta

from sqlalchemy import extract
from sqlalchemy.orm import Session

from src.database.models import Contact
from src.schemas import ContactBase


async def get_contacts(
    skip: int, 
    limit: int, 
    db: Session,
    first_name: Optional[str] = None,
    last_name: Optional[str] = None,
    email: Optional[str] = None
) -> List[Contact]:
    query = db.query(Contact)
    
    if first_name:
        query = query.filter(Contact.first_name.ilike(f"%{first_name}%"))
    if last_name:
        query = query.filter(Contact.last_name.ilike(f"%{last_name}%"))
    if email:
        query = query.filter(Contact.email.ilike(f"%{email}%"))
    
    return query.offset(skip).limit(limit).all()


async def get_contact(contact_id: int, db: Session) -> Contact:
    return db.query(Contact).filter(Contact.id == contact_id).first()


async def create_contact(body: ContactBase, db: Session) -> Contact:
    contact = Contact(**body.model_dump(exclude_unset=True))
    db.add(contact)
    db.commit()
    db.refresh(contact)
    return contact


async def update_contact(contact_id: int, body: ContactBase, db: Session) -> Contact | None:
    contact = db.query(Contact).filter(Contact.id == contact_id).first()
    if contact:
        contact.first_name = body.first_name
        contact.last_name = body.last_name
        contact.email = body.email
        contact.phone_number = body.phone_number
        contact.birth_date = body.birth_date
        contact.additional_info = body.additional_info
        db.commit()
    return contact


async def remove_contact(contact_id: int, db: Session)  -> Contact | None:
    contact = db.query(Contact).filter(Contact.id == contact_id).first()
    if contact:
        db.delete(contact)
        db.commit()
    return contact

async def get_upcoming_birthdays(db: Session) -> List[Contact]:
    today = date.today()
    next_week = today + timedelta(days=7)
    
    today_month = today.month
    today_day = today.day
    next_week_month = next_week.month
    next_week_day = next_week.day
    
    if today_month == next_week_month:
        query = db.query(Contact).filter(
            extract('month', Contact.birth_date) == today_month,
            extract('day', Contact.birth_date).between(today_day, next_week_day)
        )
    else:
        query = db.query(Contact).filter(
            (extract('month', Contact.birth_date) == today_month) & (extract('day', Contact.birth_date) >= today_day) |
            (extract('month', Contact.birth_date) == next_week_month) & (extract('day', Contact.birth_date) <= next_week_day)
        )
    
    return query.all()
