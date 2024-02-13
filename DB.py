from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.dialects.postgresql import UUID
import uuid
from datetime import datetime


engine = create_engine('postgresql://postgres:password@127.0.0.1/test_db')

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tg_id = Column(Integer)



class Pushup(Base):
    __tablename__ = 'pushups'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4())
    number = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)
    user = Column(UUID, ForeignKey('users.id'))

    def __repr__(self):
        return f'Отжимания [ID: {self.id}, Количество: {self.number}, Дата: {self.created_at}'




# Создаем схему базы данных
Base.metadata.create_all(engine)

# Создаем сессию
Session = sessionmaker(bind=engine)
session = Session()

# Пример использования
# user1 = User(name='Alice', age=25)
# user2 = User(name='Bob', age=30)

# Добавляем записи в базу данных
# session.add(user1)
# session.add(user2)
session.commit()

# Закрываем сессию
session.close()
