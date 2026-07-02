from app.core.config import Base
from datetime import datetime
from sqlalchemy.orm import Mapped , mapped_column
from sqlalchemy import ForeignKey , BigInteger , Integer , Text

class CheckLog (Base) :
    
    __tablename__ = "checklog"
    
    id : Mapped[int] = mapped_column(BigInteger,  primary_key=True)
    target_id : Mapped[int] = mapped_column(ForeignKey("target.id" , ondelete="CASCADE"))
    status_code : Mapped[int | None] = mapped_column(Integer , nullable=True)
    is_up : Mapped[bool] = mapped_column(default=True)
    error_message : Mapped[str] = mapped_column(Text)
    checked_at : Mapped[datetime] = mapped_column(default=datetime.now , index=True)