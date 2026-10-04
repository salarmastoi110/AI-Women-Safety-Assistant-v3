from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models import models, schemas
from app.models.database import get_db

router = APIRouter(prefix="/api/contacts", tags=["contacts"])


@router.post("", response_model=schemas.ContactOut)
def add_contact(data: schemas.ContactIn, db: Session = Depends(get_db)):
    c = models.Contact(**data.model_dump())
    db.add(c); db.commit(); db.refresh(c)
    return c


@router.get("", response_model=List[schemas.ContactOut])
def list_contacts(db: Session = Depends(get_db)):
    return db.query(models.Contact).order_by(models.Contact.id).all()


@router.delete("/{contact_id}")
def delete_contact(contact_id: int, db: Session = Depends(get_db)):
    c = db.get(models.Contact, contact_id)
    if not c:
        raise HTTPException(404, "Contact not found")
    db.delete(c); db.commit()
    return {"deleted": contact_id}
