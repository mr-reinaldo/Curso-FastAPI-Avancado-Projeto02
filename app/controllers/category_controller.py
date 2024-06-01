from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from sqlalchemy.future import select
from fastapi import status
from fastapi.exceptions import HTTPException
from fastapi_pagination import Params, Page
from fastapi_pagination.ext.sqlalchemy import paginate
from app.schemas.responses import Message
from datetime import datetime
from uuid import UUID
from app.models.category_model import CategoryModel
from app.schemas.category_schema import CategorySchemaCreate, CategorySchemaUpdate


class CategoryController:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self, page: int = 1, size: int = 50) -> Page[CategoryModel]:
        """
        Método para retornar uma lista de categorias.

        Parâmetros:
        - page: int (Página atual)
        - size: int (Quantidade de registros por página)

        Retorno:
        - Page[CategoryModel] (Lista de categorias)

        """
        query = select(CategoryModel).order_by(CategoryModel.created_at.desc())
        params = Params(page=page, size=size)

        return paginate(self.db, query, params)

    def get(self, uuid: UUID) -> CategoryModel:
        """
        Método para retornar uma categoria.

        Parâmetros:
        - uuid: UUID (Identificador da categoria)

        Retorno:
        - CategoryModel (Categoria)
        """
        category = (
            self.db.query(CategoryModel).filter(CategoryModel.uuid == uuid).first()
        )

        if not category:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Category not found.",
            )

        return category

    def create(self, category: CategorySchemaCreate) -> Message:
        """
        Método para criar uma categoria.

        Parâmetros:
        - category: CategorySchemaCreate (Categoria)

        Retorno:
        - Message (Mensagem de retorno)
        """
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
        """
        Método para atualizar uma categoria.

        Parâmetros:
        - category: CategorySchemaUpdate (Categoria)
        - uuid: UUID (Identificador da categoria)

        Retorno:
        - Message (Mensagem de retorno)
        """
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
            category_model.slug = category.slug
            category_model.updated_at = datetime.now()

            self.db.commit()

            return Message(status=True, message="Category updated successfully.")
        except IntegrityError:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Category already exists.",
            )

    def partial_update(self, category: CategorySchemaUpdate, uuid: UUID) -> Message:
        """
        Método para atualizar parcialmente uma categoria.

        Parâmetros:
        - category: CategorySchemaUpdate (Categoria)
        - uuid: UUID (Identificador da categoria)

        Retorno:
        - Message (Mensagem de retorno)
        """
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
            if category.slug:
                category_model.slug = category.slug

            category_model.updated_at = datetime.now()

            self.db.commit()

            return Message(status=True, message="Category updated successfully.")
        except IntegrityError:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Category already exists.",
            )

    def delete(self, uuid: UUID) -> Message:
        """
        Método para deletar uma categoria.

        Parâmetros:
        - uuid: UUID (Identificador da categoria)

        Retorno:
        - Message (Mensagem de retorno)
        """
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
