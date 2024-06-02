from sqlalchemy import Column, String, DateTime, UUID
from app.core.settings import settings
from datetime import datetime
from pytz import timezone
from uuid import uuid4


class UserModel(settings.DATABASE_BASE_MODEL):

    __tablename__ = "users"

    uuid = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid4)
    username = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(
        DateTime, nullable=False, default=datetime.now(timezone(settings.TIMEZONE))
    )
    updated_at = Column(
        DateTime,
        nullable=False,
        default=datetime.now(timezone(settings.TIMEZONE)),
        onupdate=datetime.now(timezone(settings.TIMEZONE)),
    )

    def __repr__(self):
        return f"<UserModel(uuid={self.uuid}, username={self.username}, email={self.email})>"
