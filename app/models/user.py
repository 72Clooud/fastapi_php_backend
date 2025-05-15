from sqlalchemy import Column, Integer, String, TIMESTAMP, text, Date
from database.database import Base

class User(Base):

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, nullable=False, index=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False, unique=True)
    dateOfBirth = Column(Date, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('NOW()'))