from app.core.config import Base
from sqlalchemy.orm import Mapped , mapped_column


class CreateUsers (Base) :
    
    __tablename__ = "users"
    
    id : Mapped[int] = mapped_column(primary_key=True)
    email : Mapped[str] = mapped_column()
    password : Mapped[int] = mapped_column()
    telegram_chat_id : Mapped[str] = mapped_column()
    is_active : Mapped[bool] = mapped_column(default=True)