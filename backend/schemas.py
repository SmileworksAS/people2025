from pydantic import BaseModel
from datetime import datetime

class UserCreate(BaseModel):
    email: str
    password: str
    full_name: str

class UserOut(BaseModel):
    id: int
    email: str
    full_name: str

class MessageCreate(BaseModel):
    content: str

class MessageOut(BaseModel):
    id: int
    content: str
    sender_id: int
    timestamp: datetime

class AppointmentCreate(BaseModel):
    title: str
    start_time: datetime
    end_time: datetime

class AppointmentOut(BaseModel):
    id: int
    title: str
    start_time: datetime
    end_time: datetime

class NewsPostCreate(BaseModel):
    title: str
    content: str

class NewsPostOut(BaseModel):
    id: int
    title: str
    content: str
    created_at: datetime
