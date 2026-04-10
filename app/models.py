from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from .database import Base


class Client(Base):
    __tablename__ = "clients"

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String(30), unique=True, nullable=False, index=True)
    name = Column(String(150), nullable=False)
    phone = Column(String(30), nullable=True)
    address = Column(String(255), nullable=True)
    zone = Column(String(120), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    events = relationship("AlarmEvent", back_populates="client")


class AlarmEvent(Base):
    __tablename__ = "alarm_events"

    id = Column(Integer, primary_key=True, index=True)
    client_id = Column(Integer, ForeignKey("clients.id"), nullable=False)
    protocol = Column(String(40), nullable=False, default="CONTACT-ID")
    event_code = Column(String(20), nullable=False)
    partition = Column(String(20), nullable=True)
    zone = Column(String(20), nullable=True)
    message = Column(String(255), nullable=False)
    status = Column(String(30), nullable=False, default="novo", index=True)
    operator = Column(String(100), nullable=True)
    notes = Column(Text, nullable=True)
    source = Column(String(30), nullable=False, default="receptor_ip")
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    client = relationship("Client", back_populates="events")
