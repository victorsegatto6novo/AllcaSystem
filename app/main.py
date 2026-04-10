from __future__ import annotations

from collections import defaultdict

from fastapi import Depends, FastAPI, Form, HTTPException, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session, joinedload

from . import models, schemas
from .database import Base, engine, get_db

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Allca Alarm Monitor", version="0.1.0")
app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")

KANBAN_STATUSES = ["novo", "triagem", "em_atendimento", "finalizado"]


@app.get("/", response_class=HTMLResponse)
def dashboard(request: Request, db: Session = Depends(get_db)):
    events = (
        db.query(models.AlarmEvent)
        .options(joinedload(models.AlarmEvent.client))
        .order_by(models.AlarmEvent.created_at.desc())
        .limit(200)
        .all()
    )
    grouped = defaultdict(list)
    for event in events:
        grouped[event.status].append(event)

    return templates.TemplateResponse(
        request,
        "dashboard.html",
        {
            "statuses": KANBAN_STATUSES,
            "grouped": grouped,
        },
    )


@app.get("/clients", response_class=HTMLResponse)
def clients_page(request: Request, db: Session = Depends(get_db)):
    clients = db.query(models.Client).order_by(models.Client.name.asc()).all()
    return templates.TemplateResponse(
        request,
        "clients.html",
        {
            "clients": clients,
        },
    )


@app.post("/clients")
def create_client(
    code: str = Form(...),
    name: str = Form(...),
    phone: str | None = Form(default=None),
    address: str | None = Form(default=None),
    zone: str | None = Form(default=None),
    db: Session = Depends(get_db),
):
    if db.query(models.Client).filter(models.Client.code == code).first():
        raise HTTPException(status_code=400, detail="Código de cliente já cadastrado")

    client = models.Client(code=code, name=name, phone=phone, address=address, zone=zone)
    db.add(client)
    db.commit()
    return RedirectResponse("/clients", status_code=303)


@app.get("/api/events", response_model=list[schemas.AlarmEventOut])
def list_events(db: Session = Depends(get_db)):
    return (
        db.query(models.AlarmEvent)
        .options(joinedload(models.AlarmEvent.client))
        .order_by(models.AlarmEvent.created_at.desc())
        .limit(500)
        .all()
    )


@app.post("/api/events", response_model=schemas.AlarmEventOut)
def create_event(payload: schemas.AlarmEventCreate, db: Session = Depends(get_db)):
    client = db.query(models.Client).filter(models.Client.id == payload.client_id).first()
    if not client:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")

    event = models.AlarmEvent(**payload.model_dump())
    db.add(event)
    db.commit()
    db.refresh(event)
    return event


@app.patch("/api/events/{event_id}", response_model=schemas.AlarmEventOut)
def update_event_status(
    event_id: int,
    payload: schemas.AlarmEventStatusUpdate,
    db: Session = Depends(get_db),
):
    if payload.status not in KANBAN_STATUSES:
        raise HTTPException(status_code=400, detail="Status inválido")

    event = db.query(models.AlarmEvent).filter(models.AlarmEvent.id == event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Evento não encontrado")

    event.status = payload.status
    event.operator = payload.operator
    event.notes = payload.notes
    db.commit()
    db.refresh(event)
    return event
