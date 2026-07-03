from app.core.config import Base
from datetime import datetime, timedelta
from sqlalchemy.orm import Mapped , mapped_column
from sqlalchemy import String


class UserTeste (Base) :
    
    __tablename__ = "userteste"
    
    id : Mapped[int] = mapped_column(primary_key=True)
    username :  Mapped[str] = mapped_column(String(100) , unique=True)
    password : Mapped[str] = mapped_column(String(100))
    email : Mapped[str] = mapped_column(String(60) , unique=True)
    code : Mapped[str] = mapped_column(String(20))
    attempts: Mapped[int] = mapped_column(default=0)
    expires_at: Mapped[datetime] = mapped_column(
        default=lambda: datetime.utcnow() + timedelta(minutes=5)
    )