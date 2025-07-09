from fastapi import FastAPI, Depends, HTTPException, status, WebSocket
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .models import Base, User, Message, Appointment, NewsPost
from .schemas import UserCreate, UserOut, MessageCreate, MessageOut, AppointmentCreate, AppointmentOut, NewsPostCreate, NewsPostOut
from .auth import verify_password, get_password_hash, create_access_token, get_current_user
import websockets
import os

# Use Fly.io PostgreSQL credentials
SQLALCHEMY_DATABASE_URL = "postgresql://orbdeqio_user_people:*4A6jds.egXF@db-host:5432/orbdeqio_people"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

app = FastAPI()

Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Authentication
@app.post("/signup", response_model=UserOut)
async def signup(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed_password = get_password_hash(user.password)
    db_user = User(email=user.email, hashed_password=hashed_password, full_name=user.full_name)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}

# Chat (WebSocket)
@app.websocket("/ws/chat")
async def websocket_endpoint(websocket: WebSocket, db: Session = Depends(get_db)):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            message = Message(content=data, sender_id=1)  # Replace with authenticated user
            db.add(message)
            db.commit()
            await websocket.send_text(f"Message: {data}")
    except WebSocketDisconnect:
        await websocket.close()

# Calendar
@app.post("/appointments", response_model=AppointmentOut)
async def create_appointment(appointment: AppointmentCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    db_appointment = Appointment(**appointment.dict(), user_id=current_user.id)
    db.add(db_appointment)
    db.commit()
    db.refresh(db_appointment)
    return db_appointment

@app.get("/appointments", response_model=list[AppointmentOut])
async def get_appointments(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return db.query(Appointment).filter(Appointment.user_id == current_user.id).all()

# News Feed
@app.post("/news", response_model=NewsPostOut)
async def create_news_post(post: NewsPostCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    db_post = NewsPost(**post.dict())
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post

@app.get("/news", response_model=list[NewsPostOut])
async def get_news_posts(db: Session = Depends(get_db)):
    return db.query(NewsPost).order_by(NewsPost.created_at.desc()).all()
