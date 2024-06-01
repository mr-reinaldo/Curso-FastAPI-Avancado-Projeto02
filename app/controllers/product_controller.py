from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import status
from fastapi.exceptions import HTTPException
from app.schemas.responses import Message
from datetime import datetime
from fastapi_pagination import Params, Page
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy.future import select
from uuid import UUID
from app.models.product_model import ProductModel
from app.schemas.product_schema import ProductSchemaCreate, ProductSchemaUpdate


class ProductController:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self, page: int = 1, size: int = 50) -> Page[ProductModel]:
        """
        Método para retornar uma lista de produtos.

        Parâmetros:
        - page: int (Página atual)
        - size: int (Quantidade de registros por página)

        Retorno:
        - Page[ProductModel] (Lista de produtos)
        """
        query = select(ProductModel).order_by(ProductModel.created_at.desc())
        params = Params(page=page, size=size)

        return paginate(self.db, query, params)

    def get(self, uuid: UUID) -> ProductModel:
        """
        Método para retornar um produto.

        Parâmetros:
        - uuid: UUID (Identificador do produto)

        Retorno:
        - ProductModel (Produto)
        """

        product = self.db.query(ProductModel).filter(ProductModel.uuid == uuid).first()

        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Product not found.",
            )

        return product

    def create(self, product: ProductSchemaCreate) -> Message:
        """
        Método para criar um produto.

        Parâmetros:
        - product: ProductSchemaCreate (Produto)

        Retorno:
        - Message (Mensagem de retorno)
        """
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
        """
        Método para atualizar um produto.

        Parâmetros:
        - product: ProductSchemaUpdate (Produto)
        - uuid: UUID (Identificador do produto)

        Retorno:
        - Message (Mensagem de retorno)
        """
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

            product_model.updated_at = datetime.now()

            self.db.commit()

            return Message(status=True, message="Product updated successfully.")
        except IntegrityError:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Product already exists.",
            )

    def partial_update(self, product: ProductSchemaUpdate, uuid: UUID) -> Message:
        """
        Método para atualizar parcialmente um produto.

        Parâmetros:
        - product: ProductSchemaUpdate (Produto)
        - uuid: UUID (Identificador do produto)

        Retorno:
        - Message (Mensagem de retorno)
        """
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

            product_model.updated_at = datetime.now()

            self.db.commit()

            return Message(status=True, message="Product updated successfully.")
        except IntegrityError:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Product already exists.",
            )

    def delete(self, uuid: UUID) -> Message:
        """
        Método para deletar um produto.

        Parâmetros:
        - uuid: UUID (Identificador do produto)

        Retorno:
        - Message (Mensagem de retorno)
        """
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
