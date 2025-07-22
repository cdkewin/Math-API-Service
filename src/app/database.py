from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import json

DATABASE_URL = "sqlite:///./math.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()


class RequestLog(Base):
    __tablename__ = "request_log"
    id = Column(Integer, primary_key=True, index=True)
    operation = Column(String)
    input_data = Column(Text)
    result = Column(String)


def init_db():
    Base.metadata.create_all(bind=engine)


async def save_to_db(operation: str, input_data: dict, result):
    db = SessionLocal()
    log = RequestLog(
        operation=operation, input_data=json.dumps(input_data), result=str(result)
    )
    db.add(log)
    db.commit()
    db.close()
