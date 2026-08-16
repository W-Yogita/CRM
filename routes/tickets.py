# routes/tickets.py
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import or_
from typing import List, Optional
from pydantic import BaseModel, EmailStr
from datetime import datetime

import database
import models

router = APIRouter(prefix="/api/tickets", tags=["Tickets"])

# -------------------------------------------------------------------
# HELPER: AUTO TRIAGE LOGIC
# -------------------------------------------------------------------
def auto_triage(description: str, subject: str):
    text = (description + " " + subject).lower()
    
    urgent_keywords = ["urgent", "broken", "refund", "fraud", "not working", "frustrated", "immediately", "critical", "emergency", "asap"]
    high_keywords = ["delayed", "wrong", "missing", "error", "failed", "issue", "problem", "help"]
    
    categories = {
        "Billing": ["refund", "charge", "payment", "invoice", "billing", "money", "price"],
        "Shipping": ["delivery", "shipped", "tracking", "delay", "package", "courier", "transit"],
        "Product": ["broken", "defect", "quality", "damaged", "not working", "malfunction"],
        "Account": ["login", "password", "access", "account", "email", "reset", "locked"]
    }
    
    if any(word in text for word in urgent_keywords):
        urgency = "Critical"
        priority = 1
    elif any(word in text for word in high_keywords):
        urgency = "High"
        priority = 2
    else:
        urgency = "Normal"
        priority = 3
    
    detected_category = "General"
    for category, keywords in categories.items():
        if any(word in text for word in keywords):
            detected_category = category
            break
    
    return {
        "urgency": urgency,
        "priority": priority,
        "category": detected_category,
        "auto_tagged": True
    }

# -------------------------------------------------------------------
# PYDANTIC SCHEMAS
# -------------------------------------------------------------------
class TicketCreate(BaseModel):
    customer_name: str
    customer_email: EmailStr
    subject: str
    description: str

class TicketUpdate(BaseModel):
    status: Optional[str] = None
    note_text: Optional[str] = None

class NoteResponse(BaseModel):
    id: int
    note_text: str
    created_at: datetime

    class Config:
        from_attributes = True

class TicketDetailResponse(BaseModel):
    ticket_id: str
    customer_name: str
    customer_email: str
    subject: str
    description: str
    status: str
    urgency: str
    priority: int
    category: str
    auto_tagged: bool
    created_at: datetime
    updated_at: datetime
    notes: List[NoteResponse] = []

    class Config:
        from_attributes = True

def generate_ticket_id(db: Session) -> str:
    count = db.query(models.Ticket).count()
    return f"TKT-{count + 1:03d}"

# -------------------------------------------------------------------
# API ENDPOINTS
# -------------------------------------------------------------------

@router.post("", status_code=201)
def create_ticket(ticket_data: TicketCreate, db: Session = Depends(database.get_db)):
    new_ticket_id = generate_ticket_id(db)
    
    # Run auto-triage step
    triage = auto_triage(ticket_data.description, ticket_data.subject)
    
    db_ticket = models.Ticket(
        ticket_id=new_ticket_id,
        customer_name=ticket_data.customer_name,
        customer_email=ticket_data.customer_email,
        subject=ticket_data.subject,
        description=ticket_data.description,
        status="Open",
        urgency=triage["urgency"],
        priority=triage["priority"],
        category=triage["category"],
        auto_tagged=triage["auto_tagged"]
    )
    
    db.add(db_ticket)
    db.commit()
    db.refresh(db_ticket)
    
    return {
        "ticket_id": db_ticket.ticket_id,
        "created_at": db_ticket.created_at,
        "auto_triage": triage
    }

@router.get("")
def get_tickets(
    status: Optional[str] = Query(None),
    search: Optional[str] = Query(None),
    db: Session = Depends(database.get_db)
):
    query = db.query(models.Ticket)
    
    if status:
        query = query.filter(models.Ticket.status == status)
        
    if search:
        search_term = f"%{search}%"
        query = query.filter(
            or_(
                models.Ticket.customer_name.ilike(search_term),
                models.Ticket.customer_email.ilike(search_term),
                models.Ticket.ticket_id.ilike(search_term),
                models.Ticket.subject.ilike(search_term)
            )
        )
        
    tickets = query.order_by(models.Ticket.created_at.desc()).all()
    
    return [
        {
            "ticket_id": t.ticket_id,
            "customer_name": t.customer_name,
            "subject": t.subject,
            "status": t.status,
            "urgency": t.urgency,
            "priority": t.priority,
            "category": t.category,
            "auto_tagged": t.auto_tagged,
            "created_at": t.created_at.isoformat() if t.created_at else None
        }
        for t in tickets
    ]

@router.get("/{ticket_id}", response_model=TicketDetailResponse)
def get_ticket_detail(ticket_id: str, db: Session = Depends(database.get_db)):
    ticket = db.query(models.Ticket).filter(models.Ticket.ticket_id == ticket_id).first()
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    return ticket

@router.put("/{ticket_id}")
def update_ticket(
    ticket_id: str,
    update_data: TicketUpdate,
    db: Session = Depends(database.get_db)
):
    ticket = db.query(models.Ticket).filter(models.Ticket.ticket_id == ticket_id).first()
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
        
    if update_data.status:
        ticket.status = update_data.status
        
    if update_data.note_text:
        new_note = models.Note(
            ticket_id=ticket.ticket_id,
            note_text=update_data.note_text
        )
        db.add(new_note)
        
    db.commit()
    db.refresh(ticket)
    
    return {"success": True, "updated_at": ticket.updated_at}