from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from typing import List
from pydantic import BaseModel
from datetime import datetime
from io import StringIO
import csv
from DB import engine, User, Pushup, Base, sessionmaker, UUID
from datetime import datetime

app = FastAPI()

# Создаем сессию
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# A Pydantic Place
class PPushup(BaseModel):
    id: str
    number: int
    created_at: datetime
    user: str

    class Config:
        from_attributes = True

# Загружаем модели
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Запрос пользователя по ID
@app.get('/users/{user_id}')
def read_user(user_id: str, db: Session = Depends(get_db)):
    user = db.query(User).filter_by(id=user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail='User not found')
    return {'id': str(user.id), 'tg_id': user.tg_id}

# Запрос всех отжиманий
@app.get('/pushups/')
def read_pushups(db: Session = Depends(get_db)):
    pushups = db.query(Pushup).all()
    return [{'id': str(pushup.id), 'number': pushup.number, 'created_at': pushup.created_at, 'user': pushup.user} for pushup in pushups]

# Создание отжимания
@app.post('/pushups/', response_model=PPushup)
def create_pushup(pushup: PPushup, db: Session = Depends(get_db)):
    pushup_obj = db.query(Pushup).filter_by(id=pushup.id).first()

    if not pushup_obj:
        pushup_obj = Pushup(number=pushup.number, created_at=pushup.created_at, user=pushup.user)
        db.add(pushup_obj)
    else:
        pushup_obj.number = pushup.number
        pushup_obj.created_at = pushup.created_at
        pushup_obj.user = pushup.user

    db.commit()
    db.refresh(pushup_obj)
    return PPushup.from_orm(pushup_obj)

# Загрузка данных в CSV-файл
@app.get('/csv')
def create_csv(request: Request, db: Session = Depends(get_db)):
    pushups = db.query(Pushup).all()
    headers = ['ID', 'Количество', 'Дата', 'ID пользователя']
    data = [[str(pushup.id), pushup.number, pushup.created_at, str(pushup.user)] for pushup in pushups]
    response = StringIO()
    writer = csv.writer(response)
    writer.writerow(headers)
    writer.writerows(data)
    return response.getvalue()