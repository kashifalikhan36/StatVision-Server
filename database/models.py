from sqlalchemy import Column, Integer, String, LargeBinary, DateTime
from database.database import Base
from datetime import datetime
from database.database import engine

class Dbaudio(Base):
    __tablename__ = "audio"
    id = Column(Integer, primary_key=True, index=True)
    user_text = Column(String)
    user_language = Column(String)
    blessi_text = Column(String)
    mail_status = Column(String)
    mail_data = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)

Dbaudio.metadata.create_all(bind=engine)