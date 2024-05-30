from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import status
from fastapi.exceptions import HTTPException
from app.schemas.responses import Message
from datetime import datetime, timezone
from uuid import UUID
from app.models.product_model import ProductModel
from app.schemas.product_schema import (
    ProductSchemaCreate,
    ProductSchemaUpdate,
    ProductSchemaRead,
)
from typing import Optional, List


class ProductController:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self) -> List[ProductModel]:

        products = self.db.query(ProductModel).all()

        if not products:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No products found.",
            )

        return products

    def get(self, uuid: UUID) -> ProductModel:

        product = self.db.query(ProductModel).filter(ProductModel.uuid == uuid).first()

        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Product not found.",
            )

        return product

    def create(self, product: ProductSchemaCreate) -> Message:

        product_model = ProductModel(**product.model_dump())

        try:
            product_exists = (
                self.db.query(ProductModel)
                .filter(ProductModel.name == product_model.name)
                .first()
            )

            if product_exists:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="Product already exists.",
                )

            self.db.add(product_model)
            self.db.commit()

            return Message(status=True, message="Product created successfully.")
        except IntegrityError:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Product already exists.",
            )

    def full_update(self, product: ProductSchemaUpdate, uuid: UUID) -> Message:

        try:
            product_model = (
                self.db.query(ProductModel).filter(ProductModel.uuid == uuid).first()
            )

            if not product_model:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Product not found.",
                )

            product_model.name = product.name
            product_model.slug = product.slug
            product_model.price = product.price
            product_model.stock = product.stock
            product_model.category_uuid = product.category_uuid

            product_model.updated_at = datetime.now(timezone.utc)

            self.db.commit()

            return Message(status=True, message="Product updated successfully.")
        except IntegrityError:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Product already exists.",
            )

    def partial_update(self, product: ProductSchemaUpdate, uuid: UUID) -> Message:

        try:
            product_model = (
                self.db.query(ProductModel).filter(ProductModel.uuid == uuid).first()
            )

            if not product_model:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Product not found.",
                )

            if product.name:
                product_model.name = product.name
            if product.slug:
                product_model.slug = product.slug
            if product.price:
                product_model.price = product.price
            if product.stock:
                product_model.stock = product.stock
            if product.category_uuid:
                product_model.category_uuid = product.category_uuid

            product_model.updated_at = datetime.now(timezone.utc)

            self.db.commit()

            return Message(status=True, message="Product updated successfully.")
        except IntegrityError:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Product already exists.",
            )

    def delete(self, uuid: UUID) -> Message:

        product_model = (
            self.db.query(ProductModel).filter(ProductModel.uuid == uuid).first()
        )

        if not product_model:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Product not found.",
            )

        self.db.delete(product_model)
        self.db.commit()

        return Message(status=True, message="Product deleted successfully.")
