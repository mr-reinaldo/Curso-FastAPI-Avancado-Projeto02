from sqlalchemy import Column, String, Float, DateTime, UUID, ForeignKey, Integer
from sqlalchemy.orm import relationship
from app.core.settings import settings
from datetime import datetime
from pytz import timezone
from uuid import uuid4


class ProductModel(settings.DATABASE_BASE_MODEL):

    __tablename__ = "products"

    uuid = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid4)
    category_uuid = Column(UUID(as_uuid=True), ForeignKey("categories.uuid"))

    name = Column(String, nullable=False)
    slug = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    stock = Column(Integer, nullable=False)

    created_at = Column(
        DateTime, nullable=False, default=datetime.now(timezone(settings.TIMEZONE))
    )
    updated_at = Column(
        DateTime,
        nullable=False,
        default=datetime.now(timezone(settings.TIMEZONE)),
        onupdate=datetime.now(timezone(settings.TIMEZONE)),
    )

    category = relationship("CategoryModel", back_populates="products", lazy="joined")

    def __repr__(self):
        return f"<ProductModel(uuid={self.uuid}, name={self.name}, price={self.price})>"
