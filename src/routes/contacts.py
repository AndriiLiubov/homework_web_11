from typing import List, Optional
from datetime import date, timedelta

from fastapi import APIRouter, HTTPException, Depends, status, Query
from sqlalchemy.orm import Session

from src.database.db import get_db
from src.schemas import ContactBase, ContactResponse
from src.repository import contacts as repository_contacts

router = APIRouter(prefix='/contacts', tags=["contacts"])


@router.get("/", response_model=List[ContactResponse])
async def read_contacts(
    skip: int = 0, 
    limit: int = 100, 
    first_name: Optional[str] = Query(None, max_length=50),
    last_name: Optional[str] = Query(None, max_length=50),
    email: Optional[str] = Query(None, max_length=100),
    db: Session = Depends(get_db)
):
    contacts = await repository_contacts.get_contacts(skip, limit, db, first_name, last_name, email)
    return contacts


@router.get("/{contact_id}", response_model=ContactResponse)
async def read_contacts(contact_id: int, db: Session = Depends(get_db)):
    contact = await repository_contacts.get_contact(contact_id, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    return contact


@router.post("/", response_model=ContactResponse)
async def create_contact(body: ContactBase, db: Session = Depends(get_db)):
    return await repository_contacts.create_contact(body, db)


@router.put("/{contact_id}", response_model=ContactResponse)
async def update_contact(body: ContactBase, contact_id: int, db: Session = Depends(get_db)):
    contact = await repository_contacts.update_contact(contact_id, body, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    return contact


@router.delete("/{contact_id}", response_model=ContactResponse)
async def remove_contact(contact_id: int, db: Session = Depends(get_db)):
    contact = await repository_contacts.remove_contact(contact_id, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    return contact


@router.get("/upcoming_birthdays/", response_model=List[ContactResponse])
async def get_upcoming_birthdays(db: Session = Depends(get_db)):
    contacts = await repository_contacts.get_upcoming_birthdays(db)
    return contacts