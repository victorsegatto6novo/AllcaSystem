from datetime import datetime

from pydantic import BaseModel


class ClientBase(BaseModel):
    code: str
    name: str
    phone: str | None = None
    address: str | None = None
    zone: str | None = None


class ClientCreate(ClientBase):
    pass


class ClientOut(ClientBase):
    id: int
    created_at: datetime

    model_config = {"from_attributes": True}


class AlarmEventBase(BaseModel):
    client_id: int
    protocol: str = "CONTACT-ID"
    event_code: str
    partition: str | None = None
    zone: str | None = None
    message: str
    source: str = "receptor_ip"


class AlarmEventCreate(AlarmEventBase):
    pass


class AlarmEventStatusUpdate(BaseModel):
    status: str
    operator: str | None = None
    notes: str | None = None


class AlarmEventOut(AlarmEventBase):
    id: int
    status: str
    operator: str | None = None
    notes: str | None = None
    created_at: datetime
    updated_at: datetime
    client: ClientOut

    model_config = {"from_attributes": True}
