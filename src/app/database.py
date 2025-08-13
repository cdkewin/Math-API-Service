from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import json
from passlib.context import CryptContext

DATABASE_URL = "sqlite:///./math.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class RequestLog(Base):
    __tablename__ = "request_log"
    id = Column(Integer, primary_key=True, index=True)
    operation = Column(String)
    input_data = Column(Text)
    result = Column(String)


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)


def init_db():
    Base.metadata.create_all(bind=engine)


def save_to_db(operation: str, input_data: dict, result):
    db = SessionLocal()
    log = RequestLog(
        operation=operation, input_data=json.dumps(input_data), result=str(result)
    )
    db.add(log)
    db.commit()
    db.close()


def get_user(username: str):
    db = SessionLocal()
    user = db.query(User).filter(User.username == username).first()
    db.close()
    return user


def create_user(username: str, password: str):
    db = SessionLocal()
    password_hash = pwd_context.hash(password)
    user = User(username=username, password_hash=password_hash)
    db.add(user)
    db.commit()
    db.close()


def verify_password(plain_password, password_hash):
    return pwd_context.verify(plain_password, password_hash)
