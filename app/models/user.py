from app.core.config import Base
from sqlalchemy.orm import Mapped , mapped_column
from sqlalchemy import String

class CreateUsers (Base) :
    
    __tablename__ = "users"
    
    id : Mapped[int] = mapped_column(primary_key=True)
    username : Mapped[str] = mapped_column(String(60) ,unique=True)
    email : Mapped[str] = mapped_column(String(60) , unique=True)
    password : Mapped[str] = mapped_column(String(100))
    telegram_chat_id : Mapped[str] = mapped_column(String(80))
    is_active : Mapped[bool] = mapped_column(default=True)