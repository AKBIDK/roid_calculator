from datetime import datetime
from sqlalchemy import Column, Integer, String, Enum, DateTime
import enum
from app.database import Base

class UserRole(str, enum.Enum):
    VIEWER = "VIEWER"
    EDITOR = "EDITOR"
    ADMIN = "ADMIN"

class User(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    role = Column(Enum(UserRole), nullable=False, default=UserRole.VIEWER)
    criado_em = Column(DateTime, default=datetime.utcnow)
