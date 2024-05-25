from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import status
from fastapi.exceptions import HTTPException
from app.schemas.responses import Message
from datetime import datetime, timezone
from uuid import UUID
from app.models.category_model import CategoryModel
from app.schemas.category_schema import (
    CategorySchemaCreate,
    CategorySchemaUpdate,
    ProductSchemaRead,
)
from typing import Optional, List


class CategoryController:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self) -> List[CategoryModel]:

        categories = self.db.query(CategoryModel).all()

        if not categories:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No categories found.",
            )

        return categories

    def get(self, uuid: UUID) -> CategoryModel:

        category = (
            self.db.query(CategoryModel).filter(CategoryModel.uuid == uuid).first()
        )

        if not category:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Category not found.",
            )

        return category

    def create(self, category: CategorySchemaCreate) -> CategoryModel:

        category_model = CategoryModel(**category.model_dump())

        try:
            category_exists = (
                self.db.query(CategoryModel)
                .filter(CategoryModel.name == category_model.name)
                .first()
            )

            if category_exists:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="Category already exists.",
                )

            self.db.add(category_model)
            self.db.commit()

            return Message(status=True, message="Category created successfully.")
        except IntegrityError:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Category already exists.",
            )

    def full_update(self, category: CategorySchemaUpdate, uuid: UUID) -> Message:

        category_model = (
            self.db.query(CategoryModel).filter(CategoryModel.uuid == uuid).first()
        )

        if not category_model:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Category not found.",
            )

        try:
            category_model.name = category.name
            category_model.description = category.description
            category_model.updated_at = datetime.now(timezone.utc)

            self.db.commit()

            return Message(status=True, message="Category updated successfully.")
        except IntegrityError:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Category already exists.",
            )

    def partial_update(self, category: CategorySchemaUpdate, uuid: UUID) -> Message:

        category_model = (
            self.db.query(CategoryModel).filter(CategoryModel.uuid == uuid).first()
        )

        if not category_model:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Category not found.",
            )

        try:
            if category.name:
                category_model.name = category.name
            if category.description:
                category_model.description = category.description

            category_model.updated_at = datetime.now(timezone.utc)

            self.db.commit()

            return Message(status=True, message="Category updated successfully.")
        except IntegrityError:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Category already exists.",
            )

    def delete(self, uuid: UUID) -> Message:

        category_model = (
            self.db.query(CategoryModel).filter(CategoryModel.uuid == uuid).first()
        )

        if not category_model:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Category not found.",
            )

        self.db.delete(category_model)
        self.db.commit()

        return Message(status=True, message="Category deleted successfully.")
