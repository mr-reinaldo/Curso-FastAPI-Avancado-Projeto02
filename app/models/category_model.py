from sqlalchemy import Column, String, DateTime, UUID
from sqlalchemy.orm import relationship
from app.core.settings import settings
from datetime import datetime
from pytz import timezone
from uuid import uuid4


class CategoryModel(settings.DATABASE_BASE_MODEL):

    __tablename__ = "categories"

    uuid = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid4)
    name = Column(String, nullable=False)
    slug = Column(String, nullable=False)
    created_at = Column(
        DateTime, nullable=False, default=datetime.now(timezone(settings.TIMEZONE))
    )
    updated_at = Column(
        DateTime,
        nullable=False,
        default=datetime.now(timezone(settings.TIMEZONE)),
        onupdate=datetime.now(timezone(settings.TIMEZONE)),
    )

    products = relationship(
        "ProductModel",
        back_populates="category",
        uselist=True,
        lazy="joined",
        cascade="all, delete-orphan",
    )

    def __repr__(self):
        return f"<CategoryModel(uuid={self.uuid}, name={self.name}, slug={self.slug})>"
