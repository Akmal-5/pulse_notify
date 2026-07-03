from app.core.config import Base
from datetime import datetime
from sqlalchemy.orm import Mapped , mapped_column
from sqlalchemy import ForeignKey , String


class Target (Base) :
    
    __tablename__ = "target"
    id : Mapped[int] = mapped_column(primary_key=True)
    user_id : Mapped[int] = mapped_column(ForeignKey("users.id"))
    url : Mapped[str] = mapped_column(String(200))
    http_method : Mapped[str] = mapped_column(String(10) ,default="GET")
    interval_seconds : Mapped[int] = mapped_column(default=300)
    status : Mapped[str] = mapped_column(String(20) ,default="active")
    created_at : Mapped[datetime] = mapped_column(default=datetime.now)