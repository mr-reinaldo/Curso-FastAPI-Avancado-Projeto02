from .user_model import UserModel
from .category_model import CategoryModel
from .product_model import ProductModel

# Lista de modelos disponíveis para importação no pacote models do aplicativo FastAPI.
__all__ = [
    "UserModel",
    "CategoryModel",
    "ProductModel",
]
